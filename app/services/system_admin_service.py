"""Enterprise System Administration business logic."""

from __future__ import annotations

from flask import url_for
from flask_login import current_user

from app.constants.system_admin import (
    DEFAULT_TAB,
    LOG_TABS,
    LOG_TAB_APPLICATION,
    SYSTEM_TABS,
    TAB_BACKUP,
    TAB_CACHE,
    TAB_HEALTH,
    TAB_LOGS,
    TAB_MAINTENANCE,
    TAB_OVERVIEW,
    TAB_STORAGE,
)
from app.providers.admin_dashboard_provider import AdminDashboardProvider
from app.providers.system_admin_provider import SystemAdminProvider
from app.schemas.admin import BreadcrumbItemDTO
from app.schemas.system_admin import ActionResultDTO
from app.utils.system_log import append_log


class SystemAdminService:
    """System administration service — super admin only."""

    @staticmethod
    def get_shell_context(*, page_title: str, active_tab: str = DEFAULT_TAB, log_tab: str = LOG_TAB_APPLICATION) -> dict:
        dashboard = AdminDashboardProvider.get_dashboard()
        return {
            "page_title": page_title,
            "active_nav": "system",
            "active_tab": active_tab,
            "log_tab": log_tab,
            "system_tabs": SYSTEM_TABS,
            "log_tabs": LOG_TABS,
            "breadcrumbs": [
                BreadcrumbItemDTO("Admin", url_for("admin.dashboard"), False),
                BreadcrumbItemDTO("System Administration", None, True),
            ],
            "notifications": dashboard.notifications,
            "unread_notification_count": dashboard.unread_notification_count,
            "user": current_user,
        }

    @staticmethod
    def get_dashboard_context(
        *,
        tab: str = DEFAULT_TAB,
        log_tab: str = LOG_TAB_APPLICATION,
        q: str = "",
        page: int = 1,
    ) -> dict:
        ctx = SystemAdminService.get_shell_context(
            page_title="System Administration",
            active_tab=tab,
            log_tab=log_tab,
        )
        ctx["overview"] = SystemAdminProvider.get_overview()
        ctx["python_env"] = SystemAdminProvider.get_python_env()
        ctx["maintenance"] = SystemAdminProvider.get_maintenance_status()
        ctx["backups"] = SystemAdminProvider.list_backup_files()
        ctx["health_checks"] = SystemAdminProvider.run_all_health_checks()
        ctx["storage_metrics"] = SystemAdminProvider.get_storage_metrics()
        ctx["cache_stats"] = SystemAdminProvider.get_cache_stats_dto()
        log_lines, log_total = SystemAdminProvider.get_log_lines(log_tab, q=q, page=page)
        ctx["log_lines"] = log_lines
        ctx["log_total"] = log_total
        ctx["log_query"] = q
        ctx["log_page"] = page
        return ctx

    @staticmethod
    def _audit(action: str, details: str, resource_id: str = "", ip_address: str | None = None) -> bool:
        SystemAdminProvider.record_audit(
            user_id=current_user.id,
            action=action,
            resource_type="system",
            resource_id=resource_id or None,
            details=details,
            ip_address=ip_address or "",
        )
        append_log("info", f"{action}: {details}")
        return SystemAdminProvider.commit()

    @staticmethod
    def enable_maintenance(*, message: str, ip_address: str | None = None) -> ActionResultDTO:
        SystemAdminProvider.set_maintenance(enabled=True, message=message)
        if not SystemAdminService._audit("system.maintenance.enable", f"Maintenance enabled: {message[:120]}", ip_address=ip_address):
            return ActionResultDTO(False, "Failed to save maintenance mode.")
        return ActionResultDTO(True, "Maintenance mode enabled.", TAB_MAINTENANCE)

    @staticmethod
    def disable_maintenance(*, ip_address: str | None = None) -> ActionResultDTO:
        status = SystemAdminProvider.get_maintenance_status()
        SystemAdminProvider.set_maintenance(enabled=False, message=status.message)
        if not SystemAdminService._audit("system.maintenance.disable", "Maintenance mode disabled", ip_address=ip_address):
            return ActionResultDTO(False, "Failed to disable maintenance mode.")
        return ActionResultDTO(True, "Maintenance mode disabled.", TAB_MAINTENANCE)

    @staticmethod
    def update_maintenance_message(*, message: str, ip_address: str | None = None) -> ActionResultDTO:
        status = SystemAdminProvider.get_maintenance_status()
        SystemAdminProvider.set_maintenance(enabled=status.enabled, message=message)
        if not SystemAdminService._audit("system.maintenance.message", "Maintenance message updated", ip_address=ip_address):
            return ActionResultDTO(False, "Failed to update maintenance message.")
        return ActionResultDTO(True, "Maintenance message saved.", TAB_MAINTENANCE)

    @staticmethod
    def create_backup(*, ip_address: str | None = None) -> ActionResultDTO:
        try:
            filename, backup_type = SystemAdminProvider.create_backup_file()
        except Exception as exc:
            append_log("error", f"Backup failed: {exc}")
            return ActionResultDTO(False, f"Backup failed: {exc}")
        if not SystemAdminService._audit(
            "system.backup.create",
            f"Created {backup_type} backup {filename}",
            resource_id=filename,
            ip_address=ip_address,
        ):
            return ActionResultDTO(False, "Backup created but audit failed.")
        return ActionResultDTO(True, f"Backup created: {filename}", TAB_BACKUP)

    @staticmethod
    def restore_backup(*, filename: str, ip_address: str | None = None) -> ActionResultDTO:
        try:
            SystemAdminProvider.restore_backup_file(filename)
        except Exception as exc:
            append_log("error", f"Restore failed: {exc}")
            return ActionResultDTO(False, f"Restore failed: {exc}")
        if not SystemAdminService._audit(
            "system.backup.restore",
            f"Restored backup {filename}",
            resource_id=filename,
            ip_address=ip_address,
        ):
            return ActionResultDTO(False, "Restore completed but audit failed.")
        return ActionResultDTO(True, f"Backup restored: {filename}", TAB_BACKUP)

    @staticmethod
    def run_health_checks(*, ip_address: str | None = None) -> ActionResultDTO:
        checks = SystemAdminProvider.run_all_health_checks()
        unhealthy = [c.label for c in checks if c.status != "healthy"]
        summary = "All checks passed" if not unhealthy else f"Issues: {', '.join(unhealthy)}"
        if not SystemAdminService._audit("system.health.check", summary, ip_address=ip_address):
            return ActionResultDTO(False, "Health check completed but audit failed.")
        msg = summary if not unhealthy else f"Health check finished with issues: {', '.join(unhealthy)}"
        return ActionResultDTO(True, msg, TAB_HEALTH)

    @staticmethod
    def clear_cache(*, ip_address: str | None = None) -> ActionResultDTO:
        removed = SystemAdminProvider.clear_system_cache()
        if not SystemAdminService._audit("system.cache.clear", f"Cleared {removed} cache entries", ip_address=ip_address):
            return ActionResultDTO(False, "Cache cleared but audit failed.")
        return ActionResultDTO(True, f"Cache cleared ({removed} entries).", TAB_CACHE)

    @staticmethod
    def rebuild_cache(*, ip_address: str | None = None) -> ActionResultDTO:
        created = SystemAdminProvider.rebuild_system_cache()
        if not SystemAdminService._audit("system.cache.rebuild", f"Rebuilt cache ({created} entries)", ip_address=ip_address):
            return ActionResultDTO(False, "Cache rebuilt but audit failed.")
        return ActionResultDTO(True, "Cache rebuilt successfully.", TAB_CACHE)
