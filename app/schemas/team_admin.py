"""Team admin module DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TeamSocialLinkDTO:
    platform: str
    url: str
    icon: str = ""


@dataclass
class TeamAdminDTO:
    id: int | None
    name: str
    slug: str
    position: str
    department: str
    member_type: str
    bio: str
    photo: str
    email: str
    phone: str
    years_experience: str
    education: str
    experience_summary: str
    sort_order: int
    is_featured: bool
    is_active: bool
    meta_title: str = ""
    meta_description: str = ""
    og_image: str = ""
    canonical_url: str = ""
    social_links: list[TeamSocialLinkDTO] = field(default_factory=list)
    gallery_paths: list[str] = field(default_factory=list)
    related_project_ids: list[int] = field(default_factory=list)
    related_service_slugs: list[str] = field(default_factory=list)
    related_equipment_ids: list[int] = field(default_factory=list)
    created_at_label: str = ""
    updated_at_label: str = ""


@dataclass
class TeamListItemDTO:
    id: int
    name: str
    slug: str
    position: str
    department: str
    member_type: str
    photo: str
    sort_order: int
    is_featured: bool
    is_active: bool
    updated_at_label: str


@dataclass
class TeamStatsDTO:
    total: int
    active: int
    inactive: int
    directors: int
    management: int
    staff: int
    recent: list[TeamListItemDTO]


@dataclass
class TeamListPageDTO:
    items: list[TeamListItemDTO]
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
    team_member_id: int | None = None
