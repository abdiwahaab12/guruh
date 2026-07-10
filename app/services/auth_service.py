"""Authentication business logic — Route → AuthService → AuthProvider → Models."""

from __future__ import annotations

from datetime import datetime, timedelta

from flask import current_app, url_for

from app.constants.rbac import PERMISSION_VIEW_DASHBOARD
from app.providers.auth_provider import AuthProvider, user_to_dto
from app.schemas.auth import LoginResultDTO, PasswordResetResultDTO


class AuthService:
    """Enterprise CMS authentication service."""

    @staticmethod
    def get_user_by_id(user_id: int):
        return AuthProvider.get_user_by_id(user_id)

    @staticmethod
    def authenticate(
        email: str,
        password: str,
        *,
        ip_address: str | None = None,
        user_agent: str | None = None,
        remember: bool = False,
    ) -> LoginResultDTO:
        normalized_email = email.lower().strip()
        user = AuthProvider.get_user_by_email(normalized_email)

        if not user:
            AuthProvider.record_login_attempt(
                email=normalized_email,
                success=False,
                failure_reason="unknown_email",
                ip_address=ip_address,
                user_agent=user_agent,
            )
            AuthProvider.commit()
            return LoginResultDTO(
                success=False,
                message="Invalid email or password.",
                failure_code="invalid_credentials",
            )

        if not user.is_active:
            AuthProvider.record_login_attempt(
                email=normalized_email,
                success=False,
                user=user,
                failure_reason="inactive_account",
                ip_address=ip_address,
                user_agent=user_agent,
            )
            AuthProvider.commit()
            return LoginResultDTO(
                success=False,
                message="This account has been deactivated. Contact an administrator.",
                failure_code="inactive",
            )

        if user.is_locked:
            AuthProvider.record_login_attempt(
                email=normalized_email,
                success=False,
                user=user,
                failure_reason="account_locked",
                ip_address=ip_address,
                user_agent=user_agent,
            )
            AuthProvider.commit()
            return LoginResultDTO(
                success=False,
                message="Account temporarily locked due to failed login attempts. Try again later.",
                failure_code="locked",
            )

        if not user.check_password(password):
            AuthProvider.increment_failed_login(user)
            AuthProvider.record_login_attempt(
                email=normalized_email,
                success=False,
                user=user,
                failure_reason="invalid_password",
                ip_address=ip_address,
                user_agent=user_agent,
            )
            AuthProvider.commit()
            return LoginResultDTO(
                success=False,
                message="Invalid email or password.",
                failure_code="invalid_credentials",
            )

        if not user.has_permission(PERMISSION_VIEW_DASHBOARD):
            AuthProvider.record_login_attempt(
                email=normalized_email,
                success=False,
                user=user,
                failure_reason="no_dashboard_access",
                ip_address=ip_address,
                user_agent=user_agent,
            )
            AuthProvider.commit()
            return LoginResultDTO(
                success=False,
                message="You do not have permission to access the admin dashboard.",
                failure_code="forbidden",
            )

        AuthProvider.update_last_login(user, ip_address)
        AuthProvider.create_user_session(
            user,
            ip_address=ip_address,
            user_agent=user_agent,
            remember=remember,
        )
        AuthProvider.record_login_attempt(
            email=normalized_email,
            success=True,
            user=user,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        if not AuthProvider.commit():
            return LoginResultDTO(
                success=False,
                message="Unable to complete login. Please try again.",
                failure_code="db_error",
            )

        return LoginResultDTO(
            success=True,
            user=user_to_dto(user),
            message="Login successful.",
        )

    @staticmethod
    def logout_user(user) -> None:
        if user and user.is_authenticated:
            AuthProvider.deactivate_user_sessions(user)
            AuthProvider.commit()

    @staticmethod
    def request_password_reset(email: str, *, ip_address: str | None = None) -> PasswordResetResultDTO:
        normalized_email = email.lower().strip()
        user = AuthProvider.get_user_by_email(normalized_email)

        generic_message = (
            "If an account exists for that email, password reset instructions have been sent."
        )

        if not user or not user.is_active:
            return PasswordResetResultDTO(success=True, message=generic_message)

        reset = AuthProvider.create_password_reset(user, ip_address=ip_address)
        if not AuthProvider.commit():
            return PasswordResetResultDTO(
                success=False,
                message="Unable to process request. Please try again later.",
            )

        reset_url = url_for("admin.reset_password", token=reset.token, _external=True)
        current_app.logger.info("Password reset URL for %s: %s", normalized_email, reset_url)

        return PasswordResetResultDTO(
            success=True,
            message=generic_message,
            reset_token=reset.token,
        )

    @staticmethod
    def reset_password(token: str, new_password: str) -> PasswordResetResultDTO:
        reset = AuthProvider.get_valid_password_reset(token)
        if not reset:
            return PasswordResetResultDTO(
                success=False,
                message="Invalid or expired reset link. Please request a new password reset.",
            )

        user = reset.user
        if not user or not user.is_active:
            return PasswordResetResultDTO(
                success=False,
                message="Invalid or expired reset link. Please request a new password reset.",
            )

        user.set_password(new_password)
        AuthProvider.mark_password_reset_used(reset)
        AuthProvider.reset_failed_login(user)
        AuthProvider.deactivate_user_sessions(user)

        if not AuthProvider.commit():
            return PasswordResetResultDTO(
                success=False,
                message="Unable to reset password. Please try again.",
            )

        return PasswordResetResultDTO(
            success=True,
            message="Your password has been reset. You can now sign in.",
        )

    @staticmethod
    def touch_session(session: dict) -> bool:
        """Return False if idle session has expired."""
        timeout_minutes = current_app.config.get("SESSION_IDLE_TIMEOUT_MINUTES", 30)
        last_activity = session.get("_last_activity")
        now = datetime.utcnow()

        if last_activity:
            if isinstance(last_activity, str):
                last_activity = datetime.fromisoformat(last_activity)
            if now - last_activity > timedelta(minutes=timeout_minutes):
                return False

        session["_last_activity"] = now.isoformat()
        session.modified = True
        return True

    @staticmethod
    def validate_password_strength(password: str) -> tuple[bool, str]:
        min_length = current_app.config.get("PASSWORD_MIN_LENGTH", 8)
        if len(password) < min_length:
            return False, f"Password must be at least {min_length} characters."
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter."
        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter."
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one number."
        return True, ""
