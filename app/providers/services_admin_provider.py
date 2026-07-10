"""Services admin data provider — MySQL / SQLAlchemy."""

from __future__ import annotations

import json
import re
import unicodedata

from flask import current_app
from sqlalchemy import asc, desc, func, or_
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models.catalog import Project, Service, TeamMember
from app.models.service_detail import ServiceDetail
from app.providers.auth_provider import AuthProvider
from app.schemas.services_admin import ServiceAdminDTO, ServiceListItemDTO


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


def _lines_to_list(text: str) -> list[str]:
    return [line.strip() for line in (text or "").splitlines() if line.strip()]


class ServicesAdminProvider:
    """Database operations for service CRUD."""

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
    def get_or_create_detail(service: Service) -> ServiceDetail:
        if service.detail:
            return service.detail
        detail = ServiceDetail(service_id=service.id)
        db.session.add(detail)
        return detail

    @staticmethod
    def to_admin_dto(service: Service) -> ServiceAdminDTO:
        detail = service.detail
        created = service.created_at.strftime("%d %b %Y") if service.created_at else ""
        updated = service.updated_at.strftime("%d %b %Y") if service.updated_at else ""
        return ServiceAdminDTO(
            id=service.id,
            title=service.title,
            slug=service.slug,
            short_description=service.short_description or "",
            description=service.description or "",
            icon=service.icon or "",
            image=service.image or "",
            sort_order=service.sort_order or 0,
            is_featured=service.is_featured,
            is_active=service.is_active,
            meta_title=detail.meta_title if detail else "",
            meta_description=detail.meta_description if detail else "",
            og_image=detail.og_image if detail else "",
            canonical_url=detail.canonical_url if detail else "",
            scope_of_work=_json_list(detail.scope_of_work_json if detail else "[]"),
            benefits=_json_list(detail.benefits_json if detail else "[]"),
            equipment=_json_list(detail.equipment_json if detail else "[]"),
            gallery_paths=_json_list(detail.gallery_paths_json if detail else "[]"),
            related_project_ids=[
                int(x)
                for x in _json_list(detail.related_project_ids_json if detail else "[]")
                if str(x).isdigit()
            ],
            related_service_slugs=_json_list(detail.related_service_slugs_json if detail else "[]"),
            team_member_ids=[
                int(x)
                for x in _json_list(detail.team_member_ids_json if detail else "[]")
                if str(x).isdigit()
            ],
            created_at_label=created,
            updated_at_label=updated,
        )

    @staticmethod
    def to_list_item(service: Service) -> ServiceListItemDTO:
        updated = service.updated_at.strftime("%d %b %Y") if service.updated_at else ""
        return ServiceListItemDTO(
            id=service.id,
            title=service.title,
            slug=service.slug,
            short_description=service.short_description or "",
            icon=service.icon or "",
            image=service.image or "",
            sort_order=service.sort_order or 0,
            is_featured=service.is_featured,
            is_active=service.is_active,
            updated_at_label=updated,
        )

    @staticmethod
    def get_service(service_id: int, include_inactive: bool = False) -> Service | None:
        try:
            query = Service.query.filter_by(id=service_id)
            if not include_inactive:
                query = query.filter_by(is_active=True)
            return query.first()
        except SQLAlchemyError as exc:
            current_app.logger.error("get_service failed: %s", exc)
            return None

    @staticmethod
    def get_by_slug(slug: str, exclude_id: int | None = None) -> Service | None:
        query = Service.query.filter_by(slug=slug)
        if exclude_id:
            query = query.filter(Service.id != exclude_id)
        return query.first()

    @staticmethod
    def ensure_unique_slug(base: str, exclude_id: int | None = None) -> str:
        slug = slugify(base) or "service"
        candidate = slug
        counter = 2
        while ServicesAdminProvider.get_by_slug(candidate, exclude_id=exclude_id):
            candidate = f"{slug}-{counter}"
            counter += 1
        return candidate

    @staticmethod
    def query_services(
        *,
        q: str = "",
        featured: str = "",
        status: str = "",
        sort: str = "date_desc",
        page: int = 1,
        per_page: int = 20,
        include_deleted: bool = False,
    ) -> tuple[list[Service], int]:
        try:
            query = Service.query
            if include_deleted:
                query = query.filter(Service.is_active.is_(False))
            elif status == "all":
                pass
            elif status == "inactive":
                query = query.filter(Service.is_active.is_(False))
            else:
                query = query.filter(Service.is_active.is_(True))

            if q:
                term = f"%{q.strip()}%"
                query = query.filter(
                    or_(
                        Service.title.ilike(term),
                        Service.slug.ilike(term),
                        Service.short_description.ilike(term),
                    )
                )
            if featured == "yes":
                query = query.filter(Service.is_featured.is_(True))
            elif featured == "no":
                query = query.filter(Service.is_featured.is_(False))

            sort_map = {
                "date_desc": desc(Service.updated_at),
                "date_asc": asc(Service.updated_at),
                "title_asc": asc(Service.title),
                "title_desc": desc(Service.title),
                "sort_order": asc(Service.sort_order),
            }
            query = query.order_by(sort_map.get(sort, desc(Service.updated_at)))

            total = query.count()
            items = query.offset((page - 1) * per_page).limit(per_page).all()
            return items, total
        except SQLAlchemyError as exc:
            current_app.logger.error("query_services failed: %s", exc)
            return [], 0

    @staticmethod
    def get_stats() -> dict:
        try:
            total = Service.query.count()
            active = Service.query.filter_by(is_active=True).count()
            inactive = total - active
            featured = Service.query.filter_by(is_active=True, is_featured=True).count()
            recent = (
                Service.query.order_by(desc(Service.updated_at)).limit(6).all()
            )
            return {
                "total": total,
                "active": active,
                "inactive": inactive,
                "featured": featured,
                "recent": recent,
            }
        except SQLAlchemyError as exc:
            current_app.logger.error("get_stats failed: %s", exc)
            return {"total": 0, "active": 0, "inactive": 0, "featured": 0, "recent": []}

    @staticmethod
    def save_from_dto(dto: ServiceAdminDTO) -> Service:
        slug = ServicesAdminProvider.ensure_unique_slug(dto.slug or dto.title, dto.id)

        if dto.id:
            service = ServicesAdminProvider.get_service(dto.id, include_inactive=True)
            if not service:
                raise ValueError("Service not found.")
        else:
            service = Service(
                title=dto.title.strip(),
                slug=slug,
                short_description=dto.short_description.strip(),
                description=dto.description.strip(),
            )
            db.session.add(service)

        service.title = dto.title.strip()
        service.slug = slug
        service.short_description = dto.short_description.strip()
        service.description = dto.description.strip()
        service.icon = dto.icon.strip()
        service.image = dto.image.strip()
        service.sort_order = dto.sort_order
        service.is_featured = dto.is_featured
        service.is_active = dto.is_active

        db.session.flush()

        detail = ServicesAdminProvider.get_or_create_detail(service)
        detail.meta_title = dto.meta_title.strip()
        detail.meta_description = dto.meta_description.strip()
        detail.og_image = dto.og_image.strip()
        detail.canonical_url = dto.canonical_url.strip()
        detail.scope_of_work_json = _dump_json(dto.scope_of_work)
        detail.benefits_json = _dump_json(dto.benefits)
        detail.equipment_json = _dump_json(dto.equipment)
        detail.gallery_paths_json = _dump_json(dto.gallery_paths)
        detail.related_project_ids_json = _dump_json(dto.related_project_ids)
        detail.related_service_slugs_json = _dump_json(dto.related_service_slugs)
        detail.team_member_ids_json = _dump_json(dto.team_member_ids)

        return service

    @staticmethod
    def soft_delete(service: Service) -> None:
        service.is_active = False
        detail = ServicesAdminProvider.get_or_create_detail(service)
        detail.mark_deleted()

    @staticmethod
    def restore(service: Service) -> None:
        service.is_active = True
        if service.detail:
            service.detail.restore()

    @staticmethod
    def list_projects() -> list[Project]:
        return Project.query.filter_by(is_active=True).order_by(Project.title).all()

    @staticmethod
    def list_services_for_related(exclude_id: int | None = None) -> list[Service]:
        query = Service.query.filter_by(is_active=True).order_by(Service.title)
        if exclude_id:
            query = query.filter(Service.id != exclude_id)
        return query.all()

    @staticmethod
    def list_team() -> list[TeamMember]:
        return TeamMember.query.filter_by(is_active=True).order_by(TeamMember.name).all()

    @staticmethod
    def list_media_assets(folder: str = "services") -> list:
        from app.models.media import MediaAsset

        return (
            MediaAsset.query.filter_by(is_active=True, folder=folder)
            .order_by(desc(MediaAsset.created_at))
            .limit(200)
            .all()
        )

    @staticmethod
    def bulk_update(service_ids: list[int], action: str) -> int:
        count = 0
        services = Service.query.filter(Service.id.in_(service_ids)).all()
        for service in services:
            if action == "feature":
                service.is_featured = True
                count += 1
            elif action == "unfeature":
                service.is_featured = False
                count += 1
            elif action == "activate":
                ServicesAdminProvider.restore(service)
                count += 1
            elif action == "deactivate":
                ServicesAdminProvider.soft_delete(service)
                count += 1
            elif action == "restore":
                ServicesAdminProvider.restore(service)
                count += 1
        return count

    @staticmethod
    def lines_to_list(text: str) -> list[str]:
        return _lines_to_list(text)
