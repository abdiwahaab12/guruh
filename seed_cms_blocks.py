"""
Seed CMS content blocks from approved company profile data into MySQL.

Usage (after DATABASE_ENABLED=true and init_db.py):
    python seed_cms_blocks.py
"""

from run import app
from app.data.cms_blocks import CMS_CONTENT_BLOCKS
from app.extensions import db
from app.models.content_blocks import ContentBlock, ContentBlockItem


def seed_cms_blocks() -> None:
    with app.app_context():
        for block_data in CMS_CONTENT_BLOCKS:
            row = ContentBlock.query.filter_by(block_key=block_data["block_key"]).first()
            if not row:
                row = ContentBlock(block_key=block_data["block_key"])
                db.session.add(row)

            row.title = block_data["title"]
            row.subtitle = block_data.get("subtitle")
            row.short_summary = block_data.get("short_summary")
            row.full_content = block_data.get("full_content", "")
            row.hero_image = block_data.get("hero_image")
            row.gallery_images = block_data.get("gallery_images") or []
            row.display_order = block_data.get("display_order", 0)
            row.is_active = block_data.get("is_active", True)
            row.meta_title = block_data.get("meta_title")
            row.meta_description = block_data.get("meta_description")
            row.og_image = block_data.get("og_image")
            row.extra = block_data.get("extra") or {}

            ContentBlockItem.query.filter_by(block_id=row.id).delete()
            db.session.flush()

            for item_data in block_data.get("items", []):
                db.session.add(
                    ContentBlockItem(
                        block_id=row.id,
                        item_key=item_data.get("item_key"),
                        title=item_data["title"],
                        subtitle=item_data.get("subtitle"),
                        short_summary=item_data.get("short_summary"),
                        full_content=item_data.get("full_content"),
                        image=item_data.get("image"),
                        icon=item_data.get("icon"),
                        sort_order=item_data.get("sort_order", 0),
                        is_active=item_data.get("is_active", True),
                        extra=item_data.get("extra") or {},
                    )
                )

        db.session.commit()
        print(f"Seeded {len(CMS_CONTENT_BLOCKS)} CMS content blocks.")


if __name__ == "__main__":
    seed_cms_blocks()
