"""
Job application submissions — Step 24 Messages inbox.

New table; public careers apply form will connect in a future release.
"""

from __future__ import annotations

from datetime import datetime

from app.extensions import db
from app.models.base import BaseModel


class JobApplication(BaseModel):
    """Stored job application form submission."""

    __tablename__ = "job_applications"
    __table_args__ = (
        db.Index("ix_job_applications_is_read_created_at", "is_read", "created_at"),
        db.Index("ix_job_applications_archived_created_at", "is_archived", "created_at"),
    )

    job_listing_id = db.Column(db.Integer, db.ForeignKey("job_listings.id"), nullable=True, index=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    phone = db.Column(db.String(50))
    position = db.Column(db.String(200))
    years_experience = db.Column(db.String(50))
    education = db.Column(db.String(200))
    cover_letter = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    is_starred = db.Column(db.Boolean, default=False, nullable=False)
    is_archived = db.Column(db.Boolean, default=False, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    admin_notes = db.Column(db.Text, default="")
    reply_subject = db.Column(db.String(200), default="")
    reply_body = db.Column(db.Text, default="")
    replied_at = db.Column(db.DateTime, nullable=True)
    replied_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    extra_json = db.Column(db.Text, default="{}")

    job_listing = db.relationship("JobListing", backref=db.backref("applications", lazy="dynamic"))

    def mark_deleted(self) -> None:
        self.deleted_at = datetime.utcnow()

    def restore(self) -> None:
        self.deleted_at = None
