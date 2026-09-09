from __future__ import annotations

import os
import uuid
from contextlib import asynccontextmanager
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Query, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .audit import append_event, verify_chain
from .db import connect, init_db, transaction
from .rules import assess_retention, calculate_expiry
from .schemas import AssetCreate, AssetView, RetentionDecision

ROLE_PERMISSIONS = {
    "viewer": {"read"},
    "data_steward": {"read", "create", "decide"},
    "admin": {"read", "create", "decide", "audit"},
}


def require(permission: str):
    def dependency(x_demo_role: str = Header(default="viewer")) -> str:
        allowed = ROLE_PERMISSIONS.get(x_demo_role)
        if not allowed or permission not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"{permission} işlemi için yetki yok.",
            )
        return x_demo_role

    return dependency


def maybe_seed_demo() -> None:
    if os.getenv("VERIYASAM_SEED_DEMO", "1") != "1":
        return
    with transaction() as connection:
        if connection.execute("SELECT COUNT(*) AS count FROM data_assets").fetchone()["count"]:
            return
        collected = date.today() - timedelta(days=25)
        payload = AssetCreate(
            record_name="Sentetik destek talebi",
            data_category="İletişim kaydı",
            purpose="Demo destek sürecini yürütmek",
            legal_basis="Demo senaryosu",
            storage_location="Yerel SQLite",
            owner_role="Destek sorumlusu",
            subject_reference="DEMO-001",
            retention_days=30,
            collected_on=collected,
        )
        _insert_asset(connection, payload, actor="demo-seed")


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    maybe_seed_demo()
    yield


app = FastAPI(
    title="VeriYaşam",
    version="1.0.0",
    description="Veri envanteri ve insan onaylı saklama kararı demonstrasyonu.",
    lifespan=lifespan,
)

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


def _insert_asset(connection, payload: AssetCreate, actor: str) -> dict:
    asset_id = str(uuid.uuid4())
    now = datetime.now(UTC).isoformat()
    expires_on = calculate_expiry(payload.collected_on, payload.retention_days)
    connection.execute(
        """
        INSERT INTO data_assets (
            id, record_name, data_category, purpose, legal_basis,
            storage_location, owner_role, subject_reference, retention_days,
            collected_on, expires_on, status, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'active', ?)
        """,
        (
            asset_id,
            payload.record_name,
            payload.data_category,
            payload.purpose,
            payload.legal_basis,
            payload.storage_location,
            payload.owner_role,
            payload.subject_reference,
            payload.retention_days,
            payload.collected_on.isoformat(),
            expires_on.isoformat(),
            now,
        ),
    )
    append_event(
        connection,
        actor=actor,
        action="asset.created",
        resource_type="data_asset",
        resource_id=asset_id,
        payload={
            "category": payload.data_category,
            "retention_days": payload.retention_days,
            "expires_on": expires_on.isoformat(),
        },
    )
    created = connection.execute("SELECT * FROM data_assets WHERE id = ?", (asset_id,)).fetchone()
    return dict(created)


@app.get("/api/assets", response_model=list[AssetView])
def list_assets(_: str = Depends(require("read"))) -> list[dict]:
    with connect() as connection:
        return [
            dict(row)
            for row in connection.execute(
                "SELECT * FROM data_assets ORDER BY expires_on, record_name"
            ).fetchall()
        ]


@app.post("/api/assets", response_model=AssetView, status_code=201)
def create_asset(payload: AssetCreate, role: str = Depends(require("create"))) -> dict:
    with transaction() as connection:
        return _insert_asset(connection, payload, actor=f"role:{role}")


@app.get("/api/retention/due")
def retention_due(
    as_of: Annotated[date | None, Query()] = None,
    _: str = Depends(require("read")),
) -> list[dict]:
    effective_date = as_of or date.today()
    result: list[dict] = []
    with connect() as connection:
        rows = connection.execute(
            "SELECT * FROM data_assets WHERE status IN ('active', 'review_due')"
        ).fetchall()
        for row in rows:
            assessment = assess_retention(
                date.fromisoformat(row["collected_on"]),
                row["retention_days"],
                effective_date,
            )
            if assessment.state != "active":
                result.append(
                    {
                        "asset_id": row["id"],
                        "record_name": row["record_name"],
                        "expires_on": assessment.expires_on.isoformat(),
                        "days_remaining": assessment.days_remaining,
                        "state": assessment.state,
                        "reason": assessment.reason,
                        "recommended_actions": ["keep", "anonymize", "delete"],
                    }
                )
    return sorted(result, key=lambda item: item["days_remaining"])


@app.post("/api/assets/{asset_id}/decision")
def decide_retention(
    asset_id: str,
    decision: RetentionDecision,
    _: str = Depends(require("decide")),
) -> dict:
    with transaction() as connection:
        row = connection.execute("SELECT * FROM data_assets WHERE id = ?", (asset_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Kayıt bulunamadı.")

        next_status = {
            "keep": "active",
            "anonymize": "anonymized",
            "delete": "deleted",
        }[decision.action]
        decision_id = str(uuid.uuid4())
        decided_at = datetime.now(UTC).isoformat()
        connection.execute(
            """
            INSERT INTO decisions (id, asset_id, action, actor, reason, decided_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                decision_id,
                asset_id,
                decision.action,
                decision.actor,
                decision.reason,
                decided_at,
            ),
        )
        if decision.action == "anonymize":
            connection.execute(
                """
                UPDATE data_assets
                SET status = ?, subject_reference = '[ANONİMLEŞTİRİLDİ]'
                WHERE id = ?
                """,
                (next_status, asset_id),
            )
        elif decision.action == "delete":
            connection.execute(
                """
                UPDATE data_assets
                SET status = ?, record_name = '[SİLİNDİ]', subject_reference = '[SİLİNDİ]'
                WHERE id = ?
                """,
                (next_status, asset_id),
            )
        else:
            connection.execute(
                "UPDATE data_assets SET status = ? WHERE id = ?",
                (next_status, asset_id),
            )

        event_hash = append_event(
            connection,
            actor=decision.actor,
            action=f"retention.{decision.action}",
            resource_type="data_asset",
            resource_id=asset_id,
            payload={"reason": decision.reason, "next_status": next_status},
        )
        return {
            "decision_id": decision_id,
            "asset_id": asset_id,
            "status": next_status,
            "audit_hash": event_hash,
            "message": "Karar insan gerekçesiyle kaydedildi.",
        }


@app.get("/api/audit/verify")
def verify_audit(_: str = Depends(require("audit"))) -> dict:
    with connect() as connection:
        result = verify_chain(connection)
        return {
            "valid": result.valid,
            "event_count": result.event_count,
            "broken_sequence": result.broken_sequence,
        }


@app.get("/api/audit/events")
def audit_events(_: str = Depends(require("audit"))) -> list[dict]:
    with connect() as connection:
        return [
            dict(row)
            for row in connection.execute(
                "SELECT * FROM audit_events ORDER BY sequence DESC LIMIT 100"
            ).fetchall()
        ]
