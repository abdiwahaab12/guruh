"""
Team & Leadership Page — CMS blocks and Page Builder sections.

Built from app.data.team_catalog.
"""

from __future__ import annotations

from typing import Any

from app.data.cms_blocks import SEED_TIMESTAMP
from app.data.team_catalog import (
    ORG_CHART_NODES,
    TEAM_BY_TYPE,
    TEAM_PAGE_CONTENT,
)

_BLOCK_ID_START = 1100
_SECTION_ID_START = 1100


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
    display_order: int = 0,
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
        "gallery_images": [],
        "display_order": display_order,
        "is_active": True,
        "meta_title": title,
        "meta_description": short_summary,
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
        "extra": {},
        "created_at": SEED_TIMESTAMP,
        "updated_at": SEED_TIMESTAMP,
    }


def _team_member_item(member: dict, item_id: int) -> dict[str, Any]:
    return _item(
        item_id,
        member["name"],
        item_key=member.get("slug", f"member-{item_id}"),
        subtitle=member["position"],
        short_summary=member.get("department", ""),
        full_content=member.get("bio", ""),
        image=member.get("photo", ""),
        icon="bi-person-badge",
        sort_order=member.get("sort_order", item_id),
        extra={
            "department": member.get("department", ""),
            "years_experience": str(member.get("years_experience", "")),
            "education": member.get("education", ""),
            "experience_summary": member.get("experience_summary", ""),
            "social_links": member.get("social_links", []),
            "member_type": member.get("member_type", ""),
            "email": member.get("email", ""),
        },
    )


def build_team_page_blocks() -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    bid = _BLOCK_ID_START
    content = TEAM_PAGE_CONTENT

    intro = content["introduction"]
    blocks.append(
        _block(
            bid,
            "team_leadership_intro",
            intro["title"],
            subtitle=intro["subtitle"],
            short_summary=intro["short_summary"],
            full_content=intro["full_content"],
            hero_image=intro["hero_image"],
            display_order=bid,
        )
    )
    bid += 1

    director_items = [_team_member_item(m, i + 1) for i, m in enumerate(TEAM_BY_TYPE["director"])]
    blocks.append(
        _block(
            bid,
            "team_board_directors",
            "Board of Directors",
            subtitle="Strategic Leadership",
            short_summary="The co-founders and directors guiding GURUH Construction's vision and delivery.",
            display_order=bid,
            items=director_items,
            extra={"leadership_tier": "director"},
        )
    )
    bid += 1

    executive_items = [_team_member_item(m, i + 1) for i, m in enumerate(TEAM_BY_TYPE["executive"])]
    blocks.append(
        _block(
            bid,
            "team_executive_management",
            "Executive Management",
            subtitle="Senior Leadership",
            short_summary="Department heads and senior managers overseeing project delivery and corporate support.",
            display_order=bid,
            items=executive_items,
            extra={"leadership_tier": "executive"},
        )
    )
    bid += 1

    org = content["org_chart"]
    org_items = [
        _item(
            i + 1,
            node["title"],
            item_key=node["id"],
            subtitle=node.get("subtitle", ""),
            sort_order=i + 1,
            extra={
                "node_id": node["id"],
                "parent_id": node.get("parent_id", ""),
                "level": node.get("level", 0),
            },
        )
        for i, node in enumerate(ORG_CHART_NODES)
    ]
    blocks.append(
        _block(
            bid,
            "team_org_structure",
            org["title"],
            subtitle=org["subtitle"],
            short_summary=org["short_summary"],
            display_order=bid,
            items=org_items,
            extra={"chart_ready": True, "chart_provider": "future-dynamic-org-chart"},
        )
    )
    bid += 1

    staff_items = [_team_member_item(m, i + 1) for i, m in enumerate(TEAM_BY_TYPE["staff"])]
    blocks.append(
        _block(
            bid,
            "team_meet_our_team",
            "Meet Our Team",
            subtitle="The People Behind GCCL",
            short_summary="Engineers, supervisors, and professionals delivering projects across Kenya.",
            display_order=bid,
            items=staff_items,
        )
    )
    bid += 1

    culture = content["culture"]
    culture_items = [
        _item(
            i + 1,
            val["title"],
            short_summary=val["summary"],
            icon=val["icon"],
            sort_order=i + 1,
        )
        for i, val in enumerate(culture["items"])
    ]
    blocks.append(
        _block(
            bid,
            "team_company_culture",
            culture["title"],
            subtitle=culture["subtitle"],
            short_summary=culture["short_summary"],
            display_order=bid,
            items=culture_items,
        )
    )
    bid += 1

    expertise = content["expertise"]
    stat_items = [
        _item(
            i + 1,
            stat["label"],
            subtitle=f"{stat['value']}{stat.get('suffix', '')}",
            icon=stat.get("icon", "bi-bar-chart"),
            sort_order=i + 1,
            extra={"value": stat["value"], "suffix": stat.get("suffix", "")},
        )
        for i, stat in enumerate(expertise["items"])
    ]
    blocks.append(
        _block(
            bid,
            "team_expertise_stats",
            expertise["title"],
            subtitle=expertise["subtitle"],
            short_summary=expertise["short_summary"],
            display_order=bid,
            items=stat_items,
        )
    )
    bid += 1

    join = content["join_team"]
    blocks.append(
        _block(
            bid,
            "team_join_careers",
            join["title"],
            subtitle=join["subtitle"],
            short_summary=join["short_summary"],
            full_content=join["full_content"],
            display_order=bid,
            extra={
                "button_text": "View Open Positions",
                "button_url": "/careers",
                "secondary_button_text": "Contact HR",
                "secondary_button_url": "/contact",
            },
        )
    )

    return blocks


