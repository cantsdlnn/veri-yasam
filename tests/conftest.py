from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("VERIYASAM_DB_PATH", str(db_path))
    monkeypatch.setenv("VERIYASAM_SEED_DEMO", "0")

    from app.db import init_db
    from app.main import app

    init_db(db_path)
    with TestClient(app) as test_client:
        yield test_client
