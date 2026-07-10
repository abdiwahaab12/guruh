"""
Extended service admin data — Step 18 Services Management.

One-to-one with Service; keeps core Service model unchanged for public site compatibility.
"""

from __future__ import annotations

from datetime import datetime

from app.extensions import db
from app.models.base import BaseModel


class ServiceDetail(BaseModel):
    """SEO, relationships, and extended content for a service."""

    __tablename__ = "service_details"

    service_id = db.Column(
        db.Integer,
        db.ForeignKey("services.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    meta_title = db.Column(db.String(200), default="")
    meta_description = db.Column(db.String(500), default="")
    og_image = db.Column(db.String(255), default="")
    canonical_url = db.Column(db.String(500), default="")

    scope_of_work_json = db.Column(db.Text, default="[]")
    benefits_json = db.Column(db.Text, default="[]")
    equipment_json = db.Column(db.Text, default="[]")
    gallery_paths_json = db.Column(db.Text, default="[]")
    related_project_ids_json = db.Column(db.Text, default="[]")
    related_service_slugs_json = db.Column(db.Text, default="[]")
    team_member_ids_json = db.Column(db.Text, default="[]")

    deleted_at = db.Column(db.DateTime, nullable=True)

    service = db.relationship("Service", backref=db.backref("detail", uselist=False))

    def mark_deleted(self) -> None:
        self.deleted_at = datetime.utcnow()

    def restore(self) -> None:
        self.deleted_at = None
