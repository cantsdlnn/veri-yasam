from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

GENESIS_HASH = "0" * 64


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def canonical_json(value: dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def calculate_event_hash(
    *,
    occurred_at: str,
    actor: str,
    action: str,
    resource_type: str,
    resource_id: str,
    payload_json: str,
    previous_hash: str,
) -> str:
    material = "|".join(
        [
            occurred_at,
            actor,
            action,
            resource_type,
            resource_id,
            payload_json,
            previous_hash,
        ]
    )
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def append_event(
    connection: sqlite3.Connection,
    *,
    actor: str,
    action: str,
    resource_type: str,
    resource_id: str,
    payload: dict[str, Any],
) -> str:
    last = connection.execute(
        "SELECT event_hash FROM audit_events ORDER BY sequence DESC LIMIT 1"
    ).fetchone()
    previous_hash = last["event_hash"] if last else GENESIS_HASH
    occurred_at = utc_now()
    payload_json = canonical_json(payload)
    event_hash = calculate_event_hash(
        occurred_at=occurred_at,
        actor=actor,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        payload_json=payload_json,
        previous_hash=previous_hash,
    )
    connection.execute(
        """
        INSERT INTO audit_events (
            occurred_at, actor, action, resource_type, resource_id,
            payload_json, previous_hash, event_hash
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            occurred_at,
            actor,
            action,
            resource_type,
            resource_id,
            payload_json,
            previous_hash,
            event_hash,
        ),
    )
    return event_hash


@dataclass(frozen=True)
class ChainVerification:
    valid: bool
    event_count: int
    broken_sequence: int | None = None


def verify_chain(connection: sqlite3.Connection) -> ChainVerification:
    rows = connection.execute("SELECT * FROM audit_events ORDER BY sequence").fetchall()
    previous_hash = GENESIS_HASH
    for row in rows:
        expected = calculate_event_hash(
            occurred_at=row["occurred_at"],
            actor=row["actor"],
            action=row["action"],
            resource_type=row["resource_type"],
            resource_id=row["resource_id"],
            payload_json=row["payload_json"],
            previous_hash=previous_hash,
        )
        if row["previous_hash"] != previous_hash or row["event_hash"] != expected:
            return ChainVerification(False, len(rows), row["sequence"])
        previous_hash = row["event_hash"]
    return ChainVerification(True, len(rows))
