"""Smoke tests for Step 17 Projects Management."""

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
    assert client.get("/admin/projects").status_code == 302
    login(client)

    for url, marker in (
        ("/admin/projects", "Country Distribution"),
        ("/admin/projects/list", "admin-projects-filters"),
        ("/admin/projects/create", "tab-general"),
    ):
        r = client.get(url)
        assert r.status_code == 200, url
        assert marker in r.data.decode(), marker

    token = extract_csrf(client.get("/admin/projects/create").data.decode())
    r = client.post(
        "/admin/projects/create",
        data={
            "csrf_token": token,
            "title": "Test Mogadishu Road Project",
            "slug": "test-mogadishu-road-project",
            "description": "Test project description for Step 17.",
            "country": "Somalia",
            "status": "Completed",
            "category": "Road Works",
            "submit": "Save Project",
        },
        follow_redirects=True,
    )
    assert r.status_code == 200
    body = r.data.decode()
    assert "saved successfully" in body.lower() or "Test Mogadishu" in body, body[:800]

    r = client.get("/admin/projects/list")
    assert b"Test Mogadishu Road Project" in r.data or b"test-mogadishu" in r.data

    client.get("/admin/logout", follow_redirects=True)
    assert client.get("/admin/projects").status_code == 302
    print("Step 17 Projects Management checks passed.")


if __name__ == "__main__":
    main()
