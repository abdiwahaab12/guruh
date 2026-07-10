"""
Maps equipment catalog data to EquipmentDTO for providers and services.
"""

from app.data.equipment_catalog import EQUIPMENT_CATALOG
from app.schemas.content import EquipmentDTO


def build_equipment() -> list[EquipmentDTO]:
    return [_catalog_to_dto(eq, i) for i, eq in enumerate(EQUIPMENT_CATALOG)]


def build_equipment_by_slug(slug: str) -> EquipmentDTO | None:
    for i, eq in enumerate(EQUIPMENT_CATALOG):
        if eq["slug"] == slug:
            return _catalog_to_dto(eq, i)
    return None


def _catalog_to_dto(eq: dict, index: int) -> EquipmentDTO:
    return EquipmentDTO(
        id=index + 1,
        name=eq["name"],
        slug=eq["slug"],
        category=eq["category"],
        short_description=eq["short_description"],
        description=eq["description"],
        image=eq["image"],
        capacity=eq.get("capacity", ""),
        condition=eq.get("condition", "Operational"),
        maintenance_status=eq.get("maintenance_status", ""),
        category_key=eq.get("category_key", ""),
        sort_order=index + 1,
        is_featured=eq.get("is_featured", False),
        usage=eq.get("usage", ""),
        specifications=list(eq.get("specifications", [])),
        gallery_images=list(eq.get("gallery_images", [])),
        gallery_categories=list(eq.get("gallery_categories", [])),
        related_project_slugs=list(eq.get("related_project_slugs", [])),
        related_service_slugs=list(eq.get("related_service_slugs", [])),
        meta_title=eq.get("meta_title", eq["name"]),
        meta_description=eq.get("meta_description", eq["short_description"]),
    )
