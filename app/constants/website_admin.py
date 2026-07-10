"""
Website CMS admin constants — managed public pages and UI presets.

Built on the existing Page Builder and Content Blocks architecture.
"""

from __future__ import annotations

from typing import Any, Final

# Public catalog pages managed through Page Builder (home uses page meta + legacy CMS)
MANAGED_PAGES: Final[tuple[dict[str, str], ...]] = (
    {"slug": "home", "title": "Home", "public_path": "/"},
    {"slug": "about", "title": "About", "public_path": "/about"},
    {"slug": "services", "title": "Services", "public_path": "/services"},
    {"slug": "projects", "title": "Projects", "public_path": "/projects"},
    {"slug": "equipment", "title": "Equipment", "public_path": "/equipment"},
    {"slug": "team", "title": "Team", "public_path": "/team"},
    {"slug": "gallery", "title": "Gallery", "public_path": "/gallery"},
    {"slug": "careers", "title": "Careers", "public_path": "/careers"},
    {"slug": "contact", "title": "Contact", "public_path": "/contact"},
    {"slug": "request-quote", "title": "Request Quote", "public_path": "/request-quote"},
)

MANAGED_PAGE_SLUGS: Final[frozenset[str]] = frozenset(p["slug"] for p in MANAGED_PAGES)

# Page hero banner → intro/overview content block (split-columns image)
PAGE_INTRO_BLOCK_KEYS: Final[dict[str, str]] = {
    "about": "company_overview",
    "services": "services_overview",
    "projects": "projects_overview",
    "equipment": "equipment_overview",
    "gallery": "gallery_intro",
    "team": "team_intro",
    "careers": "careers_intro",
    "contact": "contact_intro",
    "request-quote": "quote_intro",
}

# Backward-compatible alias used by overview image enrichment
PAGE_OVERVIEW_BLOCK_KEYS: Final[dict[str, str]] = {
    slug: key
    for slug, key in PAGE_INTRO_BLOCK_KEYS.items()
    if slug in {"services", "projects"}
}

PAGE_STATUS_LABELS: Final[dict[str, str]] = {
    "published": "Published",
    "draft": "Draft",
}

SECTION_ACTIONS: Final[tuple[str, ...]] = ("up", "down", "toggle", "preview")

BLOCK_ITEM_ACTIONS: Final[tuple[str, ...]] = ("up", "down", "toggle", "delete")

MEDIA_FOLDER: Final[str] = "content"

# DTO fields excluded from dynamic block/item editors (managed separately)
BLOCK_EDITOR_SKIP: Final[frozenset[str]] = frozenset(
    {
        "id",
        "block_key",
        "items",
        "created_at",
        "updated_at",
        "display_order",
        "is_active",
    }
)

ITEM_EDITOR_SKIP: Final[frozenset[str]] = frozenset(
    {
        "id",
        "block_key",
        "item_key",
        "created_at",
        "updated_at",
        "sort_order",
        "is_active",
    }
)

# Human labels for standard ContentBlockDTO / ContentBlockItemDTO fields
FIELD_LABELS: Final[dict[str, str]] = {
    "title": "Title",
    "subtitle": "Subtitle",
    "short_summary": "Summary",
    "full_content": "Content",
    "hero_image": "Hero Image",
    "gallery_images": "Gallery Images",
    "meta_title": "Meta Title",
    "meta_description": "Meta Description",
    "og_image": "Open Graph Image",
    "image": "Image",
    "icon": "Icon",
    "file_url": "PDF / Document File",
    "file_type": "File Type",
    "is_ready": "Enable Download Button",
    "extra": "Extra Settings",
}

FIELD_HELP: Final[dict[str, str]] = {
    "file_url": "Upload a PDF from your computer or pick one from the Downloads library.",
    "is_ready": "Turn on after the PDF is uploaded so visitors see a Download button.",
    "file_type": "Shown on the card, e.g. PDF.",
}

FIELD_GROUPS: Final[dict[str, str]] = {
    "title": "content",
    "subtitle": "content",
    "short_summary": "content",
    "full_content": "content",
    "hero_image": "media",
    "gallery_images": "media",
    "meta_title": "seo",
    "meta_description": "seo",
    "og_image": "seo",
    "image": "media",
    "icon": "content",
}

FORM_TABS: Final[tuple[dict[str, str], ...]] = (
    {"slug": "content", "label": "Content", "icon": "bi-file-text"},
    {"slug": "media", "label": "Media", "icon": "bi-image"},
    {"slug": "items", "label": "Items", "icon": "bi-list-ul"},
    {"slug": "seo", "label": "SEO", "icon": "bi-search"},
    {"slug": "extra", "label": "Extra", "icon": "bi-braces"},
)

SECTION_FORM_TABS: Final[tuple[dict[str, str], ...]] = (
    {"slug": "general", "label": "General", "icon": "bi-sliders"},
    {"slug": "layout", "label": "Page Builder", "icon": "bi-layout-wtf"},
    {"slug": "block", "label": "Content Block", "icon": "bi-puzzle"},
)
