"""
Projects Page and project detail pages — CMS blocks and Page Builder sections.

Built from app.data.projects_catalog (official company profile + portfolio).
"""

from __future__ import annotations

from typing import Any

from app.data.cms_blocks import SEED_TIMESTAMP
from app.data.projects_catalog import (
    PROJECTS_CATALOG,
    PROJECTS_PAGE_CONTENT,
    PROJECT_CLIENTS,
    PROJECT_COUNTIES,
    PROJECT_COUNTRIES,
    PROJECT_STATUSES,
    PROJECT_TESTIMONIALS,
    PROJECT_YEARS,
    CATEGORY_TO_SERVICE_SLUG,
)

_BLOCK_ID_START = 200
_SECTION_ID_START = 200
_DETAIL_BLOCK_ID_START = 400
_DETAIL_SECTION_ID_START = 400


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


def build_projects_page_blocks() -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    bid = _BLOCK_ID_START
    content = PROJECTS_PAGE_CONTENT

    overview = content["overview"]
    blocks.append(
        _block(
            bid,
            "projects_overview",
            overview["title"],
            subtitle=overview["subtitle"],
            short_summary=overview["short_summary"],
            full_content=overview["full_content"],
            hero_image=overview["hero_image"],
            display_order=bid,
        )
    )
    bid += 1

    portfolio = content["portfolio"]
    filter_extra = {
        "categories": sorted({p["category"] for p in PROJECTS_CATALOG}),
        "countries": PROJECT_COUNTRIES,
        "counties": PROJECT_COUNTIES + ["Banaadir", "Hodan District"],
        "statuses": PROJECT_STATUSES,
        "years": PROJECT_YEARS,
        "clients": PROJECT_CLIENTS,
        "services": list(CATEGORY_TO_SERVICE_SLUG.values()),
        "service_labels": {v: k for k, v in CATEGORY_TO_SERVICE_SLUG.items()},
    }
    blocks.append(
        _block(
            bid,
            "projects_portfolio",
            portfolio["title"],
            subtitle=portfolio["subtitle"],
            short_summary=portfolio["short_summary"],
            full_content=portfolio["full_content"],
            display_order=bid,
            extra=filter_extra,
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
            "projects_statistics",
            stats["title"],
            subtitle=stats["subtitle"],
            short_summary=stats["short_summary"],
            display_order=bid,
            items=stat_items,
        )
    )
    bid += 1

    areas = content["areas_map"]
    county_items = [
        _item(
            i + 1,
            county,
            item_key=county.lower().replace(" ", "-"),
            icon="bi-geo-alt-fill",
            sort_order=i + 1,
            extra={
                "county_key": county.lower().replace(" ", "-"),
                "project_count": sum(
                    1 for p in PROJECTS_CATALOG if p.get("county") == county and p.get("country", "Kenya") == "Kenya"
                ),
                "country": "Kenya",
            },
        )
        for i, county in enumerate(PROJECT_COUNTIES)
    ]
    county_items.extend(
        _item(
            len(PROJECT_COUNTIES) + i + 1,
            region,
            item_key=region.lower().replace(" ", "-"),
            icon="bi-geo-alt-fill",
            sort_order=len(PROJECT_COUNTIES) + i + 1,
            extra={
                "county_key": region.lower().replace(" ", "-"),
                "project_count": sum(
                    1 for p in PROJECTS_CATALOG if p.get("county") == region and p.get("country") == "Somalia"
                ),
                "country": "Somalia",
            },
        )
        for i, region in enumerate(["Banaadir", "Hodan District"])
    )
    blocks.append(
        _block(
            bid,
            "projects_areas_map",
            areas["title"],
            subtitle=areas["subtitle"],
            short_summary=areas["short_summary"],
            full_content=areas["full_content"],
            display_order=bid,
            items=county_items,
            extra={
                "map_ready": True,
                "map_provider": "future-multi-region-map",
                "founded_country": "Kenya",
                "operating_country": "Somalia",
            },
        )
    )
    bid += 1

    testimonials = content["testimonials"]
    testimonial_items = [
        _item(
            t["id"],
            t["client_name"],
            subtitle=t["client_title"],
            short_summary=t["company"],
            full_content=t["content"],
            sort_order=t["id"],
            extra={
                "rating": t.get("rating", 5),
                "project_slug": t.get("project_slug", ""),
            },
        )
        for t in PROJECT_TESTIMONIALS
    ]
    blocks.append(
        _block(
            bid,
            "projects_testimonials",
            testimonials["title"],
            subtitle=testimonials["subtitle"],
            short_summary=testimonials["short_summary"],
            display_order=bid,
            items=testimonial_items,
        )
    )

    return blocks


