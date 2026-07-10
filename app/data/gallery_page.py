"""
Gallery & Media Center page — CMS blocks and Page Builder sections.

Built from app.data.gallery_catalog.
"""

from __future__ import annotations

from typing import Any

from app.data.cms_blocks import SEED_TIMESTAMP
from app.data.gallery_catalog import (
    GALLERY_AWARDS_EVENTS,
    GALLERY_BEFORE_AFTER,
    GALLERY_DOWNLOADS,
    GALLERY_FEATURED_ALBUMS,
    GALLERY_MEDIA_ITEMS,
    GALLERY_PAGE_CONTENT,
    GALLERY_PROGRESS_ITEMS,
    GALLERY_VIDEOS,
)
from app.providers.gallery_loader import build_gallery_filter_options

_BLOCK_ID_START = 1700
_SECTION_ID_START = 1700


def _item(
    item_id: int,
    title: str,
    *,
    item_key: str = "",
    subtitle: str = "",
    short_summary: str = "",
    full_content: str = "",
    image: str = "",
    icon: str = "",
    sort_order: int = 0,
    extra: dict | None = None,
) -> dict[str, Any]:
    return {
        "id": item_id,
        "item_key": item_key or f"item-{item_id}",
        "title": title,
        "subtitle": subtitle,
        "short_summary": short_summary,
        "full_content": full_content,
        "image": image,
        "icon": icon,
        "sort_order": sort_order,
        "is_active": True,
        "extra": extra or {},
        "created_at": SEED_TIMESTAMP,
        "updated_at": SEED_TIMESTAMP,
    }


def _block(
    block_id: int,
    block_key: str,
    title: str,
    *,
    subtitle: str = "",
    short_summary: str = "",
    full_content: str = "",
    hero_image: str = "",
    gallery_images: list[str] | None = None,
    display_order: int = 0,
    meta_title: str = "",
    meta_description: str = "",
    items: list[dict[str, Any]] | None = None,
    extra: dict | None = None,
) -> dict[str, Any]:
    return {
        "id": block_id,
        "block_key": block_key,
        "title": title,
        "subtitle": subtitle,
        "short_summary": short_summary,
        "full_content": full_content,
        "hero_image": hero_image,
        "gallery_images": gallery_images or [],
        "display_order": display_order,
        "is_active": True,
        "meta_title": meta_title or title,
        "meta_description": meta_description or short_summary,
        "og_image": hero_image,
        "items": items or [],
        "extra": extra or {},
        "created_at": SEED_TIMESTAMP,
        "updated_at": SEED_TIMESTAMP,
    }


def _section(
    page_slug: str,
    section_id: int,
    section_key: str,
    section_title: str,
    *,
    block_key: str = "",
    display_order: int = 0,
    layout_type: str = "default",
    background_style: str = "default",
    spacing: str = "default",
    animation: str = "none",
    seo_anchor: str = "",
) -> dict[str, Any]:
    anchor = seo_anchor or section_key.replace("_", "-")
    return {
        "id": section_id,
        "page_slug": page_slug,
        "section_key": section_key,
        "section_title": section_title,
        "block_key": block_key,
        "display_order": display_order,
        "layout_type": layout_type,
        "background_style": background_style,
        "spacing": spacing,
        "animation": animation,
        "seo_anchor": anchor,
        "is_active": True,
        "is_visible": True,
        "created_at": SEED_TIMESTAMP,
        "updated_at": SEED_TIMESTAMP,
    }


