"""Gallery admin module — filter options and constants."""

from __future__ import annotations

from typing import Final

from app.data.gallery_catalog import GALLERY_FEATURED_ALBUMS, GALLERY_MEDIA_ITEMS

BEFORE_AFTER_CATEGORY: Final[str] = "Before & After"
PROGRESS_CATEGORY: Final[str] = "Project Progress"
AWARDS_CATEGORIES: Final[frozenset[str]] = frozenset({"Awards", "Company Events"})

GALLERY_SECTION_CATEGORIES: Final[frozenset[str]] = frozenset(
    {BEFORE_AFTER_CATEGORY, PROGRESS_CATEGORY, *AWARDS_CATEGORIES}
)

GALLERY_CATEGORIES: Final[list[str]] = sorted(
    {item.get("category", "") for item in GALLERY_MEDIA_ITEMS if item.get("category")}
    | {BEFORE_AFTER_CATEGORY, PROGRESS_CATEGORY}
)

GALLERY_ALBUMS: Final[list[tuple[str, str]]] = [    (a["filter_album"], a["title"]) for a in GALLERY_FEATURED_ALBUMS
]

GALLERY_COUNTRIES: Final[list[str]] = ["Somalia", "Kenya"]

GALLERY_COUNTIES: Final[list[str]] = sorted(
    {item.get("county", "") for item in GALLERY_MEDIA_ITEMS if item.get("county")}
)

GALLERY_YEARS: Final[list[str]] = sorted(
    {item.get("year", "") for item in GALLERY_MEDIA_ITEMS if item.get("year")},
    reverse=True,
)

MEDIA_TYPES: Final[list[tuple[str, str]]] = [
    ("image", "Image"),
    ("video", "Video"),
]

VIDEO_PROVIDERS: Final[list[tuple[str, str]]] = [
    ("", "—"),
    ("youtube", "YouTube"),
    ("vimeo", "Vimeo"),
    ("upload", "Uploaded Video"),
]

DEFAULT_PER_PAGE: Final[int] = 24
MAX_PER_PAGE: Final[int] = 96

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

GALLERY_FORM_TABS: Final[list[dict[str, str]]] = [
    {"slug": "general", "label": "General", "icon": "bi-info-circle"},
    {"slug": "media", "label": "Media", "icon": "bi-images"},
    {"slug": "relationships", "label": "Relationships", "icon": "bi-link-45deg"},
    {"slug": "seo", "label": "SEO", "icon": "bi-search"},
]

__all__ = [
    "GALLERY_CATEGORIES",
    "BEFORE_AFTER_CATEGORY",
    "PROGRESS_CATEGORY",
    "AWARDS_CATEGORIES",
    "GALLERY_SECTION_CATEGORIES",
    "GALLERY_ALBUMS",
    "GALLERY_COUNTRIES",
    "GALLERY_COUNTIES",
    "GALLERY_YEARS",
    "MEDIA_TYPES",
    "VIDEO_PROVIDERS",
    "DEFAULT_PER_PAGE",
    "MAX_PER_PAGE",
    "BULK_ACTIONS",
    "SORT_OPTIONS",
    "FEATURED_FILTER_OPTIONS",
    "STATUS_FILTER_OPTIONS",
    "GALLERY_FORM_TABS",
]
