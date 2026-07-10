"""Extended quote request inbox data — Step 24 Messages."""

from __future__ import annotations

from datetime import datetime

from app.extensions import db
from app.models.base import BaseModel


class QuoteRequestDetail(BaseModel):
    """Inbox workflow fields for a quote request submission."""

    __tablename__ = "quote_request_details"

    quote_request_id = db.Column(
        db.Integer,
        db.ForeignKey("quote_requests.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    is_starred = db.Column(db.Boolean, default=False, nullable=False)
    is_archived = db.Column(db.Boolean, default=False, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    admin_notes = db.Column(db.Text, default="")
    reply_subject = db.Column(db.String(200), default="")
    reply_body = db.Column(db.Text, default="")
    replied_at = db.Column(db.DateTime, nullable=True)
    replied_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    extra_json = db.Column(db.Text, default="{}")

    request = db.relationship(
        "QuoteRequest",
        backref=db.backref("detail", uselist=False),
    )

    def mark_deleted(self) -> None:
        self.deleted_at = datetime.utcnow()

    def restore(self) -> None:
        self.deleted_at = None
