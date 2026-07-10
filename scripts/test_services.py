"""Smoke tests for Step 18 Services Management."""

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
    assert client.get("/admin/services").status_code == 302
    login(client)

    for url, marker in (
        ("/admin/services", "Recent Updates"),
        ("/admin/services/list", "admin-services-filters"),
        ("/admin/services/create", "tab-general"),
    ):
        r = client.get(url)
        assert r.status_code == 200, url
        assert marker in r.data.decode(), marker

    token = extract_csrf(client.get("/admin/services/create").data.decode())
    r = client.post(
        "/admin/services/create",
        data={
            "csrf_token": token,
            "title": "Test Road Construction Service",
            "slug": "test-road-construction-service",
            "short_description": "Test service short description for Step 18.",
            "description": "Test service full description for Step 18 enterprise module.",
            "icon": "bi-signpost-split-fill",
            "submit": "Save Service",
        },
        follow_redirects=True,
    )
    assert r.status_code == 200
    body = r.data.decode()
    assert "saved successfully" in body.lower() or "Test Road Construction" in body, body[:800]

    r = client.get("/admin/services/list")
    assert b"Test Road Construction Service" in r.data or b"test-road-construction" in r.data

    client.get("/admin/logout", follow_redirects=True)
    assert client.get("/admin/services").status_code == 302
    print("Step 18 Services Management checks passed.")


if __name__ == "__main__":
    main()
