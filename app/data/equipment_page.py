"""
Equipment Page and equipment detail pages — CMS blocks and Page Builder sections.

Built from app.data.equipment_catalog.
"""

from __future__ import annotations

from typing import Any

from app.data.cms_blocks import SEED_TIMESTAMP
from app.data.equipment_catalog import (
    EQUIPMENT_CATALOG,
    EQUIPMENT_CATEGORIES,
    EQUIPMENT_PAGE_CONTENT,
    FLEET_GALLERY_IMAGES,
)

_BLOCK_ID_START = 600
_SECTION_ID_START = 600
_DETAIL_BLOCK_ID_START = 900
_DETAIL_SECTION_ID_START = 900


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
    extra: dict | None = None,
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
        "is_visible": True,
        "seo_anchor": anchor,
        "is_active": True,
        "extra": extra or {},
        "created_at": SEED_TIMESTAMP,
        "updated_at": SEED_TIMESTAMP,
    }


def build_equipment_page_blocks() -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    bid = _BLOCK_ID_START
    content = EQUIPMENT_PAGE_CONTENT

    overview = content["overview"]
    blocks.append(
        _block(
            bid,
            "equipment_page_overview",
            overview["title"],
            subtitle=overview["subtitle"],
            short_summary=overview["short_summary"],
            full_content=overview["full_content"],
            hero_image=overview["hero_image"],
            display_order=bid,
        )
    )
    bid += 1

    category_items = [
        _item(
            i + 1,
            cat["title"],
            item_key=cat["slug"],
            short_summary=cat["summary"],
            icon=cat["icon"],
            sort_order=i + 1,
            extra={"category_key": cat["slug"]},
        )
        for i, cat in enumerate(EQUIPMENT_CATEGORIES)
    ]
    blocks.append(
        _block(
            bid,
            "equipment_categories",
            "Equipment Categories",
            subtitle="Fleet by Sector",
            short_summary="Six specialist plant categories supporting GCCL project delivery.",
            display_order=bid,
            items=category_items,
        )
    )
    bid += 1

    grid_items = [
        _item(
            i + 1,
            eq["name"],
            item_key=eq["slug"],
            short_summary=eq["short_description"],
            full_content=eq["description"],
            image=eq["image"],
            subtitle=eq["category"],
            sort_order=i + 1,
            extra={
                "equipment_slug": eq["slug"],
                "category_key": eq.get("category_key", ""),
                "capacity": eq.get("capacity", ""),
                "condition": eq.get("condition", "Operational"),
                "learn_more_url": f"/equipment/{eq['slug']}",
            },
        )
        for i, eq in enumerate(EQUIPMENT_CATALOG)
    ]
    blocks.append(
        _block(
            bid,
            "equipment_main_grid",
            "Our Equipment Fleet",
            subtitle="Plant & Machinery",
            short_summary="Browse GCCL construction equipment by category, capacity, and condition.",
            full_content="Select equipment to view specifications, usage, and related project experience.",
            display_order=bid,
            items=grid_items,
            extra={"categories": [c["slug"] for c in EQUIPMENT_CATEGORIES]},
        )
    )
    bid += 1

    gallery = content["gallery"]
    blocks.append(
        _block(
            bid,
            "equipment_fleet_gallery",
            gallery["title"],
            subtitle=gallery["subtitle"],
            short_summary=gallery["short_summary"],
            gallery_images=FLEET_GALLERY_IMAGES,
            display_order=bid,
            extra={
                "gallery_categories": [
                    {"label": "Fleet Overview", "images": FLEET_GALLERY_IMAGES[:4]},
                    {"label": "Site Deployment", "images": FLEET_GALLERY_IMAGES[4:] or FLEET_GALLERY_IMAGES[:2]},
                ]
            },
        )
    )
    bid += 1

    stats = content["statistics"]
    stat_items = [
        _item(
            i + 1,
            stat["label"],
            subtitle=f"{stat['value']}{stat.get('suffix', '')}",
            icon=stat.get("icon", "bi-bar-chart"),
            sort_order=i + 1,
            extra={"value": stat["value"], "suffix": stat.get("suffix", "")},
        )
        for i, stat in enumerate(stats["items"])
    ]
    blocks.append(
        _block(
            bid,
            "equipment_statistics",
            stats["title"],
            subtitle=stats["subtitle"],
            short_summary=stats["short_summary"],
            display_order=bid,
            items=stat_items,
        )
    )
    bid += 1

    safety = content["safety_maintenance"]
    blocks.append(
        _block(
            bid,
            "equipment_safety_maintenance",
            safety["title"],
            subtitle=safety["subtitle"],
            short_summary=safety["short_summary"],
            full_content=safety["full_content"],
            display_order=bid,
        )
    )
    bid += 1

    faq_items = [
        _item(
            i + 1,
            faq["question"],
            full_content=faq["answer"],
            item_key=f"eq-faq-{i + 1}",
            sort_order=i + 1,
        )
        for i, faq in enumerate(content["faq"])
    ]
    blocks.append(
        _block(
            bid,
            "equipment_faq",
            "Frequently Asked Questions",
            subtitle="Equipment & Fleet",
            short_summary="Common questions about GCCL plant, mobilisation, and maintenance.",
            display_order=bid,
            items=faq_items,
        )
    )

    return blocks


