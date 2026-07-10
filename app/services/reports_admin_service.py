"""Reports & Analytics admin business logic."""

from __future__ import annotations

from flask import url_for
from flask_login import current_user

from app.constants.reports_admin import AUDIT_TABS, DATE_PRESETS, EXPORT_FORMATS, REPORTS_TABS, TAB_AUDIT, TAB_OVERVIEW
from app.providers.admin_dashboard_provider import AdminDashboardProvider
from app.providers.reports_admin_provider import ReportsAdminProvider
from app.schemas.admin import BreadcrumbItemDTO
from app.schemas.reports_admin import ExportResultDTO
from app.utils.report_export import export_csv, export_excel, export_pdf


class ReportsAdminService:
    """Enterprise reports and analytics service."""

    @staticmethod
    def get_shell_context(
        *,
        page_title: str,
        active_tab: str = TAB_OVERVIEW,
        audit_tab: str = "user",
        date_range=None,
    ) -> dict:
        dashboard = AdminDashboardProvider.get_dashboard()
        return {
            "page_title": page_title,
            "active_nav": "reports",
            "reports_active_section": active_tab,
            "active_tab": active_tab,
            "audit_tab": audit_tab,
            "reports_tabs": REPORTS_TABS,
            "audit_tabs": AUDIT_TABS,
            "date_presets": DATE_PRESETS,
            "export_formats": EXPORT_FORMATS,
            "date_range": date_range,
            "breadcrumbs": [
                BreadcrumbItemDTO("Admin", url_for("admin.dashboard"), False),
                BreadcrumbItemDTO("Reports", None, True),
            ],
            "notifications": dashboard.notifications,
            "unread_notification_count": dashboard.unread_notification_count,
            "user": current_user,
        }

    @staticmethod
    def get_dashboard_context(
        *,
        preset: str = "month",
        date_from: str = "",
        date_to: str = "",
        tab: str = TAB_OVERVIEW,
        audit_tab: str = "user",
    ) -> dict:
        start, end, date_range = ReportsAdminProvider.parse_date_range(preset, date_from=date_from, date_to=date_to)
        ctx = ReportsAdminService.get_shell_context(
            page_title="Reports & Analytics",
            active_tab=tab,
            audit_tab=audit_tab,
            date_range=date_range,
        )
        ctx["overview"] = ReportsAdminProvider.get_overview(start, end)
        ctx["audit_report"] = ReportsAdminProvider.get_audit_report(audit_tab, start, end)
        ctx["chart_data"] = [c.__dict__ for c in ctx["overview"].charts]
        return ctx

    @staticmethod
    def export_report(
        *,
        report_type: str,
        fmt: str,
        preset: str = "month",
        date_from: str = "",
        date_to: str = "",
        audit_tab: str = "user",
        ip_address: str | None = None,
    ) -> ExportResultDTO:
        start, end, date_range = ReportsAdminProvider.parse_date_range(preset, date_from=date_from, date_to=date_to)

        if report_type.startswith("audit"):
            tab = audit_tab if report_type == "audit" else report_type.replace("audit_", "")
            report = ReportsAdminProvider.get_audit_report(tab, start, end)
            rows = ReportsAdminProvider.audit_export_rows(report)
            title = f"GURUH CMS — {report.title} ({date_range.label})"
        else:
            overview = ReportsAdminProvider.get_overview(start, end)
            rows = ReportsAdminProvider.overview_export_rows(overview)
            title = f"GURUH CMS — Overview Report ({date_range.label})"

        filename_base = f"guruh-report-{report_type}-{date_range.preset}"
        if fmt == "csv":
            data = export_csv(rows)
            mime = "text/csv"
            filename = f"{filename_base}.csv"
        elif fmt == "excel":
            data = export_excel(rows, sheet_name=report_type)
            mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            filename = f"{filename_base}.xlsx"
        elif fmt == "pdf":
            data = export_pdf(title, rows)
            mime = "application/pdf"
            filename = f"{filename_base}.pdf"
        else:
            return ExportResultDTO(False, "Unsupported export format.")

        ReportsAdminProvider.record_audit(
            user_id=current_user.id,
            action="reports.export",
            resource_type="report",
            resource_id=f"{report_type}:{fmt}",
            details=f"Exported {report_type} as {fmt} for {date_range.label}",
            ip_address=ip_address or "",
        )
        if not ReportsAdminProvider.commit():
            return ExportResultDTO(False, "Export audit failed.")

        return ExportResultDTO(True, "Export ready.", data=data, mime_type=mime, filename=filename)
