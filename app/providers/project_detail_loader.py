"""
Build Page Builder composition for a single project detail page from ProjectDTO.

Used for admin-created projects (and any project) when seed page sections are absent.
"""

from __future__ import annotations

from typing import Any

from app.data.projects_page import build_project_detail_blocks, build_project_detail_sections
from app.providers.block_loader import block_from_dict
from app.providers.page_loader import section_from_dict
from app.schemas.content import (
    ContentBlockDTO,
    PageCompositionDTO,
    PageSectionDTO,
    PageSectionResolvedDTO,
    ProjectDTO,
)


def _project_to_seed_dict(project: ProjectDTO) -> dict[str, Any]:
    service_slugs = list(dict.fromkeys(
        [*(project.service_slugs or []), *(getattr(project, "related_service_slugs", None) or [])]
    ))
    return {
        "slug": project.slug,
        "title": project.title,
        "description": project.description,
        "location": project.location,
        "client": project.client,
        "category": project.category,
        "cover_image": project.cover_image,
        "completion_date": project.completion_date,
        "completion_year": project.completion_year or (project.completion_date[:4] if project.completion_date else ""),
        "county": project.county,
        "country": project.country,
        "status": project.status,
        "consultant": project.consultant,
        "duration": project.duration,
        "overview": project.overview or project.description,
        "scope_of_work": list(project.scope_of_work or []),
        "challenges": list(project.challenges or []),
        "solutions": list(project.solutions or []),
        "equipment_used": list(project.equipment_used or []),
        "gallery_images": list(project.gallery_images or []),
        "gallery_categories": list(project.gallery_categories or []),
        "service_slugs": service_slugs,
        "related_project_slugs": list(project.related_project_slugs or []),
        "meta_title": project.meta_title or project.title,
        "meta_description": project.meta_description or project.description,
    }


def _skip_section_keys(proj: dict[str, Any]) -> set[str]:
    skip: set[str] = set()
    if not proj.get("gallery_images"):
        skip.add("gallery")
    if not proj.get("scope_of_work"):
        skip.add("scope")
    if not proj.get("challenges") and not proj.get("solutions"):
        skip.add("challenges")
    if not proj.get("equipment_used"):
        skip.add("equipment")
    if not proj.get("service_slugs") and not proj.get("related_project_slugs"):
        skip.add("related")
    return skip


def _resolve_section(
    section: PageSectionDTO,
    blocks_by_key: dict[str, ContentBlockDTO],
) -> PageSectionResolvedDTO | None:
    block = blocks_by_key.get(section.block_key) if section.block_key else None
    if not block:
        return None
    return PageSectionResolvedDTO(
        id=section.id,
        page_slug=section.page_slug,
        section_key=section.section_key,
        section_title=section.section_title,
        block_key=section.block_key,
        display_order=section.display_order,
        layout_type=section.layout_type,
        background_style=section.background_style,
        spacing=section.spacing,
        animation=section.animation,
        is_visible=section.is_visible,
        seo_anchor=section.seo_anchor,
        is_active=section.is_active,
        extra=section.extra,
        created_at=section.created_at,
        updated_at=section.updated_at,
        block=block,
        blocks=[block],
    )


def build_composition_for_project(project: ProjectDTO) -> PageCompositionDTO:
    """Build a full project detail page from live project data."""
    from app.services.content_service import ContentBlockService

    proj = _project_to_seed_dict(project)
    page_slug = f"project-{project.slug}"
    id_base = 80000 + max(project.id, 0)

    blocks_data = build_project_detail_blocks(proj, id_base)
    sections_data = build_project_detail_sections(proj, id_base)
    skip = _skip_section_keys(proj)

    blocks_by_key: dict[str, ContentBlockDTO] = {
        block["block_key"]: block_from_dict(block) for block in blocks_data
    }

    cta = ContentBlockService.get_registry(active_only=True).get("call_to_action")
    if cta:
        blocks_by_key["call_to_action"] = cta

    sections: list[PageSectionResolvedDTO] = []
    for sec_data in sections_data:
        if sec_data["section_key"] in skip:
            continue
        section = section_from_dict(sec_data)
        resolved = _resolve_section(section, blocks_by_key)
        if resolved:
            sections.append(resolved)

    return PageCompositionDTO(page_slug=page_slug, sections=sections)