def build_equipment_page_sections() -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    sid = _SECTION_ID_START
    order = 1
    slug = "equipment"

    sections.append(
        _section(slug, sid, "hero_banner", "Hero Banner", display_order=order,
                 layout_type="hero-banner", background_style="brand", spacing="none", animation="fade-in")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "equipment_overview", "Equipment Overview",
                 block_key="equipment_page_overview", display_order=order,
                 layout_type="split-columns", background_style="default", animation="fade-up",
                 seo_anchor="equipment-overview")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "equipment_categories", "Equipment Categories",
                 block_key="equipment_categories", display_order=order,
                 layout_type="equipment-categories", background_style="light", animation="stagger",
                 seo_anchor="equipment-categories")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "equipment_grid", "Equipment Fleet",
                 block_key="equipment_main_grid", display_order=order,
                 layout_type="equipment-grid", background_style="default", animation="stagger",
                 seo_anchor="equipment-fleet")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "equipment_gallery", "Equipment Gallery",
                 block_key="equipment_fleet_gallery", display_order=order,
                 layout_type="project-gallery", background_style="muted", animation="fade-up",
                 seo_anchor="equipment-gallery")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "equipment_statistics", "Equipment Statistics",
                 block_key="equipment_statistics", display_order=order,
                 layout_type="stats-row", background_style="dark", animation="fade-up",
                 seo_anchor="equipment-statistics")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "safety_maintenance", "Safety & Maintenance",
                 block_key="equipment_safety_maintenance", display_order=order,
                 layout_type="rich-text", background_style="default", animation="fade-up",
                 seo_anchor="safety-maintenance")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "faq", "Frequently Asked Questions",
                 block_key="equipment_faq", display_order=order,
                 layout_type="faq-accordion", background_style="light", animation="fade-up",
                 seo_anchor="faq")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "call_to_action", "Call To Action",
                 block_key="call_to_action", display_order=order,
                 layout_type="cta-banner", background_style="brand", spacing="relaxed", animation="fade-up",
                 seo_anchor="contact-us")
    )

    return sections


def _slug_key(slug: str) -> str:
    return slug.replace("-", "_")


