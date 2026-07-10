"""Enterprise System Administration constants — Step 27."""

from __future__ import annotations

from typing import Final

TAB_OVERVIEW: Final[str] = "overview"
TAB_MAINTENANCE: Final[str] = "maintenance"
TAB_BACKUP: Final[str] = "backup"
TAB_HEALTH: Final[str] = "health"
TAB_LOGS: Final[str] = "logs"
TAB_STORAGE: Final[str] = "storage"
TAB_CACHE: Final[str] = "cache"

DEFAULT_TAB: Final[str] = TAB_OVERVIEW

SYSTEM_TABS: Final[tuple[dict[str, str], ...]] = (
    {"slug": TAB_OVERVIEW, "label": "Dashboard", "icon": "bi-speedometer2"},
    {"slug": TAB_MAINTENANCE, "label": "Maintenance", "icon": "bi-cone-striped"},
    {"slug": TAB_BACKUP, "label": "Backup", "icon": "bi-cloud-arrow-up"},
    {"slug": TAB_HEALTH, "label": "Health Check", "icon": "bi-heart-pulse"},
    {"slug": TAB_LOGS, "label": "Logs", "icon": "bi-journal-text"},
    {"slug": TAB_STORAGE, "label": "Storage", "icon": "bi-hdd"},
    {"slug": TAB_CACHE, "label": "Cache", "icon": "bi-lightning-charge"},
)

LOG_TAB_APPLICATION: Final[str] = "application"
LOG_TAB_ERROR: Final[str] = "error"
LOG_TAB_AUDIT: Final[str] = "audit"

LOG_TABS: Final[tuple[dict[str, str], ...]] = (
    {"slug": LOG_TAB_APPLICATION, "label": "Application Logs", "icon": "bi-file-text"},
    {"slug": LOG_TAB_ERROR, "label": "Error Logs", "icon": "bi-exclamation-triangle"},
    {"slug": LOG_TAB_AUDIT, "label": "Audit Logs", "icon": "bi-shield-check"},
)

HEALTH_CHECK_SLUGS: Final[tuple[str, ...]] = (
    "database",
    "filesystem",
    "uploads",
    "media",
    "application",
)

HEALTH_CHECK_LABELS: Final[dict[str, str]] = {
    "database": "Database",
    "filesystem": "Filesystem",
    "uploads": "Uploads",
    "media": "Media Library",
    "application": "Application",
}

BACKUP_DIR_NAME: Final[str] = "backups"
CACHE_DIR_NAME: Final[str] = "cache"
LOG_DIR_NAME: Final[str] = "logs"

LOG_FILES: Final[dict[str, str]] = {
    LOG_TAB_APPLICATION: "application.log",
    LOG_TAB_ERROR: "error.log",
}

MAX_LOG_LINES: Final[int] = 200
MAX_BACKUPS_LISTED: Final[int] = 50
