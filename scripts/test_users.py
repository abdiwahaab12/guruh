"""Smoke tests for Step 25 Users & RBAC Management."""

import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import app.models  # noqa: F401
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
    client = app.test_client()
    assert client.get("/admin/users").status_code == 302
    login(client)

    for tab, marker in (
        ("users", "admin-users-filters"),
        ("roles", "Edit Permissions"),
        ("permissions", "manage_pages"),
        ("sessions", "User Agent"),
        ("login-history", "login-history"),
        ("audit-logs", "audit-logs"),
    ):
        r = client.get(f"/admin/users?tab={tab}")
        assert r.status_code == 200, tab
        body = r.data.decode()
        if tab == "login-history":
            assert "Email" in body
        elif tab == "audit-logs":
            assert "Action" in body
        else:
            assert marker in body or tab.replace("-", " ") in body.lower(), tab

    r = client.get("/admin/users/create")
    assert r.status_code == 200
    token = extract_csrf(r.data.decode())
    test_email = f"test.manager.{int(time.time())}@guruh.com"
    r = client.post(
        "/admin/users/create",
        data={
            "csrf_token": token,
            "email": test_email,
            "first_name": "Test",
            "last_name": "Manager",
            "role_id": "3",
            "password": "TestPass123",
            "is_active": "y",
            "submit": "Save User",
        },
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert "saved successfully" in r.data.decode().lower()

    r = client.get(f"/admin/users?tab=users&q={test_email.split('@')[0]}")
    assert test_email.encode() in r.data

    client.get("/admin/logout", follow_redirects=True)
    assert client.get("/admin/users").status_code == 302
    print("Step 25 Users & RBAC Management checks passed.")


if __name__ == "__main__":
    main()
