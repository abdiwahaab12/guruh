"""
Extended gallery admin data — Step 21 Gallery Management.

One-to-one with GalleryImage; keeps core GalleryImage model unchanged for public site compatibility.
"""

from __future__ import annotations

from datetime import datetime

from app.extensions import db
from app.models.base import BaseModel


class GalleryDetail(BaseModel):
    """SEO, relationships, album metadata, and extended content for a gallery item."""

    __tablename__ = "gallery_details"

    gallery_image_id = db.Column(
        db.Integer,
        db.ForeignKey("gallery_images.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    slug = db.Column(db.String(150), unique=True, nullable=False, index=True)
    media_type = db.Column(db.String(20), default="image", nullable=False)
    album = db.Column(db.String(100), default="")
    caption = db.Column(db.Text, default="")
    location = db.Column(db.String(150), default="")
    county = db.Column(db.String(100), default="")
    country = db.Column(db.String(100), default="Somalia")
    media_date = db.Column(db.String(50), default="")
    year = db.Column(db.String(10), default="")
    is_featured = db.Column(db.Boolean, default=False, nullable=False)

    meta_title = db.Column(db.String(200), default="")
    meta_description = db.Column(db.String(500), default="")
    og_image = db.Column(db.String(255), default="")
    canonical_url = db.Column(db.String(500), default="")

    service_slug = db.Column(db.String(150), default="")
    equipment_slug = db.Column(db.String(150), default="")
    team_member_ids_json = db.Column(db.Text, default="[]")

    video_provider = db.Column(db.String(50), default="")
    video_id = db.Column(db.String(100), default="")
    embed_url = db.Column(db.String(500), default="")

    deleted_at = db.Column(db.DateTime, nullable=True)

    gallery_image = db.relationship("GalleryImage", backref=db.backref("detail", uselist=False))

    def mark_deleted(self) -> None:
        self.deleted_at = datetime.utcnow()

    def restore(self) -> None:
        self.deleted_at = None
