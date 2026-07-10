"""
Extended project admin data — Step 17 Projects Management.

One-to-one with Project; keeps core Project model unchanged for public site compatibility.
"""

from __future__ import annotations

from datetime import datetime

from app.extensions import db
from app.models.base import BaseModel


class ProjectDetail(BaseModel):
    """SEO, relationships, timeline, and extended content for a project."""

    __tablename__ = "project_details"

    project_id = db.Column(
        db.Integer,
        db.ForeignKey("projects.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    meta_title = db.Column(db.String(200), default="")
    meta_description = db.Column(db.String(500), default="")
    og_image = db.Column(db.String(255), default="")
    canonical_url = db.Column(db.String(500), default="")

    overview = db.Column(db.Text, default="")
    consultant = db.Column(db.String(150), default="")
    duration = db.Column(db.String(100), default="")
    completion_year = db.Column(db.String(10), default="")

    challenges_json = db.Column(db.Text, default="[]")
    solutions_json = db.Column(db.Text, default="[]")
    scope_of_work_json = db.Column(db.Text, default="[]")
    timeline_json = db.Column(db.Text, default="[]")

    service_slugs_json = db.Column(db.Text, default="[]")
    equipment_json = db.Column(db.Text, default="[]")
    team_member_ids_json = db.Column(db.Text, default="[]")
    related_project_ids_json = db.Column(db.Text, default="[]")
    related_service_slugs_json = db.Column(db.Text, default="[]")
    document_paths_json = db.Column(db.Text, default="[]")

    deleted_at = db.Column(db.DateTime, nullable=True)

    project = db.relationship("Project", backref=db.backref("detail", uselist=False))

    def mark_deleted(self) -> None:
        self.deleted_at = datetime.utcnow()

    def restore(self) -> None:
        self.deleted_at = None
