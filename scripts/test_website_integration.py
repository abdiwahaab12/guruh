"""
Step 23.1 — Website CMS & Media Integration smoke tests.

Verifies the admin -> public content flow for pages, hero slides, and that
no SVG placeholder artwork is used for hero banners.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env", override=True)

from run import app

PUBLIC_ROUTES = {
    "home": "/",
    "about": "/about",
    "services": "/services",
    "projects": "/projects",
    "equipment": "/equipment",
    "team": "/team",
    "gallery": "/gallery",
    "careers": "/careers",
    "contact": "/contact",
    "request-quote": "/request-quote",
}


def main() -> None:
    client = app.test_client()
    failures: list[str] = []

    with app.app_context():
        from app.extensions import db
        from app.models.cms import Page
        from app.providers.website_admin_provider import WebsiteAdminProvider

        try:
            slides = WebsiteAdminProvider.ensure_hero_slides()
            db.session.commit()
            if len(slides) < 3:
                failures.append(f"hero_slides count {len(slides)} < 3")
        except Exception as exc:  # noqa: BLE001
            failures.append(f"ensure_hero_slides: {exc}")

        # Simulate an admin saving a Media Library image on the About page.
        test_image = "uploads/content/integration-test-hero.jpg"
        try:
            row = Page.query.filter_by(slug="about").first()
            if row:
                row.banner_image = test_image
                db.session.commit()
        except Exception as exc:  # noqa: BLE001
            failures.append(f"about banner save: {exc}")

    about_html = client.get("/about").data.decode(errors="replace")
    if test_image not in about_html:
        failures.append("about page did not reflect saved Media Library banner_image")

    home_html = client.get("/").data.decode(errors="replace")
    if "hero-slider" not in home_html:
        failures.append("homepage missing hero-slider")

    for slug, route in PUBLIC_ROUTES.items():
        resp = client.get(route)
        if resp.status_code != 200:
            failures.append(f"{route} -> HTTP {resp.status_code}")
            continue
        body = resp.data.decode(errors="replace")
        if slug != "home" and "page-hero" not in body:
            failures.append(f"{route} missing page-hero section")
        if "url('/static/img/fallbacks/" in body:
            failures.append(f"{route} hero banner uses SVG placeholder background")

    admin = client.get("/admin/website/pages/home")
    if admin.status_code not in (200, 302):
        failures.append(f"admin home page editor -> HTTP {admin.status_code}")

    if failures:
        print("WEBSITE INTEGRATION FAILURES:")
        for item in failures:
            print(f"  - {item}")
        raise SystemExit(1)

    print(f"Website CMS integration checks passed ({len(PUBLIC_ROUTES)} public pages).")


if __name__ == "__main__":
    main()
