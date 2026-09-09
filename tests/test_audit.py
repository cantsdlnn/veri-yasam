from pathlib import Path

from app.audit import append_event, verify_chain
from app.db import connect, init_db, transaction


def test_hash_chain_detects_tampering(tmp_path: Path) -> None:
    path = tmp_path / "audit.db"
    init_db(path)
    with transaction(path) as connection:
        append_event(
            connection,
            actor="tester",
            action="first",
            resource_type="demo",
            resource_id="1",
            payload={"value": 1},
        )
        append_event(
            connection,
            actor="tester",
            action="second",
            resource_type="demo",
            resource_id="1",
            payload={"value": 2},
        )

    with connect(path) as connection:
        assert verify_chain(connection).valid is True
        connection.execute(
            "UPDATE audit_events SET payload_json = ? WHERE sequence = 1",
            ('{"value":999}',),
        )
        connection.commit()
        result = verify_chain(connection)
        assert result.valid is False
        assert result.broken_sequence == 1
