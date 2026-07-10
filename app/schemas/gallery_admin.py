"""Gallery admin module DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class GalleryAdminDTO:
    id: int | None
    title: str
    slug: str
    image: str
    category: str
    project_id: int | None
    sort_order: int
    is_active: bool
    media_type: str = "image"
    album: str = ""
    caption: str = ""
    location: str = ""
    county: str = ""
    country: str = "Somalia"
    media_date: str = ""
    year: str = ""
    is_featured: bool = False
    meta_title: str = ""
    meta_description: str = ""
    og_image: str = ""
    canonical_url: str = ""
    service_slug: str = ""
    equipment_slug: str = ""
    team_member_ids: list[int] = field(default_factory=list)
    video_provider: str = ""
    video_id: str = ""
    embed_url: str = ""
    created_at_label: str = ""
    updated_at_label: str = ""


@dataclass
class GalleryListItemDTO:
    id: int
    title: str
    slug: str
    image: str
    category: str
    album: str
    media_type: str
    country: str
    project_id: int | None
    sort_order: int
    is_featured: bool
    is_active: bool
    updated_at_label: str


@dataclass
class GalleryStatsDTO:
    total: int
    albums: int
    images: int
    videos: int
    featured: int
    active: int
    inactive: int
    recent: list[GalleryListItemDTO]


@dataclass
class GalleryListPageDTO:
    items: list[GalleryListItemDTO]
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
    gallery_item_id: int | None = None
