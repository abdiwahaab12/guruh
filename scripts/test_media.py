"""Smoke tests for Step 16 Enterprise Media Manager."""

import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import app.models  # noqa: F401
from run import app


def extract_csrf(html: str) -> str:
    match = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', html)
    if not match:
        raise AssertionError("CSRF token missing")
    return match.group(1)


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

    r = client.get("/admin/media")
    assert r.status_code == 302

    login(client)

    for url, marker in (
        ("/admin/media", "Media Types"),
        ("/admin/media/library", "admin-media-filters"),
        ("/admin/media/upload", "mediaDropzone"),
    ):
        r = client.get(url)
        assert r.status_code == 200, f"{url} -> {r.status_code}"
        assert marker in r.data.decode(), f"Missing {marker} on {url}"

    token = extract_csrf(client.get("/admin/media/upload").data.decode())
    png_bytes = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
        b"\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
        b"\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01"
        b"\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    data = {
        "csrf_token": token,
        "folder": "general",
        "title": "Test Upload",
        "alt_text": "Test alt",
        "submit": "Upload Files",
    }
    r = client.post(
        "/admin/media/upload",
        data=data,
        content_type="multipart/form-data",
        buffered=True,
        follow_redirects=False,
    )
    # multipart via test client needs different approach
    from werkzeug.datastructures import FileStorage

    r = client.post(
        "/admin/media/upload",
        data={
            **data,
            "files": (FileStorage(stream=io.BytesIO(png_bytes), filename="test.png", content_type="image/png"),),
        },
        content_type="multipart/form-data",
        follow_redirects=True,
    )
    assert r.status_code == 200

    r = client.get("/admin/media/library")
    body = r.data.decode()
    assert "Test Upload" in body or "test.png" in body

    r = client.get("/admin/media/library?view=list")
    assert r.status_code == 200
    assert "admin-media-table" in r.data.decode()

    client.get("/admin/logout", follow_redirects=True)
    r = client.get("/admin/media")
    assert r.status_code == 302

    print("Step 16 Media Manager checks passed.")


if __name__ == "__main__":
    main()
