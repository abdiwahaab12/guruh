"""Smoke tests for Step 21 Gallery Management."""

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
    assert client.get("/admin/gallery").status_code == 302
    login(client)

    for url, marker in (
        ("/admin/gallery", "Recent Uploads"),
        ("/admin/gallery/list", "admin-gallery-filters"),
        ("/admin/gallery/create", "tab-general"),
    ):
        r = client.get(url)
        assert r.status_code == 200, url
        assert marker in r.data.decode(), marker

    token = extract_csrf(client.get("/admin/gallery/create").data.decode())
    r = client.post(
        "/admin/gallery/create",
        data={
            "csrf_token": token,
            "title": "Test Banadir Road Gallery Item",
            "slug": "test-banadir-road-gallery",
            "image": "img/fallbacks/project.svg",
            "category": "Road Construction",
            "media_type": "image",
            "album": "road-construction",
            "country": "Somalia",
            "submit": "Save Gallery Item",
        },
        follow_redirects=True,
    )
    assert r.status_code == 200
    body = r.data.decode()
    assert "saved successfully" in body.lower() or "Test Banadir Road" in body, body[:800]

    r = client.get("/admin/gallery/list")
    assert b"Test Banadir Road Gallery Item" in r.data or b"test-banadir-road" in r.data

    client.get("/admin/logout", follow_redirects=True)
    assert client.get("/admin/gallery").status_code == 302
    print("Step 21 Gallery Management checks passed.")


if __name__ == "__main__":
    main()
