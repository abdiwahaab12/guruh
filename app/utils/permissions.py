"""RBAC permission decorators and middleware helpers."""

from __future__ import annotations

from functools import wraps

from flask import abort, redirect, request, url_for
from flask_login import current_user

from app.constants.rbac import (
    PERMISSION_MANAGE_CAREERS,
    PERMISSION_MANAGE_CONTACTS,
    PERMISSION_MANAGE_EQUIPMENT,
    PERMISSION_MANAGE_GALLERY,
    PERMISSION_MANAGE_JOB_APPLICATIONS,
    PERMISSION_MANAGE_MEDIA,
    PERMISSION_MANAGE_PAGES,
    PERMISSION_MANAGE_PROJECTS,
    PERMISSION_MANAGE_QUOTES,
    PERMISSION_MANAGE_SERVICES,
    PERMISSION_MANAGE_SETTINGS,
    PERMISSION_MANAGE_TEAM,
    PERMISSION_MANAGE_USERS,
    PERMISSION_VIEW_DASHBOARD,
    PERMISSION_VIEW_REPORTS,
    ROLE_SUPER_ADMIN,
)


def permission_required(permission_slug: str):
    """Require authenticated user with a specific permission."""

    def decorator(view_func):
        @wraps(view_func)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("admin.login", next=request.url))
            if not current_user.has_permission(permission_slug):
                abort(403)
            return view_func(*args, **kwargs)

        return wrapped

    return decorator


def role_required(*role_slugs: str):
    """Require authenticated user with one of the specified roles."""

    def decorator(view_func):
        @wraps(view_func)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("admin.login", next=request.url))
            if current_user.role.slug not in role_slugs:
                abort(403)
            return view_func(*args, **kwargs)

        return wrapped

    return decorator


super_admin_required = role_required(ROLE_SUPER_ADMIN)

# Permission decorator shortcuts
can_manage_pages = permission_required(PERMISSION_MANAGE_PAGES)
can_manage_projects = permission_required(PERMISSION_MANAGE_PROJECTS)
can_manage_gallery = permission_required(PERMISSION_MANAGE_GALLERY)
can_manage_equipment = permission_required(PERMISSION_MANAGE_EQUIPMENT)
can_manage_team = permission_required(PERMISSION_MANAGE_TEAM)
can_manage_users = permission_required(PERMISSION_MANAGE_USERS)
can_manage_settings = permission_required(PERMISSION_MANAGE_SETTINGS)
can_manage_quotes = permission_required(PERMISSION_MANAGE_QUOTES)
can_manage_contacts = permission_required(PERMISSION_MANAGE_CONTACTS)
can_manage_services = permission_required(PERMISSION_MANAGE_SERVICES)
can_manage_careers = permission_required(PERMISSION_MANAGE_CAREERS)
can_manage_job_applications = permission_required(PERMISSION_MANAGE_JOB_APPLICATIONS)
can_manage_media = permission_required(PERMISSION_MANAGE_MEDIA)
can_view_dashboard = permission_required(PERMISSION_VIEW_DASHBOARD)
can_view_reports = permission_required(PERMISSION_VIEW_REPORTS)

MESSAGE_INBOX_PERMISSIONS = (
    PERMISSION_MANAGE_CONTACTS,
    PERMISSION_MANAGE_QUOTES,
    PERMISSION_MANAGE_JOB_APPLICATIONS,
)


def can_access_messages(view_func):
    """Require at least one messages inbox permission."""

    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("admin.login", next=request.url))
        if not any(current_user.has_permission(p) for p in MESSAGE_INBOX_PERMISSIONS):
            abort(403)
        return view_func(*args, **kwargs)

    return wrapped