def build_gallery_page_blocks() -> list[dict[str, Any]]:
    content = GALLERY_PAGE_CONTENT
    blocks: list[dict[str, Any]] = []
    bid = _BLOCK_ID_START

    intro = content["intro"]
    blocks.append(
        _block(
            bid,
            "gallery_intro",
            intro["title"],
            subtitle=intro["subtitle"],
            short_summary=intro["short_summary"],
            full_content=intro["full_content"],
            hero_image=intro["image"],
            display_order=bid,
        )
    )
    bid += 1

    filters_meta = content["filters"]
    filter_opts = build_gallery_filter_options()
    blocks.append(
        _block(
            bid,
            "gallery_filters",
            filters_meta["title"],
            subtitle=filters_meta["subtitle"],
            short_summary=filters_meta["short_summary"],
            display_order=bid,
            extra={
                "filter_dimensions": [
                    {"key": "project", "label": "Project"},
                    {"key": "service", "label": "Service"},
                    {"key": "equipment", "label": "Equipment"},
                    {"key": "category", "label": "Category"},
                    {"key": "county", "label": "County"},
                    {"key": "year", "label": "Year"},
                ],
                "filter_options": {
                    "projects": filter_opts.projects,
                    "services": filter_opts.services,
                    "equipment": filter_opts.equipment,
                    "categories": filter_opts.categories,
                    "counties": filter_opts.counties,
                    "years": filter_opts.years,
                },
            },
        )
    )
    bid += 1

    grid_meta = content["grid"]
    grid_items = [
        _item(
            m["id"],
            m["title"],
            subtitle=m.get("category", ""),
            short_summary=m.get("caption", ""),
            image=m["image"],
            sort_order=m.get("sort_order", 0),
            extra={
                "slug": m.get("slug", ""),
                "project_title": m.get("project_title", ""),
                "service_title": m.get("service_title", ""),
                "equipment_title": m.get("equipment_title", ""),
                "category": m.get("category", ""),
                "county": m.get("county", ""),
                "year": m.get("year", ""),
                "location": m.get("location", ""),
                "date": m.get("date", ""),
                "album": m.get("album", ""),
            },
        )
        for m in GALLERY_MEDIA_ITEMS
    ]
    blocks.append(
        _block(
            bid,
            "gallery_media_grid",
            grid_meta["title"],
            subtitle=grid_meta["subtitle"],
            short_summary=grid_meta["short_summary"],
            gallery_images=[m["image"] for m in GALLERY_MEDIA_ITEMS],
            display_order=bid,
            items=grid_items,
        )
    )
    bid += 1

    albums_meta = content["albums"]
    album_items = [
        _item(
            a["id"],
            a["title"],
            short_summary=a["description"],
            image=a["image"],
            icon=a.get("icon", "bi-images"),
            sort_order=a.get("sort_order", 0),
            extra={"filter_album": a["filter_album"], "slug": a["slug"]},
        )
        for a in GALLERY_FEATURED_ALBUMS
    ]
    blocks.append(
        _block(
            bid,
            "gallery_featured_albums",
            albums_meta["title"],
            subtitle=albums_meta["subtitle"],
            short_summary=albums_meta["short_summary"],
            display_order=bid,
            items=album_items,
        )
    )
    bid += 1

    videos_meta = content["videos"]
    video_items = [
        _item(
            v["id"],
            v["title"],
            short_summary=v.get("description", ""),
            image=v.get("thumbnail", ""),
            sort_order=v.get("sort_order", 0),
            extra={
                "provider": v["provider"],
                "video_id": v.get("video_id", ""),
                "embed_url": v.get("embed_url", ""),
                "is_ready": v.get("is_ready", False),
            },
        )
        for v in GALLERY_VIDEOS
    ]
    blocks.append(
        _block(
            bid,
            "gallery_videos",
            videos_meta["title"],
            subtitle=videos_meta["subtitle"],
            short_summary=videos_meta["short_summary"],
            display_order=bid,
            items=video_items,
        )
    )
    bid += 1

    ba_meta = content["before_after"]
    ba_items = [
        _item(
            b["id"],
            b["title"],
            subtitle=b.get("project_title", ""),
            short_summary=b.get("location", ""),
            image=b["after_image"],
            sort_order=b.get("sort_order", 0),
            extra={
                "before_image": b["before_image"],
                "after_image": b["after_image"],
                "project_title": b.get("project_title", ""),
                "location": b.get("location", ""),
            },
        )
        for b in GALLERY_BEFORE_AFTER
    ]
    blocks.append(
        _block(
            bid,
            "gallery_before_after",
            ba_meta["title"],
            subtitle=ba_meta["subtitle"],
            short_summary=ba_meta["short_summary"],
            display_order=bid,
            items=ba_items,
        )
    )
    bid += 1

    progress_meta = content["progress"]
    progress_items = [
        _item(
            p["id"],
            p["title"],
            subtitle=p.get("subtitle", ""),
            image=p["image"],
            sort_order=p.get("sort_order", 0),
            extra={"date": p.get("date", "")},
        )
        for p in GALLERY_PROGRESS_ITEMS
    ]
    blocks.append(
        _block(
            bid,
            "gallery_progress",
            progress_meta["title"],
            subtitle=progress_meta["subtitle"],
            short_summary=progress_meta["short_summary"],
            display_order=bid,
            items=progress_items,
        )
    )
    bid += 1

    awards_meta = content["awards"]
    awards_items = [
        _item(
            a["id"],
            a["title"],
            subtitle=a.get("category", ""),
            short_summary=a.get("caption", ""),
            image=a["image"],
            sort_order=a.get("sort_order", 0),
            extra={
                "location": a.get("location", ""),
                "date": a.get("date", ""),
                "year": a.get("year", ""),
            },
        )
        for a in GALLERY_AWARDS_EVENTS
    ]
    blocks.append(
        _block(
            bid,
            "gallery_awards",
            awards_meta["title"],
            subtitle=awards_meta["subtitle"],
            short_summary=awards_meta["short_summary"],
            display_order=bid,
            items=awards_items,
        )
    )
    bid += 1

    downloads_meta = content["downloads"]
    download_items = [
        _item(
            d["id"],
            d["title"],
            subtitle=d.get("file_type", ""),
            short_summary=d.get("description", ""),
            icon=d.get("icon", "bi-file-earmark-pdf"),
            sort_order=d.get("sort_order", 0),
            extra={
                "file_url": d.get("file_url", ""),
                "is_ready": d.get("is_ready", False),
                "file_type": d.get("file_type", ""),
            },
        )
        for d in GALLERY_DOWNLOADS
    ]
    blocks.append(
        _block(
            bid,
            "gallery_downloads",
            downloads_meta["title"],
            subtitle=downloads_meta["subtitle"],
            short_summary=downloads_meta["short_summary"],
            display_order=bid,
            items=download_items,
        )
    )

    return blocks


