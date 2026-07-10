"""Enterprise Media Manager DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MediaUsageDTO:
    location: str
    label: str
    resource_type: str
    resource_id: str | int


@dataclass
class MediaAssetDTO:
    id: int
    filename: str
    original_filename: str
    storage_path: str
    public_url: str
    folder: str
    folder_label: str
    media_type: str
    media_type_label: str
    mime_type: str
    file_size: int
    file_size_label: str
    title: str
    alt_text: str
    caption: str
    description: str
    tags: str
    category: str
    seo_title: str
    seo_description: str
    width: int | None
    height: int | None
    uploaded_by_name: str
    created_at_label: str
    is_active: bool
    usage: list[MediaUsageDTO] = field(default_factory=list)
    is_image: bool = False
    is_video: bool = False
    is_pdf: bool = False


@dataclass
class MediaStatsDTO:
    total_files: int
    total_storage_bytes: int
    total_storage_label: str
    by_type: dict[str, int]
    by_folder: dict[str, int]
    recent_uploads: list[MediaAssetDTO]


@dataclass
class MediaLibraryPageDTO:
    items: list[MediaAssetDTO]
    total: int
    page: int
    per_page: int
    total_pages: int
    query: str
    folder: str
    media_type: str
    sort: str
    view: str


@dataclass
class MediaUploadResultDTO:
    success: bool
    message: str
    asset: MediaAssetDTO | None = None
    errors: list[str] = field(default_factory=list)


@dataclass
class SaveResultDTO:
    success: bool
    message: str
