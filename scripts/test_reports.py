"""Smoke tests for Step 26 Reports & Analytics."""

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
    assert client.get("/admin/reports").status_code == 302
    login(client)

    r = client.get("/admin/reports")
    assert r.status_code == 200
    body = r.data.decode()
    assert "Reports" in body and "Analytics" in body
    assert "monthlyActivity" in body
    assert "Website Pages" in body

    for preset in ("today", "week", "month", "year"):
        r = client.get(f"/admin/reports?preset={preset}")
        assert r.status_code == 200, preset

    r = client.get("/admin/reports?tab=audit&audit_tab=login")
    assert r.status_code == 200
    assert "Login Activity" in r.data.decode()

    for fmt, mime in (("csv", "text/csv"), ("excel", "spreadsheet"), ("pdf", "pdf")):
        r = client.get(f"/admin/reports/export?report=overview&format={fmt}&preset=month")
        assert r.status_code == 200, fmt
        assert mime.split("/")[-1] in r.content_type or mime in r.content_type, fmt
        assert "attachment" in r.headers.get("Content-Disposition", "")

    r = client.get("/admin/reports/export?report=audit&format=csv&preset=month&audit_tab=system")
    assert r.status_code == 200
    assert b"Label" in r.data

    print("All Reports & Analytics tests passed.")


if __name__ == "__main__":
    main()
