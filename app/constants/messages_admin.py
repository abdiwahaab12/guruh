"""Messages / Inbox admin constants — Step 24."""

from __future__ import annotations

from typing import Final

TAB_CONTACTS: Final[str] = "contacts"
TAB_QUOTES: Final[str] = "quotes"
TAB_APPLICATIONS: Final[str] = "applications"

INBOX_TABS: Final[tuple[dict[str, str], ...]] = (
    {"slug": TAB_CONTACTS, "label": "Contact Messages", "icon": "bi-envelope", "permission": "manage_contacts"},
    {"slug": TAB_QUOTES, "label": "Quote Requests", "icon": "bi-file-earmark-text", "permission": "manage_quotes"},
    {"slug": TAB_APPLICATIONS, "label": "Job Applications", "icon": "bi-person-badge", "permission": "manage_job_applications"},
)

DEFAULT_TAB: Final[str] = TAB_CONTACTS
DEFAULT_PER_PAGE: Final[int] = 20
MAX_PER_PAGE: Final[int] = 100

STATUS_FILTER_OPTIONS: Final[dict[str, str]] = {
    "": "All (inbox)",
    "unread": "Unread",
    "read": "Read",
    "starred": "Starred",
    "archived": "Archived",
}

SORT_OPTIONS: Final[dict[str, str]] = {
    "newest": "Newest first",
    "oldest": "Oldest first",
    "name_asc": "Name A–Z",
    "name_desc": "Name Z–A",
}

BULK_ACTIONS: Final[dict[str, str]] = {
    "mark_read": "Mark as read",
    "mark_unread": "Mark as unread",
    "star": "Star",
    "unstar": "Unstar",
    "archive": "Archive",
    "unarchive": "Unarchive",
    "delete": "Soft delete",
    "restore": "Restore",
}

EXPORT_COLUMNS: Final[dict[str, tuple[str, ...]]] = {
    TAB_CONTACTS: ("id", "name", "email", "phone", "subject", "message", "is_read", "created_at"),
    TAB_QUOTES: ("id", "name", "email", "phone", "project_type", "budget", "message", "is_read", "created_at"),
    TAB_APPLICATIONS: (
        "id",
        "full_name",
        "email",
        "phone",
        "position",
        "years_experience",
        "education",
        "cover_letter",
        "is_read",
        "created_at",
    ),
}
