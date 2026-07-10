"""Smoke tests for Step 20 Team Management."""

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
    assert client.get("/admin/team").status_code == 302
    login(client)

    for url, marker in (
        ("/admin/team", "Recent Updates"),
        ("/admin/team/list", "admin-team-filters"),
        ("/admin/team/create", "tab-general"),
    ):
        r = client.get(url)
        assert r.status_code == 200, url
        assert marker in r.data.decode(), marker

    token = extract_csrf(client.get("/admin/team/create").data.decode())
    r = client.post(
        "/admin/team/create",
        data={
            "csrf_token": token,
            "name": "Test Site Engineer",
            "slug": "test-site-engineer",
            "position": "Site Engineer",
            "department": "Site Engineering",
            "member_type": "staff",
            "bio": "Test biography for Step 20 team module.",
            "submit": "Save Team Member",
        },
        follow_redirects=True,
    )
    assert r.status_code == 200
    body = r.data.decode()
    assert "saved successfully" in body.lower() or "Test Site Engineer" in body, body[:800]

    r = client.get("/admin/team/list")
    assert b"Test Site Engineer" in r.data or b"test-site-engineer" in r.data

    client.get("/admin/logout", follow_redirects=True)
    assert client.get("/admin/team").status_code == 302
    print("Step 20 Team Management checks passed.")


if __name__ == "__main__":
    main()
