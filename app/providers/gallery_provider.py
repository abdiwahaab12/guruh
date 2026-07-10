"""
Public gallery data — loads admin-managed gallery items for the website.
"""

from __future__ import annotations

from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models.catalog import GalleryImage, Project, Service
from app.models.equipment import Equipment
from app.models.gallery_detail import GalleryDetail
from app.constants.gallery_admin import (
    AWARDS_CATEGORIES,
    BEFORE_AFTER_CATEGORY,
    GALLERY_SECTION_CATEGORIES,
    PROGRESS_CATEGORY,
)
from app.providers.gallery_loader import build_gallery_filter_options
from app.schemas.content import (
    BeforeAfterItemDTO,
    GalleryAlbumDTO,
    GalleryFilterOptionsDTO,
    GalleryImageDTO,
    GalleryVideoDTO,
    ProgressGalleryItemDTO,
)

_VIDEO_EXTENSIONS = frozenset({"mp4", "webm", "mov", "avi", "mkv"})


def _path_extension(path: str) -> str:
    if not path or "." not in path:
        return ""
    return path.rsplit(".", 1)[-1].lower()


def _is_video_path(path: str) -> bool:
    return _path_extension(path) in _VIDEO_EXTENSIONS


def _active_detail_filters():
    return GalleryDetail.deleted_at.is_(None)


def _video_play_url(row: GalleryImage, detail: GalleryDetail) -> str:
    embed = (detail.embed_url or "").strip()
    if embed:
        if embed.startswith(("http://", "https://", "//")):
            return embed
        return embed.lstrip("/")

    provider = (detail.video_provider or "").strip().lower()
    video_id = (detail.video_id or "").strip()
    if provider == "youtube" and video_id:
        return f"https://www.youtube.com/embed/{video_id}"
    if provider == "vimeo" and video_id:
        return f"https://player.vimeo.com/video/{video_id}"

    image_path = (row.image or "").strip()
    if _is_video_path(image_path):
        return image_path
    return ""


def _video_is_ready(row: GalleryImage, detail: GalleryDetail) -> bool:
    if (detail.embed_url or "").strip() or (detail.video_id or "").strip():
        return True
    return _is_video_path(row.image or "")


def _video_thumbnail(row: GalleryImage, detail: GalleryDetail) -> str:
    image_path = (row.image or "").strip()
    og_image = (detail.og_image or "").strip()
    if _is_video_path(image_path):
        return og_image or ""
    return image_path or og_image


def _relation_maps(rows: list[GalleryImage]) -> tuple[dict[int, Project], dict[str, Service], dict[str, Equipment]]:
    project_ids = {r.project_id for r in rows if r.project_id}
    service_slugs = set()
    equipment_slugs = set()
    for row in rows:
        detail = row.detail
        if detail and detail.service_slug:
            service_slugs.add(detail.service_slug)
        if detail and detail.equipment_slug:
            equipment_slugs.add(detail.equipment_slug)

    projects = (
        Project.query.filter(Project.id.in_(project_ids), Project.is_active.is_(True)).all()
        if project_ids
        else []
    )
    services = (
        Service.query.filter(Service.slug.in_(service_slugs), Service.is_active.is_(True)).all()
        if service_slugs
        else []
    )
    equipment = (
        Equipment.query.filter(Equipment.slug.in_(equipment_slugs), Equipment.is_active.is_(True)).all()
        if equipment_slugs
        else []
    )
    return (
        {p.id: p for p in projects},
        {s.slug: s for s in services},
        {e.slug: e for e in equipment},
    )


