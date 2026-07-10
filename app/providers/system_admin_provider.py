"""Enterprise System Administration data provider."""

from __future__ import annotations

import os
import platform
import shutil
import sys
from datetime import datetime
from pathlib import Path

import flask
import sqlalchemy
from flask import current_app
from sqlalchemy import desc, func, or_, text
from sqlalchemy.exc import SQLAlchemyError

from app.constants.settings_keys import (
    KEY_MAINTENANCE_ALLOWED_IPS,
    KEY_MAINTENANCE_ENABLED,
    KEY_MAINTENANCE_MESSAGE,
    MAINTENANCE_KEYS,
    parse_bool,
)
from app.constants.system_admin import (
    HEALTH_CHECK_LABELS,
    HEALTH_CHECK_SLUGS,
    LOG_TAB_AUDIT,
    MAX_BACKUPS_LISTED,
)
from app.extensions import db
from app.models.auth import AuditLog, LoginHistory, User
from app.models.media import MediaAsset
from app.providers.auth_provider import AuthProvider
from app.providers.settings_provider import SettingsProvider
from app.schemas.system_admin import (
    BackupFileDTO,
    CacheStatsDTO,
    HealthCheckDTO,
    LogLineDTO,
    MaintenanceStatusDTO,
    PythonEnvDTO,
    StorageMetricDTO,
    SystemOverviewDTO,
)
from app.utils.system_backup import create_backup, list_backups, restore_backup
from app.utils.system_cache import clear_cache, get_cache_stats, rebuild_cache
from app.utils.system_log import append_log, tail_log


