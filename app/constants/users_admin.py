"""Users & RBAC admin constants — Step 25."""

from __future__ import annotations

from typing import Final

TAB_USERS: Final[str] = "users"
TAB_ROLES: Final[str] = "roles"
TAB_PERMISSIONS: Final[str] = "permissions"
TAB_SESSIONS: Final[str] = "sessions"
TAB_LOGIN_HISTORY: Final[str] = "login-history"
TAB_AUDIT_LOGS: Final[str] = "audit-logs"

USERS_TABS: Final[tuple[dict[str, str], ...]] = (
    {"slug": TAB_USERS, "label": "Users", "icon": "bi-people"},
    {"slug": TAB_ROLES, "label": "Roles", "icon": "bi-shield-check"},
    {"slug": TAB_PERMISSIONS, "label": "Permissions", "icon": "bi-key"},
    {"slug": TAB_SESSIONS, "label": "User Sessions", "icon": "bi-pc-display"},
    {"slug": TAB_LOGIN_HISTORY, "label": "Login History", "icon": "bi-clock-history"},
    {"slug": TAB_AUDIT_LOGS, "label": "Audit Logs", "icon": "bi-journal-text"},
)

DEFAULT_TAB: Final[str] = TAB_USERS
DEFAULT_PER_PAGE: Final[int] = 20
MAX_PER_PAGE: Final[int] = 100

USER_STATUS_OPTIONS: Final[dict[str, str]] = {
    "": "All statuses",
    "active": "Active",
    "inactive": "Inactive",
    "locked": "Locked",
}

USER_SORT_OPTIONS: Final[dict[str, str]] = {
    "newest": "Newest first",
    "oldest": "Oldest first",
    "name_asc": "Name A–Z",
    "name_desc": "Name Z–A",
    "email_asc": "Email A–Z",
}

USER_BULK_ACTIONS: Final[dict[str, str]] = {
    "activate": "Activate",
    "deactivate": "Deactivate",
    "unlock": "Unlock accounts",
    "revoke_sessions": "Revoke sessions",
}

SESSION_STATUS_OPTIONS: Final[dict[str, str]] = {
    "": "All sessions",
    "active": "Active",
    "inactive": "Revoked / expired",
}

LOGIN_STATUS_OPTIONS: Final[dict[str, str]] = {
    "": "All attempts",
    "success": "Successful",
    "failed": "Failed",
}

PROTECTED_ROLE_SLUGS: Final[frozenset[str]] = frozenset({"super_admin"})
