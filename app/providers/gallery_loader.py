"""Gallery catalog loader — maps seed data to DTOs for provider layer."""

from __future__ import annotations

from app.data.gallery_catalog import (
    GALLERY_AWARDS_EVENTS,
    GALLERY_BEFORE_AFTER,
    GALLERY_DOWNLOADS,
    GALLERY_FEATURED_ALBUMS,
    GALLERY_MEDIA_ITEMS,
    GALLERY_PROGRESS_ITEMS,
    GALLERY_VIDEOS,
)
from app.schemas.content import (
    BeforeAfterItemDTO,
    GalleryAlbumDTO,
    GalleryDownloadDTO,
    GalleryFilterOptionsDTO,
    GalleryImageDTO,
    GalleryVideoDTO,
    ProgressGalleryItemDTO,
)


def _media_item(raw: dict) -> GalleryImageDTO:
    return GalleryImageDTO(
        id=raw["id"],
        title=raw["title"],
        image=raw["image"],
        category=raw["category"],
        sort_order=raw.get("sort_order", 0),
        is_active=raw.get("is_active", True),
        slug=raw.get("slug", ""),
        project_slug=raw.get("project_slug", ""),
        project_title=raw.get("project_title", ""),
        service_slug=raw.get("service_slug", ""),
        service_title=raw.get("service_title", ""),
        equipment_slug=raw.get("equipment_slug", ""),
        equipment_title=raw.get("equipment_title", ""),
        county=raw.get("county", ""),
        year=raw.get("year", ""),
        location=raw.get("location", ""),
        date=raw.get("date", ""),
        album=raw.get("album", ""),
        caption=raw.get("caption", ""),
    )


def build_gallery_images() -> list[GalleryImageDTO]:
    return [_media_item(item) for item in GALLERY_MEDIA_ITEMS if item.get("is_active", True)]


def build_gallery_albums() -> list[GalleryAlbumDTO]:
    return [
        GalleryAlbumDTO(
            id=item["id"],
            title=item["title"],
            slug=item["slug"],
            description=item["description"],
            image=item["image"],
            filter_album=item["filter_album"],
            icon=item.get("icon", "bi-images"),
            sort_order=item.get("sort_order", 0),
            is_active=item.get("is_active", True),
        )
        for item in GALLERY_FEATURED_ALBUMS
        if item.get("is_active", True)
    ]


def build_gallery_videos() -> list[GalleryVideoDTO]:
    return [
        GalleryVideoDTO(
            id=item["id"],
            title=item["title"],
            provider=item["provider"],
            description=item.get("description", ""),
            video_id=item.get("video_id", ""),
            embed_url=item.get("embed_url", ""),
            thumbnail=item.get("thumbnail", ""),
            is_ready=item.get("is_ready", False),
            sort_order=item.get("sort_order", 0),
            is_active=item.get("is_active", True),
        )
        for item in GALLERY_VIDEOS
        if item.get("is_active", True)
    ]


def build_gallery_downloads() -> list[GalleryDownloadDTO]:
    return [
        GalleryDownloadDTO(
            id=item["id"],
            title=item["title"],
            file_type=item["file_type"],
            description=item["description"],
            file_url=item.get("file_url", ""),
            is_ready=item.get("is_ready", False),
            icon=item.get("icon", "bi-file-earmark-pdf"),
            sort_order=item.get("sort_order", 0),
            is_active=item.get("is_active", True),
        )
        for item in GALLERY_DOWNLOADS
        if item.get("is_active", True)
    ]


def build_before_after_items() -> list[BeforeAfterItemDTO]:
    return [
        BeforeAfterItemDTO(
            id=item["id"],
            title=item["title"],
            before_image=item["before_image"],
            after_image=item["after_image"],
            project_title=item.get("project_title", ""),
            location=item.get("location", ""),
            sort_order=item.get("sort_order", 0),
            is_active=item.get("is_active", True),
        )
        for item in GALLERY_BEFORE_AFTER
        if item.get("is_active", True)
    ]


def build_progress_gallery_items() -> list[ProgressGalleryItemDTO]:
    return [
        ProgressGalleryItemDTO(
            id=item["id"],
            title=item["title"],
            subtitle=item["subtitle"],
            image=item["image"],
            date=item.get("date", ""),
            sort_order=item.get("sort_order", 0),
            is_active=item.get("is_active", True),
        )
        for item in GALLERY_PROGRESS_ITEMS
        if item.get("is_active", True)
    ]


def build_awards_gallery_items() -> list[GalleryImageDTO]:
    return [_media_item(item) for item in GALLERY_AWARDS_EVENTS if item.get("is_active", True)]


def build_gallery_filter_options(images: list[GalleryImageDTO] | None = None) -> GalleryFilterOptionsDTO:
    items = images or build_gallery_images()

    def _unique(values: list[str]) -> list[str]:
        seen: set[str] = set()
        ordered: list[str] = []
        for value in values:
            if value and value not in seen:
                seen.add(value)
                ordered.append(value)
        return sorted(ordered, key=str.lower)

    return GalleryFilterOptionsDTO(
        projects=_unique([i.project_title for i in items if i.project_title]),
        services=_unique([i.service_title for i in items if i.service_title]),
        equipment=_unique([i.equipment_title for i in items if i.equipment_title]),
        categories=_unique([i.category for i in items if i.category]),
        counties=_unique([i.county for i in items if i.county]),
        years=_unique([i.year for i in items if i.year]),
        albums=_unique([i.album for i in items if i.album]),
    )
