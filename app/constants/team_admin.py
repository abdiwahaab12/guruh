"""Team admin module — filter options and constants."""

from __future__ import annotations

from typing import Final

from app.data.team_catalog import TEAM_CATALOG

TEAM_DEPARTMENTS: Final[list[str]] = sorted(
    {m.get("department", "") for m in TEAM_CATALOG if m.get("department")}
)

TEAM_POSITIONS: Final[list[str]] = sorted({m["position"] for m in TEAM_CATALOG if m.get("position")})

MEMBER_TYPES: Final[list[tuple[str, str]]] = [
    ("director", "Director"),
    ("executive", "Management"),
    ("staff", "Staff"),
]

MEMBER_TYPE_SLUGS: Final[list[str]] = [t[0] for t in MEMBER_TYPES]

SOCIAL_PLATFORMS: Final[list[tuple[str, str]]] = [
    ("linkedin", "LinkedIn"),
    ("twitter", "Twitter / X"),
    ("facebook", "Facebook"),
    ("instagram", "Instagram"),
    ("email", "Email"),
    ("website", "Website"),
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

TEAM_FORM_TABS: Final[list[dict[str, str]]] = [
    {"slug": "general", "label": "General", "icon": "bi-person"},
    {"slug": "professional", "label": "Professional Information", "icon": "bi-briefcase"},
    {"slug": "biography", "label": "Biography", "icon": "bi-file-text"},
    {"slug": "media", "label": "Media", "icon": "bi-images"},
    {"slug": "social", "label": "Social Links", "icon": "bi-share"},
    {"slug": "seo", "label": "SEO", "icon": "bi-search"},
]

__all__ = [
    "TEAM_DEPARTMENTS",
    "TEAM_POSITIONS",
    "MEMBER_TYPES",
    "MEMBER_TYPE_SLUGS",
    "SOCIAL_PLATFORMS",
    "DEFAULT_PER_PAGE",
    "MAX_PER_PAGE",
    "BULK_ACTIONS",
    "SORT_OPTIONS",
    "FEATURED_FILTER_OPTIONS",
    "STATUS_FILTER_OPTIONS",
    "TEAM_FORM_TABS",
]
