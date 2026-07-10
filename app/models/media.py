"""
Central media library model — Enterprise Media Manager (Step 16).

All CMS modules reference assets via storage_path (relative to static/).
"""

from __future__ import annotations

from datetime import datetime

from app.extensions import db
from app.models.base import BaseModel


class MediaAsset(BaseModel):
    """Uploaded file in the centralized media library."""

    __tablename__ = "media_assets"

    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    storage_path = db.Column(db.String(500), nullable=False, unique=True, index=True)

    folder = db.Column(db.String(50), nullable=False, default="general", index=True)
    media_type = db.Column(db.String(20), nullable=False, index=True)
    mime_type = db.Column(db.String(120), nullable=False)
    file_size = db.Column(db.BigInteger, nullable=False, default=0)

    title = db.Column(db.String(200), nullable=False, default="")
    alt_text = db.Column(db.String(255), default="")
    caption = db.Column(db.String(500), default="")
    description = db.Column(db.Text, default="")
    tags = db.Column(db.String(500), default="")
    category = db.Column(db.String(100), default="")
    seo_title = db.Column(db.String(200), default="")
    seo_description = db.Column(db.String(500), default="")

    width = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)

    uploaded_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    uploaded_by = db.relationship("User", backref=db.backref("media_uploads", lazy="dynamic"))

    @property
    def is_deleted(self) -> bool:
        return not self.is_active or self.deleted_at is not None

    def soft_delete(self) -> None:
        self.is_active = False
        self.deleted_at = datetime.utcnow()

    def restore(self) -> None:
        self.is_active = True
        self.deleted_at = None
