"""
Page Builder — ordered page sections that reference CMS content blocks.

Hierarchy: Page → Page Sections → Content Blocks → Content Block Items
"""

from app.extensions import db
from app.models.base import BaseModel


class PageSection(BaseModel):
    """
    Configurable section placement on a public page.

    Admin dashboard can reorder, hide, or change layout without code changes.
    """

    __tablename__ = "page_sections"

    page_slug = db.Column(db.String(100), nullable=False, index=True)
    section_key = db.Column(db.String(100), nullable=False, index=True)
    section_title = db.Column(db.String(200), nullable=False)
    block_key = db.Column(db.String(100), index=True)
    display_order = db.Column(db.Integer, default=0, nullable=False, index=True)
    layout_type = db.Column(db.String(50), default="default", nullable=False)
    background_style = db.Column(db.String(50), default="default", nullable=False)
    spacing = db.Column(db.String(50), default="default", nullable=False)
    animation = db.Column(db.String(50), default="none", nullable=False)
    is_visible = db.Column(db.Boolean, default=True, nullable=False)
    seo_anchor = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    extra = db.Column(db.JSON, default=dict)

    __table_args__ = (
        db.UniqueConstraint("page_slug", "section_key", name="uq_page_section_key"),
    )
