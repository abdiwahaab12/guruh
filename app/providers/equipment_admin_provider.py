"""Equipment admin data provider — MySQL / SQLAlchemy."""

from __future__ import annotations

import json
import re
import unicodedata

from flask import current_app
from sqlalchemy import asc, desc, or_
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models.catalog import Project, Service, TeamMember
from app.models.equipment import Equipment, EquipmentDetail
from app.providers.auth_provider import AuthProvider
from app.schemas.equipment_admin import EquipmentAdminDTO, EquipmentListItemDTO, EquipmentSpecDTO


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


def _parse_specs(raw: str | None) -> list[EquipmentSpecDTO]:
    items = []
    for entry in _json_list(raw):
        if isinstance(entry, dict):
            items.append(
                EquipmentSpecDTO(
                    label=str(entry.get("label", "")),
                    value=str(entry.get("value", "")),
                )
            )
    return items


class EquipmentAdminProvider:
    """Database operations for equipment CRUD."""

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
    def get_or_create_detail(equipment: Equipment) -> EquipmentDetail:
        if equipment.detail:
            return equipment.detail
        detail = EquipmentDetail(equipment_id=equipment.id)
        db.session.add(detail)
        return detail

    @staticmethod
    def to_admin_dto(equipment: Equipment) -> EquipmentAdminDTO:
        detail = equipment.detail
        created = equipment.created_at.strftime("%d %b %Y") if equipment.created_at else ""
        updated = equipment.updated_at.strftime("%d %b %Y") if equipment.updated_at else ""
        return EquipmentAdminDTO(
            id=equipment.id,
            name=equipment.name,
            slug=equipment.slug,
            category=equipment.category or "",
            short_description=equipment.short_description or "",
            description=equipment.description or "",
            image=equipment.image or "",
            capacity=equipment.capacity or "",
            condition=equipment.condition or "Operational",
            maintenance_status=equipment.maintenance_status or "",
            usage=equipment.usage or "",
            sort_order=equipment.sort_order or 0,
            is_featured=equipment.is_featured,
            is_active=equipment.is_active,
            meta_title=detail.meta_title if detail else "",
            meta_description=detail.meta_description if detail else "",
            og_image=detail.og_image if detail else "",
            canonical_url=detail.canonical_url if detail else "",
            specifications=_parse_specs(detail.specifications_json if detail else "[]"),
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
    def to_list_item(equipment: Equipment) -> EquipmentListItemDTO:
        updated = equipment.updated_at.strftime("%d %b %Y") if equipment.updated_at else ""
        return EquipmentListItemDTO(
            id=equipment.id,
            name=equipment.name,
            slug=equipment.slug,
            category=equipment.category or "",
            short_description=equipment.short_description or "",
            image=equipment.image or "",
            condition=equipment.condition or "",
            sort_order=equipment.sort_order or 0,
            is_featured=equipment.is_featured,
            is_active=equipment.is_active,
            updated_at_label=updated,
        )

    @staticmethod
    def get_equipment(equipment_id: int, include_inactive: bool = False) -> Equipment | None:
        try:
            query = Equipment.query.filter_by(id=equipment_id)
            if not include_inactive:
                query = query.filter_by(is_active=True)
            return query.first()
        except SQLAlchemyError as exc:
            current_app.logger.error("get_equipment failed: %s", exc)
            return None

    @staticmethod
    def get_by_slug(slug: str, exclude_id: int | None = None) -> Equipment | None:
        query = Equipment.query.filter_by(slug=slug)
        if exclude_id:
            query = query.filter(Equipment.id != exclude_id)
        return query.first()

    @staticmethod
    def ensure_unique_slug(base: str, exclude_id: int | None = None) -> str:
        slug = slugify(base) or "equipment"
        candidate = slug
        counter = 2
        while EquipmentAdminProvider.get_by_slug(candidate, exclude_id=exclude_id):
            candidate = f"{slug}-{counter}"
            counter += 1
        return candidate

    @staticmethod
    def query_equipment(
        *,
        q: str = "",
        category: str = "",
        featured: str = "",
        status: str = "",
        sort: str = "date_desc",
        page: int = 1,
        per_page: int = 20,
        include_deleted: bool = False,
    ) -> tuple[list[Equipment], int]:
        try:
            query = Equipment.query
            if include_deleted:
                query = query.filter(Equipment.is_active.is_(False))
            elif status == "all":
                pass
            elif status == "inactive":
                query = query.filter(Equipment.is_active.is_(False))
            else:
                query = query.filter(Equipment.is_active.is_(True))

            if q:
                term = f"%{q.strip()}%"
                query = query.filter(
                    or_(
                        Equipment.name.ilike(term),
                        Equipment.slug.ilike(term),
                        Equipment.short_description.ilike(term),
                        Equipment.category.ilike(term),
                    )
                )
            if category:
                query = query.filter(Equipment.category == category)
            if featured == "yes":
                query = query.filter(Equipment.is_featured.is_(True))
            elif featured == "no":
                query = query.filter(Equipment.is_featured.is_(False))

            sort_map = {
                "date_desc": desc(Equipment.updated_at),
                "date_asc": asc(Equipment.updated_at),
                "name_asc": asc(Equipment.name),
                "name_desc": desc(Equipment.name),
                "sort_order": asc(Equipment.sort_order),
            }
            query = query.order_by(sort_map.get(sort, desc(Equipment.updated_at)))

            total = query.count()
            items = query.offset((page - 1) * per_page).limit(per_page).all()
            return items, total
        except SQLAlchemyError as exc:
            current_app.logger.error("query_equipment failed: %s", exc)
            return [], 0

    @staticmethod
    def get_stats() -> dict:
        try:
            total = Equipment.query.count()
            active = Equipment.query.filter_by(is_active=True).count()
            inactive = total - active
            featured = Equipment.query.filter_by(is_active=True, is_featured=True).count()
            recent = Equipment.query.order_by(desc(Equipment.updated_at)).limit(6).all()
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
    def save_from_dto(dto: EquipmentAdminDTO) -> Equipment:
        slug = EquipmentAdminProvider.ensure_unique_slug(dto.slug or dto.name, dto.id)

        if dto.id:
            equipment = EquipmentAdminProvider.get_equipment(dto.id, include_inactive=True)
            if not equipment:
                raise ValueError("Equipment not found.")
        else:
            equipment = Equipment(
                name=dto.name.strip(),
                slug=slug,
                category=dto.category.strip(),
                short_description=dto.short_description.strip(),
                description=dto.description.strip(),
            )
            db.session.add(equipment)

        equipment.name = dto.name.strip()
        equipment.slug = slug
        equipment.category = dto.category.strip()
        equipment.short_description = dto.short_description.strip()
        equipment.description = dto.description.strip()
        equipment.image = dto.image.strip()
        equipment.capacity = dto.capacity.strip()
        equipment.condition = dto.condition.strip() or "Operational"
        equipment.maintenance_status = dto.maintenance_status.strip()
        equipment.usage = dto.usage.strip()
        equipment.sort_order = dto.sort_order
        equipment.is_featured = dto.is_featured
        equipment.is_active = dto.is_active

        db.session.flush()

        detail = EquipmentAdminProvider.get_or_create_detail(equipment)
        detail.meta_title = dto.meta_title.strip()
        detail.meta_description = dto.meta_description.strip()
        detail.og_image = dto.og_image.strip()
        detail.canonical_url = dto.canonical_url.strip()
        detail.specifications_json = _dump_json(
            [{"label": s.label, "value": s.value} for s in dto.specifications]
        )
        detail.gallery_paths_json = _dump_json(dto.gallery_paths)
        detail.related_project_ids_json = _dump_json(dto.related_project_ids)
        detail.related_service_slugs_json = _dump_json(dto.related_service_slugs)
        detail.team_member_ids_json = _dump_json(dto.team_member_ids)

        return equipment

    @staticmethod
    def soft_delete(equipment: Equipment) -> None:
        equipment.is_active = False
        detail = EquipmentAdminProvider.get_or_create_detail(equipment)
        detail.mark_deleted()

    @staticmethod
    def restore(equipment: Equipment) -> None:
        equipment.is_active = True
        if equipment.detail:
            equipment.detail.restore()

    @staticmethod
    def list_projects() -> list[Project]:
        return Project.query.filter_by(is_active=True).order_by(Project.title).all()

    @staticmethod
    def list_services() -> list[Service]:
        return Service.query.filter_by(is_active=True).order_by(Service.title).all()

    @staticmethod
    def list_team() -> list[TeamMember]:
        return TeamMember.query.filter_by(is_active=True).order_by(TeamMember.name).all()

    @staticmethod
    def list_media_assets(folder: str = "equipment") -> list:
        from app.models.media import MediaAsset

        return (
            MediaAsset.query.filter_by(is_active=True, folder=folder)
            .order_by(desc(MediaAsset.created_at))
            .limit(200)
            .all()
        )

    @staticmethod
    def bulk_update(equipment_ids: list[int], action: str) -> int:
        count = 0
        rows = Equipment.query.filter(Equipment.id.in_(equipment_ids)).all()
        for equipment in rows:
            if action == "feature":
                equipment.is_featured = True
                count += 1
            elif action == "unfeature":
                equipment.is_featured = False
                count += 1
            elif action == "activate":
                EquipmentAdminProvider.restore(equipment)
                count += 1
            elif action == "deactivate":
                EquipmentAdminProvider.soft_delete(equipment)
                count += 1
            elif action == "restore":
                EquipmentAdminProvider.restore(equipment)
                count += 1
        return count

    @staticmethod
    def parse_specs_text(text: str) -> list[EquipmentSpecDTO]:
        items = []
        for line in (text or "").splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split("|", 1)
            if len(parts) == 2:
                items.append(EquipmentSpecDTO(parts[0].strip(), parts[1].strip()))
        return items

    @staticmethod
    def specs_to_text(specs: list[EquipmentSpecDTO]) -> str:
        return "\n".join(f"{s.label}|{s.value}" for s in specs if s.label or s.value)
