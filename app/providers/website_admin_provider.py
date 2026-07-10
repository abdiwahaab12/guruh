"""Website CMS admin data provider — pages, sections, and content blocks."""

from __future__ import annotations

import json
from datetime import datetime

from flask import url_for
from sqlalchemy import desc, func
from sqlalchemy.exc import SQLAlchemyError

from app.constants.website_admin import MANAGED_PAGES, MANAGED_PAGE_SLUGS
from app.extensions import db
from app.models.cms import Page
from app.models.content_blocks import ContentBlock, ContentBlockItem
from app.models.page_sections import PageSection
from app.providers.auth_provider import AuthProvider
from app.providers import block_loader, page_loader
from app.providers.placeholder import PlaceholderContentProvider
from app.schemas.content import ContentBlockDTO, ContentBlockItemDTO, PageMetaDTO
from app.schemas.website_admin import WebsitePageEditorDTO, WebsitePageListItemDTO


class WebsiteAdminProvider:
    """Database operations for Website CMS admin."""

    _placeholder = PlaceholderContentProvider()

    @staticmethod
    def commit() -> bool:
        return AuthProvider.commit()

    @staticmethod
    def rollback() -> None:
        AuthProvider.rollback()

    @staticmethod
    def record_audit(**kwargs) -> None:
        AuthProvider.record_audit_event(**kwargs)

    @staticmethod
    def _format_dt(value: datetime | None) -> str:
        return value.strftime("%d %b %Y, %H:%M") if value else "—"

    @staticmethod
    def _public_path(slug: str) -> str:
        for page in MANAGED_PAGES:
            if page["slug"] == slug:
                return page["public_path"]
        return f"/{slug}" if slug != "home" else "/"

    @staticmethod
    def get_page_meta_fallback(slug: str) -> PageMetaDTO | None:
        return WebsiteAdminProvider._placeholder.get_page_meta(slug)

    @staticmethod
    def ensure_page(slug: str) -> Page:
        if slug not in MANAGED_PAGE_SLUGS:
            raise ValueError(f"Unknown page slug: {slug}")

        row = Page.query.filter_by(slug=slug).first()
        if row:
            return row

        meta = WebsiteAdminProvider.get_page_meta_fallback(slug)
        if not meta:
            meta = PageMetaDTO(
                slug=slug,
                title=slug.replace("-", " ").title(),
                meta_title=slug.replace("-", " ").title(),
                meta_description="",
                is_published=True,
            )

        row = Page(
            slug=slug,
            title=meta.title,
            meta_title=meta.meta_title or meta.title,
            meta_description=meta.meta_description or "",
            banner_subtitle=meta.banner_subtitle or "",
            banner_image=meta.banner_image or "",
            is_published=meta.is_published,
        )
        db.session.add(row)
        db.session.flush()
        return row

    @staticmethod
    def get_page_row(slug: str) -> Page | None:
        return Page.query.filter_by(slug=slug).first()

    @staticmethod
    def _page_canonical(slug: str) -> str:
        section = (
            PageSection.query.filter_by(page_slug=slug)
            .order_by(PageSection.display_order)
            .first()
        )
        if section and isinstance(section.extra, dict):
            canonical = section.extra.get("page_canonical") or section.extra.get("canonical_url")
            if canonical:
                return str(canonical)
        return WebsiteAdminProvider._public_path(slug)

    @staticmethod
    def _set_page_canonical(slug: str, canonical_url: str) -> None:
        section = (
            PageSection.query.filter_by(page_slug=slug)
            .order_by(PageSection.display_order)
            .first()
        )
        if not section:
            return
        extra = dict(section.extra or {})
        extra["page_canonical"] = canonical_url.strip()
        section.extra = extra

    @staticmethod
    def list_pages() -> list[WebsitePageListItemDTO]:
        items: list[WebsitePageListItemDTO] = []
        for page_def in MANAGED_PAGES:
            slug = page_def["slug"]
            row = Page.query.filter_by(slug=slug).first()
            meta = WebsiteAdminProvider.get_page_meta_fallback(slug)

            title = row.title if row else (meta.title if meta else page_def["title"])
            is_published = row.is_published if row else (meta.is_published if meta else True)
            status = "published" if is_published else "draft"

            section_count = PageSection.query.filter_by(page_slug=slug, is_active=True).count()
            if section_count == 0:
                fallback = page_loader.build_section_list_from_seed(slug)
                section_count = len(fallback.sections)

            updated_candidates = []
            if row and row.updated_at:
                updated_candidates.append(row.updated_at)
            latest_section = (
                PageSection.query.filter_by(page_slug=slug)
                .order_by(desc(PageSection.updated_at))
                .first()
            )
            if latest_section and latest_section.updated_at:
                updated_candidates.append(latest_section.updated_at)
            updated_at = max(updated_candidates) if updated_candidates else None

            public_path = page_def["public_path"]
            try:
                preview_url = url_for("main.index") if slug == "home" else public_path
            except RuntimeError:
                preview_url = public_path

            items.append(
                WebsitePageListItemDTO(
                    slug=slug,
                    title=title,
                    public_path=public_path,
                    status=status,
                    status_label="Published" if is_published else "Draft",
                    sections_count=section_count,
                    updated_at_label=WebsiteAdminProvider._format_dt(updated_at),
                    preview_url=preview_url,
                )
            )
        return items

    @staticmethod
    def materialize_page_sections(page_slug: str) -> None:
        """Create DB rows from seed when a page has no sections yet."""
        if PageSection.query.filter_by(page_slug=page_slug).count() > 0:
            return
        seed = page_loader.build_section_list_from_seed(page_slug)
        for section in seed.sections:
            WebsiteAdminProvider.ensure_section_from_seed(page_slug, section.section_key)
        db.session.flush()

    @staticmethod
    def get_page_editor(slug: str) -> WebsitePageEditorDTO | None:
        if slug not in MANAGED_PAGE_SLUGS:
            return None

        WebsiteAdminProvider.materialize_page_sections(slug)

        row = Page.query.filter_by(slug=slug).first()
        meta = WebsiteAdminProvider.get_page_meta_fallback(slug)
        page_def = next(p for p in MANAGED_PAGES if p["slug"] == slug)

        sections = WebsiteAdminProvider.get_sections(slug, active_only=False)
        if not sections:
            seed = page_loader.build_section_list_from_seed(slug)
            sections = seed.sections

        title = row.title if row else (meta.title if meta else page_def["title"])
        public_path = page_def["public_path"]

        return WebsitePageEditorDTO(
            slug=slug,
            title=title,
            meta_title=(row.meta_title if row else (meta.meta_title if meta else title)),
            meta_description=(row.meta_description if row else (meta.meta_description if meta else "")),
            banner_subtitle=(row.banner_subtitle if row else (meta.banner_subtitle if meta else "")),
            banner_image=(row.banner_image if row else (meta.banner_image if meta else "")),
            canonical_url=WebsiteAdminProvider._page_canonical(slug),
            is_published=row.is_published if row else (meta.is_published if meta else True),
            public_path=public_path,
            preview_url=public_path,
            sections=sections,
        )

    @staticmethod
    def save_page_seo(
        *,
        slug: str,
        title: str,
        meta_title: str,
        meta_description: str,
        banner_subtitle: str,
        banner_image: str,
        canonical_url: str,
        is_published: bool,
    ) -> Page:
        row = WebsiteAdminProvider.ensure_page(slug)
        row.title = title.strip()
        row.meta_title = meta_title.strip() or row.title
        row.meta_description = meta_description.strip()
        row.banner_subtitle = banner_subtitle.strip()
        row.banner_image = WebsiteAdminProvider._normalize_media_path(banner_image)
        row.is_published = is_published
        if canonical_url.strip():
            WebsiteAdminProvider._set_page_canonical(slug, canonical_url.strip())
        return row

    @staticmethod
    def get_sections(page_slug: str, *, active_only: bool = False) -> list:
        query = PageSection.query.filter_by(page_slug=page_slug).order_by(PageSection.display_order)
        if active_only:
            query = query.filter_by(is_active=True)
        rows = query.all()
        if rows:
            return [page_loader.section_from_model(row) for row in rows]
        seed = page_loader.build_section_list_from_seed(page_slug)
        return seed.sections

    @staticmethod
    def get_section(section_id: int) -> PageSection | None:
        return PageSection.query.get(section_id)

    @staticmethod
    def ensure_section_from_seed(page_slug: str, section_key: str) -> PageSection | None:
        seed = page_loader.build_section_list_from_seed(page_slug)
        seed_data = next((s for s in seed.sections if s.section_key == section_key), None)
        if not seed_data:
            return None

        row = PageSection.query.filter_by(page_slug=page_slug, section_key=section_key).first()
        if row:
            return row

        row = PageSection(
            page_slug=page_slug,
            section_key=section_key,
            section_title=seed_data.section_title,
            block_key=seed_data.block_key or None,
            display_order=seed_data.display_order,
            layout_type=seed_data.layout_type,
            background_style=seed_data.background_style,
            spacing=seed_data.spacing,
            animation=seed_data.animation,
            is_visible=seed_data.is_visible,
            seo_anchor=seed_data.seo_anchor,
            is_active=seed_data.is_active,
            extra=dict(seed_data.extra or {}),
        )
        db.session.add(row)
        db.session.flush()
        return row

    @staticmethod
    def save_section(
        *,
        section_id: int | None,
        page_slug: str,
        section_key: str,
        section_title: str,
        block_key: str,
        display_order: int,
        layout_type: str,
        background_style: str,
        spacing: str,
        animation: str,
        is_visible: bool,
        seo_anchor: str,
        is_active: bool,
        extra: dict | None = None,
    ) -> PageSection:
        row = None
        if section_id:
            row = PageSection.query.get(section_id)
        if not row:
            row = PageSection.query.filter_by(page_slug=page_slug, section_key=section_key).first()
        if not row:
            row = WebsiteAdminProvider.ensure_section_from_seed(page_slug, section_key)
        if not row:
            row = PageSection(page_slug=page_slug, section_key=section_key)
            db.session.add(row)

        row.section_title = section_title.strip()
        row.block_key = block_key.strip() or None
        row.display_order = display_order
        row.layout_type = layout_type
        row.background_style = background_style
        row.spacing = spacing
        row.animation = animation
        row.is_visible = is_visible
        row.seo_anchor = seo_anchor.strip() or section_key.replace("_", "-")
        row.is_active = is_active
        if extra is not None:
            row.extra = extra
        db.session.flush()
        return row

    @staticmethod
    def toggle_section_visibility(section_id: int) -> PageSection | None:
        row = PageSection.query.get(section_id)
        if not row:
            return None
        row.is_visible = not row.is_visible
        return row

    @staticmethod
    def move_section(section_id: int, direction: str) -> bool:
        row = PageSection.query.get(section_id)
        if not row:
            return False

        if direction == "up":
            neighbor = (
                PageSection.query.filter(
                    PageSection.page_slug == row.page_slug,
                    PageSection.display_order < row.display_order,
                )
                .order_by(desc(PageSection.display_order))
                .first()
            )
        else:
            neighbor = (
                PageSection.query.filter(
                    PageSection.page_slug == row.page_slug,
                    PageSection.display_order > row.display_order,
                )
                .order_by(PageSection.display_order)
                .first()
            )

        if not neighbor:
            return False

        row.display_order, neighbor.display_order = neighbor.display_order, row.display_order
        return True

    @staticmethod
    def get_block_model(block_key: str) -> ContentBlock | None:
        if not block_key:
            return None
        return ContentBlock.query.filter_by(block_key=block_key).first()

    @staticmethod
    def ensure_block_from_seed(block_key: str) -> ContentBlock | None:
        if not block_key:
            return None
        row = ContentBlock.query.filter_by(block_key=block_key).first()
        if row:
            return row
        seed = block_loader.get_seed_block(block_key)
        if not seed:
            return None
        row = ContentBlock(block_key=block_key, title=seed.title, full_content=seed.full_content or "")
        db.session.add(row)
        db.session.flush()
        row.subtitle = seed.subtitle
        row.short_summary = seed.short_summary
        row.hero_image = seed.hero_image
        row.gallery_images = list(seed.gallery_images or [])
        row.display_order = seed.display_order
        row.is_active = seed.is_active
        row.meta_title = seed.meta_title
        row.meta_description = seed.meta_description
        row.og_image = seed.og_image
        row.extra = dict(seed.extra or {})
        for item in seed.items:
            db.session.add(
                ContentBlockItem(
                    block_id=row.id,
                    item_key=item.item_key,
                    title=item.title,
                    subtitle=item.subtitle,
                    short_summary=item.short_summary,
                    full_content=item.full_content,
                    image=item.image,
                    icon=item.icon,
                    sort_order=item.sort_order,
                    is_active=item.is_active,
                    extra=dict(item.extra or {}),
                )
            )
        db.session.flush()
        return row

    @staticmethod
    def get_block_dto(block_key: str, *, include_inactive_items: bool = True) -> ContentBlockDTO | None:
        if not block_key:
            return None
        row = WebsiteAdminProvider.get_block_model(block_key)
        if not row:
            seed = block_loader.get_seed_block(block_key)
            return seed
        if include_inactive_items:
            items = row.items.order_by(ContentBlockItem.sort_order).all()
            return block_loader.block_from_model(row, items=items)
        return block_loader.block_from_model(row)

    @staticmethod
    def save_block(block_key: str, payload: dict) -> ContentBlock:
        row = WebsiteAdminProvider.ensure_block_from_seed(block_key)
        if not row:
            row = ContentBlock(block_key=block_key, title=payload.get("title") or block_key)
            db.session.add(row)

        for field in (
            "title",
            "subtitle",
            "short_summary",
            "full_content",
            "hero_image",
            "meta_title",
            "meta_description",
            "og_image",
        ):
            if field in payload:
                setattr(row, field, payload.get(field) or "")

        if "gallery_images" in payload:
            row.gallery_images = list(payload.get("gallery_images") or [])
        if "extra" in payload:
            row.extra = dict(payload.get("extra") or {})
        if "is_active" in payload:
            row.is_active = bool(payload.get("is_active"))
        db.session.flush()
        return row

    @staticmethod
    def get_block_item(item_id: int) -> ContentBlockItem | None:
        return ContentBlockItem.query.get(item_id)

    @staticmethod
    def save_block_item(
        *,
        block_key: str,
        item_id: int | None,
        payload: dict,
    ) -> ContentBlockItem:
        block = WebsiteAdminProvider.ensure_block_from_seed(block_key)
        if not block:
            raise ValueError(f"Unknown block: {block_key}")

        row = ContentBlockItem.query.get(item_id) if item_id else None
        if not row:
            max_order = (
                db.session.query(func.max(ContentBlockItem.sort_order))
                .filter_by(block_id=block.id)
                .scalar()
            ) or 0
            row = ContentBlockItem(block_id=block.id, sort_order=max_order + 1)
            db.session.add(row)

        row.item_key = payload.get("item_key") or row.item_key or f"item-{row.id or 'new'}"
        for field in ("title", "subtitle", "short_summary", "full_content", "image", "icon"):
            if field in payload:
                setattr(row, field, payload.get(field) or "")
        if "extra" in payload:
            row.extra = dict(payload.get("extra") or {})
        if "is_active" in payload:
            row.is_active = bool(payload.get("is_active"))
        if "sort_order" in payload and payload.get("sort_order") is not None:
            row.sort_order = int(payload["sort_order"])
        db.session.flush()
        return row

    @staticmethod
    def delete_block_item(item_id: int) -> bool:
        row = ContentBlockItem.query.get(item_id)
        if not row:
            return False
        db.session.delete(row)
        return True

    @staticmethod
    def toggle_block_item(item_id: int) -> ContentBlockItem | None:
        row = ContentBlockItem.query.get(item_id)
        if not row:
            return None
        row.is_active = not row.is_active
        return row

    @staticmethod
    def move_block_item(item_id: int, direction: str) -> bool:
        row = ContentBlockItem.query.get(item_id)
        if not row:
            return False

        if direction == "up":
            neighbor = (
                ContentBlockItem.query.filter(
                    ContentBlockItem.block_id == row.block_id,
                    ContentBlockItem.sort_order < row.sort_order,
                )
                .order_by(desc(ContentBlockItem.sort_order))
                .first()
            )
        else:
            neighbor = (
                ContentBlockItem.query.filter(
                    ContentBlockItem.block_id == row.block_id,
                    ContentBlockItem.sort_order > row.sort_order,
                )
                .order_by(ContentBlockItem.sort_order)
                .first()
            )

        if not neighbor:
            return False

        row.sort_order, neighbor.sort_order = neighbor.sort_order, row.sort_order
        return True

    @staticmethod
    def item_to_dto(row: ContentBlockItem, block_key: str = "") -> ContentBlockItemDTO:
        return block_loader.item_from_model(row, block_key)

    @staticmethod
    def list_media_assets(folder: str = "content") -> list:
        """Return selectable image assets for the CMS media picker.

        Images can be uploaded to any folder (general, projects, content, ...),
        so the picker lists all active images across folders — most recent
        first — rather than restricting to a single folder.
        """
        from app.models.media import MediaAsset
        from sqlalchemy import or_

        try:
            return (
                MediaAsset.query.filter(
                    MediaAsset.is_active.is_(True),
                    or_(
                        MediaAsset.media_type == "image",
                        MediaAsset.media_type == "icon",
                    ),
                    MediaAsset.mime_type.like("image/%"),
                )
                .order_by(desc(MediaAsset.created_at))
                .limit(48)
                .all()
            )
        except SQLAlchemyError:
            return []

    @staticmethod
    def list_document_assets(folder: str = "downloads") -> list:
        """Return PDF and document assets for download-center pickers."""
        from app.models.media import MediaAsset

        try:
            return (
                MediaAsset.query.filter(
                    MediaAsset.is_active.is_(True),
                    MediaAsset.folder == folder,
                    MediaAsset.media_type.in_(("pdf", "document")),
                )
                .order_by(desc(MediaAsset.created_at))
                .limit(48)
                .all()
            )
        except SQLAlchemyError:
            return []

    @staticmethod
    def ensure_minimum_hero_slides(min_count: int = 3) -> None:
        """Add seed slides until at least min_count exist."""
        from app.models.cms import HeroSlide

        rows = HeroSlide.query.order_by(HeroSlide.sort_order).all()
        if len(rows) >= min_count:
            return
        existing_titles = {r.title for r in rows}
        added = 0
        for dto in WebsiteAdminProvider._placeholder._hero_slides():
            if len(rows) + added >= min_count:
                break
            if dto.title in existing_titles:
                continue
            db.session.add(
                HeroSlide(
                    title=dto.title,
                    subtitle=dto.subtitle or "",
                    description=dto.description or "",
                    image=dto.image or "",
                    cta_text=dto.cta_text or "",
                    cta_url=dto.cta_url or "",
                    secondary_cta_text=dto.secondary_cta_text or "",
                    secondary_cta_url=dto.secondary_cta_url or "",
                    overlay_opacity=dto.overlay_opacity,
                    sort_order=dto.sort_order,
                    is_active=True,
                )
            )
            added += 1
        if added:
            db.session.flush()

    @staticmethod
    def ensure_hero_slides() -> list:
        """Ensure home hero slides exist in the database (seeds up to 3 defaults)."""
        from app.models.cms import HeroSlide

        try:
            rows = HeroSlide.query.order_by(HeroSlide.sort_order).all()
            if rows:
                WebsiteAdminProvider.ensure_minimum_hero_slides(3)
                return HeroSlide.query.order_by(HeroSlide.sort_order).all()
        except SQLAlchemyError:
            return []

        for dto in WebsiteAdminProvider._placeholder._hero_slides():
            db.session.add(
                HeroSlide(
                    title=dto.title,
                    subtitle=dto.subtitle or "",
                    description=dto.description or "",
                    image=dto.image or "",
                    cta_text=dto.cta_text or "",
                    cta_url=dto.cta_url or "",
                    secondary_cta_text=dto.secondary_cta_text or "",
                    secondary_cta_url=dto.secondary_cta_url or "",
                    overlay_opacity=dto.overlay_opacity,
                    sort_order=dto.sort_order,
                    is_active=True,
                )
            )
        try:
            db.session.flush()
            return HeroSlide.query.order_by(HeroSlide.sort_order).all()
        except SQLAlchemyError:
            return []

    @staticmethod
    def get_hero_slide(slide_id: int):
        from app.models.cms import HeroSlide

        return HeroSlide.query.get(slide_id)

    @staticmethod
    def list_hero_slides_admin() -> list:
        from app.providers.mappers import hero_to_dto
        from app.schemas.website_admin import WebsiteHeroSlideEditorDTO

        rows = WebsiteAdminProvider.ensure_hero_slides()
        items: list[WebsiteHeroSlideEditorDTO] = []
        for row in rows:
            dto = hero_to_dto(row)
            items.append(
                WebsiteHeroSlideEditorDTO(
                    id=dto.id,
                    title=dto.title,
                    subtitle=dto.subtitle,
                    description=dto.description,
                    image=dto.image,
                    cta_text=dto.cta_text,
                    cta_url=dto.cta_url,
                    secondary_cta_text=dto.secondary_cta_text,
                    secondary_cta_url=dto.secondary_cta_url,
                    overlay_opacity=dto.overlay_opacity,
                    text_alignment=dto.text_alignment,
                    sort_order=dto.sort_order,
                    is_active=dto.is_active,
                )
            )
        return items

    @staticmethod
    def count_hero_slides() -> int:
        from app.models.cms import HeroSlide

        try:
            return HeroSlide.query.count()
        except SQLAlchemyError:
            return 0

    @staticmethod
    def _parse_overlay(value) -> float:
        try:
            parsed = float(value if value not in (None, "") else 0.65)
        except (TypeError, ValueError):
            parsed = 0.65
        return max(0.0, min(1.0, parsed))

    @staticmethod
    def _parse_text_alignment(value: str | None) -> str:
        allowed = {"left", "center", "right"}
        val = (value or "left").strip().lower()
        return val if val in allowed else "left"

    @staticmethod
    def _normalize_media_path(path: str) -> str:
        """Accept only full file paths (e.g. uploads/content/photo.jpg), not folders."""
        cleaned = (path or "").strip().replace("\\", "/")
        if not cleaned:
            return ""
        if cleaned.endswith("/"):
            return ""
        filename = cleaned.rsplit("/", 1)[-1]
        if "." not in filename:
            return ""
        return cleaned

    @staticmethod
    def save_hero_slide(
        *,
        slide_id: int | None,
        title: str,
        subtitle: str,
        description: str,
        image: str,
        cta_text: str,
        cta_url: str,
        secondary_cta_text: str,
        secondary_cta_url: str,
        overlay_opacity,
        text_alignment: str,
        sort_order: int,
        is_active: bool,
    ):
        from app.constants.public_nav import MAX_HERO_SLIDES
        from app.models.cms import HeroSlide

        if slide_id:
            row = HeroSlide.query.get(slide_id)
            if not row:
                return None
        else:
            if WebsiteAdminProvider.count_hero_slides() >= MAX_HERO_SLIDES:
                return "limit"
            row = HeroSlide(title=title.strip() or "New Slide", image="", sort_order=sort_order)
            db.session.add(row)

        row.title = title.strip()
        row.subtitle = subtitle.strip()
        row.description = description.strip()
        row.image = WebsiteAdminProvider._normalize_media_path(image)
        row.cta_text = cta_text.strip()
        row.cta_url = cta_url.strip()
        row.secondary_cta_text = secondary_cta_text.strip()
        row.secondary_cta_url = secondary_cta_url.strip()
        row.overlay_opacity = WebsiteAdminProvider._parse_overlay(overlay_opacity)
        row.text_alignment = WebsiteAdminProvider._parse_text_alignment(text_alignment)
        row.sort_order = sort_order
        row.is_active = is_active
        db.session.flush()
        return row

    @staticmethod
    def delete_hero_slide(slide_id: int) -> bool:
        from app.models.cms import HeroSlide

        row = HeroSlide.query.get(slide_id)
        if not row:
            return False
        db.session.delete(row)
        return True

    @staticmethod
    def reorder_hero_slide(slide_id: int, direction: str) -> bool:
        from app.models.cms import HeroSlide

        row = HeroSlide.query.get(slide_id)
        if not row:
            return False
        if direction == "up":
            neighbor = (
                HeroSlide.query.filter(HeroSlide.sort_order < row.sort_order)
                .order_by(HeroSlide.sort_order.desc())
                .first()
            )
        else:
            neighbor = (
                HeroSlide.query.filter(HeroSlide.sort_order > row.sort_order)
                .order_by(HeroSlide.sort_order.asc())
                .first()
            )
        if not neighbor:
            return False
        row.sort_order, neighbor.sort_order = neighbor.sort_order, row.sort_order
        return True

    @staticmethod
    def toggle_hero_slide(slide_id: int) -> bool:
        from app.models.cms import HeroSlide

        row = HeroSlide.query.get(slide_id)
        if not row:
            return False
        row.is_active = not row.is_active
        return True

    @staticmethod
    def save_hero_slide_image(slide_id: int, image: str) -> bool:
        from app.models.cms import HeroSlide

        row = HeroSlide.query.get(slide_id)
        if not row:
            return False
        row.image = image.strip()
        return True

    @staticmethod
    def resolve_page_banner_image(page_slug: str) -> str:
        """Best available hero/cover image for a public page."""
        from app.models.cms import AboutSection, HeroSlide, Page
        from app.models.content_blocks import ContentBlock
        from app.constants.website_admin import PAGE_INTRO_BLOCK_KEYS

        page = Page.query.filter_by(slug=page_slug).first()
        if page and page.banner_image:
            path = WebsiteAdminProvider._normalize_media_path(page.banner_image)
            if path and not path.startswith("img/fallbacks/"):
                return path

        block_key = PAGE_INTRO_BLOCK_KEYS.get(page_slug)
        if block_key:
            block = ContentBlock.query.filter_by(block_key=block_key).first()
            if block and block.hero_image and not block.hero_image.startswith("img/fallbacks/"):
                path = WebsiteAdminProvider._normalize_media_path(block.hero_image)
                if path:
                    return path

        if page_slug == "about":
            about_row = AboutSection.query.filter_by(page_slug="about", is_active=True).first()
            if about_row and about_row.image and not about_row.image.startswith("img/fallbacks/"):
                path = WebsiteAdminProvider._normalize_media_path(about_row.image)
                if path:
                    return path

        if page_slug == "home":
            slide = (
                HeroSlide.query.filter_by(is_active=True)
                .order_by(HeroSlide.sort_order)
                .first()
            )
            if slide and slide.image:
                path = WebsiteAdminProvider._normalize_media_path(slide.image)
                if path:
                    return path

        return ""

    @staticmethod
    def resolve_about_image() -> str:
        """Return the best available About/company overview image from CMS."""
        return WebsiteAdminProvider.resolve_page_banner_image("about")

    @staticmethod
    def sync_about_banner_to_content(banner_image: str) -> None:
        """Apply About page banner to homepage about preview and company overview block."""
        from app.models.cms import AboutSection
        from app.providers.profile_loader import build_about_section

        path = WebsiteAdminProvider._normalize_media_path(banner_image)
        if not path:
            return

        block = WebsiteAdminProvider.ensure_block_from_seed("company_overview")
        if block:
            block.hero_image = path

        for slug in ("home", "about"):
            seed = build_about_section(slug)
            if not seed:
                continue
            row = AboutSection.query.filter_by(page_slug=slug).first()
            if not row:
                row = AboutSection(
                    page_slug=slug,
                    heading=seed.heading,
                    subheading=seed.subheading,
                    content=seed.content,
                    highlights=seed.highlights,
                    cta_text=seed.cta_text,
                    cta_url=seed.cta_url,
                    is_active=True,
                )
                db.session.add(row)
            row.image = path

    @staticmethod
    def sync_page_banner_to_overview_block(page_slug: str, banner_image: str) -> None:
        """Apply a page hero banner to its overview content block image."""
        from app.constants.website_admin import PAGE_INTRO_BLOCK_KEYS

        block_key = PAGE_INTRO_BLOCK_KEYS.get(page_slug)
        if not block_key:
            return
        path = WebsiteAdminProvider._normalize_media_path(banner_image)
        if not path:
            return
        block = WebsiteAdminProvider.ensure_block_from_seed(block_key)
        if block:
            block.hero_image = path

    @staticmethod
    def resolve_page_overview_image(page_slug: str) -> str:
        """Return overview section image from page banner or content block."""
        from app.constants.website_admin import PAGE_INTRO_BLOCK_KEYS
        from app.models.cms import Page
        from app.models.content_blocks import ContentBlock

        page = Page.query.filter_by(slug=page_slug).first()
        if page and page.banner_image:
            path = WebsiteAdminProvider._normalize_media_path(page.banner_image)
            if path:
                return path

        block_key = PAGE_INTRO_BLOCK_KEYS.get(page_slug)
        if block_key:
            block = ContentBlock.query.filter_by(block_key=block_key).first()
            if block and block.hero_image and not block.hero_image.startswith("img/fallbacks/"):
                path = WebsiteAdminProvider._normalize_media_path(block.hero_image)
                if path:
                    return path

        if page_slug == "projects":
            from app.models.media import MediaAsset

            asset = (
                MediaAsset.query.filter_by(folder="projects", media_type="image", is_active=True)
                .order_by(MediaAsset.created_at.desc())
                .first()
            )
            if asset and asset.storage_path:
                return asset.storage_path

        return ""

    @staticmethod
    def sync_home_banner_to_slides(banner_image: str) -> None:
        """Apply page banner image to slides that do not have their own image."""
        from app.models.cms import HeroSlide

        if not banner_image.strip():
            return
        for row in WebsiteAdminProvider.ensure_hero_slides():
            if not (row.image or "").strip():
                row.image = banner_image.strip()

    @staticmethod
    def safe_commit(action: str, resource_type: str, resource_id: str, details: str, user_id: int, ip: str) -> bool:
        try:
            WebsiteAdminProvider.record_audit(
                user_id=user_id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                details=details,
                ip_address=ip,
            )
            return WebsiteAdminProvider.commit()
        except SQLAlchemyError:
            WebsiteAdminProvider.rollback()
            return False
