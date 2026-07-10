"""Services admin module — filter options and constants."""

from __future__ import annotations

from typing import Final

from app.data.services_catalog import SERVICES_CATALOG

SERVICE_ICONS: Final[list[str]] = sorted(
    {s.get("icon", "") for s in SERVICES_CATALOG if s.get("icon")} | {"bi-grid"}
)

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

FEATURED_FILTER_OPTIONS: Final[dict[str, str]] = {
    "": "All",
    "yes": "Featured only",
    "no": "Not featured",
}

STATUS_FILTER_OPTIONS: Final[dict[str, str]] = {
    "": "Active only",
    "inactive": "Inactive only",
    "all": "All statuses",
}

SERVICE_FORM_TABS: Final[list[dict[str, str]]] = [
    {"slug": "general", "label": "General", "icon": "bi-info-circle"},
    {"slug": "content", "label": "Content", "icon": "bi-file-text"},
    {"slug": "media", "label": "Media", "icon": "bi-images"},
    {"slug": "related", "label": "Related Projects", "icon": "bi-building"},
    {"slug": "seo", "label": "SEO", "icon": "bi-search"},
]

__all__ = [
    "SERVICE_ICONS",
    "DEFAULT_PER_PAGE",
    "MAX_PER_PAGE",
    "BULK_ACTIONS",
    "SORT_OPTIONS",
    "FEATURED_FILTER_OPTIONS",
    "STATUS_FILTER_OPTIONS",
    "SERVICE_FORM_TABS",
]
