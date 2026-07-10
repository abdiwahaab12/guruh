"""Smoke tests for Step 23 Website CMS."""

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
    assert client.get("/admin/website").status_code == 302
    login(client)

    r = client.get("/admin/website")
    assert r.status_code == 200, r.status_code
    body = r.data.decode()
    assert "About" in body and "Services" in body, body[:600]

    r = client.get("/admin/website/pages/about")
    assert r.status_code == 200
    body = r.data.decode()
    assert "Page Sections" in body and "company_overview" in body.lower() or "Company Overview" in body

    token = extract_csrf(body)
    r = client.post(
        "/admin/website/pages/about",
        data={
            "csrf_token": token,
            "slug": "about",
            "title": "About GURUH Construction",
            "meta_title": "About Us",
            "meta_description": "Learn about GURUH Construction.",
            "banner_subtitle": "Our Story",
            "banner_image": "img/fallbacks/about.svg",
            "canonical_url": "/about",
            "is_published": "y",
            "submit": "Save Page",
        },
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert "saved successfully" in r.data.decode().lower()

    r = client.get("/admin/website/pages/about")
    body = r.data.decode()
    m = re.search(r'/admin/website/pages/about/sections/(\d+)/edit', body)
    assert m, "Section edit link missing"
    section_id = m.group(1)

    r = client.get(f"/admin/website/pages/about/sections/{section_id}/edit")
    assert r.status_code == 200
    assert "Page Builder" in r.data.decode()

    r = client.get("/admin/website/blocks/company_overview/edit?page_slug=about&section_id=" + section_id)
    assert r.status_code == 200
    block_body = r.data.decode()
    assert "ContentBlockDTO" in block_body or "Company Overview" in block_body

    token = extract_csrf(block_body)
    r = client.post(
        "/admin/website/blocks/company_overview/edit",
        data={
            "csrf_token": token,
            "page_slug": "about",
            "section_id": section_id,
            "title": "Company Overview Updated",
            "subtitle": "Who We Are",
            "short_summary": "Updated summary for smoke test.",
            "full_content": "Updated content body for website CMS test.",
            "hero_image": "img/fallbacks/about.svg",
            "gallery_images": "",
            "meta_title": "Company Overview",
            "meta_description": "Overview meta",
            "og_image": "img/fallbacks/about.svg",
            "is_active": "1",
            "submit": "Save",
        },
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert "saved successfully" in r.data.decode().lower()

    client.get("/admin/logout", follow_redirects=True)
    assert client.get("/admin/website").status_code == 302
    print("Step 23 Website CMS checks passed.")


if __name__ == "__main__":
    main()
