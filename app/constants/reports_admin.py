"""Reports & Analytics admin constants — Step 26."""

from __future__ import annotations

from typing import Final

TAB_OVERVIEW: Final[str] = "overview"
TAB_AUDIT: Final[str] = "audit"

REPORTS_TABS: Final[tuple[dict[str, str], ...]] = (
    {"slug": TAB_OVERVIEW, "label": "Overview", "icon": "bi-bar-chart-line"},
    {"slug": TAB_AUDIT, "label": "Audit Reports", "icon": "bi-journal-check"},
)

AUDIT_TABS: Final[tuple[dict[str, str], ...]] = (
    {"slug": "user", "label": "User Activity", "icon": "bi-person-lines-fill"},
    {"slug": "login", "label": "Login Activity", "icon": "bi-box-arrow-in-right"},
    {"slug": "system", "label": "System Activity", "icon": "bi-cpu"},
)

DATE_PRESETS: Final[dict[str, str]] = {
    "today": "Today",
    "week": "This Week",
    "month": "This Month",
    "year": "This Year",
    "custom": "Custom Range",
}

EXPORT_FORMATS: Final[dict[str, str]] = {
    "csv": "CSV",
    "excel": "Excel",
    "pdf": "PDF",
}

REPORT_TYPES: Final[dict[str, str]] = {
    "overview": "Overview Summary",
    "messages": "Messages Trend",
    "projects": "Projects by Country",
    "gallery": "Gallery Growth",
    "users": "Users Activity",
    "audit_user": "User Activity Audit",
    "audit_login": "Login Activity Audit",
    "audit_system": "System Activity Audit",
}