def build_projects_page_sections() -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    sid = _SECTION_ID_START
    order = 1
    slug = "projects"

    sections.append(
        _section(slug, sid, "hero_banner", "Hero Banner", display_order=order, layout_type="hero-banner", background_style="brand", spacing="none", animation="fade-in")
    )
    sid += 1
    order += 1

    sections.append(
        _section(
            slug, sid, "projects_overview", "Projects Overview",
            block_key="projects_overview", display_order=order,
            layout_type="split-columns", background_style="default", animation="fade-up",
            seo_anchor="projects-overview",
        )
    )
    sid += 1
    order += 1

    sections.append(
        _section(
            slug, sid, "projects_portfolio", "Project Portfolio",
            block_key="projects_portfolio", display_order=order,
            layout_type="projects-portfolio", background_style="light", animation="stagger",
            seo_anchor="project-portfolio",
        )
    )
    sid += 1
    order += 1

    sections.append(
        _section(
            slug, sid, "projects_statistics", "Project Statistics",
            block_key="projects_statistics", display_order=order,
            layout_type="stats-row", background_style="dark", animation="fade-up",
            seo_anchor="project-statistics",
        )
    )
    sid += 1
    order += 1

    sections.append(
        _section(
            slug, sid, "areas_of_operation", "Areas of Operation",
            block_key="projects_areas_map", display_order=order,
            layout_type="areas-map", background_style="default", animation="fade-up",
            seo_anchor="areas-of-operation",
        )
    )
    sid += 1
    order += 1

    sections.append(
        _section(
            slug, sid, "project_testimonials", "Client Testimonials",
            block_key="projects_testimonials", display_order=order,
            layout_type="testimonials-grid", background_style="muted", animation="stagger",
            seo_anchor="testimonials",
        )
    )
    sid += 1
    order += 1

    sections.append(
        _section(
            slug, sid, "call_to_action", "Call To Action",
            block_key="call_to_action", display_order=order,
            layout_type="cta-banner", background_style="brand", spacing="relaxed", animation="fade-up",
            seo_anchor="contact-us",
        )
    )

    return sections


def _slug_key(slug: str) -> str:
    return slug.replace("-", "_")


def build_project_detail_blocks(proj: dict[str, Any], block_id_start: int) -> list[dict[str, Any]]:
    sk = _slug_key(proj["slug"])
    bid = block_id_start
    blocks: list[dict[str, Any]] = []

    blocks.append(
        _block(
            bid,
            f"project_{sk}_hero",
            proj["title"],
            subtitle=proj["category"],
            short_summary=proj["location"],
            full_content=proj["description"],
            hero_image=proj["cover_image"],
            meta_title=proj.get("meta_title", proj["title"]),
            meta_description=proj.get("meta_description", proj["description"]),
            extra={
                "status": proj.get("status", ""),
                "client": proj.get("client", ""),
                "county": proj.get("county", ""),
                "completion_year": proj.get("completion_year", ""),
            },
        )
    )
    bid += 1

    gallery_cats = proj.get("gallery_categories") or []
    all_images = proj.get("gallery_images") or []
    blocks.append(
        _block(
            bid,
            f"project_{sk}_gallery",
            "Project Gallery",
            subtitle="Site Photography",
            short_summary="Browse project images by category.",
            gallery_images=all_images,
            display_order=bid,
            extra={"gallery_categories": gallery_cats, "project_slug": proj["slug"]},
        )
    )
    bid += 1

    blocks.append(
        _block(
            bid,
            f"project_{sk}_overview",
            "Project Overview",
            subtitle="Delivery Summary",
            full_content=proj.get("overview", proj["description"]),
            hero_image=proj["cover_image"],
            display_order=bid,
            extra={
                "client": proj.get("client", ""),
                "consultant": proj.get("consultant", ""),
                "location": proj.get("location", ""),
                "county": proj.get("county", ""),
                "duration": proj.get("duration", ""),
                "completion_date": proj.get("completion_date", ""),
                "status": proj.get("status", ""),
                "category": proj.get("category", ""),
            },
        )
    )
    bid += 1

    scope_items = [_item(i + 1, line, sort_order=i + 1) for i, line in enumerate(proj.get("scope_of_work", []))]
    blocks.append(
        _block(
            bid,
            f"project_{sk}_scope",
            "Scope of Work",
            subtitle="Deliverables",
            short_summary="Key works executed under this contract.",
            display_order=bid,
            items=scope_items,
        )
    )
    bid += 1

    challenge_items = [_item(i + 1, line, sort_order=i + 1, icon="bi-exclamation-triangle") for i, line in enumerate(proj.get("challenges", []))]
    solution_items = [_item(i + 1, line, sort_order=i + 1, icon="bi-check-circle-fill") for i, line in enumerate(proj.get("solutions", []))]
    blocks.append(
        _block(
            bid,
            f"project_{sk}_challenges",
            "Challenges & Solutions",
            subtitle="Problem Solving",
            short_summary="How GCCL addressed site and delivery challenges.",
            display_order=bid,
            items=challenge_items,
            extra={"solutions": solution_items},
        )
    )
    bid += 1

    equip_items = [_item(i + 1, eq, sort_order=i + 1) for i, eq in enumerate(proj.get("equipment_used", []))]
    blocks.append(
        _block(
            bid,
            f"project_{sk}_equipment",
            "Equipment Used",
            subtitle="Plant & Machinery",
            short_summary="Heavy equipment deployed on this project.",
            display_order=bid,
            items=equip_items,
        )
    )
    bid += 1

    blocks.append(
        _block(
            bid,
            f"project_{sk}_related",
            "Related Services & Projects",
            subtitle="Explore Further",
            short_summary="Connected capabilities and portfolio projects.",
            display_order=bid,
            extra={
                "service_slugs": proj.get("service_slugs", []),
                "related_project_slugs": proj.get("related_project_slugs", []),
            },
        )
    )

    return blocks


