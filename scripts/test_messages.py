"""Smoke tests for Step 24 Messages / Inbox."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import app.models  # noqa: F401
from app.extensions import db
from app.providers.messages_admin_provider import MessagesAdminProvider
from run import app


def extract_csrf(html: str) -> str:
    m = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', html)
    if not m:
        raise AssertionError("CSRF missing")
    return m.group(1)


def login(client):
    token = extract_csrf(client.get("/admin/login").data.decode())
    return client.post(
        "/admin/login",
        data={
            "csrf_token": token,
            "email": "admin@guruh.com",
            "password": "GuruhAdmin2026!",
            "remember": "y",
            "submit": "Sign In",
        },
        follow_redirects=True,
    )


def main() -> None:
    with app.app_context():
        MessagesAdminProvider.seed_sample_messages()
        db.session.commit()

    client = app.test_client()
    assert client.get("/admin/messages").status_code == 302
    login(client)

    r = client.get("/admin/messages/inbox")
    assert r.status_code == 200, r.status_code
    body = r.data.decode()
    assert "Contact Messages" in body and "admin-messages-filters" in body

    for tab, marker in (
        ("contacts", "Ahmed Hassan"),
        ("quotes", "Somali Infrastructure"),
        ("applications", "Fatima Ali"),
    ):
        r = client.get(f"/admin/messages/inbox?tab={tab}")
        assert r.status_code == 200
        assert marker in r.data.decode(), tab

    r = client.get("/admin/messages/inbox?tab=contacts")
    body = r.data.decode()
    m = re.search(r'/admin/messages/contacts/(\d+)', body)
    assert m, "Contact detail link missing"
    contact_id = m.group(1)

    r = client.get(f"/admin/messages/contacts/{contact_id}")
    assert r.status_code == 200
    assert "Road project inquiry" in r.data.decode()

    token = extract_csrf(r.data.decode())
    r = client.post(
        f"/admin/messages/contacts/{contact_id}",
        data={
            "csrf_token": token,
            "reply_subject": "Re: Road project inquiry",
            "reply_body": "Thank you for your inquiry. Our team will contact you shortly.",
            "admin_notes": "Follow up with estimation team.",
            "submit": "Save Reply",
        },
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert "saved successfully" in r.data.decode().lower()

    r = client.get("/admin/messages/export?tab=contacts")
    assert r.status_code == 200
    assert "text/csv" in r.content_type
    assert b"Ahmed Hassan" in r.data

    token = extract_csrf(client.get("/admin/messages/inbox?tab=contacts").data.decode())
    r = client.post(
        "/admin/messages/bulk",
        data={
            "csrf_token": token,
            "tab": "contacts",
            "action": "star",
            "message_ids": contact_id,
            "submit": "Apply to Selected",
        },
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert "updated" in r.data.decode().lower()

    client.get("/admin/logout", follow_redirects=True)
    assert client.get("/admin/messages").status_code == 302
    print("Step 24 Messages / Inbox checks passed.")


if __name__ == "__main__":
    main()
