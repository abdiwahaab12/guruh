"""
Request Quote Page — CMS blocks and Page Builder sections.

Built from app.data.quote_catalog.
"""

from __future__ import annotations

from typing import Any

from app.data.cms_blocks import SEED_TIMESTAMP
from app.data.quote_catalog import (
    QUOTE_FAQ,
    QUOTE_FORM_FIELDS,
    QUOTE_FORM_STEPS,
    QUOTE_PAGE_CONTENT,
    QUOTE_TESTIMONIALS,
    WHY_REQUEST_QUOTE_ITEMS,
)

_BLOCK_ID_START = 1300
_SECTION_ID_START = 1300


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


def build_quote_page_blocks() -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    bid = _BLOCK_ID_START
    content = QUOTE_PAGE_CONTENT

    intro = content["introduction"]
    blocks.append(
        _block(
            bid,
            "quote_introduction",
            intro["title"],
            subtitle=intro["subtitle"],
            short_summary=intro["short_summary"],
            full_content=intro["full_content"],
            hero_image=intro["hero_image"],
            display_order=bid,
        )
    )
    bid += 1

    why = content["why_request"]
    why_items = [
        _item(
            i + 1,
            item["title"],
            full_content=item["summary"],
            icon=item["icon"],
            sort_order=i + 1,
        )
        for i, item in enumerate(WHY_REQUEST_QUOTE_ITEMS)
    ]
    blocks.append(
        _block(
            bid,
            "quote_why_request",
            why["title"],
            subtitle=why["subtitle"],
            short_summary=why["short_summary"],
            full_content=why["full_content"],
            display_order=bid,
            items=why_items,
        )
    )
    bid += 1

    form = content["form"]
    blocks.append(
        _block(
            bid,
            "quote_form_block",
            form["title"],
            subtitle=form["subtitle"],
            short_summary=form["short_summary"],
            display_order=bid,
            extra={
                "submit_label": form["submit_label"],
                "success_message": form["success_message"],
                "action_url": form["action_url"],
                "form_id": "quote-form",
                "autosave_key": form["autosave_key"],
                "multistep": True,
                "steps": QUOTE_FORM_STEPS,
                "fields": QUOTE_FORM_FIELDS,
            },
        )
    )
    bid += 1

    faq_meta = content["faq"]
    faq_items = [
        _item(
            i + 1,
            faq["question"],
            full_content=faq["answer"],
            short_summary=faq["answer"],
            sort_order=i + 1,
        )
        for i, faq in enumerate(QUOTE_FAQ)
    ]
    blocks.append(
        _block(
            bid,
            "quote_faq",
            faq_meta["title"],
            subtitle=faq_meta["subtitle"],
            short_summary=faq_meta["short_summary"],
            display_order=bid,
            items=faq_items,
        )
    )
    bid += 1

    testimonials_meta = content["testimonials"]
    testimonial_items = [
        _item(
            i + 1,
            t["name"],
            subtitle=t["role"],
            full_content=t["quote"],
            short_summary=t["quote"],
            sort_order=i + 1,
            extra={"rating": t.get("rating", 5)},
        )
        for i, t in enumerate(QUOTE_TESTIMONIALS)
    ]
    blocks.append(
        _block(
            bid,
            "quote_testimonials",
            testimonials_meta["title"],
            subtitle=testimonials_meta["subtitle"],
            short_summary=testimonials_meta["short_summary"],
            display_order=bid,
            items=testimonial_items,
        )
    )

    return blocks


def build_quote_page_sections() -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    sid = _SECTION_ID_START
    order = 1
    slug = "request-quote"

    sections.append(
        _section(slug, sid, "hero_banner", "Hero Banner", display_order=order,
                 layout_type="hero-banner", background_style="brand", spacing="none", animation="fade-in")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "quote_intro", "Quote Introduction",
                 block_key="quote_introduction", display_order=order,
                 layout_type="split-columns", background_style="default", animation="fade-up",
                 seo_anchor="quote-introduction")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "why_request_quote", "Why Request a Quote",
                 block_key="quote_why_request", display_order=order,
                 layout_type="feature-list", background_style="muted", animation="fade-up",
                 seo_anchor="why-request-quote")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "quote_form", "Multi-Step Quote Form",
                 block_key="quote_form_block", display_order=order,
                 layout_type="quote-multistep-form", background_style="light", animation="fade-up",
                 seo_anchor="quote-form")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "faq", "Frequently Asked Questions",
                 block_key="quote_faq", display_order=order,
                 layout_type="faq-accordion", background_style="default", animation="fade-up",
                 seo_anchor="quote-faq")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "testimonials", "Testimonials",
                 block_key="quote_testimonials", display_order=order,
                 layout_type="testimonials-grid", background_style="muted", animation="fade-up",
                 seo_anchor="quote-testimonials")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "call_to_action", "Call To Action",
                 block_key="call_to_action", display_order=order,
                 layout_type="cta-banner", background_style="brand", spacing="relaxed", animation="fade-up",
                 seo_anchor="quote-cta")
    )

    return sections


QUOTE_PAGE_BLOCKS: list[dict[str, Any]] = build_quote_page_blocks()
QUOTE_PAGE_SECTIONS: list[dict[str, Any]] = build_quote_page_sections()
