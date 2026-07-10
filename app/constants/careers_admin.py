"""Careers admin module — filter options and constants."""

from __future__ import annotations

from typing import Final

from app.data.careers_catalog import EXPERIENCE_LEVELS, JOBS_CATALOG

JOB_DEPARTMENTS: Final[list[str]] = sorted(
    {j.get("department", "") for j in JOBS_CATALOG if j.get("department")}
)

JOB_LOCATIONS: Final[list[str]] = sorted(
    {j.get("location", "") for j in JOBS_CATALOG if j.get("location")}
)

EMPLOYMENT_TYPES: Final[list[str]] = [
    "Full-time",
    "Part-time",
    "Contract",
    "Internship",
    "Temporary",
]

JOB_STATUSES: Final[list[tuple[str, str]]] = [
    ("draft", "Draft"),
    ("active", "Active"),
    ("closed", "Closed"),
]

STATUS_FILTER_OPTIONS: Final[dict[str, str]] = {
    "": "All (non-deleted)",
    "draft": "Draft",
    "active": "Active",
    "closed": "Closed",
}

DEFAULT_PER_PAGE: Final[int] = 20
MAX_PER_PAGE: Final[int] = 100

BULK_ACTIONS: Final[dict[str, str]] = {
    "feature": "Mark Featured",
    "unfeature": "Remove Featured",
    "activate": "Publish / Activate",
    "close": "Close Job",
    "deactivate": "Soft Delete",
    "restore": "Restore",
}

SORT_OPTIONS: Final[dict[str, str]] = {
    "date_desc": "Newest first",
    "date_asc": "Oldest first",
    "title_asc": "Title A–Z",
    "title_desc": "Title Z–A",
    "sort_order": "Manual order",
    "deadline_asc": "Deadline soonest",
}

CAREERS_FORM_TABS: Final[list[dict[str, str]]] = [
    {"slug": "general", "label": "General", "icon": "bi-info-circle"},
    {"slug": "details", "label": "Job Details", "icon": "bi-file-text"},
    {"slug": "application", "label": "Application Settings", "icon": "bi-envelope"},
    {"slug": "seo", "label": "SEO", "icon": "bi-search"},
]

__all__ = [
    "JOB_DEPARTMENTS",
    "JOB_LOCATIONS",
    "EMPLOYMENT_TYPES",
    "EXPERIENCE_LEVELS",
    "JOB_STATUSES",
    "STATUS_FILTER_OPTIONS",
    "DEFAULT_PER_PAGE",
    "MAX_PER_PAGE",
    "BULK_ACTIONS",
    "SORT_OPTIONS",
    "CAREERS_FORM_TABS",
]
