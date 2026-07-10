"""Smoke tests for Step 13 authentication."""

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


def main() -> None:
    client = app.test_client()

    r = client.get("/admin/login")
    assert r.status_code == 200, r.status_code
    assert b"Sign In" in r.data

    r = client.get("/admin/")
    assert r.status_code == 302
    assert "/admin/login" in r.location

    token = extract_csrf(client.get("/admin/login").data.decode())
    r = client.post(
        "/admin/login",
        data={
            "csrf_token": token,
            "email": "admin@guruh.com",
            "password": "GuruhAdmin2026!",
            "remember": "y",
            "submit": "Sign In",
        },
        follow_redirects=False,
    )
    assert r.status_code == 302, r.status_code

    r = client.get("/admin/", follow_redirects=True)
    assert r.status_code == 200
    assert b"Dashboard" in r.data
    assert b"admin@guruh.com" in r.data

    r = client.get("/admin/logout", follow_redirects=True)
    assert r.status_code == 200
    assert b"Sign In" in r.data

    token = extract_csrf(client.get("/admin/forgot-password").data.decode())
    r = client.post(
        "/admin/forgot-password",
        data={"csrf_token": token, "email": "admin@guruh.com", "submit": "Send Reset Link"},
        follow_redirects=True,
    )
    assert r.status_code == 200

    r = client.get("/admin/403")
    assert r.status_code == 403
    assert b"403" in r.data

    r = client.get("/admin/401")
    assert r.status_code == 401
    assert b"401" in r.data

    print("All auth smoke tests passed.")


if __name__ == "__main__":
    main()
