from __future__ import annotations

import os
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS data_assets (
    id TEXT PRIMARY KEY,
    record_name TEXT NOT NULL,
    data_category TEXT NOT NULL,
    purpose TEXT NOT NULL,
    legal_basis TEXT NOT NULL,
    storage_location TEXT NOT NULL,
    owner_role TEXT NOT NULL,
    subject_reference TEXT NOT NULL,
    retention_days INTEGER NOT NULL CHECK (retention_days > 0),
    collected_on TEXT NOT NULL,
    expires_on TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review_due', 'anonymized', 'deleted')),
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS decisions (
    id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL REFERENCES data_assets(id),
    action TEXT NOT NULL CHECK (action IN ('keep', 'anonymize', 'delete')),
    actor TEXT NOT NULL,
    reason TEXT NOT NULL,
    decided_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_events (
    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
    occurred_at TEXT NOT NULL,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    resource_type TEXT NOT NULL,
    resource_id TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    previous_hash TEXT NOT NULL,
    event_hash TEXT NOT NULL UNIQUE
);
"""


def database_path() -> Path:
    configured = os.getenv("VERIYASAM_DB_PATH", "./var/veriyasam.db")
    return Path(configured).expanduser().resolve()


def connect(path: Path | None = None) -> sqlite3.Connection:
    target = path or database_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(target, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


@contextmanager
def transaction(path: Path | None = None) -> Iterator[sqlite3.Connection]:
    connection = connect(path)
    try:
        connection.execute("BEGIN IMMEDIATE")
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def init_db(path: Path | None = None) -> None:
    with connect(path) as connection:
        connection.executescript(SCHEMA)