def build_gallery_page_sections() -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    sid = _SECTION_ID_START
    order = 1
    slug = "gallery"

    sections.append(
        _section(
            slug,
            sid,
            "hero_banner",
            "Hero Banner",
            display_order=order,
            layout_type="hero-banner",
            background_style="brand",
            spacing="none",
            animation="fade-in",
        )
    )
    sid += 1
    order += 1

    sections.append(
        _section(
            slug,
            sid,
            "gallery_intro",
            "Gallery Introduction",
            block_key="gallery_intro",
            display_order=order,
            layout_type="split-columns",
            background_style="light",
            animation="fade-up",
            seo_anchor="gallery-intro",
        )
    )
    sid += 1
    order += 1

    sections.append(
        _section(
            slug,
            sid,
            "gallery_filters",
            "Advanced Gallery Filters",
            block_key="gallery_filters",
            display_order=order,
            layout_type="gallery-filters",
            background_style="default",
            spacing="compact",
            animation="fade-up",
            seo_anchor="gallery-filters",
        )
    )
    sid += 1
    order += 1

    sections.append(
        _section(
            slug,
            sid,
            "gallery_grid",
            "Gallery Grid",
            block_key="gallery_media_grid",
            display_order=order,
            layout_type="gallery-media-grid",
            background_style="default",
            animation="stagger",
            seo_anchor="gallery-grid",
        )
    )
    sid += 1
    order += 1

    sections.append(
        _section(
            slug,
            sid,
            "featured_albums",
            "Featured Albums",
            block_key="gallery_featured_albums",
            display_order=order,
            layout_type="featured-albums",
            background_style="muted",
            animation="fade-up",
            seo_anchor="featured-albums",
        )
    )
    sid += 1
    order += 1

    sections.append(
        _section(
            slug,
            sid,
            "video_gallery",
            "Video Gallery",
            block_key="gallery_videos",
            display_order=order,
            layout_type="video-gallery",
            background_style="light",
            animation="fade-up",
            seo_anchor="video-gallery",
        )
    )
    sid += 1
    order += 1

    sections.append(
        _section(
            slug,
            sid,
            "before_after",
            "Before & After Gallery",
            block_key="gallery_before_after",
            display_order=order,
            layout_type="before-after",
            background_style="default",
            animation="fade-up",
            seo_anchor="before-after",
        )
    )
    sid += 1
    order += 1

    sections.append(
        _section(
            slug,
            sid,
            "project_progress",
            "Project Progress Gallery",
            block_key="gallery_progress",
            display_order=order,
            layout_type="progress-gallery",
            background_style="muted",
            animation="fade-up",
            seo_anchor="project-progress",
        )
    )
    sid += 1
    order += 1

    sections.append(
        _section(
            slug,
            sid,
            "awards_events",
            "Awards & Events Gallery",
            block_key="gallery_awards",
            display_order=order,
            layout_type="awards-gallery",
            background_style="light",
            animation="fade-up",
            seo_anchor="awards-events",
        )
    )
    sid += 1
    order += 1

    sections.append(
        _section(
            slug,
            sid,
            "download_center",
            "Download Center",
            block_key="gallery_downloads",
            display_order=order,
            layout_type="download-center",
            background_style="default",
            animation="fade-up",
            seo_anchor="download-center",
        )
    )
    sid += 1
    order += 1

    sections.append(
        _section(
            slug,
            sid,
            "call_to_action",
            "Call To Action",
            block_key="call_to_action",
            display_order=order,
            layout_type="cta-banner",
            background_style="brand",
            spacing="relaxed",
            animation="fade-up",
            seo_anchor="gallery-cta",
        )
    )

    return sections


GALLERY_PAGE_BLOCKS: list[dict[str, Any]] = build_gallery_page_blocks()
GALLERY_PAGE_SECTIONS: list[dict[str, Any]] = build_gallery_page_sections()
