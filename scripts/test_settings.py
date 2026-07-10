"""Smoke tests for Step 15 Website Settings module."""

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

    r = client.get("/admin/settings")
    assert r.status_code == 302

    login(client)

    sections = [
        ("/admin/settings", "Website Settings"),
        ("/admin/settings/company", "Company Information"),
        ("/admin/settings/contact", "Contact Information"),
        ("/admin/settings/offices", "Office Locations"),
        ("/admin/settings/business", "Business Information"),
        ("/admin/settings/social", "Social Media"),
        ("/admin/settings/seo", "SEO Settings"),
        ("/admin/settings/email", "Email (SMTP)"),
        ("/admin/settings/maps", "Google Maps"),
        ("/admin/settings/localization", "Localization"),
        ("/admin/settings/theme", "Theme Settings"),
        ("/admin/settings/maintenance", "Maintenance Mode"),
        ("/admin/settings/analytics", "Analytics"),
    ]

    for url, label in sections:
        r = client.get(url)
        assert r.status_code == 200, f"{url} -> {r.status_code}"
        body = r.data.decode()
        assert label in body, f"Missing label {label} on {url}"
        assert "admin-settings-nav" in body

    # Save company info
    r = client.get("/admin/settings/company")
    token = extract_csrf(r.data.decode())
    r = client.post(
        "/admin/settings/company",
        data={
            "csrf_token": token,
            "name": "GURUH Construction Company Limited",
            "short_name": "GURUH Construction",
            "tagline": "Building Excellence Across East Africa",
            "description": "Test company description for settings module.",
            "logo_path": "img/logo.png",
            "founded_country": "Kenya",
            "founded_country_code": "KE",
            "operating_country": "Somalia",
            "operating_country_code": "SO",
            "headquarters": "Mogadishu, Somalia",
            "submit": "Save Company Information",
        },
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert b"saved successfully" in r.data.lower()

    # RBAC: logout and verify redirect
    client.get("/admin/logout", follow_redirects=True)
    r = client.get("/admin/settings/company")
    assert r.status_code == 302
    assert "/admin/login" in r.location

    print("Step 15 Website Settings checks passed.")


if __name__ == "__main__":
    main()
