"""
Maps Page Builder seed/ORM data to DTOs.
"""

from app.data.page_sections import ALL_PAGE_SECTIONS, PAGE_SECTIONS_BY_SLUG
from app.models.page_sections import PageSection
from app.schemas.content import PageSectionDTO, PageSectionListDTO


def section_from_dict(data: dict) -> PageSectionDTO:
    return PageSectionDTO(
        id=data["id"],
        page_slug=data["page_slug"],
        section_key=data["section_key"],
        section_title=data["section_title"],
        block_key=data.get("block_key") or "",
        display_order=data.get("display_order", 0),
        layout_type=data.get("layout_type", "default"),
        background_style=data.get("background_style", "default"),
        spacing=data.get("spacing", "default"),
        animation=data.get("animation", "none"),
        is_visible=data.get("is_visible", True),
        seo_anchor=data.get("seo_anchor") or data["section_key"].replace("_", "-"),
        is_active=data.get("is_active", True),
        extra=dict(data.get("extra") or {}),
        created_at=data.get("created_at", ""),
        updated_at=data.get("updated_at", ""),
    )


def section_from_model(row: PageSection) -> PageSectionDTO:
    return PageSectionDTO(
        id=row.id,
        page_slug=row.page_slug,
        section_key=row.section_key,
        section_title=row.section_title,
        block_key=row.block_key or "",
        display_order=row.display_order,
        layout_type=row.layout_type,
        background_style=row.background_style,
        spacing=row.spacing,
        animation=row.animation,
        is_visible=row.is_visible,
        seo_anchor=row.seo_anchor or row.section_key.replace("_", "-"),
        is_active=row.is_active,
        extra=dict(row.extra or {}),
        created_at=row.created_at.isoformat() if row.created_at else "",
        updated_at=row.updated_at.isoformat() if row.updated_at else "",
    )


def build_section_list_from_seed(page_slug: str) -> PageSectionListDTO:
    rows = PAGE_SECTIONS_BY_SLUG.get(page_slug, [])
    sections = [section_from_dict(data) for data in rows]
    sections.sort(key=lambda s: s.display_order)
    return PageSectionListDTO(page_slug=page_slug, sections=sections)


def get_all_seed_sections() -> list[PageSectionDTO]:
    return [section_from_dict(data) for data in ALL_PAGE_SECTIONS]
