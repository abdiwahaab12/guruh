"""Services admin module DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ServiceAdminDTO:
    id: int | None
    title: str
    slug: str
    short_description: str
    description: str
    icon: str
    image: str
    sort_order: int
    is_featured: bool
    is_active: bool
    meta_title: str = ""
    meta_description: str = ""
    og_image: str = ""
    canonical_url: str = ""
    scope_of_work: list[str] = field(default_factory=list)
    benefits: list[str] = field(default_factory=list)
    equipment: list[str] = field(default_factory=list)
    gallery_paths: list[str] = field(default_factory=list)
    related_project_ids: list[int] = field(default_factory=list)
    related_service_slugs: list[str] = field(default_factory=list)
    team_member_ids: list[int] = field(default_factory=list)
    created_at_label: str = ""
    updated_at_label: str = ""


@dataclass
class ServiceListItemDTO:
    id: int
    title: str
    slug: str
    short_description: str
    icon: str
    image: str
    sort_order: int
    is_featured: bool
    is_active: bool
    updated_at_label: str


@dataclass
class ServiceStatsDTO:
    total: int
    active: int
    inactive: int
    featured: int
    recent: list[ServiceListItemDTO]


@dataclass
class ServiceListPageDTO:
    items: list[ServiceListItemDTO]
    total: int
    page: int
    per_page: int
    total_pages: int
    query: str
    filters: dict[str, str]
    sort: str
    include_deleted: bool


@dataclass
class SaveResultDTO:
    success: bool
    message: str
    service_id: int | None = None
