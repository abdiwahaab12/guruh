"""
Public equipment data — loads admin-managed fleet records for the website.
"""

from __future__ import annotations

import json

from sqlalchemy.orm import joinedload

from app.data.equipment_catalog import CATEGORY_KEY_MAP
from app.models.catalog import Project
from app.models.equipment import Equipment
from app.schemas.content import EquipmentDTO


def _json_list(raw: str | None) -> list:
    if not raw:
        return []
    try:
        data = json.loads(raw)
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def _parse_specifications(detail) -> list[dict]:
    items: list[dict] = []
    if not detail:
        return items
    for entry in _json_list(detail.specifications_json):
        if isinstance(entry, dict):
            items.append(
                {
                    "label": str(entry.get("label", "")),
                    "value": str(entry.get("value", "")),
                }
            )
    return items


def _project_slug_map(project_ids: set[int]) -> dict[int, str]:
    if not project_ids:
        return {}
    rows = Project.query.filter(Project.id.in_(project_ids), Project.is_active.is_(True)).all()
    return {row.id: row.slug for row in rows}


def equipment_row_to_dto(
    row: Equipment,
    *,
    project_slugs: list[str] | None = None,
) -> EquipmentDTO:
    detail = row.detail
    if project_slugs is None and detail:
        project_ids = {
            int(value)
            for value in _json_list(detail.related_project_ids_json)
            if str(value).isdigit()
        }
        slug_map = _project_slug_map(project_ids)
        project_slugs = [slug_map[pid] for pid in sorted(project_ids) if pid in slug_map]
    else:
        project_slugs = project_slugs or []

    return EquipmentDTO(
        id=row.id,
        name=row.name,
        slug=row.slug,
        category=row.category or "",
        short_description=row.short_description or "",
        description=row.description or "",
        image=row.image or "",
        capacity=row.capacity or "",
        condition=row.condition or "Operational",
        maintenance_status=row.maintenance_status or "",
        category_key=CATEGORY_KEY_MAP.get(row.category or "", ""),
        sort_order=row.sort_order or 0,
        is_featured=row.is_featured,
        is_active=row.is_active,
        usage=row.usage or "",
        specifications=_parse_specifications(detail),
        gallery_images=_json_list(detail.gallery_paths_json if detail else "[]"),
        gallery_categories=[],
        related_project_slugs=project_slugs,
        related_service_slugs=_json_list(detail.related_service_slugs_json if detail else "[]"),
        meta_title=(detail.meta_title if detail else "") or row.name,
        meta_description=(detail.meta_description if detail else "") or row.short_description,
    )


def load_equipment(*, featured_only: bool = False) -> list[EquipmentDTO]:
    query = (
        Equipment.query.options(joinedload(Equipment.detail))
        .filter(Equipment.is_active.is_(True))
        .order_by(Equipment.sort_order, Equipment.name)
    )
    if featured_only:
        query = query.filter(Equipment.is_featured.is_(True))

    rows = []
    project_ids: set[int] = set()
    for row in query.all():
        detail = row.detail
        if detail and detail.deleted_at is not None:
            continue
        rows.append(row)
        if detail:
            for value in _json_list(detail.related_project_ids_json):
                if str(value).isdigit():
                    project_ids.add(int(value))

    slug_map = _project_slug_map(project_ids)
    return [
        equipment_row_to_dto(
            row,
            project_slugs=[
                slug_map[pid]
                for pid in sorted(
                    {
                        int(value)
                        for value in _json_list(row.detail.related_project_ids_json if row.detail else "[]")
                        if str(value).isdigit()
                    }
                )
                if pid in slug_map
            ],
        )
        for row in rows
    ]


def load_equipment_by_slug(slug: str) -> EquipmentDTO | None:
    row = (
        Equipment.query.options(joinedload(Equipment.detail))
        .filter(Equipment.slug == slug, Equipment.is_active.is_(True))
        .first()
    )
    if not row:
        return None
    if row.detail and row.detail.deleted_at is not None:
        return None
    return equipment_row_to_dto(row)
