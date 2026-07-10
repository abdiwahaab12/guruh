"""
Seed Page Builder sections into MySQL.

Usage (after DATABASE_ENABLED=true and init_db.py):
    python seed_page_sections.py
"""

from run import app
from app.data.page_sections import ALL_PAGE_SECTIONS
from app.extensions import db
from app.models.page_sections import PageSection


def seed_page_sections() -> None:
    with app.app_context():
        for section_data in ALL_PAGE_SECTIONS:
            row = PageSection.query.filter_by(
                page_slug=section_data["page_slug"],
                section_key=section_data["section_key"],
            ).first()
            if not row:
                row = PageSection(
                    page_slug=section_data["page_slug"],
                    section_key=section_data["section_key"],
                )
                db.session.add(row)

            row.section_title = section_data["section_title"]
            row.block_key = section_data.get("block_key") or None
            row.display_order = section_data.get("display_order", 0)
            row.layout_type = section_data.get("layout_type", "default")
            row.background_style = section_data.get("background_style", "default")
            row.spacing = section_data.get("spacing", "default")
            row.animation = section_data.get("animation", "none")
            row.is_visible = section_data.get("is_visible", True)
            row.seo_anchor = section_data.get("seo_anchor")
            row.is_active = section_data.get("is_active", True)
            row.extra = section_data.get("extra") or {}

        db.session.commit()
        print(f"Seeded {len(ALL_PAGE_SECTIONS)} page sections.")


if __name__ == "__main__":
    seed_page_sections()
