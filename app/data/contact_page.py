"""
Contact Page — CMS blocks and Page Builder sections.

Built from app.data.contact_catalog.
"""

from __future__ import annotations

from typing import Any

from app.data.cms_blocks import SEED_TIMESTAMP
from app.data.contact_catalog import (
    CONTACT_FORM_FIELDS,
    CONTACT_PAGE_CONTENT,
    DEPARTMENT_CONTACTS,
)
from app.providers.profile_loader import phone_to_tel

_BLOCK_ID_START = 1200
_SECTION_ID_START = 1200


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


def build_contact_page_blocks() -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    bid = _BLOCK_ID_START
    content = CONTACT_PAGE_CONTENT

    intro = content["introduction"]
    blocks.append(
        _block(
            bid,
            "contact_introduction",
            intro["title"],
            subtitle=intro["subtitle"],
            short_summary=intro["short_summary"],
            full_content=intro["full_content"],
            hero_image=intro["hero_image"],
            display_order=bid,
        )
    )
    bid += 1

    office = content["office"]
    blocks.append(
        _block(
            bid,
            "contact_office_info",
            "Office Information",
            subtitle=office.get("address_locality", "Head Office"),
            short_summary=f"Visit, call, or email our head office in {office.get('address_locality', 'Mogadishu')}.",
            display_order=bid,
            extra={
                "office_name": office["name"],
                "address": office["address"],
                "postal_address": office["postal_address"],
                "phone_primary": office["phone_primary"],
                "phone_secondary": office.get("phone_secondary", ""),
                "phone_tel": phone_to_tel(office["phone_primary"]),
                "email": office["email"],
                "office_hours": office["office_hours"],
            },
        )
    )
    bid += 1

    map_data = content["map"]
    blocks.append(
        _block(
            bid,
            "contact_google_map",
            map_data["title"],
            subtitle=map_data["subtitle"],
            short_summary=map_data["short_summary"],
            display_order=bid,
            extra={
                "latitude": map_data["latitude"],
                "longitude": map_data["longitude"],
                "zoom": map_data["zoom"],
                "embed_url": map_data["embed_url"],
                "map_provider": map_data["map_provider"],
                "map_ready": map_data["map_ready"],
            },
        )
    )
    bid += 1

    form = content["form"]
    blocks.append(
        _block(
            bid,
            "contact_form_block",
            form["title"],
            subtitle=form["subtitle"],
            short_summary=form["short_summary"],
            display_order=bid,
            extra={
                "submit_label": form["submit_label"],
                "success_message": form["success_message"],
                "action_url": form["action_url"],
                "form_id": "contact-form",
                "fields": CONTACT_FORM_FIELDS,
            },
        )
    )
    bid += 1

    dept_meta = content["departments"]
    dept_items = [
        _item(
            i + 1,
            dept["name"],
            item_key=dept["id"],
            subtitle=dept.get("contact_person", ""),
            short_summary=dept.get("description", ""),
            icon=dept.get("icon", "bi-building"),
            sort_order=dept.get("sort_order", i + 1),
            extra={
                "phone": dept.get("phone", ""),
                "phone_tel": phone_to_tel(dept.get("phone", "")),
                "email": dept.get("email", ""),
                "contact_person": dept.get("contact_person", ""),
            },
        )
        for i, dept in enumerate(DEPARTMENT_CONTACTS)
    ]
    blocks.append(
        _block(
            bid,
            "contact_departments",
            dept_meta["title"],
            subtitle=dept_meta["subtitle"],
            short_summary=dept_meta["short_summary"],
            display_order=bid,
            items=dept_items,
        )
    )
    bid += 1

    emergency = content["emergency"]
    blocks.append(
        _block(
            bid,
            "contact_emergency",
            emergency["title"],
            subtitle=emergency["subtitle"],
            short_summary=emergency["description"],
            display_order=bid,
            extra={
                "phone": emergency["phone"],
                "phone_tel": phone_to_tel(emergency["phone"]),
                "availability": emergency["availability"],
                "icon": emergency["icon"],
            },
        )
    )
    bid += 1

    social = content["social"]
    blocks.append(
        _block(
            bid,
            "contact_social_media",
            social["title"],
            subtitle=social["subtitle"],
            short_summary=social["short_summary"],
            display_order=bid,
            extra={"use_site_social_links": True},
        )
    )

    return blocks


def build_contact_page_sections() -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    sid = _SECTION_ID_START
    order = 1
    slug = "contact"

    sections.append(
        _section(slug, sid, "hero_banner", "Hero Banner", display_order=order,
                 layout_type="hero-banner", background_style="brand", spacing="none", animation="fade-in")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "contact_intro", "Contact Introduction",
                 block_key="contact_introduction", display_order=order,
                 layout_type="split-columns", background_style="default", animation="fade-up",
                 seo_anchor="contact-introduction")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "office_information", "Office Information",
                 block_key="contact_office_info", display_order=order,
                 layout_type="contact-office-info", background_style="light", animation="fade-up",
                 seo_anchor="office-information")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "google_maps", "Google Maps",
                 block_key="contact_google_map", display_order=order,
                 layout_type="google-maps", background_style="default", animation="fade-up",
                 seo_anchor="find-us")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "contact_form", "Contact Form",
                 block_key="contact_form_block", display_order=order,
                 layout_type="contact-form", background_style="muted", animation="fade-up",
                 seo_anchor="contact-form")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "department_contacts", "Department Contacts",
                 block_key="contact_departments", display_order=order,
                 layout_type="department-contacts", background_style="default", animation="stagger",
                 seo_anchor="department-contacts")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "emergency_contact", "Emergency Contact",
                 block_key="contact_emergency", display_order=order,
                 layout_type="emergency-contact", background_style="dark", animation="fade-up",
                 seo_anchor="emergency-contact")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "social_media", "Social Media",
                 block_key="contact_social_media", display_order=order,
                 layout_type="social-media", background_style="light", animation="fade-up",
                 seo_anchor="connect-with-us")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "call_to_action", "Call To Action",
                 block_key="call_to_action", display_order=order,
                 layout_type="cta-banner", background_style="brand", spacing="relaxed", animation="fade-up",
                 seo_anchor="request-quote")
    )

    return sections


CONTACT_PAGE_BLOCKS: list[dict[str, Any]] = build_contact_page_blocks()
CONTACT_PAGE_SECTIONS: list[dict[str, Any]] = build_contact_page_sections()
