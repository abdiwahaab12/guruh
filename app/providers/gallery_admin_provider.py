"""Gallery admin data provider — MySQL / SQLAlchemy."""

from __future__ import annotations

import json
import re
import unicodedata

from flask import current_app
from sqlalchemy import asc, desc, func, or_
from sqlalchemy.exc import SQLAlchemyError

from app.constants.gallery_admin import BEFORE_AFTER_CATEGORY
from app.extensions import db
from app.models.catalog import GalleryImage, Project, Service, TeamMember
from app.models.equipment import Equipment
from app.models.gallery_detail import GalleryDetail
from app.providers.auth_provider import AuthProvider
from app.schemas.gallery_admin import GalleryAdminDTO, GalleryListItemDTO


def _is_upload_video_path(path: str) -> bool:
    if not path or "." not in path:
        return False
    return path.rsplit(".", 1)[-1].lower() in {"mp4", "webm", "mov", "avi", "mkv"}


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-")


def _json_list(raw: str | None) -> list:
    if not raw:
        return []
    try:
        data = json.loads(raw)
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def _dump_json(data: list) -> str:
    return json.dumps(data)


class GalleryAdminProvider:
    """Database operations for gallery CRUD."""

    @staticmethod
    def commit() -> bool:
        return AuthProvider.commit()

    @staticmethod
    def rollback() -> None:
        AuthProvider.rollback()

    @staticmethod
    def record_audit(**kwargs) -> None:
        AuthProvider.record_audit_event(**kwargs)

    @staticmethod
    def get_or_create_detail(item: GalleryImage, slug: str = "") -> GalleryDetail:
        if item.detail:
            return item.detail
        detail = GalleryDetail(
            gallery_image_id=item.id,
            slug=slug or slugify(item.title) or f"gallery-{item.id}",
        )
        db.session.add(detail)
        return detail

    @staticmethod
    def to_admin_dto(item: GalleryImage) -> GalleryAdminDTO:
        detail = item.detail
        created = item.created_at.strftime("%d %b %Y") if item.created_at else ""
        updated = item.updated_at.strftime("%d %b %Y") if item.updated_at else ""
        return GalleryAdminDTO(
            id=item.id,
            title=item.title,
            slug=detail.slug if detail else "",
            image=item.image or "",
            category=item.category or "",
            project_id=item.project_id,
            sort_order=item.sort_order or 0,
            is_active=item.is_active,
            media_type=detail.media_type if detail else "image",
            album=detail.album if detail else "",
            caption=detail.caption if detail else "",
            location=detail.location if detail else "",
            county=detail.county if detail else "",
            country=detail.country if detail else "Somalia",
            media_date=detail.media_date if detail else "",
            year=detail.year if detail else "",
            is_featured=detail.is_featured if detail else False,
            meta_title=detail.meta_title if detail else "",
            meta_description=detail.meta_description if detail else "",
            og_image=detail.og_image if detail else "",
            canonical_url=detail.canonical_url if detail else "",
            service_slug=detail.service_slug if detail else "",
            equipment_slug=detail.equipment_slug if detail else "",
            team_member_ids=[
                int(x)
                for x in _json_list(detail.team_member_ids_json if detail else "[]")
                if str(x).isdigit()
            ],
            video_provider=detail.video_provider if detail else "",
            video_id=detail.video_id if detail else "",
            embed_url=detail.embed_url if detail else "",
            created_at_label=created,
            updated_at_label=updated,
        )

    @staticmethod
    def to_list_item(item: GalleryImage) -> GalleryListItemDTO:
        detail = item.detail
        updated = item.updated_at.strftime("%d %b %Y") if item.updated_at else ""
        return GalleryListItemDTO(
            id=item.id,
            title=item.title,
            slug=detail.slug if detail else "",
            image=item.image or "",
            category=item.category or "",
            album=detail.album if detail else "",
            media_type=detail.media_type if detail else "image",
            country=detail.country if detail else "",
            project_id=item.project_id,
            sort_order=item.sort_order or 0,
            is_featured=detail.is_featured if detail else False,
            is_active=item.is_active,
            updated_at_label=updated,
        )

    @staticmethod
    def get_item(item_id: int, include_inactive: bool = False) -> GalleryImage | None:
        try:
            query = GalleryImage.query.filter_by(id=item_id)
            if not include_inactive:
                query = query.filter_by(is_active=True)
            return query.first()
        except SQLAlchemyError as exc:
            current_app.logger.error("get_item failed: %s", exc)
            return None

    @staticmethod
    def get_by_slug(slug: str, exclude_id: int | None = None) -> GalleryDetail | None:
        query = GalleryDetail.query.filter_by(slug=slug)
        if exclude_id:
            query = query.filter(GalleryDetail.gallery_image_id != exclude_id)
        return query.first()

    @staticmethod
    def ensure_unique_slug(base: str, exclude_id: int | None = None) -> str:
        slug = slugify(base) or "gallery-item"
        candidate = slug
        counter = 2
        while GalleryAdminProvider.get_by_slug(candidate, exclude_id=exclude_id):
            candidate = f"{slug}-{counter}"
            counter += 1
        return candidate

    @staticmethod
    def query_gallery(
        *,
        q: str = "",
        album: str = "",
        category: str = "",
        project_id: int | None = None,
        service: str = "",
        country: str = "",
        featured: str = "",
        status: str = "",
        sort: str = "date_desc",
        page: int = 1,
        per_page: int = 24,
        include_deleted: bool = False,
    ) -> tuple[list[GalleryImage], int]:
        try:
            query = GalleryImage.query.outerjoin(
                GalleryDetail, GalleryDetail.gallery_image_id == GalleryImage.id
            )

            if include_deleted:
                query = query.filter(GalleryImage.is_active.is_(False))
            elif status == "all":
                pass
            elif status == "inactive":
                query = query.filter(GalleryImage.is_active.is_(False))
            else:
                query = query.filter(GalleryImage.is_active.is_(True))

            if q:
                term = f"%{q.strip()}%"
                query = query.filter(
                    or_(
                        GalleryImage.title.ilike(term),
                        GalleryDetail.slug.ilike(term),
                        GalleryDetail.caption.ilike(term),
                        GalleryImage.category.ilike(term),
                        GalleryDetail.location.ilike(term),
                    )
                )
            if album:
                query = query.filter(GalleryDetail.album == album)
            if category:
                query = query.filter(GalleryImage.category == category)
            if project_id:
                query = query.filter(GalleryImage.project_id == project_id)
            if service:
                query = query.filter(GalleryDetail.service_slug == service)
            if country:
                query = query.filter(GalleryDetail.country == country)
            if featured == "yes":
                query = query.filter(GalleryDetail.is_featured.is_(True))
            elif featured == "no":
                query = query.filter(GalleryDetail.is_featured.is_(False))

            sort_map = {
                "date_desc": desc(GalleryImage.updated_at),
                "date_asc": asc(GalleryImage.updated_at),
                "title_asc": asc(GalleryImage.title),
                "title_desc": desc(GalleryImage.title),
                "sort_order": asc(GalleryImage.sort_order),
            }
            query = query.order_by(sort_map.get(sort, desc(GalleryImage.updated_at)))

            total = query.count()
            items = query.offset((page - 1) * per_page).limit(per_page).all()
            return items, total
        except SQLAlchemyError as exc:
            current_app.logger.error("query_gallery failed: %s", exc)
            return [], 0

    @staticmethod
    def get_stats() -> dict:
        try:
            total = GalleryImage.query.count()
            active = GalleryImage.query.filter_by(is_active=True).count()
            inactive = total - active

            base = db.session.query(GalleryImage).join(
                GalleryDetail, GalleryDetail.gallery_image_id == GalleryImage.id
            )

            albums = (
                db.session.query(func.count(func.distinct(GalleryDetail.album)))
                .filter(GalleryDetail.album != "")
                .scalar()
                or 0
            )
            images = base.filter(GalleryDetail.media_type == "image").count()
            videos = base.filter(GalleryDetail.media_type == "video").count()
            featured = (
                base.filter(GalleryImage.is_active.is_(True), GalleryDetail.is_featured.is_(True)).count()
            )
            recent = GalleryImage.query.order_by(desc(GalleryImage.updated_at)).limit(8).all()

            return {
                "total": total,
                "albums": albums,
                "images": images,
                "videos": videos,
                "featured": featured,
                "active": active,
                "inactive": inactive,
                "recent": recent,
            }
        except SQLAlchemyError as exc:
            current_app.logger.error("get_stats failed: %s", exc)
            return {
                "total": 0,
                "albums": 0,
                "images": 0,
                "videos": 0,
                "featured": 0,
                "active": 0,
                "inactive": 0,
                "recent": [],
            }

    @staticmethod
    def save_from_dto(dto: GalleryAdminDTO) -> GalleryImage:
        if not dto.image or not dto.image.strip():
            raise ValueError("Media path is required — select from the Media Library.")

        slug = GalleryAdminProvider.ensure_unique_slug(dto.slug or dto.title, dto.id)

        if dto.id:
            item = GalleryAdminProvider.get_item(dto.id, include_inactive=True)
            if not item:
                raise ValueError("Gallery item not found.")
        else:
            item = GalleryImage(
                title=dto.title.strip(),
                image=dto.image.strip(),
                category=dto.category.strip(),
            )
            db.session.add(item)

        item.title = dto.title.strip()
        item.image = dto.image.strip()
        item.category = dto.category.strip()
        item.project_id = dto.project_id or None
        item.sort_order = dto.sort_order
        item.is_active = dto.is_active

        db.session.flush()

        detail = GalleryAdminProvider.get_or_create_detail(item, slug)
        detail.slug = slug
        detail.media_type = dto.media_type.strip() or "image"
        detail.album = dto.album.strip()
        detail.caption = dto.caption.strip()
        detail.location = dto.location.strip()
        detail.county = dto.county.strip()
        detail.country = dto.country.strip() or "Somalia"
        detail.media_date = dto.media_date.strip()
        detail.year = dto.year.strip()
        detail.is_featured = dto.is_featured
        detail.meta_title = dto.meta_title.strip()
        detail.meta_description = dto.meta_description.strip()
        detail.og_image = dto.og_image.strip()
        detail.canonical_url = dto.canonical_url.strip()
        detail.service_slug = dto.service_slug.strip()
        detail.equipment_slug = dto.equipment_slug.strip()
        detail.team_member_ids_json = _dump_json(dto.team_member_ids)
        detail.video_provider = dto.video_provider.strip()
        detail.video_id = dto.video_id.strip()
        detail.embed_url = dto.embed_url.strip()

        if dto.category.strip() == BEFORE_AFTER_CATEGORY:
            detail.media_type = "image"
            if not detail.og_image.strip():
                raise ValueError("Before image is required for Before & After items.")
        elif detail.media_type == "video":
            if not detail.video_provider:
                detail.video_provider = "upload"
            if not detail.embed_url and _is_upload_video_path(item.image):
                detail.embed_url = item.image.strip()
            if _is_upload_video_path(item.image) and not detail.og_image:
                pass
        elif _is_upload_video_path(item.image):
            detail.media_type = "video"
            detail.video_provider = detail.video_provider or "upload"
            if not detail.embed_url:
                detail.embed_url = item.image.strip()

        return item

    @staticmethod
    def soft_delete(item: GalleryImage) -> None:
        item.is_active = False
        detail = GalleryAdminProvider.get_or_create_detail(item)
        detail.mark_deleted()

    @staticmethod
    def restore(item: GalleryImage) -> None:
        item.is_active = True
        if item.detail:
            item.detail.restore()

    @staticmethod
    def list_projects() -> list[Project]:
        return Project.query.filter_by(is_active=True).order_by(Project.title).all()

    @staticmethod
    def list_services() -> list[Service]:
        return Service.query.filter_by(is_active=True).order_by(Service.title).all()

    @staticmethod
    def list_equipment() -> list[Equipment]:
        return Equipment.query.filter_by(is_active=True).order_by(Equipment.name).all()

    @staticmethod
    def list_team() -> list[TeamMember]:
        return TeamMember.query.filter_by(is_active=True).order_by(TeamMember.name).all()

    @staticmethod
    def list_media_assets(folder: str = "gallery") -> list:
        from app.models.media import MediaAsset

        folders = [folder] if folder != "gallery" else ["gallery", "general"]
        return (
            MediaAsset.query.filter(
                MediaAsset.is_active.is_(True),
                MediaAsset.folder.in_(folders),
            )
            .order_by(desc(MediaAsset.created_at))
            .limit(200)
            .all()
        )

    @staticmethod
    def bulk_update(item_ids: list[int], action: str) -> int:
        count = 0
        items = GalleryImage.query.filter(GalleryImage.id.in_(item_ids)).all()
        for item in items:
            if action == "feature":
                detail = GalleryAdminProvider.get_or_create_detail(item)
                detail.is_featured = True
                count += 1
            elif action == "unfeature":
                if item.detail:
                    item.detail.is_featured = False
                count += 1
            elif action == "activate":
                GalleryAdminProvider.restore(item)
                count += 1
            elif action == "deactivate":
                GalleryAdminProvider.soft_delete(item)
                count += 1
            elif action == "restore":
                GalleryAdminProvider.restore(item)
                count += 1
        return count
