"""Admin dashboard business logic — Route → AdminDashboardService → Provider → DTO."""

from __future__ import annotations

import json
from dataclasses import asdict

from flask import url_for
from flask_login import current_user

from app.constants.admin_nav import MODULE_LABELS, MODULE_SLUGS, build_sidebar_nav
from app.providers.admin_dashboard_provider import AdminDashboardProvider
from app.schemas.admin import BreadcrumbItemDTO


class AdminDashboardService:
    """Enterprise admin dashboard service."""

    @staticmethod
    def get_sidebar_nav() -> list[dict]:
        return build_sidebar_nav()

    @staticmethod
    def get_dashboard_context() -> dict:
        dashboard = AdminDashboardProvider.get_dashboard()
        return {
            "dashboard": dashboard,
            "stats": dashboard.stats,
            "charts": dashboard.charts,
            "activities": dashboard.activities,
            "notifications": dashboard.notifications,
            "unread_notification_count": dashboard.unread_notification_count,
            "quick_actions": AdminDashboardProvider.get_quick_actions(),
            "breadcrumbs": AdminDashboardService.get_breadcrumbs("Dashboard"),
            "page_title": "Dashboard",
            "active_nav": "dashboard",
            "user": current_user,
            "charts_json": AdminDashboardService._serialize_charts(dashboard.charts),
        }

    @staticmethod
    def _serialize_charts(charts) -> str:
        payload = []
        for chart in charts:
            entry = asdict(chart)
            payload.append(entry)
        return json.dumps(payload)

    @staticmethod
    def get_module_context(module_slug: str) -> dict | None:
        if module_slug not in MODULE_SLUGS:
            return None
        label = MODULE_LABELS.get(module_slug, module_slug.replace("-", " ").title())
        dashboard = AdminDashboardProvider.get_dashboard()
        return {
            "module_slug": module_slug,
            "module_label": label,
            "breadcrumbs": AdminDashboardService.get_breadcrumbs(label),
            "page_title": label,
            "active_nav": module_slug,
            "notifications": dashboard.notifications,
            "unread_notification_count": dashboard.unread_notification_count,
            "user": current_user,
        }

    @staticmethod
    def get_breadcrumbs(current_label: str) -> list[BreadcrumbItemDTO]:
        return [
            BreadcrumbItemDTO("Admin", url_for("admin.dashboard"), False),
            BreadcrumbItemDTO(current_label, None, True),
        ]

    @staticmethod
    def get_admin_shell_context(
        *,
        page_title: str,
        active_nav: str,
        breadcrumbs: list[BreadcrumbItemDTO] | None = None,
    ) -> dict:
        dashboard = AdminDashboardProvider.get_dashboard()
        return {
            "page_title": page_title,
            "active_nav": active_nav,
            "breadcrumbs": breadcrumbs
            or AdminDashboardService.get_breadcrumbs(page_title),
            "notifications": dashboard.notifications,
            "unread_notification_count": dashboard.unread_notification_count,
            "user": current_user,
        }
