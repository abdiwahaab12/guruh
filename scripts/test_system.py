"""Smoke tests for Step 27 Enterprise System Administration."""

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
    assert client.get("/admin/system").status_code == 302
    login(client)

    for tab, marker in (
        ("overview", "Database Status"),
        ("maintenance", "Maintenance Mode"),
        ("backup", "Create Backup"),
        ("health", "Health Check"),
        ("logs", "Application Logs"),
        ("storage", "Storage"),
        ("cache", "Clear Cache"),
    ):
        r = client.get(f"/admin/system?tab={tab}")
        assert r.status_code == 200, tab
        assert marker in r.data.decode(), tab

    token = extract_csrf(client.get("/admin/system?tab=health").data.decode())

    r = client.post(
        "/admin/system/health/run",
        data={"csrf_token": token},
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert b"Health check" in r.data or b"checks" in r.data.lower()

    token = extract_csrf(client.get("/admin/system?tab=backup").data.decode())
    r = client.post(
        "/admin/system/backup/create",
        data={"csrf_token": token},
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert b"guruh-backup" in r.data or b"Backup created" in r.data

    token = extract_csrf(client.get("/admin/system?tab=cache").data.decode())
    r = client.post(
        "/admin/system/cache/rebuild",
        data={"csrf_token": token},
        follow_redirects=True,
    )
    assert r.status_code == 200

    r = client.get("/admin/system?tab=logs&log_tab=audit")
    assert r.status_code == 200

    print("All System Administration tests passed.")


if __name__ == "__main__":
    main()
