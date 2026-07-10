"""Enterprise System Administration DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class HealthCheckDTO:
    slug: str
    label: str
    status: str
    message: str
    detail: str = ""


@dataclass
class StorageMetricDTO:
    label: str
    path: str
    total_bytes: int
    used_bytes: int
    free_bytes: int
    total_label: str
    used_label: str
    free_label: str
    percent_used: float


@dataclass
class PythonEnvDTO:
    python_version: str
    platform: str
    flask_version: str
    sqlalchemy_version: str
    config_name: str
    debug: bool
    database_enabled: bool
    database_uri_masked: str


@dataclass
class LogLineDTO:
    line_number: int
    content: str
    level: str = "info"


@dataclass
class BackupFileDTO:
    filename: str
    size_bytes: int
    size_label: str
    created_at_label: str
    backup_type: str


@dataclass
class MaintenanceStatusDTO:
    enabled: bool
    message: str
    allowed_ips: str


@dataclass
class CacheStatsDTO:
    entry_count: int
    total_bytes: int
    total_label: str
    last_rebuilt_label: str


@dataclass
class SystemOverviewDTO:
    database_status: str
    database_message: str
    storage_used_label: str
    storage_percent: float
    application_status: str
    application_message: str
    python_version: str
    recent_errors: list[LogLineDTO] = field(default_factory=list)
    health_checks: list[HealthCheckDTO] = field(default_factory=list)


@dataclass
class ActionResultDTO:
    success: bool
    message: str
    redirect_tab: str | None = None
