"""
Maps CMS content block seed/ORM data to DTOs.
"""

from app.data.cms_blocks import CMS_BLOCKS_BY_KEY, CMS_CONTENT_BLOCKS
from app.models.content_blocks import ContentBlock, ContentBlockItem
from app.schemas.content import ContentBlockDTO, ContentBlockItemDTO, ContentBlockRegistryDTO


def _item_from_dict(data: dict, block_key: str) -> ContentBlockItemDTO:
    return ContentBlockItemDTO(
        id=data["id"],
        block_key=block_key,
        item_key=data.get("item_key", ""),
        title=data["title"],
        subtitle=data.get("subtitle", ""),
        short_summary=data.get("short_summary", ""),
        full_content=data.get("full_content", ""),
        image=data.get("image", ""),
        icon=data.get("icon", ""),
        sort_order=data.get("sort_order", 0),
        is_active=data.get("is_active", True),
        extra=data.get("extra") or {},
        created_at=data.get("created_at", ""),
        updated_at=data.get("updated_at", ""),
    )


def block_from_dict(data: dict) -> ContentBlockDTO:
    block_key = data["block_key"]
    return ContentBlockDTO(
        id=data["id"],
        block_key=block_key,
        title=data["title"],
        subtitle=data.get("subtitle", ""),
        short_summary=data.get("short_summary", ""),
        full_content=data.get("full_content", ""),
        hero_image=data.get("hero_image", ""),
        gallery_images=list(data.get("gallery_images") or []),
        display_order=data.get("display_order", 0),
        is_active=data.get("is_active", True),
        meta_title=data.get("meta_title", ""),
        meta_description=data.get("meta_description", ""),
        og_image=data.get("og_image", ""),
        extra=dict(data.get("extra") or {}),
        items=[_item_from_dict(item, block_key) for item in data.get("items", [])],
        created_at=data.get("created_at", ""),
        updated_at=data.get("updated_at", ""),
    )


def block_from_model(row: ContentBlock, items: list[ContentBlockItem] | None = None) -> ContentBlockDTO:
    item_rows = items if items is not None else row.items.filter_by(is_active=True).all()
    return ContentBlockDTO(
        id=row.id,
        block_key=row.block_key,
        title=row.title,
        subtitle=row.subtitle or "",
        short_summary=row.short_summary or "",
        full_content=row.full_content or "",
        hero_image=row.hero_image or "",
        gallery_images=list(row.gallery_images or []),
        display_order=row.display_order,
        is_active=row.is_active,
        meta_title=row.meta_title or "",
        meta_description=row.meta_description or "",
        og_image=row.og_image or "",
        extra=dict(row.extra or {}),
        items=[item_from_model(i, row.block_key) for i in item_rows],
        created_at=row.created_at.isoformat() if row.created_at else "",
        updated_at=row.updated_at.isoformat() if row.updated_at else "",
    )


def item_from_model(row: ContentBlockItem, block_key: str = "") -> ContentBlockItemDTO:
    key = block_key or (row.block.block_key if row.block else "")
    return ContentBlockItemDTO(
        id=row.id,
        block_key=key,
        item_key=row.item_key or "",
        title=row.title,
        subtitle=row.subtitle or "",
        short_summary=row.short_summary or "",
        full_content=row.full_content or "",
        image=row.image or "",
        icon=row.icon or "",
        sort_order=row.sort_order,
        is_active=row.is_active,
        extra=dict(row.extra or {}),
        created_at=row.created_at.isoformat() if row.created_at else "",
        updated_at=row.updated_at.isoformat() if row.updated_at else "",
    )


def build_block_registry_from_seed() -> ContentBlockRegistryDTO:
    blocks = [block_from_dict(data) for data in CMS_CONTENT_BLOCKS]
    return ContentBlockRegistryDTO(blocks=blocks)


def get_seed_block(block_key: str) -> ContentBlockDTO | None:
    data = CMS_BLOCKS_BY_KEY.get(block_key)
    return block_from_dict(data) if data else None
