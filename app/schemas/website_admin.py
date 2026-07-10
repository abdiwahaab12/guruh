"""Website CMS admin module DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.schemas.content import ContentBlockDTO, ContentBlockItemDTO, PageSectionDTO


@dataclass
class AdminFieldDefinitionDTO:
    """Dynamic form field derived from a ContentBlock DTO."""

    name: str
    label: str
    field_type: str
    value: Any
    group: str = "content"
    help_text: str = ""


@dataclass
class WebsitePageListItemDTO:
    slug: str
    title: str
    public_path: str
    status: str
    status_label: str
    sections_count: int
    updated_at_label: str
    preview_url: str


@dataclass
class WebsitePageEditorDTO:
    slug: str
    title: str
    meta_title: str
    meta_description: str
    banner_subtitle: str
    banner_image: str
    canonical_url: str
    is_published: bool
    public_path: str
    preview_url: str
    sections: list[PageSectionDTO] = field(default_factory=list)


@dataclass
class WebsiteHeroSlideEditorDTO:
    id: int
    title: str
    subtitle: str
    description: str
    image: str
    cta_text: str
    cta_url: str
    secondary_cta_text: str
    secondary_cta_url: str
    overlay_opacity: float
    text_alignment: str
    sort_order: int
    is_active: bool


@dataclass
class WebsiteSectionEditorDTO:
    section: PageSectionDTO
    page_slug: str
    page_title: str
    block: ContentBlockDTO | None = None
    block_keys: list[str] = field(default_factory=list)


@dataclass
class WebsiteBlockEditorDTO:
    block: ContentBlockDTO
    page_slug: str | None
    section_id: int | None
    fields: list[AdminFieldDefinitionDTO] = field(default_factory=list)
    items: list[ContentBlockItemDTO] = field(default_factory=list)
    is_itemized: bool = False


@dataclass
class WebsiteBlockItemEditorDTO:
    item: ContentBlockItemDTO
    block_key: str
    block_title: str
    fields: list[AdminFieldDefinitionDTO] = field(default_factory=list)


@dataclass
class SaveResultDTO:
    success: bool
    message: str
    resource_id: int | None = None
    redirect_url: str | None = None
