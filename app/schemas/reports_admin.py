"""Reports & Analytics admin DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DateRangeDTO:
    preset: str
    label: str
    start: str
    end: str


@dataclass
class StatCardDTO:
    key: str
    label: str
    value: int | str
    sublabel: str = ""
    icon: str = "bi-circle"
    color: str = "primary"


@dataclass
class ChartSeriesDTO:
    chart_id: str
    title: str
    chart_type: str
    labels: list[str] = field(default_factory=list)
    datasets: list[dict] = field(default_factory=list)


@dataclass
class ReportsOverviewDTO:
    cards: list[StatCardDTO] = field(default_factory=list)
    charts: list[ChartSeriesDTO] = field(default_factory=list)
    website: dict = field(default_factory=dict)
    projects: dict = field(default_factory=dict)
    services: dict = field(default_factory=dict)
    equipment: dict = field(default_factory=dict)
    gallery: dict = field(default_factory=dict)
    careers: dict = field(default_factory=dict)
    messages: dict = field(default_factory=dict)
    users: dict = field(default_factory=dict)


@dataclass
class AuditReportRowDTO:
    label: str
    count: int
    detail: str = ""


@dataclass
class AuditReportDTO:
    tab: str
    title: str
    rows: list[AuditReportRowDTO] = field(default_factory=list)
    total: int = 0


@dataclass
class ExportResultDTO:
    success: bool
    message: str
    data: bytes | None = None
    mime_type: str = ""
    filename: str = ""
