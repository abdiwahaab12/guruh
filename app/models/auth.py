"""Authentication and authorization SQLAlchemy models — MySQL ready."""

from __future__ import annotations

from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.constants.rbac import ROLE_SUPER_ADMIN
from app.extensions import db
from app.models.base import BaseModel


class Role(BaseModel):
    """RBAC role — assigned to users."""

    __tablename__ = "roles"

    slug = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default="")
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    users = db.relationship("User", back_populates="role", lazy="dynamic")
    role_permissions = db.relationship(
        "RolePermission",
        back_populates="role",
        cascade="all, delete-orphan",
        lazy="joined",
    )

    @property
    def permissions(self) -> list["Permission"]:
        return [rp.permission for rp in self.role_permissions if rp.permission.is_active]


class Permission(BaseModel):
    """Granular CMS permission."""

    __tablename__ = "permissions"

    slug = db.Column(db.String(80), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, default="")
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    role_permissions = db.relationship(
        "RolePermission",
        back_populates="permission",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )


class RolePermission(BaseModel):
    """Many-to-many join: roles ↔ permissions."""

    __tablename__ = "role_permissions"
    __table_args__ = (db.UniqueConstraint("role_id", "permission_id", name="uq_role_permission"),)

    role_id = db.Column(db.Integer, db.ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    permission_id = db.Column(
        db.Integer, db.ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False
    )

    role = db.relationship("Role", back_populates="role_permissions")
    permission = db.relationship("Permission", back_populates="role_permissions")


class User(BaseModel, UserMixin):
    """CMS admin user account."""

    __tablename__ = "users"

    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False, default="")
    last_name = db.Column(db.String(100), nullable=False, default="")
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    failed_login_attempts = db.Column(db.Integer, default=0, nullable=False)
    locked_until = db.Column(db.DateTime, nullable=True)
    last_login_at = db.Column(db.DateTime, nullable=True)
    last_login_ip = db.Column(db.String(45), nullable=True)

    role = db.relationship("Role", back_populates="users", lazy="joined")
    sessions = db.relationship("UserSession", back_populates="user", lazy="dynamic")
    password_resets = db.relationship("PasswordReset", back_populates="user", lazy="dynamic")
    login_history = db.relationship("LoginHistory", back_populates="user", lazy="dynamic")

    def get_id(self) -> str:
        return str(self.id)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip() or self.email

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def is_locked(self) -> bool:
        if self.locked_until is None:
            return False
        return datetime.utcnow() < self.locked_until

    def has_permission(self, permission_slug: str) -> bool:
        if not self.is_active:
            return False
        if self.role and self.role.slug == ROLE_SUPER_ADMIN:
            return True
        return any(p.slug == permission_slug for p in self.role.permissions)

    def has_any_permission(self, *permission_slugs: str) -> bool:
        return any(self.has_permission(slug) for slug in permission_slugs)


class UserSession(BaseModel):
    """Active login session — audit and session management."""

    __tablename__ = "user_sessions"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    session_token = db.Column(db.String(128), unique=True, nullable=False, index=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(512), nullable=True)
    expires_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    logged_out_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User", back_populates="sessions")


class PasswordReset(BaseModel):
    """Password reset token — single use with expiry."""

    __tablename__ = "password_resets"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = db.Column(db.String(128), unique=True, nullable=False, index=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    used_at = db.Column(db.DateTime, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)

    user = db.relationship("User", back_populates="password_resets")

    @property
    def is_valid(self) -> bool:
        if self.used_at is not None:
            return False
        return datetime.utcnow() < self.expires_at


class LoginHistory(BaseModel):
    """Login attempt audit trail — success and failure."""

    __tablename__ = "login_history"
    __table_args__ = (db.Index("ix_login_history_user_id_created_at", "user_id", "created_at"),)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    email_attempted = db.Column(db.String(255), nullable=False, index=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(512), nullable=True)
    success = db.Column(db.Boolean, default=False, nullable=False)
    failure_reason = db.Column(db.String(120), nullable=True)

    user = db.relationship("User", back_populates="login_history")


class AuditLog(BaseModel):
    """Audit log placeholder — admin actions recorded in future CMS steps."""

    __tablename__ = "audit_logs"
    __table_args__ = (
        db.Index("ix_audit_logs_resource_type_resource_id", "resource_type", "resource_id"),
    )

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = db.Column(db.String(80), nullable=False, index=True)
    resource_type = db.Column(db.String(80), nullable=True)
    resource_id = db.Column(db.String(80), nullable=True)
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)

    user = db.relationship("User", foreign_keys=[user_id])
