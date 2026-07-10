"""Projects admin module DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ProjectTimelineItemDTO:
    date: str
    title: str
    description: str


@dataclass
class ProjectAdminDTO:
    id: int | None
    title: str
    slug: str
    description: str
    location: str
    country: str
    county: str
    status: str
    client: str
    category: str
    cover_image: str
    completion_date: str
    sort_order: int
    is_featured: bool
    is_active: bool
    meta_title: str = ""
    meta_description: str = ""
    og_image: str = ""
    canonical_url: str = ""
    overview: str = ""
    consultant: str = ""
    duration: str = ""
    completion_year: str = ""
    challenges: list[str] = field(default_factory=list)
    solutions: list[str] = field(default_factory=list)
    scope_of_work: list[str] = field(default_factory=list)
    timeline: list[ProjectTimelineItemDTO] = field(default_factory=list)
    service_slugs: list[str] = field(default_factory=list)
    equipment: list[str] = field(default_factory=list)
    team_member_ids: list[int] = field(default_factory=list)
    related_project_ids: list[int] = field(default_factory=list)
    related_service_slugs: list[str] = field(default_factory=list)
    document_paths: list[str] = field(default_factory=list)
    gallery_paths: list[str] = field(default_factory=list)
    created_at_label: str = ""
    updated_at_label: str = ""


@dataclass
class ProjectListItemDTO:
    id: int
    title: str
    slug: str
    country: str
    county: str
    status: str
    category: str
    client: str
    completion_year: str
    is_featured: bool
    is_active: bool
    cover_image: str
    sort_order: int


@dataclass
class ProjectStatsDTO:
    total: int
    active: int
    featured: int
    by_country: dict[str, int]
    by_status: dict[str, int]
    recent: list[ProjectListItemDTO]


@dataclass
class ProjectListPageDTO:
    items: list[ProjectListItemDTO]
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
    project_id: int | None = None
