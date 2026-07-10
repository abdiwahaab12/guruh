"""Authentication data provider — MySQL / SQLAlchemy access layer."""

from __future__ import annotations

import secrets
from datetime import datetime, timedelta

from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models.auth import AuditLog, LoginHistory, PasswordReset, User, UserSession
from app.schemas.auth import PermissionDTO, RoleDTO, UserDTO


def _role_to_dto(role) -> RoleDTO:
    return RoleDTO(
        id=role.id,
        slug=role.slug,
        name=role.name,
        description=role.description or "",
        is_active=role.is_active,
    )


def user_to_dto(user: User) -> UserDTO:
    perms = [p.slug for p in user.role.permissions] if user.role else []
    return UserDTO(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=_role_to_dto(user.role),
        is_active=user.is_active,
        last_login_at=user.last_login_at,
        last_login_ip=user.last_login_ip,
        permission_slugs=perms,
    )


class AuthProvider:
    """Database-backed authentication operations."""

    @staticmethod
    def get_user_by_id(user_id: int) -> User | None:
        try:
            return User.query.filter_by(id=user_id, is_active=True).first()
        except SQLAlchemyError as exc:
            current_app.logger.error("get_user_by_id failed: %s", exc)
            return None

    @staticmethod
    def get_user_by_email(email: str) -> User | None:
        try:
            return User.query.filter_by(email=email.lower().strip()).first()
        except SQLAlchemyError as exc:
            current_app.logger.error("get_user_by_email failed: %s", exc)
            return None

    @staticmethod
    def record_login_attempt(
        *,
        email: str,
        success: bool,
        user: User | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        failure_reason: str | None = None,
    ) -> None:
        entry = LoginHistory(
            user_id=user.id if user else None,
            email_attempted=email.lower().strip(),
            ip_address=ip_address,
            user_agent=(user_agent or "")[:512],
            success=success,
            failure_reason=failure_reason,
        )
        db.session.add(entry)

    @staticmethod
    def increment_failed_login(user: User) -> None:
        max_attempts = current_app.config.get("MAX_LOGIN_ATTEMPTS", 5)
        lockout_minutes = current_app.config.get("LOCKOUT_DURATION_MINUTES", 15)
        user.failed_login_attempts += 1
        if user.failed_login_attempts >= max_attempts:
            user.locked_until = datetime.utcnow() + timedelta(minutes=lockout_minutes)

    @staticmethod
    def reset_failed_login(user: User) -> None:
        user.failed_login_attempts = 0
        user.locked_until = None

    @staticmethod
    def update_last_login(user: User, ip_address: str | None = None) -> None:
        user.last_login_at = datetime.utcnow()
        user.last_login_ip = ip_address
        AuthProvider.reset_failed_login(user)

    @staticmethod
    def create_user_session(
        user: User,
        *,
        ip_address: str | None = None,
        user_agent: str | None = None,
        remember: bool = False,
    ) -> UserSession:
        lifetime = (
            current_app.config.get("REMEMBER_COOKIE_DURATION")
            if remember
            else current_app.config.get("PERMANENT_SESSION_LIFETIME")
        )
        expires_at = datetime.utcnow() + lifetime if lifetime else None
        session = UserSession(
            user_id=user.id,
            session_token=secrets.token_urlsafe(32),
            ip_address=ip_address,
            user_agent=(user_agent or "")[:512],
            expires_at=expires_at,
            is_active=True,
        )
        db.session.add(session)
        return session

    @staticmethod
    def deactivate_user_sessions(user: User) -> None:
        now = datetime.utcnow()
        for session in user.sessions.filter_by(is_active=True):
            session.is_active = False
            session.logged_out_at = now

    @staticmethod
    def create_password_reset(user: User, ip_address: str | None = None) -> PasswordReset:
        expiry_hours = current_app.config.get("PASSWORD_RESET_EXPIRY_HOURS", 1)
        reset = PasswordReset(
            user_id=user.id,
            token=secrets.token_urlsafe(48),
            expires_at=datetime.utcnow() + timedelta(hours=expiry_hours),
            ip_address=ip_address,
        )
        db.session.add(reset)
        return reset

    @staticmethod
    def get_valid_password_reset(token: str) -> PasswordReset | None:
        try:
            reset = PasswordReset.query.filter_by(token=token).first()
            if reset and reset.is_valid:
                return reset
        except SQLAlchemyError as exc:
            current_app.logger.error("get_valid_password_reset failed: %s", exc)
        return None

    @staticmethod
    def mark_password_reset_used(reset: PasswordReset) -> None:
        reset.used_at = datetime.utcnow()

    @staticmethod
    def commit() -> bool:
        try:
            db.session.commit()
            return True
        except SQLAlchemyError as exc:
            db.session.rollback()
            current_app.logger.error("Auth DB commit failed: %s", exc)
            return False

    @staticmethod
    def rollback() -> None:
        db.session.rollback()

    @staticmethod
    def record_audit_event(
        *,
        user_id: int | None,
        action: str,
        resource_type: str | None = None,
        resource_id: str | None = None,
        details: str | None = None,
        ip_address: str | None = None,
    ) -> None:
        """Persist an audit log entry — used by future admin CMS modules."""
        from app.models.auth import AuditLog

        entry = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
        )
        db.session.add(entry)
