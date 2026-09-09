# VeriYaşam — English summary

VeriYaşam is an auditable data-inventory and retention-decision demo. It connects each record to its purpose, legal basis, storage location, responsible role and retention period. Expired records are never silently deleted: an authorised human must choose keep, anonymise or delete and provide a reason.

The decision is written to a SHA-256 hash-chained audit log. The project includes a FastAPI service, SQLite persistence, a small responsive interface, role checks and automated tests for date boundaries, permissions, lifecycle decisions and tamper detection.

This is an educational architecture demo, not legal advice or a production compliance product. All bundled data is synthetic. See [AI_USAGE.md](AI_USAGE.md) for the transparent AI-assisted development statement.

Run locally:

    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements-dev.txt
    uvicorn app.main:app --reload
    pytest