def gallery_row_to_dto(
    row: GalleryImage,
    *,
    projects_by_id: dict[int, Project],
    services_by_slug: dict[str, Service],
    equipment_by_slug: dict[str, Equipment],
) -> GalleryImageDTO:
    detail = row.detail
    project_title = ""
    project_slug = ""
    if row.project_id and row.project_id in projects_by_id:
        proj = projects_by_id[row.project_id]
        project_title = proj.title
        project_slug = proj.slug

    service_title = ""
    service_slug = detail.service_slug if detail else ""
    if service_slug and service_slug in services_by_slug:
        service_title = services_by_slug[service_slug].title

    equipment_title = ""
    equipment_slug = detail.equipment_slug if detail else ""
    if equipment_slug and equipment_slug in equipment_by_slug:
        equipment_title = equipment_by_slug[equipment_slug].title

    return GalleryImageDTO(
        id=row.id,
        title=row.title,
        image=row.image or "",
        category=row.category or "",
        sort_order=row.sort_order or 0,
        is_active=row.is_active,
        slug=detail.slug if detail else "",
        project_slug=project_slug,
        project_title=project_title,
        service_slug=service_slug,
        service_title=service_title,
        equipment_slug=equipment_slug,
        equipment_title=equipment_title,
        county=detail.county if detail else "",
        year=detail.year if detail else "",
        location=detail.location if detail else "",
        date=detail.media_date if detail else "",
        album=detail.album if detail else "",
        caption=detail.caption if detail else "",
    )


def _is_section_category(category: str) -> bool:
    return category in GALLERY_SECTION_CATEGORIES


def load_gallery_images(*, images_only: bool = True) -> list[GalleryImageDTO]:
    rows = (
        GalleryImage.query.options(joinedload(GalleryImage.detail))
        .filter(GalleryImage.is_active.is_(True))
        .order_by(GalleryImage.sort_order, GalleryImage.created_at.desc())
        .all()
    )
    if images_only:
        rows = [
            row
            for row in rows
            if not _is_section_category(row.category or "")
            and (not row.detail or row.detail.deleted_at is None)
            and (not row.detail or row.detail.media_type in ("image", ""))
            and not _is_video_path(row.image or "")
        ]
    else:
        rows = [row for row in rows if not row.detail or row.detail.deleted_at is None]
    if not rows:
        return []

    projects_by_id, services_by_slug, equipment_by_slug = _relation_maps(rows)
    return [
        gallery_row_to_dto(
            row,
            projects_by_id=projects_by_id,
            services_by_slug=services_by_slug,
            equipment_by_slug=equipment_by_slug,
        )
        for row in rows
    ]


def load_gallery_videos() -> list[GalleryVideoDTO]:
    rows = (
        GalleryImage.query.options(joinedload(GalleryImage.detail))
        .join(GalleryDetail)
        .filter(
            GalleryImage.is_active.is_(True),
            GalleryImage.category != BEFORE_AFTER_CATEGORY,
            ~GalleryImage.category.in_(list(AWARDS_CATEGORIES)),
            GalleryImage.category != PROGRESS_CATEGORY,
            _active_detail_filters(),
            db.or_(
                GalleryDetail.media_type == "video",
                GalleryImage.image.like("%.mp4"),
                GalleryImage.image.like("%.webm"),
                GalleryImage.image.like("%.mov"),
                GalleryImage.image.like("%.avi"),
                GalleryImage.image.like("%.mkv"),
            ),
        )
        .order_by(GalleryImage.sort_order, GalleryImage.created_at.desc())
        .all()
    )
    videos: list[GalleryVideoDTO] = []
    for idx, row in enumerate(rows, start=1):
        detail = row.detail
        if not detail:
            continue
        play_url = _video_play_url(row, detail)
        videos.append(
            GalleryVideoDTO(
                id=row.id,
                title=row.title,
                provider=detail.video_provider or "upload",
                description=detail.caption or "",
                video_id=detail.video_id or "",
                embed_url=detail.embed_url or "",
                thumbnail=_video_thumbnail(row, detail),
                play_url=play_url,
                is_ready=bool(play_url),
                sort_order=row.sort_order or idx,
                is_active=True,
            )
        )
    return videos


