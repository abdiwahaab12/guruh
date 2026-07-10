"""
Extended team admin data — Step 20 Team Management.

One-to-one with TeamMember; keeps core TeamMember model unchanged for public site compatibility.
"""

from __future__ import annotations

from datetime import datetime

from app.extensions import db
from app.models.base import BaseModel


class TeamDetail(BaseModel):
    """SEO, professional profile, relationships, and extended content for a team member."""

    __tablename__ = "team_details"

    team_member_id = db.Column(
        db.Integer,
        db.ForeignKey("team_members.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    slug = db.Column(db.String(150), unique=True, nullable=False, index=True)

    department = db.Column(db.String(150), default="")
    member_type = db.Column(db.String(50), default="staff")
    years_experience = db.Column(db.String(50), default="")
    education = db.Column(db.String(255), default="")
    experience_summary = db.Column(db.Text, default="")
    is_featured = db.Column(db.Boolean, default=False, nullable=False)

    meta_title = db.Column(db.String(200), default="")
    meta_description = db.Column(db.String(500), default="")
    og_image = db.Column(db.String(255), default="")
    canonical_url = db.Column(db.String(500), default="")

    social_links_json = db.Column(db.Text, default="[]")
    gallery_paths_json = db.Column(db.Text, default="[]")
    related_project_ids_json = db.Column(db.Text, default="[]")
    related_service_slugs_json = db.Column(db.Text, default="[]")
    related_equipment_ids_json = db.Column(db.Text, default="[]")

    deleted_at = db.Column(db.DateTime, nullable=True)

    team_member = db.relationship("TeamMember", backref=db.backref("detail", uselist=False))

    def mark_deleted(self) -> None:
        self.deleted_at = datetime.utcnow()

    def restore(self) -> None:
        self.deleted_at = None
