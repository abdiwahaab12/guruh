"""
Services Page — CMS blocks and Page Builder sections.

Built from app.data.services_catalog (official company profile).
"""

from __future__ import annotations

from typing import Any

from app.data.cms_blocks import SEED_TIMESTAMP
from app.data.services_catalog import (
    PROJECT_CATEGORY_TO_FILTER,
    SERVICES_CATALOG,
    SERVICES_PAGE_CONTENT,
)

_BLOCK_ID_START = 100
_SECTION_ID_START = 100


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
        "page_slug": "services",
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


def build_services_page_blocks() -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    bid = _BLOCK_ID_START
    content = SERVICES_PAGE_CONTENT
    overview = content["overview"]

    blocks.append(
        _block(
            bid,
            "services_overview",
            overview["title"],
            subtitle=overview["subtitle"],
            short_summary=overview["short_summary"],
            full_content=overview["full_content"],
            hero_image=overview["hero_image"],
            display_order=bid,
        )
    )
    bid += 1

    grid_items = [
        _item(
            i + 1,
            svc["title"],
            item_key=svc["slug"],
            short_summary=svc["short_description"],
            full_content=svc["description"],
            image=svc["image"],
            icon=svc["icon"],
            sort_order=i + 1,
            extra={
                "service_slug": svc["slug"],
                "learn_more_url": f"#service-{svc['slug']}",
            },
        )
        for i, svc in enumerate(SERVICES_CATALOG)
    ]
    blocks.append(
        _block(
            bid,
            "services_main_grid",
            "Our Construction Services",
            subtitle="Core Capabilities",
            short_summary="Eight specialist service areas delivered by qualified GCCL teams.",
            full_content="Select a service to view scope, benefits, and related project experience.",
            display_order=bid,
            items=grid_items,
        )
    )
    bid += 1

    for svc in SERVICES_CATALOG:
        blocks.append(
            _block(
                bid,
                f"service_detail_{svc['slug'].replace('-', '_')}",
                svc["title"],
                subtitle="Service Detail",
                short_summary=svc["short_description"],
                full_content=svc["description"],
                hero_image=svc["image"],
                gallery_images=list(svc.get("gallery_images") or []),
                display_order=bid,
                extra={
                    "service_slug": svc["slug"],
                    "scope_of_work": svc["scope_of_work"],
                    "benefits": svc["benefits"],
                    "typical_project_slugs": svc["typical_project_slugs"],
                    "related_equipment": svc["related_equipment"],
                    "project_categories": svc["project_categories"],
                },
            )
        )
        bid += 1

    process_items = [
        _item(
            i + 1,
            step["title"],
            full_content=step["description"],
            icon=step["icon"],
            sort_order=i + 1,
            extra={"step_number": i + 1},
        )
        for i, step in enumerate(content["working_process"])
    ]
    blocks.append(
        _block(
            bid,
            "services_working_process",
            "Our Working Process",
            subtitle="How We Deliver",
            short_summary="A professional, transparent approach from consultation to handover.",
            display_order=bid,
            items=process_items,
        )
    )
    bid += 1

    industry_items = [
        _item(
            i + 1,
            ind["title"],
            short_summary=ind["summary"],
            icon=ind["icon"],
            sort_order=i + 1,
        )
        for i, ind in enumerate(content["industries"])
    ]
    blocks.append(
        _block(
            bid,
            "services_industries",
            "Industries We Serve",
            subtitle="Sectors & Clients",
            short_summary="Construction solutions for diverse public and private sectors.",
            display_order=bid,
            items=industry_items,
        )
    )
    bid += 1

    why_items = [
        _item(
            i + 1,
            w["title"],
            short_summary=w["summary"],
            icon=w["icon"],
            sort_order=i + 1,
        )
        for i, w in enumerate(content["why_choose"])
    ]
    blocks.append(
        _block(
            bid,
            "services_why_choose",
            "Why Choose Our Services",
            subtitle="The GCCL Advantage",
            short_summary="Quality, safety, and reliability on every project.",
            display_order=bid,
            items=why_items,
        )
    )
    bid += 1

    fp = content["featured_projects_intro"]
    filter_items = [
        _item(
            i + 1,
            f["title"],
            item_key=f["item_key"],
            sort_order=i + 1,
            extra=f["extra"],
        )
        for i, f in enumerate(content["project_filters"])
    ]
    blocks.append(
        _block(
            bid,
            "services_featured_projects",
            fp["title"],
            subtitle=fp["subtitle"],
            short_summary=fp["short_summary"],
            full_content=fp["full_content"],
            display_order=bid,
            items=filter_items,
            extra={"category_map": PROJECT_CATEGORY_TO_FILTER},
        )
    )
    bid += 1

    faq_items = [
        _item(
            i + 1,
            faq["question"],
            full_content=faq["answer"],
            item_key=f"faq-{i + 1}",
            sort_order=i + 1,
        )
        for i, faq in enumerate(content["faq"])
    ]
    blocks.append(
        _block(
            bid,
            "services_faq",
            "Frequently Asked Questions",
            subtitle="Common Questions",
            short_summary="Answers to common questions about GCCL construction services.",
            display_order=bid,
            items=faq_items,
        )
    )

    return blocks


