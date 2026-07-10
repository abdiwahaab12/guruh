"""
Seed website settings from company profile — run after init_db.py.

Usage:
    python init_db.py
    python scripts/seed_settings.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import app.models  # noqa: F401
from app.constants.settings_keys import SETTING_DESCRIPTIONS, default_settings_from_profile
from app.data.company_profile import COMPANY_PROFILE
from app.extensions import db
from app.models.site import CompanyInfo, OfficeLocation, SiteSetting, SocialLink
from app.providers.settings_provider import SettingsProvider
from run import app


def seed_company_info() -> None:
    if CompanyInfo.query.filter_by(is_active=True).first():
        print("Company info already seeded — skipping.")
        return
    defaults = SettingsProvider._company_defaults()
    db.session.add(CompanyInfo(**defaults, is_active=True))
    print("Seeded company_info.")


def seed_offices() -> None:
    if OfficeLocation.query.first():
        print("Office locations already seeded — skipping.")
        return
    for office in COMPANY_PROFILE["offices"]:
        map_data = office.get("map", {})
        db.session.add(
            OfficeLocation(
                slug=office["slug"],
                name=office["name"],
                office_label=office.get("office_label", "Office"),
                address=office["address"],
                postal_address=office.get("postal_address", ""),
                address_area=office.get("address_area", ""),
                address_district=office.get("address_district", ""),
                address_locality=office.get("address_locality", ""),
                country=office["country"],
                country_code=office["country_code"],
                phone_primary=office["phone_primary"],
                phone_secondary=office.get("phone_secondary", ""),
                email=office["email"],
                office_hours=office.get("office_hours", ""),
                is_headquarters=office.get("is_headquarters", False),
                show_on_contact_page=office.get("show_on_contact_page", True),
                map_latitude=map_data.get("latitude"),
                map_longitude=map_data.get("longitude"),
                map_zoom=map_data.get("zoom", 16),
                sort_order=office.get("sort_order", 0),
                is_active=office.get("is_active", True),
            )
        )
    print("Seeded office_locations.")


def seed_social_links() -> None:
    if SocialLink.query.first():
        print("Social links already seeded — skipping.")
        return
    defaults = [
        ("facebook", "Facebook", "bi-facebook", "https://facebook.com/", 1),
        ("linkedin", "LinkedIn", "bi-linkedin", "https://linkedin.com/", 2),
        ("instagram", "Instagram", "bi-instagram", "https://instagram.com/", 3),
    ]
    for platform, label, icon, url, order in defaults:
        db.session.add(
            SocialLink(
                platform=platform,
                label=label,
                icon=icon,
                url=url,
                sort_order=order,
                is_active=True,
            )
        )
    print("Seeded social_links.")


def seed_site_settings() -> None:
    defaults = default_settings_from_profile()
    created = 0
    for key, value in defaults.items():
        if SiteSetting.query.filter_by(key=key).first():
            continue
        db.session.add(
            SiteSetting(
                key=key,
                value=value,
                description=SETTING_DESCRIPTIONS.get(key),
            )
        )
        created += 1
    print(f"Seeded site_settings ({created} new keys).")


def seed_settings() -> None:
    with app.app_context():
        seed_company_info()
        seed_offices()
        seed_social_links()
        seed_site_settings()
        db.session.commit()
        print("Website settings seed completed.")


if __name__ == "__main__":
    seed_settings()
