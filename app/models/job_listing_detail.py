"""
Extended job listing admin data — Step 22 Careers Management.

One-to-one with JobListing; keeps core JobListing model unchanged for public site compatibility.
"""

from __future__ import annotations

from datetime import datetime

from app.extensions import db
from app.models.base import BaseModel


class JobListingDetail(BaseModel):
    """SEO, application settings, extended content, and workflow status for a job."""

    __tablename__ = "job_listing_details"

    job_listing_id = db.Column(
        db.Integer,
        db.ForeignKey("job_listings.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    status = db.Column(db.String(20), default="draft", nullable=False)
    short_description = db.Column(db.String(500), default="")
    experience_required = db.Column(db.String(100), default="")
    image = db.Column(db.String(255), default="")

    responsibilities_json = db.Column(db.Text, default="[]")
    qualifications_json = db.Column(db.Text, default="[]")
    skills_json = db.Column(db.Text, default="[]")
    benefits_json = db.Column(db.Text, default="[]")

    is_featured = db.Column(db.Boolean, default=False, nullable=False)
    accept_applications = db.Column(db.Boolean, default=True, nullable=False)
    notify_email = db.Column(db.String(120), default="")
    auto_reply_enabled = db.Column(db.Boolean, default=False, nullable=False)
    auto_reply_message = db.Column(db.Text, default="")

    meta_title = db.Column(db.String(200), default="")
    meta_description = db.Column(db.String(500), default="")
    og_image = db.Column(db.String(255), default="")
    canonical_url = db.Column(db.String(500), default="")

    deleted_at = db.Column(db.DateTime, nullable=True)

    job_listing = db.relationship("JobListing", backref=db.backref("detail", uselist=False))

    def mark_deleted(self) -> None:
        self.deleted_at = datetime.utcnow()

    def restore(self) -> None:
        self.deleted_at = None
