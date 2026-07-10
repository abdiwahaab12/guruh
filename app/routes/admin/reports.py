"""Reports & Analytics admin routes — Step 26."""

from __future__ import annotations

from flask import Response, render_template, request

from app.constants.reports_admin import TAB_AUDIT, TAB_OVERVIEW
from app.services.reports_admin_service import ReportsAdminService
from app.utils.permissions import can_view_reports


def register_reports_routes(admin_bp) -> None:
    """Register reports and analytics routes."""

    @admin_bp.route("/reports")
    @admin_bp.route("/reports/dashboard")
    @can_view_reports
    def reports_dashboard():
        tab = request.args.get("tab", TAB_OVERVIEW)
        ctx = ReportsAdminService.get_dashboard_context(
            preset=request.args.get("preset", "month"),
            date_from=request.args.get("date_from", ""),
            date_to=request.args.get("date_to", ""),
            tab=tab,
            audit_tab=request.args.get("audit_tab", "user"),
        )
        return render_template("admin/reports/dashboard.html", **ctx)

    @admin_bp.route("/reports/export")
    @can_view_reports
    def reports_export():
        result = ReportsAdminService.export_report(
            report_type=request.args.get("report", "overview"),
            fmt=request.args.get("format", "csv"),
            preset=request.args.get("preset", "month"),
            date_from=request.args.get("date_from", ""),
            date_to=request.args.get("date_to", ""),
            audit_tab=request.args.get("audit_tab", "user"),
            ip_address=request.remote_addr,
        )
        if not result.success or not result.data:
            return Response(result.message, status=400, mimetype="text/plain")
        return Response(
            result.data,
            mimetype=result.mime_type,
            headers={"Content-Disposition": f'attachment; filename="{result.filename}"'},
        )
