"""Admin dashboard DTOs — service layer data transfer."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DashboardStatDTO:
    """Summary stat widget on the dashboard home."""

    key: str
    label: str
    value: int | str
    icon: str
    color: str = "primary"
    trend: str = ""
    trend_direction: str = "neutral"  # up | down | neutral
    module_slug: str = ""
    i18n_key: str = ""


@dataclass
class ChartDatasetDTO:
    label: str
    data: list[float | int]
    backgroundColor: str | list[str] = ""
    borderColor: str = ""


@dataclass
class ChartConfigDTO:
    """Chart.js placeholder configuration."""

    chart_id: str
    chart_type: str
    title: str
    labels: list[str]
    datasets: list[ChartDatasetDTO]
    i18n_key: str = ""


@dataclass
class ActivityItemDTO:
    """Recent activity timeline entry."""

    id: int
    title: str
    description: str
    icon: str
    color: str
    timestamp_label: str
    actor: str = ""
    resource_type: str = ""


@dataclass
class NotificationDTO:
    """Header notification item."""

    id: int
    title: str
    message: str
    icon: str
    color: str
    time_label: str
    is_read: bool = False
    href: str = ""


@dataclass
class BreadcrumbItemDTO:
    label: str
    url: str | None = None
    is_current: bool = False


@dataclass
class AdminDashboardDTO:
    """Aggregated dashboard homepage context."""

    stats: list[DashboardStatDTO] = field(default_factory=list)
    charts: list[ChartConfigDTO] = field(default_factory=list)
    activities: list[ActivityItemDTO] = field(default_factory=list)
    notifications: list[NotificationDTO] = field(default_factory=list)
    unread_notification_count: int = 0
