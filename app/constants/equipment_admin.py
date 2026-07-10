"""Equipment admin module — filter options and constants."""

from __future__ import annotations

from typing import Final

from app.data.equipment_catalog import EQUIPMENT_CATEGORIES

EQUIPMENT_CATEGORY_TITLES: Final[list[str]] = [c["title"] for c in EQUIPMENT_CATEGORIES]

CONDITION_OPTIONS: Final[list[str]] = [
    "Operational",
    "Under Maintenance",
    "Mobilised",
    "Standby",
    "Decommissioned",
]

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
    "name_asc": "Name A–Z",
    "name_desc": "Name Z–A",
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

EQUIPMENT_FORM_TABS: Final[list[dict[str, str]]] = [
    {"slug": "general", "label": "General", "icon": "bi-info-circle"},
    {"slug": "specifications", "label": "Specifications", "icon": "bi-clipboard-data"},
    {"slug": "media", "label": "Media", "icon": "bi-images"},
    {"slug": "related", "label": "Related Projects", "icon": "bi-building"},
    {"slug": "seo", "label": "SEO", "icon": "bi-search"},
]

__all__ = [
    "EQUIPMENT_CATEGORY_TITLES",
    "CONDITION_OPTIONS",
    "DEFAULT_PER_PAGE",
    "MAX_PER_PAGE",
    "BULK_ACTIONS",
    "SORT_OPTIONS",
    "FEATURED_FILTER_OPTIONS",
    "STATUS_FILTER_OPTIONS",
    "EQUIPMENT_FORM_TABS",
]