def _format_bytes(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{round(size / 1024, 1)} KB"
    if size < 1024 * 1024 * 1024:
        return f"{round(size / (1024 * 1024), 1)} MB"
    return f"{round(size / (1024 * 1024 * 1024), 2)} GB"


def _mask_db_uri(uri: str) -> str:
    if "@" in uri:
        prefix, suffix = uri.split("@", 1)
        if "://" in prefix:
            scheme, _ = prefix.split("://", 1)
            return f"{scheme}://***@{suffix}"
    return uri


class SystemAdminProvider:
    """Infrastructure queries and system operations."""

    @staticmethod
    def record_audit(**kwargs) -> None:
        AuthProvider.record_audit_event(**kwargs)

    @staticmethod
    def commit() -> bool:
        return AuthProvider.commit()

    @staticmethod
    def _static_root() -> Path:
        return Path(current_app.static_folder or "static")

    @staticmethod
    def _upload_root() -> Path:
        upload = current_app.config.get("MEDIA_UPLOAD_ROOT", "uploads")
        return SystemAdminProvider._static_root() / upload

    @staticmethod
    def _instance_root() -> Path:
        return Path(current_app.instance_path)

    @staticmethod
    def _dir_size(path: Path) -> int:
        if not path.exists():
            return 0
        if path.is_file():
            return path.stat().st_size
        total = 0
        for root, _dirs, files in os.walk(path):
            for name in files:
                try:
                    total += (Path(root) / name).stat().st_size
                except OSError:
                    pass
        return total

    @staticmethod
    def get_python_env() -> PythonEnvDTO:
        uri = current_app.config.get("SQLALCHEMY_DATABASE_URI", "")
        return PythonEnvDTO(
            python_version=sys.version.split()[0],
            platform=platform.platform(),
            flask_version=getattr(flask, "__version__", "unknown"),
            sqlalchemy_version=getattr(sqlalchemy, "__version__", "unknown"),
            config_name=current_app.config.get("ENV", "development"),
            debug=bool(current_app.config.get("DEBUG")),
            database_enabled=bool(current_app.config.get("DATABASE_ENABLED")),
            database_uri_masked=_mask_db_uri(uri),
        )

    @staticmethod
    def run_health_check(slug: str) -> HealthCheckDTO:
        label = HEALTH_CHECK_LABELS.get(slug, slug.title())
        try:
            if slug == "database":
                db.session.execute(text("SELECT 1"))
                db.session.commit()
                return HealthCheckDTO(slug, label, "healthy", "Database connection OK", "SELECT 1 succeeded")

            if slug == "filesystem":
                instance = SystemAdminProvider._instance_root()
                instance.mkdir(parents=True, exist_ok=True)
                test_file = instance / ".health_check"
                test_file.write_text("ok", encoding="utf-8")
                test_file.unlink()
                return HealthCheckDTO(slug, label, "healthy", "Instance directory is writable")

            if slug == "uploads":
                upload = SystemAdminProvider._upload_root()
                upload.mkdir(parents=True, exist_ok=True)
                test_file = upload / ".health_check"
                test_file.write_text("ok", encoding="utf-8")
                test_file.unlink()
                count = sum(1 for _ in upload.rglob("*") if _.is_file())
                return HealthCheckDTO(slug, label, "healthy", "Upload directory is writable", f"{count} files on disk")

            if slug == "media":
                total = MediaAsset.query.filter_by(is_active=True).count()
                return HealthCheckDTO(
                    slug,
                    label,
                    "healthy" if total >= 0 else "warning",
                    f"{total} active media assets indexed",
                )

            if slug == "application":
                env = SystemAdminProvider.get_python_env()
                detail = f"Flask {env.flask_version} · Python {env.python_version}"
                return HealthCheckDTO(slug, label, "healthy", "Application is running", detail)

        except Exception as exc:
            append_log("error", f"Health check failed ({slug}): {exc}")
            return HealthCheckDTO(slug, label, "unhealthy", str(exc))

        return HealthCheckDTO(slug, label, "unknown", "Check not implemented")

    @staticmethod
    def run_all_health_checks() -> list[HealthCheckDTO]:
        return [SystemAdminProvider.run_health_check(slug) for slug in HEALTH_CHECK_SLUGS]

    @staticmethod
    def get_overview() -> SystemOverviewDTO:
        checks = SystemAdminProvider.run_all_health_checks()
        db_check = next((c for c in checks if c.slug == "database"), None)
        app_check = next((c for c in checks if c.slug == "application"), None)

        disk = shutil.disk_usage(SystemAdminProvider._static_root())
        percent = round((disk.used / disk.total) * 100, 1) if disk.total else 0.0

        error_lines = tail_log("error", limit=5)
        recent_errors = [LogLineDTO(n, c, lvl) for n, c, lvl in error_lines]

        if not recent_errors:
            try:
                failed = (
                    LoginHistory.query.filter(LoginHistory.success.is_(False))
                    .order_by(desc(LoginHistory.created_at))
                    .limit(5)
                    .all()
                )
                for row in failed:
                    recent_errors.append(
                        LogLineDTO(
                            row.id,
                            f"{row.created_at.strftime('%Y-%m-%d %H:%M')} failed login: {row.email_attempted}",
                            "error",
                        )
                    )
            except SQLAlchemyError:
                pass

        return SystemOverviewDTO(
            database_status=db_check.status if db_check else "unknown",
            database_message=db_check.message if db_check else "",
            storage_used_label=_format_bytes(disk.used),
            storage_percent=percent,
            application_status=app_check.status if app_check else "unknown",
            application_message=app_check.message if app_check else "",
            python_version=sys.version.split()[0],
            recent_errors=recent_errors,
            health_checks=checks,
        )

    @staticmethod
    def get_storage_metrics() -> list[StorageMetricDTO]:
        metrics: list[StorageMetricDTO] = []

        for label, path in (
            ("Static / Disk", SystemAdminProvider._static_root()),
            ("Instance Data", SystemAdminProvider._instance_root()),
            ("Media Uploads", SystemAdminProvider._upload_root()),
        ):
            try:
                if path.exists():
                    disk = shutil.disk_usage(path if path.is_dir() else path.parent)
                    used = SystemAdminProvider._dir_size(path)
                else:
                    disk = shutil.disk_usage(SystemAdminProvider._instance_root())
                    used = 0
                pct = round((disk.used / disk.total) * 100, 1) if disk.total else 0.0
                metrics.append(
                    StorageMetricDTO(
                        label=label,
                        path=str(path),
                        total_bytes=disk.total,
                        used_bytes=used,
                        free_bytes=disk.free,
                        total_label=_format_bytes(disk.total),
                        used_label=_format_bytes(used),
                        free_label=_format_bytes(disk.free),
                        percent_used=pct,
                    )
                )
            except OSError as exc:
                metrics.append(
                    StorageMetricDTO(
                        label=label,
                        path=str(path),
                        total_bytes=0,
                        used_bytes=0,
                        free_bytes=0,
                        total_label="—",
                        used_label="—",
                        free_label="—",
                        percent_used=0.0,
                    )
                )
                append_log("error", f"Storage metric failed for {label}: {exc}")

        db_size = 0
        db_label = "—"
        try:
            uri = current_app.config.get("SQLALCHEMY_DATABASE_URI", "")
            if uri.startswith("sqlite:///"):
                raw = uri.replace("sqlite:///", "").split("?")[0]
                if raw != ":memory:":
                    db_path = Path(raw)
                    if db_path.is_file():
                        db_size = db_path.stat().st_size
                        db_label = _format_bytes(db_size)
            elif "mysql" in uri:
                row = db.session.execute(
                    text(
                        "SELECT SUM(data_length + index_length) AS size "
                        "FROM information_schema.tables WHERE table_schema = DATABASE()"
                    )
                ).scalar()
                db_size = int(row or 0)
                db_label = _format_bytes(db_size)
        except (SQLAlchemyError, OSError):
            db_label = "Unavailable"

        metrics.append(
            StorageMetricDTO(
                label="Database Size",
                path=_mask_db_uri(current_app.config.get("SQLALCHEMY_DATABASE_URI", "")),
                total_bytes=db_size,
                used_bytes=db_size,
                free_bytes=0,
                total_label=db_label,
                used_label=db_label,
                free_label="—",
                percent_used=0.0,
            )
        )

        try:
            media_bytes = (
                db.session.query(func.coalesce(func.sum(MediaAsset.file_size), 0))
                .filter(MediaAsset.is_active.is_(True))
                .scalar()
                or 0
            )
            metrics.append(
                StorageMetricDTO(
                    label="Media Library (DB index)",
                    path="media_assets.file_size",
                    total_bytes=int(media_bytes),
                    used_bytes=int(media_bytes),
                    free_bytes=0,
                    total_label=_format_bytes(int(media_bytes)),
                    used_label=_format_bytes(int(media_bytes)),
                    free_label="—",
                    percent_used=0.0,
                )
            )
        except SQLAlchemyError:
            pass

        return metrics

    @staticmethod
    def get_maintenance_status() -> MaintenanceStatusDTO:
        settings = SettingsProvider.get_settings(MAINTENANCE_KEYS)
        return MaintenanceStatusDTO(
            enabled=parse_bool(settings.get(KEY_MAINTENANCE_ENABLED)),
            message=settings.get(KEY_MAINTENANCE_MESSAGE, ""),
            allowed_ips=settings.get(KEY_MAINTENANCE_ALLOWED_IPS, ""),
        )

    @staticmethod
    def set_maintenance(*, enabled: bool, message: str) -> None:
        SettingsProvider.upsert_settings(
            {
                KEY_MAINTENANCE_ENABLED: "true" if enabled else "false",
                KEY_MAINTENANCE_MESSAGE: message.strip(),
            }
        )

    @staticmethod
    def list_backup_files() -> list[BackupFileDTO]:
        return [
            BackupFileDTO(
                filename=item["filename"],
                size_bytes=item["size_bytes"],
                size_label=item["size_label"],
                created_at_label=item["created_at_label"],
                backup_type=item["backup_type"],
            )
            for item in list_backups()[:MAX_BACKUPS_LISTED]
        ]

    @staticmethod
    def create_backup_file() -> tuple[str, str]:
        return create_backup()

    @staticmethod
    def restore_backup_file(filename: str) -> None:
        restore_backup(filename)

    @staticmethod
    def get_cache_stats_dto() -> CacheStatsDTO:
        stats = get_cache_stats()
        return CacheStatsDTO(
            entry_count=stats["entry_count"],
            total_bytes=stats["total_bytes"],
            total_label=_format_bytes(stats["total_bytes"]),
            last_rebuilt_label=stats["last_rebuilt_label"],
        )

    @staticmethod
    def clear_system_cache() -> int:
        return clear_cache()

    @staticmethod
    def rebuild_system_cache() -> int:
        return rebuild_cache()

    @staticmethod
    def get_log_lines(log_tab: str, *, q: str = "", page: int = 1, per_page: int = 50) -> tuple[list[LogLineDTO], int]:
        if log_tab == LOG_TAB_AUDIT:
            return SystemAdminProvider._query_audit_logs(q=q, page=page, per_page=per_page)

        raw = tail_log(log_tab)
        if q:
            q_lower = q.lower()
            raw = [item for item in raw if q_lower in item[1].lower()]
        total = len(raw)
        start = (page - 1) * per_page
        chunk = raw[start : start + per_page]
        return [LogLineDTO(n, c, lvl) for n, c, lvl in chunk], total

    @staticmethod
    def _query_audit_logs(*, q: str = "", page: int = 1, per_page: int = 50) -> tuple[list[LogLineDTO], int]:
        query = AuditLog.query.outerjoin(User, AuditLog.user_id == User.id)
        if q:
            like = f"%{q}%"
            query = query.filter(
                or_(
                    AuditLog.action.ilike(like),
                    AuditLog.resource_type.ilike(like),
                    AuditLog.details.ilike(like),
                    User.email.ilike(like),
                )
            )
        query = query.order_by(desc(AuditLog.created_at))
        total = query.count()
        rows = query.offset((page - 1) * per_page).limit(per_page).all()
        items = []
        for row in rows:
            email = row.user.email if row.user else "system"
            content = (
                f"{row.created_at.strftime('%Y-%m-%d %H:%M')} · {email} · "
                f"{row.action} · {row.resource_type} · {row.details or ''}"
            )
            items.append(LogLineDTO(row.id, content.strip(), "info"))
        return items, total