def build_services_page_sections() -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    sid = _SECTION_ID_START
    order = 1

    sections.append(
        _section(sid, "hero_banner", "Hero Banner", display_order=order, layout_type="hero-banner", background_style="brand", spacing="none", animation="fade-in")
    )
    sid += 1
    order += 1

    sections.append(
        _section(
            sid,
            "services_overview",
            "Services Overview",
            block_key="services_overview",
            display_order=order,
            layout_type="split-columns",
            background_style="default",
            animation="fade-up",
            seo_anchor="services-overview",
        )
    )
    sid += 1
    order += 1

    sections.append(
        _section(
            sid,
            "services_main_grid",
            "Our Construction Services",
            block_key="services_main_grid",
            display_order=order,
            layout_type="services-grid",
            background_style="light",
            animation="stagger",
            seo_anchor="services-grid",
        )
    )
    sid += 1
    order += 1

    for svc in SERVICES_CATALOG:
        block_key = f"service_detail_{svc['slug'].replace('-', '_')}"
        sections.append(
            _section(
                sid,
                f"service_{svc['slug'].replace('-', '_')}",
                svc["title"],
                block_key=block_key,
                display_order=order,
                layout_type="service-detail",
                background_style="default" if order % 2 else "muted",
                animation="fade-up",
                seo_anchor=f"service-{svc['slug']}",
            )
        )
        sid += 1
        order += 1

    sections.append(
        _section(
            sid,
            "working_process",
            "Our Working Process",
            block_key="services_working_process",
            display_order=order,
            layout_type="process-steps",
            background_style="brand",
            animation="stagger",
            seo_anchor="working-process",
        )
    )
    sid += 1
    order += 1

    sections.append(
        _section(
            sid,
            "industries",
            "Industries We Serve",
            block_key="services_industries",
            display_order=order,
            layout_type="card-grid",
            background_style="light",
            animation="stagger",
            seo_anchor="industries",
        )
    )
    sid += 1
    order += 1

    sections.append(
        _section(
            sid,
            "why_choose_services",
            "Why Choose Our Services",
            block_key="services_why_choose",
            display_order=order,
            layout_type="card-grid",
            background_style="default",
            animation="stagger",
            seo_anchor="why-choose",
        )
    )
    sid += 1
    order += 1

    sections.append(
        _section(
            sid,
            "featured_projects",
            "Featured Projects",
            block_key="services_featured_projects",
            display_order=order,
            layout_type="projects-showcase",
            background_style="muted",
            animation="fade-up",
            seo_anchor="featured-projects",
        )
    )
    sid += 1
    order += 1

    sections.append(
        _section(
            sid,
            "faq",
            "Frequently Asked Questions",
            block_key="services_faq",
            display_order=order,
            layout_type="faq-accordion",
            background_style="light",
            animation="fade-up",
            seo_anchor="faq",
        )
    )
    sid += 1
    order += 1

    sections.append(
        _section(
            sid,
            "call_to_action",
            "Call To Action",
            block_key="call_to_action",
            display_order=order,
            layout_type="cta-banner",
            background_style="brand",
            spacing="relaxed",
            animation="fade-up",
            seo_anchor="contact-us",
        )
    )

    return sections


SERVICES_PAGE_BLOCKS: list[dict[str, Any]] = build_services_page_blocks()
SERVICES_PAGE_SECTIONS: list[dict[str, Any]] = build_services_page_sections()
