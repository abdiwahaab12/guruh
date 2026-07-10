"""Admin authentication middleware — protects all non-public admin routes."""

from __future__ import annotations

from flask import redirect, request, url_for
from flask_login import current_user

# Routes accessible without authentication
PUBLIC_ADMIN_ENDPOINTS: frozenset[str] = frozenset(
    {
        "admin.login",
        "admin.forgot_password",
        "admin.reset_password",
        "admin.unauthorized_page",
        "admin.forbidden_page",
        "static",
    }
)


def register_admin_middleware(admin_bp) -> None:
    """Register before_request hook to enforce authentication on admin routes."""

    @admin_bp.before_request
    def require_admin_authentication():
        endpoint = request.endpoint or ""
        if endpoint in PUBLIC_ADMIN_ENDPOINTS:
            return None
        if not current_user.is_authenticated:
            return redirect(url_for("admin.login", next=request.url))
        if not getattr(current_user, "is_active", True):
            return redirect(url_for("admin.logout"))
        return None