def build_team_page_sections() -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    sid = _SECTION_ID_START
    order = 1
    slug = "team"

    sections.append(
        _section(slug, sid, "hero_banner", "Hero Banner", display_order=order,
                 layout_type="hero-banner", background_style="brand", spacing="none", animation="fade-in")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "leadership_intro", "Leadership Introduction",
                 block_key="team_leadership_intro", display_order=order,
                 layout_type="split-columns", background_style="default", animation="fade-up",
                 seo_anchor="leadership-introduction")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "board_directors", "Board of Directors",
                 block_key="team_board_directors", display_order=order,
                 layout_type="team-leadership", background_style="light", animation="stagger",
                 seo_anchor="board-of-directors")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "executive_management", "Executive Management",
                 block_key="team_executive_management", display_order=order,
                 layout_type="team-leadership", background_style="default", animation="stagger",
                 seo_anchor="executive-management")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "org_structure", "Organization Structure",
                 block_key="team_org_structure", display_order=order,
                 layout_type="org-chart", background_style="muted", animation="fade-up",
                 seo_anchor="organization-structure")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "meet_our_team", "Meet Our Team",
                 block_key="team_meet_our_team", display_order=order,
                 layout_type="team-staff-grid", background_style="default", animation="stagger",
                 seo_anchor="meet-our-team")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "company_culture", "Company Culture",
                 block_key="team_company_culture", display_order=order,
                 layout_type="card-grid", background_style="brand", animation="stagger",
                 seo_anchor="company-culture")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "team_expertise", "Our Expertise",
                 block_key="team_expertise_stats", display_order=order,
                 layout_type="stats-row", background_style="dark", animation="fade-up",
                 seo_anchor="our-expertise")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "join_our_team", "Join Our Team",
                 block_key="team_join_careers", display_order=order,
                 layout_type="join-team", background_style="light", animation="fade-up",
                 seo_anchor="join-our-team")
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


TEAM_PAGE_BLOCKS: list[dict[str, Any]] = build_team_page_blocks()
TEAM_PAGE_SECTIONS: list[dict[str, Any]] = build_team_page_sections()