def load_before_after_items() -> list[BeforeAfterItemDTO]:
    rows = (
        GalleryImage.query.options(joinedload(GalleryImage.detail))
        .join(GalleryDetail)
        .filter(
            GalleryImage.is_active.is_(True),
            GalleryImage.category == BEFORE_AFTER_CATEGORY,
            _active_detail_filters(),
        )
        .order_by(GalleryImage.sort_order, GalleryImage.created_at.desc())
        .all()
    )
    items: list[BeforeAfterItemDTO] = []
    for idx, row in enumerate(rows, start=1):
        detail = row.detail
        if not detail or not detail.og_image or not row.image:
            continue
        project_title = ""
        if row.project_id:
            project = Project.query.filter_by(id=row.project_id, is_active=True).first()
            project_title = project.title if project else ""
        items.append(
            BeforeAfterItemDTO(
                id=row.id,
                title=row.title,
                before_image=detail.og_image,
                after_image=row.image,
                project_title=project_title,
                location=detail.location or "",
                sort_order=row.sort_order or idx,
                is_active=True,
            )
        )
    return items


def load_progress_items() -> list[ProgressGalleryItemDTO]:
    rows = (
        GalleryImage.query.options(joinedload(GalleryImage.detail))
        .join(GalleryDetail)
        .filter(
            GalleryImage.is_active.is_(True),
            GalleryImage.category == PROGRESS_CATEGORY,
            _active_detail_filters(),
        )
        .order_by(GalleryImage.sort_order, GalleryImage.created_at.desc())
        .all()
    )
    items: list[ProgressGalleryItemDTO] = []
    for idx, row in enumerate(rows, start=1):
        detail = row.detail
        if not detail or not row.image:
            continue
        subtitle = (detail.caption or "").strip()
        if not subtitle and row.project_id:
            project = Project.query.filter_by(id=row.project_id, is_active=True).first()
            subtitle = project.title if project else ""
        items.append(
            ProgressGalleryItemDTO(
                id=row.id,
                title=row.title,
                subtitle=subtitle,
                image=row.image,
                date=detail.media_date or "",
                sort_order=row.sort_order or idx,
                is_active=True,
            )
        )
    return items


def load_awards_items() -> list[GalleryImageDTO]:
    rows = (
        GalleryImage.query.options(joinedload(GalleryImage.detail))
        .join(GalleryDetail)
        .filter(
            GalleryImage.is_active.is_(True),
            GalleryImage.category.in_(list(AWARDS_CATEGORIES)),
            _active_detail_filters(),
        )
        .order_by(GalleryImage.sort_order, GalleryImage.created_at.desc())
        .all()
    )
    if not rows:
        return []

    projects_by_id, services_by_slug, equipment_by_slug = _relation_maps(rows)
    return [
        gallery_row_to_dto(
            row,
            projects_by_id=projects_by_id,
            services_by_slug=services_by_slug,
            equipment_by_slug=equipment_by_slug,
        )
        for row in rows
        if row.image
    ]


def load_gallery_albums(images: list[GalleryImageDTO] | None = None) -> list[GalleryAlbumDTO]:
    items = images or load_gallery_images()
    albums: dict[str, GalleryAlbumDTO] = {}
    for idx, item in enumerate(items):
        if not item.album or item.album in albums:
            continue
        slug = item.album.lower().replace(" ", "-")
        albums[item.album] = GalleryAlbumDTO(
            id=idx + 1,
            title=item.album,
            slug=slug,
            description=item.caption or f"Photos from {item.album}.",
            image=item.image,
            filter_album=item.album,
            icon="bi-images",
            sort_order=idx + 1,
            is_active=True,
        )
    return list(albums.values())


def load_gallery_filter_options(images: list[GalleryImageDTO] | None = None) -> GalleryFilterOptionsDTO:
    items = images or load_gallery_images()
    return build_gallery_filter_options(items)
