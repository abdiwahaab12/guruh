"""
Reusable CMS content blocks — admin-manageable page sections.

Each block is a self-contained section (title, content, SEO, media) that can be
composed into any page template without frontend changes when content is updated.
"""

from app.extensions import db
from app.models.base import BaseModel


class ContentBlock(BaseModel):
    """
    Dynamic CMS section block.

    Examples: company_overview, vision, core_values, call_to_action.
    """

    __tablename__ = "content_blocks"

    block_key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(255))
    short_summary = db.Column(db.Text)
    full_content = db.Column(db.Text, nullable=False, default="")
    hero_image = db.Column(db.String(255))
    gallery_images = db.Column(db.JSON, default=list)
    display_order = db.Column(db.Integer, default=0, nullable=False, index=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False, index=True)

    # SEO — optional per-block overrides for section landing / JSON-LD
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.Text)
    og_image = db.Column(db.String(255))
    extra = db.Column(db.JSON, nullable=True)

    items = db.relationship(
        "ContentBlockItem",
        back_populates="block",
        lazy="dynamic",
        cascade="all, delete-orphan",
        order_by="ContentBlockItem.sort_order",
    )


class ContentBlockItem(BaseModel):
    """
    Repeatable item within a content block.

    Used for core values, certifications, equipment, counties, directors, etc.
    """

    __tablename__ = "content_block_items"

    block_id = db.Column(db.Integer, db.ForeignKey("content_blocks.id"), nullable=False, index=True)
    item_key = db.Column(db.String(100), index=True)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(255))
    short_summary = db.Column(db.Text)
    full_content = db.Column(db.Text)
    image = db.Column(db.String(255))
    icon = db.Column(db.String(50))
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    extra = db.Column(db.JSON, default=dict)

    block = db.relationship("ContentBlock", back_populates="items")
