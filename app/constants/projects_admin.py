"""Projects admin module — filter options and constants."""

from __future__ import annotations

from typing import Final

from app.data.projects_catalog import (
    PROJECT_CLIENTS,
    PROJECT_COUNTIES,
    PROJECT_COUNTRIES,
    PROJECT_REGIONS_SOMALIA,
    PROJECT_STATUSES,
    PROJECT_YEARS,
    PROJECTS_CATALOG,
)

PROJECT_CATEGORIES: Final[list[str]] = sorted(
    {p.get("category", "") for p in PROJECTS_CATALOG if p.get("category")}
)

SOMALIA_COUNTIES: Final[list[str]] = list(PROJECT_REGIONS_SOMALIA)

DEFAULT_PER_PAGE: Final[int] = 20
MAX_PER_PAGE: Final[int] = 100

BULK_ACTIONS: Final[dict[str, str]] = {
    "feature": "Mark Featured",
    "unfeature": "Remove Featured",
    "activate": "Activate",
    "deactivate": "Soft Delete",
    "restore": "Restore",
}

SORT_OPTIONS: Final[dict[str, str]] = {
    "date_desc": "Newest first",
    "date_asc": "Oldest first",
    "title_asc": "Title A–Z",
    "title_desc": "Title Z–A",
    "sort_order": "Manual order",
}

PROJECT_FORM_TABS: Final[list[dict[str, str]]] = [
    {"slug": "general", "label": "General", "icon": "bi-info-circle"},
    {"slug": "location", "label": "Location", "icon": "bi-geo-alt"},
    {"slug": "services", "label": "Services", "icon": "bi-grid"},
    {"slug": "equipment", "label": "Equipment", "icon": "bi-truck"},
    {"slug": "team", "label": "Team", "icon": "bi-people"},
    {"slug": "seo", "label": "SEO", "icon": "bi-search"},
    {"slug": "gallery", "label": "Gallery", "icon": "bi-images"},
    {"slug": "documents", "label": "Documents", "icon": "bi-file-earmark"},
    {"slug": "timeline", "label": "Timeline", "icon": "bi-calendar-event"},
    {"slug": "content", "label": "Challenges & Solutions", "icon": "bi-lightbulb"},
    {"slug": "related", "label": "Related", "icon": "bi-link-45deg"},
]

__all__ = [
    "PROJECT_CATEGORIES",
    "PROJECT_CLIENTS",
    "PROJECT_COUNTIES",
    "PROJECT_COUNTRIES",
    "SOMALIA_COUNTIES",
    "PROJECT_STATUSES",
    "PROJECT_YEARS",
    "DEFAULT_PER_PAGE",
    "MAX_PER_PAGE",
    "BULK_ACTIONS",
    "SORT_OPTIONS",
    "PROJECT_FORM_TABS",
]
