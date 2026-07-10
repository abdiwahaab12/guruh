"""Admin dashboard and module placeholder routes."""

from __future__ import annotations

from flask import abort, render_template

from app.constants.admin_nav import MODULE_SLUGS
from app.services.admin_service import AdminDashboardService
from app.utils.permissions import can_view_dashboard


def register_dashboard_routes(admin_bp) -> None:
    """Register dashboard home and future module placeholder routes."""

    @admin_bp.route("/")
    @can_view_dashboard
    def dashboard():
        context = AdminDashboardService.get_dashboard_context()
        return render_template("admin/dashboard/index.html", **context)

    @admin_bp.route("/<module_slug>")
    @can_view_dashboard
    def module(module_slug: str):
        if module_slug not in MODULE_SLUGS:
            abort(404)
        context = AdminDashboardService.get_module_context(module_slug)
        if context is None:
            abort(404)
        return render_template("admin/module_placeholder.html", **context)