def build_project_detail_sections(proj: dict[str, Any], section_id_start: int) -> list[dict[str, Any]]:
    sk = _slug_key(proj["slug"])
    page_slug = f"project-{proj['slug']}"
    sid = section_id_start
    order = 1
    sections: list[dict[str, Any]] = []

    sections.append(
        _section(page_slug, sid, "hero", "Hero Banner", block_key=f"project_{sk}_hero",
                 display_order=order, layout_type="project-hero", background_style="image", spacing="none", animation="fade-in")
    )
    sid += 1
    order += 1

    sections.append(
        _section(page_slug, sid, "gallery", "Project Gallery", block_key=f"project_{sk}_gallery",
                 display_order=order, layout_type="project-gallery", background_style="default", animation="fade-up", seo_anchor="gallery")
    )
    sid += 1
    order += 1

    sections.append(
        _section(page_slug, sid, "overview", "Project Overview", block_key=f"project_{sk}_overview",
                 display_order=order, layout_type="project-detail-overview", background_style="muted", animation="fade-up", seo_anchor="overview")
    )
    sid += 1
    order += 1

    sections.append(
        _section(page_slug, sid, "scope", "Scope of Work", block_key=f"project_{sk}_scope",
                 display_order=order, layout_type="feature-list", background_style="default", animation="fade-up", seo_anchor="scope-of-work")
    )
    sid += 1
    order += 1

    sections.append(
        _section(page_slug, sid, "challenges", "Challenges & Solutions", block_key=f"project_{sk}_challenges",
                 display_order=order, layout_type="project-challenges", background_style="light", animation="fade-up", seo_anchor="challenges")
    )
    sid += 1
    order += 1

    sections.append(
        _section(page_slug, sid, "equipment", "Equipment Used", block_key=f"project_{sk}_equipment",
                 display_order=order, layout_type="card-grid", background_style="default", animation="stagger", seo_anchor="equipment")
    )
    sid += 1
    order += 1

    sections.append(
        _section(page_slug, sid, "related", "Related Services & Projects", block_key=f"project_{sk}_related",
                 display_order=order, layout_type="project-related", background_style="muted", animation="fade-up", seo_anchor="related")
    )
    sid += 1
    order += 1

    sections.append(
        _section(page_slug, sid, "call_to_action", "Call To Action", block_key="call_to_action",
                 display_order=order, layout_type="cta-banner", background_style="brand", spacing="relaxed", animation="fade-up", seo_anchor="contact-us")
    )

    return sections


def build_all_project_detail_data() -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    all_blocks: list[dict[str, Any]] = []
    sections_by_slug: dict[str, list[dict[str, Any]]] = {}
    bid = _DETAIL_BLOCK_ID_START
    sid = _DETAIL_SECTION_ID_START

    for proj in PROJECTS_CATALOG:
        proj_blocks = build_project_detail_blocks(proj, bid)
        all_blocks.extend(proj_blocks)
        bid += len(proj_blocks)

        page_slug = f"project-{proj['slug']}"
        proj_sections = build_project_detail_sections(proj, sid)
        sections_by_slug[page_slug] = proj_sections
        sid += len(proj_sections)

    return all_blocks, sections_by_slug


PROJECTS_PAGE_BLOCKS: list[dict[str, Any]] = build_projects_page_blocks()
PROJECTS_PAGE_SECTIONS: list[dict[str, Any]] = build_projects_page_sections()
PROJECT_DETAIL_BLOCKS, PROJECT_DETAIL_SECTIONS_BY_SLUG = build_all_project_detail_data()
