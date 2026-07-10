"""Equipment admin module DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class EquipmentSpecDTO:
    label: str
    value: str


@dataclass
class EquipmentAdminDTO:
    id: int | None
    name: str
    slug: str
    category: str
    short_description: str
    description: str
    image: str
    capacity: str
    condition: str
    maintenance_status: str
    usage: str
    sort_order: int
    is_featured: bool
    is_active: bool
    meta_title: str = ""
    meta_description: str = ""
    og_image: str = ""
    canonical_url: str = ""
    specifications: list[EquipmentSpecDTO] = field(default_factory=list)
    gallery_paths: list[str] = field(default_factory=list)
    related_project_ids: list[int] = field(default_factory=list)
    related_service_slugs: list[str] = field(default_factory=list)
    team_member_ids: list[int] = field(default_factory=list)
    created_at_label: str = ""
    updated_at_label: str = ""


@dataclass
class EquipmentListItemDTO:
    id: int
    name: str
    slug: str
    category: str
    short_description: str
    image: str
    condition: str
    sort_order: int
    is_featured: bool
    is_active: bool
    updated_at_label: str


@dataclass
class EquipmentStatsDTO:
    total: int
    active: int
    inactive: int
    featured: int
    recent: list[EquipmentListItemDTO]


@dataclass
class EquipmentListPageDTO:
    items: list[EquipmentListItemDTO]
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
    equipment_id: int | None = None
