"""Smoke tests for Step 19 Equipment Management."""

import re
import sys
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
    assert client.get("/admin/equipment").status_code == 302
    login(client)

    for url, marker in (
        ("/admin/equipment", "Recent Updates"),
        ("/admin/equipment/list", "admin-equipment-filters"),
        ("/admin/equipment/create", "tab-general"),
    ):
        r = client.get(url)
        assert r.status_code == 200, url
        assert marker in r.data.decode(), marker

    token = extract_csrf(client.get("/admin/equipment/create").data.decode())
    r = client.post(
        "/admin/equipment/create",
        data={
            "csrf_token": token,
            "name": "Test Motor Grader Fleet",
            "slug": "test-motor-grader-fleet",
            "category": "Road Construction Equipment",
            "short_description": "Test equipment short description for Step 19.",
            "description": "Test equipment full description for Step 19 enterprise module.",
            "condition": "Operational",
            "submit": "Save Equipment",
        },
        follow_redirects=True,
    )
    assert r.status_code == 200
    body = r.data.decode()
    assert "saved successfully" in body.lower() or "Test Motor Grader" in body, body[:800]

    r = client.get("/admin/equipment/list")
    assert b"Test Motor Grader Fleet" in r.data or b"test-motor-grader" in r.data

    client.get("/admin/logout", follow_redirects=True)
    assert client.get("/admin/equipment").status_code == 302
    print("Step 19 Equipment Management checks passed.")


if __name__ == "__main__":
    main()
