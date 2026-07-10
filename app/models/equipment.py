"""
Equipment fleet models — Step 19 Equipment Management.

New tables; catalog.py and public providers remain unchanged for compatibility.
"""

from __future__ import annotations

from datetime import datetime

from app.extensions import db
from app.models.base import BaseModel


class Equipment(BaseModel):
    """Core equipment fleet record."""

    __tablename__ = "equipment"

    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False, index=True)
    category = db.Column(db.String(150), nullable=False)
    short_description = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255))
    capacity = db.Column(db.String(150))
    condition = db.Column(db.String(50), default="Operational", nullable=False)
    maintenance_status = db.Column(db.String(255))
    usage = db.Column(db.Text)
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    is_featured = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    detail = db.relationship(
        "EquipmentDetail",
        back_populates="equipment",
        uselist=False,
        cascade="all, delete-orphan",
    )


class EquipmentDetail(BaseModel):
    """SEO, specifications, relationships, and extended content for equipment."""

    __tablename__ = "equipment_details"

    equipment_id = db.Column(
        db.Integer,
        db.ForeignKey("equipment.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    meta_title = db.Column(db.String(200), default="")
    meta_description = db.Column(db.String(500), default="")
    og_image = db.Column(db.String(255), default="")
    canonical_url = db.Column(db.String(500), default="")

    specifications_json = db.Column(db.Text, default="[]")
    gallery_paths_json = db.Column(db.Text, default="[]")
    related_project_ids_json = db.Column(db.Text, default="[]")
    related_service_slugs_json = db.Column(db.Text, default="[]")
    team_member_ids_json = db.Column(db.Text, default="[]")

    deleted_at = db.Column(db.DateTime, nullable=True)

    equipment = db.relationship("Equipment", back_populates="detail")

    def mark_deleted(self) -> None:
        self.deleted_at = datetime.utcnow()

    def restore(self) -> None:
        self.deleted_at = None
