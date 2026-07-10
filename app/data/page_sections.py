"""
Page Builder seed data — section compositions per public page.

Defines which CMS blocks appear on each page and in what order.
Templates consume resolved PageCompositionDTO — never import this module directly.
"""

from __future__ import annotations

from typing import Any

SEED_TIMESTAMP = "2026-07-08T00:00:00Z"


def _section(
    section_id: int,
    page_slug: str,
    section_key: str,
    section_title: str,
    *,
    block_key: str = "",
    display_order: int = 0,
    layout_type: str = "default",
    background_style: str = "default",
    spacing: str = "default",
    animation: str = "none",
    is_visible: bool = True,
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
        "is_visible": is_visible,
        "seo_anchor": anchor,
        "is_active": True,
        "extra": extra or {},
        "created_at": SEED_TIMESTAMP,
        "updated_at": SEED_TIMESTAMP,
    }


ABOUT_PAGE_SECTIONS: list[dict[str, Any]] = [
    _section(
        1,
        "about",
        "hero_banner",
        "Hero Banner",
        display_order=1,
        layout_type="hero-banner",
        background_style="brand",
        spacing="none",
        animation="fade-in",
    ),
    _section(
        2,
        "about",
        "company_overview",
        "Company Overview",
        block_key="company_overview",
        display_order=2,
        layout_type="split-columns",
        background_style="default",
        animation="fade-up",
        seo_anchor="company-overview",
    ),
    _section(
        3,
        "about",
        "company_story",
        "Company Story",
        block_key="company_introduction",
        display_order=3,
        layout_type="rich-text",
        background_style="light",
        animation="fade-up",
        seo_anchor="company-story",
    ),
    _section(
        4,
        "about",
        "directors_message",
        "Directors' Message",
        block_key="directors_message",
        display_order=4,
        layout_type="two-column",
        background_style="default",
        animation="fade-up",
        seo_anchor="directors-message",
    ),
    _section(
        5,
        "about",
        "vision_mission",
        "Vision & Mission",
        block_key="vision",
        display_order=5,
        layout_type="split-columns",
        background_style="brand",
        animation="stagger",
        seo_anchor="vision-mission",
        extra={"block_keys": ["vision", "mission"]},
    ),
    _section(
        6,
        "about",
        "core_values",
        "Core Values",
        block_key="core_values",
        display_order=6,
        layout_type="card-grid",
        background_style="light",
        animation="stagger",
        seo_anchor="core-values",
    ),
    _section(
        7,
        "about",
        "company_history",
        "Company History Timeline",
        block_key="company_history",
        display_order=7,
        layout_type="timeline",
        background_style="default",
        animation="fade-up",
        seo_anchor="company-history",
    ),
    _section(
        8,
        "about",
        "company_strengths",
        "Company Strengths",
        block_key="company_strengths",
        display_order=8,
        layout_type="feature-list",
        background_style="muted",
        animation="stagger",
        seo_anchor="company-strengths",
    ),
    _section(
        9,
        "about",
        "why_choose_guruh",
        "Why Choose GURUH",
        block_key="why_choose_guruh",
        display_order=9,
        layout_type="rich-text",
        background_style="default",
        animation="fade-up",
        seo_anchor="why-choose-guruh",
    ),
    _section(
        10,
        "about",
        "hse_policy",
        "Health, Safety & Environmental Policy",
        block_key="hse_policy",
        display_order=10,
        layout_type="feature-list",
        background_style="light",
        animation="fade-up",
        seo_anchor="hse-policy",
    ),
    _section(
        11,
        "about",
        "certifications",
        "Certifications & Registrations",
        block_key="certifications_registrations",
        display_order=11,
        layout_type="card-grid",
        background_style="default",
        animation="stagger",
        seo_anchor="certifications",
    ),
    _section(
        12,
        "about",
        "equipment_overview",
        "Equipment Overview",
        block_key="equipment_overview",
        display_order=12,
        layout_type="card-grid",
        background_style="muted",
        animation="stagger",
        seo_anchor="equipment",
    ),
    _section(
        13,
        "about",
        "company_statistics",
        "Company Statistics",
        block_key="company_statistics",
        display_order=13,
        layout_type="stats-row",
        background_style="brand",
        spacing="compact",
        animation="fade-up",
        seo_anchor="statistics",
    ),
    _section(
        14,
        "about",
        "leadership_team",
        "Leadership Team",
        block_key="leadership_team",
        display_order=14,
        layout_type="team-grid",
        background_style="default",
        animation="stagger",
        seo_anchor="leadership",
    ),
    _section(
        15,
        "about",
        "areas_of_operation",
        "Areas of Operation",
        block_key="areas_of_operation",
        display_order=15,
        layout_type="card-grid",
        background_style="light",
        animation="fade-up",
        seo_anchor="areas-of-operation",
    ),
    _section(
        16,
        "about",
        "partners",
        "Partners",
        block_key="partners",
        display_order=16,
        layout_type="logo-grid",
        background_style="default",
        animation="fade-in",
        seo_anchor="partners",
    ),
    _section(
        17,
        "about",
        "call_to_action",
        "Call To Action",
        block_key="call_to_action",
        display_order=17,
        layout_type="cta-banner",
        background_style="brand",
        spacing="relaxed",
        animation="fade-up",
        seo_anchor="contact-us",
    ),
]

