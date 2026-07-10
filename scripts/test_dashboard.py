"""Smoke tests for Step 14 admin dashboard foundation."""

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

    r = client.get("/admin/")
    assert r.status_code == 302 and "/admin/login" in r.location

    r = login(client)
    assert r.status_code == 200, r.status_code
    body = r.data.decode()

    for marker in (
        "Dashboard",
        "admin-stats-grid",
        "adminChartsData",
        "Quick Actions",
        "Recent Activity",
        "admin-theme.css",
        "admin-charts.js",
        "chartTrafficOverview",
        "Total Pages",
        "Quote Requests",
    ):
        assert marker in body, f"Missing: {marker}"

    r = client.get("/admin/projects")
    assert r.status_code == 200
    assert "Projects" in r.data.decode()

    r = client.get("/admin/users?tab=audit-logs")
    assert r.status_code == 200
    assert "Audit Logs" in r.data.decode() or "Action" in r.data.decode()

    r = client.get("/admin/login")
    assert r.status_code == 302

    print("Step 14 dashboard foundation checks passed.")


if __name__ == "__main__":
    main()
