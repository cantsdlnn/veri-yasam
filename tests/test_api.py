from datetime import date, timedelta


def asset_payload(**overrides):
    payload = {
        "record_name": "Sentetik başvuru",
        "data_category": "İletişim",
        "purpose": "Demo talebini sonuçlandırmak",
        "legal_basis": "Demo kullanıcı talebi",
        "storage_location": "Yerel test veritabanı",
        "owner_role": "Süreç sorumlusu",
        "subject_reference": "DEMO-101",
        "retention_days": 30,
        "collected_on": (date.today() - timedelta(days=31)).isoformat(),
    }
    payload.update(overrides)
    return payload


def test_viewer_cannot_create_asset(client) -> None:
    response = client.post("/api/assets", json=asset_payload())
    assert response.status_code == 403


def test_create_due_and_human_anonymize_flow(client) -> None:
    created = client.post(
        "/api/assets",
        headers={"X-Demo-Role": "data_steward"},
        json=asset_payload(),
    )
    assert created.status_code == 201
    asset_id = created.json()["id"]

    due = client.get("/api/retention/due").json()
    assert due[0]["asset_id"] == asset_id
    assert due[0]["state"] == "overdue"

    decision = client.post(
        f"/api/assets/{asset_id}/decision",
        headers={"X-Demo-Role": "data_steward"},
        json={
            "action": "anonymize",
            "actor": "test-sorumlusu",
            "reason": "Saklama amacı sona erdiği için anonimleştirildi.",
        },
    )
    assert decision.status_code == 200
    assert decision.json()["status"] == "anonymized"

    assets = client.get("/api/assets").json()
    assert assets[0]["subject_reference"] == "[ANONİMLEŞTİRİLDİ]"


def test_admin_can_verify_audit_chain(client) -> None:
    client.post(
        "/api/assets",
        headers={"X-Demo-Role": "admin"},
        json=asset_payload(retention_days=60),
    )
    response = client.get("/api/audit/verify", headers={"X-Demo-Role": "admin"})
    assert response.status_code == 200
    assert response.json() == {
        "valid": True,
        "event_count": 1,
        "broken_sequence": None,
    }