PAGE_SECTIONS_BY_SLUG: dict[str, list[dict[str, Any]]] = {
    "about": ABOUT_PAGE_SECTIONS,
}

from app.data.services_page import SERVICES_PAGE_SECTIONS
from app.data.projects_page import PROJECTS_PAGE_SECTIONS, PROJECT_DETAIL_SECTIONS_BY_SLUG
from app.data.equipment_page import EQUIPMENT_PAGE_SECTIONS, EQUIPMENT_DETAIL_SECTIONS_BY_SLUG
from app.data.team_page import TEAM_PAGE_SECTIONS
from app.data.contact_page import CONTACT_PAGE_SECTIONS
from app.data.quote_page import QUOTE_PAGE_SECTIONS
from app.data.careers_page import CAREERS_PAGE_SECTIONS, CAREER_DETAIL_SECTIONS_BY_SLUG
from app.data.gallery_page import GALLERY_PAGE_SECTIONS

PAGE_SECTIONS_BY_SLUG["services"] = SERVICES_PAGE_SECTIONS
PAGE_SECTIONS_BY_SLUG["projects"] = PROJECTS_PAGE_SECTIONS
PAGE_SECTIONS_BY_SLUG["equipment"] = EQUIPMENT_PAGE_SECTIONS
PAGE_SECTIONS_BY_SLUG["team"] = TEAM_PAGE_SECTIONS
PAGE_SECTIONS_BY_SLUG["contact"] = CONTACT_PAGE_SECTIONS
PAGE_SECTIONS_BY_SLUG["request-quote"] = QUOTE_PAGE_SECTIONS
PAGE_SECTIONS_BY_SLUG["careers"] = CAREERS_PAGE_SECTIONS
PAGE_SECTIONS_BY_SLUG["gallery"] = GALLERY_PAGE_SECTIONS
PAGE_SECTIONS_BY_SLUG.update(PROJECT_DETAIL_SECTIONS_BY_SLUG)
PAGE_SECTIONS_BY_SLUG.update(EQUIPMENT_DETAIL_SECTIONS_BY_SLUG)
PAGE_SECTIONS_BY_SLUG.update(CAREER_DETAIL_SECTIONS_BY_SLUG)
ALL_PAGE_SECTIONS: list[dict[str, Any]] = (
    ABOUT_PAGE_SECTIONS + SERVICES_PAGE_SECTIONS + PROJECTS_PAGE_SECTIONS
    + EQUIPMENT_PAGE_SECTIONS + TEAM_PAGE_SECTIONS
    + CONTACT_PAGE_SECTIONS + QUOTE_PAGE_SECTIONS + CAREERS_PAGE_SECTIONS
    + GALLERY_PAGE_SECTIONS
)