def build_equipment_detail_blocks(eq: dict[str, Any], block_id_start: int) -> list[dict[str, Any]]:
    sk = _slug_key(eq["slug"])
    bid = block_id_start
    blocks: list[dict[str, Any]] = []

    blocks.append(
        _block(
            bid,
            f"equipment_{sk}_hero",
            eq["name"],
            subtitle=eq["category"],
            short_summary=eq.get("capacity", ""),
            full_content=eq["short_description"],
            hero_image=eq["image"],
            meta_title=eq.get("meta_title", eq["name"]),
            meta_description=eq.get("meta_description", eq["short_description"]),
            extra={
                "condition": eq.get("condition", ""),
                "capacity": eq.get("capacity", ""),
                "maintenance_status": eq.get("maintenance_status", ""),
            },
        )
    )
    bid += 1

    blocks.append(
        _block(
            bid,
            f"equipment_{sk}_gallery",
            "Equipment Gallery",
            subtitle="Plant Photography",
            short_summary="Browse images of this equipment type on GCCL project sites.",
            gallery_images=eq.get("gallery_images", []),
            display_order=bid,
            extra={"gallery_categories": eq.get("gallery_categories", []), "equipment_slug": eq["slug"]},
        )
    )
    bid += 1

    spec_items = [
        _item(i + 1, spec["label"], subtitle=spec["value"], sort_order=i + 1)
        for i, spec in enumerate(eq.get("specifications", []))
    ]
    blocks.append(
        _block(
            bid,
            f"equipment_{sk}_detail",
            "Specifications & Usage",
            subtitle="Technical Overview",
            full_content=eq.get("usage", eq["description"]),
            hero_image=eq["image"],
            display_order=bid,
            items=spec_items,
            extra={
                "capacity": eq.get("capacity", ""),
                "condition": eq.get("condition", ""),
                "maintenance_status": eq.get("maintenance_status", ""),
                "usage": eq.get("usage", ""),
            },
        )
    )
    bid += 1

    blocks.append(
        _block(
            bid,
            f"equipment_{sk}_related",
            "Related Projects & Services",
            subtitle="Connected Capability",
            short_summary="Projects and services where this equipment is typically deployed.",
            display_order=bid,
            extra={
                "related_project_slugs": eq.get("related_project_slugs", []),
                "related_service_slugs": eq.get("related_service_slugs", []),
                "maintenance_status": eq.get("maintenance_status", ""),
            },
        )
    )

    return blocks


def build_equipment_detail_sections(eq: dict[str, Any], section_id_start: int) -> list[dict[str, Any]]:
    sk = _slug_key(eq["slug"])
    page_slug = f"equipment-{eq['slug']}"
    sid = section_id_start
    order = 1
    sections: list[dict[str, Any]] = []

    sections.append(
        _section(page_slug, sid, "hero", "Hero Banner", block_key=f"equipment_{sk}_hero",
                 display_order=order, layout_type="equipment-hero", background_style="image", spacing="none", animation="fade-in")
    )
    sid += 1
    order += 1

    sections.append(
        _section(page_slug, sid, "gallery", "Gallery", block_key=f"equipment_{sk}_gallery",
                 display_order=order, layout_type="project-gallery", background_style="default", animation="fade-up", seo_anchor="gallery")
    )
    sid += 1
    order += 1

    sections.append(
        _section(page_slug, sid, "specifications", "Specifications", block_key=f"equipment_{sk}_detail",
                 display_order=order, layout_type="equipment-detail-overview", background_style="muted", animation="fade-up", seo_anchor="specifications")
    )
    sid += 1
    order += 1

    sections.append(
        _section(page_slug, sid, "related", "Related Projects & Services", block_key=f"equipment_{sk}_related",
                 display_order=order, layout_type="equipment-related", background_style="light", animation="fade-up", seo_anchor="related")
    )
    sid += 1
    order += 1

    sections.append(
        _section(page_slug, sid, "call_to_action", "Call To Action", block_key="call_to_action",
                 display_order=order, layout_type="cta-banner", background_style="brand", spacing="relaxed", animation="fade-up", seo_anchor="contact-us")
    )

    return sections


def build_all_equipment_detail_data() -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    all_blocks: list[dict[str, Any]] = []
    sections_by_slug: dict[str, list[dict[str, Any]]] = {}
    bid = _DETAIL_BLOCK_ID_START
    sid = _DETAIL_SECTION_ID_START

    for eq in EQUIPMENT_CATALOG:
        eq_blocks = build_equipment_detail_blocks(eq, bid)
        all_blocks.extend(eq_blocks)
        bid += len(eq_blocks)

        page_slug = f"equipment-{eq['slug']}"
        eq_sections = build_equipment_detail_sections(eq, sid)
        sections_by_slug[page_slug] = eq_sections
        sid += len(eq_sections)

    return all_blocks, sections_by_slug


EQUIPMENT_PAGE_BLOCKS: list[dict[str, Any]] = build_equipment_page_blocks()
EQUIPMENT_PAGE_SECTIONS: list[dict[str, Any]] = build_equipment_page_sections()
EQUIPMENT_DETAIL_BLOCKS, EQUIPMENT_DETAIL_SECTIONS_BY_SLUG = build_all_equipment_detail_data()
