"""Website CMS admin business logic."""

from __future__ import annotations

from flask import session, url_for
from flask_login import current_user

from app.constants.content_blocks import ITEMIZED_BLOCK_KEYS
from app.constants.page_builder import (
    ANIMATION_LABELS,
    ANIMATION_PRESETS,
    BACKGROUND_STYLE_LABELS,
    BACKGROUND_STYLES,
    LAYOUT_TYPE_LABELS,
    LAYOUT_TYPES,
    SPACING_LABELS,
    SPACING_PRESETS,
)
from app.constants.public_nav import MAX_HERO_SLIDES
from app.constants.website_admin import FORM_TABS, MANAGED_PAGE_SLUGS, SECTION_FORM_TABS
from app.forms.website_forms import WebsiteHeroSlideActionForm, WebsiteHeroSlideForm
from app.providers.admin_dashboard_provider import AdminDashboardProvider
from app.providers.website_admin_provider import WebsiteAdminProvider
from app.schemas.admin import BreadcrumbItemDTO
from app.schemas.website_admin import SaveResultDTO, WebsiteBlockEditorDTO, WebsiteBlockItemEditorDTO
from app.utils.cms_field_builder import (
    apply_form_to_block_dto,
    apply_form_to_item_dto,
    build_block_editor_fields,
    build_item_editor_fields,
)


def _block_media_folder(block_key: str) -> str:
    if block_key == "partners":
        return "general"
    if block_key == "gallery_downloads":
        return "downloads"
    return "content"


def _sort_download_item_fields(fields: list) -> list:
    """Surface PDF upload controls before long text fields."""
    priority = {
        "title": 10,
        "subtitle": 20,
        "extra__file_url": 30,
        "extra__is_ready": 40,
        "short_summary": 50,
        "full_content": 60,
        "extra__file_type": 70,
    }
    return sorted(fields, key=lambda field: (priority.get(field.name, 100), field.name))


class WebsiteAdminService:
    """Enterprise Website CMS — pages, sections, and content blocks."""

    PREVIEW_SESSION_KEY = "website_cms_preview"

    @staticmethod
    def get_shell_context(
        *,
        page_title: str,
        active_section: str | None = None,
        breadcrumbs: list[BreadcrumbItemDTO] | None = None,
    ) -> dict:
        dashboard = AdminDashboardProvider.get_dashboard()
        return {
            "page_title": page_title,
            "active_nav": "content",
            "website_active_section": active_section,
            "breadcrumbs": breadcrumbs
            or WebsiteAdminService.build_breadcrumbs(page_title),
            "notifications": dashboard.notifications,
            "unread_notification_count": dashboard.unread_notification_count,
            "user": current_user,
        }

    @staticmethod
    def build_breadcrumbs(current_label: str, *, page_slug: str | None = None) -> list[BreadcrumbItemDTO]:
        crumbs = [
            BreadcrumbItemDTO("Admin", url_for("admin.dashboard"), False),
            BreadcrumbItemDTO("Website", url_for("admin.website_dashboard"), False),
        ]
        if page_slug:
            editor = WebsiteAdminProvider.get_page_editor(page_slug)
            if editor:
                crumbs.append(
                    BreadcrumbItemDTO(editor.title, url_for("admin.website_page", slug=page_slug), False)
                )
        crumbs.append(BreadcrumbItemDTO(current_label, None, True))
        return crumbs

    @staticmethod
    def get_dashboard_context() -> dict:
        ctx = WebsiteAdminService.get_shell_context(
            page_title="Website CMS",
            active_section="dashboard",
            breadcrumbs=[
                BreadcrumbItemDTO("Admin", url_for("admin.dashboard"), False),
                BreadcrumbItemDTO("Website", None, True),
            ],
        )
        ctx["pages"] = WebsiteAdminProvider.list_pages()
        return ctx

    @staticmethod
    def get_page_context(slug: str) -> dict | None:
        if slug not in MANAGED_PAGE_SLUGS:
            return None
        editor = WebsiteAdminProvider.get_page_editor(slug)
        if not editor:
            return None

        ctx = WebsiteAdminService.get_shell_context(
            page_title=editor.title,
            active_section="page",
            breadcrumbs=WebsiteAdminService.build_breadcrumbs(editor.title, page_slug=slug),
        )
        ctx["page_editor"] = editor
        ctx["media_assets"] = WebsiteAdminProvider.list_media_assets("content")
        if slug == "home":
            ctx["hero_slides"] = WebsiteAdminProvider.list_hero_slides_admin()
            ctx["hero_slide_action_form"] = WebsiteHeroSlideActionForm()
            ctx["hero_slide_count"] = len(ctx["hero_slides"])
            ctx["max_hero_slides"] = MAX_HERO_SLIDES
        return ctx

    @staticmethod
    def get_hero_slide_context(slide_id: int | None = None) -> dict | None:
        from app.providers.mappers import hero_to_dto

        slide = None
        if slide_id:
            row = WebsiteAdminProvider.get_hero_slide(slide_id)
            if not row:
                return None
            slide = hero_to_dto(row)

        ctx = WebsiteAdminService.get_shell_context(
            page_title="Edit Hero Slide" if slide_id else "Add Hero Slide",
            active_section="page",
            breadcrumbs=WebsiteAdminService.build_breadcrumbs("Hero Slide", page_slug="home"),
        )
        ctx["slide"] = slide
        ctx["slide_id"] = slide_id
        ctx["form"] = WebsiteHeroSlideForm()
        ctx["media_assets"] = WebsiteAdminProvider.list_media_assets("content")
        return ctx

    @staticmethod
    def fill_hero_slide_form(form: WebsiteHeroSlideForm, slide) -> None:
        form.slide_id.data = slide.id
        form.title.data = slide.title
        form.subtitle.data = slide.subtitle
        form.description.data = slide.description
        form.image.data = slide.image
        form.cta_text.data = slide.cta_text
        form.cta_url.data = slide.cta_url
        form.secondary_cta_text.data = slide.secondary_cta_text
        form.secondary_cta_url.data = slide.secondary_cta_url
        form.overlay_opacity.data = str(slide.overlay_opacity)
        form.text_alignment.data = slide.text_alignment or "left"
        form.sort_order.data = slide.sort_order
        form.is_active.data = slide.is_active

    @staticmethod
    def get_section_context(page_slug: str, section_id: int) -> dict | None:
        if page_slug not in MANAGED_PAGE_SLUGS:
            return None

        row = WebsiteAdminProvider.get_section(section_id)
        if not row:
            return None

        from app.providers import page_loader

        section = page_loader.section_from_model(row)
        block = WebsiteAdminProvider.get_block_dto(section.block_key) if section.block_key else None
        block_keys = []
        if section.block_key:
            block_keys.append(section.block_key)
        extra_keys = (section.extra or {}).get("block_keys") or []
        block_keys.extend(k for k in extra_keys if k not in block_keys)

        page_editor = WebsiteAdminProvider.get_page_editor(page_slug)
        ctx = WebsiteAdminService.get_shell_context(
            page_title=f"Section — {section.section_title}",
            active_section="section",
            breadcrumbs=WebsiteAdminService.build_breadcrumbs(
                section.section_title,
                page_slug=page_slug,
            ),
        )
        ctx.update(
            {
                "page_slug": page_slug,
                "page_title": page_editor.title if page_editor else page_slug,
                "section": section,
                "section_row_id": row.id,
                "block": block,
                "block_keys": block_keys,
                "section_form_tabs": SECTION_FORM_TABS,
                "layout_types": list(LAYOUT_TYPES),
                "layout_labels": LAYOUT_TYPE_LABELS,
                "background_styles": list(BACKGROUND_STYLES),
                "background_labels": BACKGROUND_STYLE_LABELS,
                "spacing_presets": list(SPACING_PRESETS),
                "spacing_labels": SPACING_LABELS,
                "animation_presets": list(ANIMATION_PRESETS),
                "animation_labels": ANIMATION_LABELS,
                "public_preview_url": page_editor.preview_url if page_editor else "/",
            }
        )
        return ctx

    @staticmethod
    def get_block_context(
        block_key: str,
        *,
        page_slug: str | None = None,
        section_id: int | None = None,
        active_tab: str = "content",
    ) -> dict | None:
        block = WebsiteAdminProvider.get_block_dto(block_key)
        if not block:
            return None

        fields = build_block_editor_fields(block)
        ctx = WebsiteAdminService.get_shell_context(
            page_title=f"Block — {block.title}",
            active_section="block",
            breadcrumbs=WebsiteAdminService.build_breadcrumbs(
                block.title,
                page_slug=page_slug,
            ),
        )
        ctx.update(
            {
                "block_editor": WebsiteBlockEditorDTO(
                    block=block,
                    page_slug=page_slug,
                    section_id=section_id,
                    fields=fields,
                    items=block.items,
                    is_itemized=block_key in ITEMIZED_BLOCK_KEYS or len(block.items) > 0,
                ),
                "form_tabs": FORM_TABS,
                "active_tab": active_tab,
                "media_assets": WebsiteAdminProvider.list_media_assets(),
                "media_folder": _block_media_folder(block_key),
                "page_slug": page_slug,
                "section_id": section_id,
            }
        )
        return ctx

    @staticmethod
    def get_block_item_context(block_key: str, item_id: int | None = None) -> dict | None:
        block = WebsiteAdminProvider.get_block_dto(block_key)
        if not block:
            return None

        if item_id:
            row = WebsiteAdminProvider.get_block_item(item_id)
            if not row:
                return None
            item = WebsiteAdminProvider.item_to_dto(row, block_key)
            title = f"Edit Item — {item.title}"
        else:
            from app.schemas.content import ContentBlockItemDTO

            item = ContentBlockItemDTO(
                id=0,
                block_key=block_key,
                item_key="",
                title="",
            )
            title = "Create Block Item"

        fields = build_item_editor_fields(item)
        if block_key == "gallery_downloads":
            fields = _sort_download_item_fields(fields)
        ctx = WebsiteAdminService.get_shell_context(
            page_title=title,
            active_section="block_item",
            breadcrumbs=WebsiteAdminService.build_breadcrumbs(title),
        )
        ctx.update(
            {
                "item_editor": WebsiteBlockItemEditorDTO(
                    item=item,
                    block_key=block_key,
                    block_title=block.title,
                    fields=fields,
                ),
                "media_assets": WebsiteAdminProvider.list_media_assets(),
                "document_assets": WebsiteAdminProvider.list_document_assets(
                    _block_media_folder(block_key)
                ),
                "media_folder": _block_media_folder(block_key),
                "block_key": block_key,
                "is_edit": bool(item_id),
            }
        )
        return ctx

    @staticmethod
    def save_page_seo(form_data: dict, *, ip_address: str | None) -> SaveResultDTO:
        slug = form_data.get("slug", "").strip()
        if slug not in MANAGED_PAGE_SLUGS:
            return SaveResultDTO(False, "Unknown page.")

        try:
            row = WebsiteAdminProvider.save_page_seo(
                slug=slug,
                title=form_data.get("title", ""),
                meta_title=form_data.get("meta_title", ""),
                meta_description=form_data.get("meta_description", ""),
                banner_subtitle=form_data.get("banner_subtitle", ""),
                banner_image=form_data.get("banner_image", ""),
                canonical_url=form_data.get("canonical_url", ""),
                is_published=form_data.get("is_published") in ("1", "true", "on", "yes", "y"),
            )
            if slug == "home" and row.banner_image:
                WebsiteAdminProvider.sync_home_banner_to_slides(row.banner_image)
            if slug == "about" and row.banner_image:
                WebsiteAdminProvider.sync_about_banner_to_content(row.banner_image)
            elif row.banner_image:
                WebsiteAdminProvider.sync_page_banner_to_overview_block(slug, row.banner_image)
            ok = WebsiteAdminProvider.safe_commit(
                action="website.page.update",
                resource_type="page",
                resource_id=slug,
                details=f"Updated page SEO: {row.title}",
                user_id=current_user.id,
                ip=ip_address or "",
            )
            if not ok:
                return SaveResultDTO(False, "Failed to save page.")
            return SaveResultDTO(True, "Page saved successfully.", redirect_url=url_for("admin.website_page", slug=slug))
        except Exception:
            WebsiteAdminProvider.rollback()
            return SaveResultDTO(False, "Failed to save page.")

    @staticmethod
    def save_section(form_data: dict, *, ip_address: str | None) -> SaveResultDTO:
        page_slug = form_data.get("page_slug", "").strip()
        section_id_raw = form_data.get("section_id", "")
        section_id = int(section_id_raw) if str(section_id_raw).isdigit() else None
        section_key = form_data.get("section_key", "").strip()

        try:
            extra_raw = form_data.get("extra_json", "").strip()
            extra = {}
            if extra_raw:
                import json

                parsed = json.loads(extra_raw)
                extra = parsed if isinstance(parsed, dict) else {}

            row = WebsiteAdminProvider.save_section(
                section_id=section_id,
                page_slug=page_slug,
                section_key=section_key,
                section_title=form_data.get("section_title", ""),
                block_key=form_data.get("block_key", ""),
                display_order=int(form_data.get("display_order") or 0),
                layout_type=form_data.get("layout_type", "default"),
                background_style=form_data.get("background_style", "default"),
                spacing=form_data.get("spacing", "default"),
                animation=form_data.get("animation", "none"),
                is_visible=form_data.get("is_visible") in ("1", "true", "on", "yes", "y"),
                seo_anchor=form_data.get("seo_anchor", ""),
                is_active=form_data.get("is_active") in ("1", "true", "on", "yes", "y"),
                extra=extra,
            )
            ok = WebsiteAdminProvider.safe_commit(
                action="website.section.update",
                resource_type="page_section",
                resource_id=str(row.id),
                details=f"Updated section {row.section_key} on {page_slug}",
                user_id=current_user.id,
                ip=ip_address or "",
            )
            if not ok:
                return SaveResultDTO(False, "Failed to save section.")
            return SaveResultDTO(
                True,
                "Section saved successfully.",
                resource_id=row.id,
                redirect_url=url_for("admin.website_section_edit", slug=page_slug, section_id=row.id),
            )
        except Exception:
            WebsiteAdminProvider.rollback()
            return SaveResultDTO(False, "Failed to save section.")

    @staticmethod
    def section_action(section_id: int, action: str, *, ip_address: str | None) -> SaveResultDTO:
        row = WebsiteAdminProvider.get_section(section_id)
        if not row:
            return SaveResultDTO(False, "Section not found.")

        audit_action = "website.section.order"
        details = f"Section {row.section_key} on {row.page_slug}"

        if action == "toggle":
            WebsiteAdminProvider.toggle_section_visibility(section_id)
            audit_action = "website.section.update"
            details = f"Toggled visibility for {row.section_key}"
        elif action in ("up", "down"):
            if not WebsiteAdminProvider.move_section(section_id, action):
                return SaveResultDTO(False, "Cannot move section further.")
            details = f"Moved section {row.section_key} {action}"
        else:
            return SaveResultDTO(False, "Unknown action.")

        ok = WebsiteAdminProvider.safe_commit(
            action=audit_action,
            resource_type="page_section",
            resource_id=str(section_id),
            details=details,
            user_id=current_user.id,
            ip=ip_address or "",
        )
        if not ok:
            return SaveResultDTO(False, "Action failed.")
        return SaveResultDTO(True, "Section updated.", redirect_url=url_for("admin.website_page", slug=row.page_slug))

    @staticmethod
    def save_block(block_key: str, form_data: dict, *, ip_address: str | None) -> SaveResultDTO:
        block = WebsiteAdminProvider.get_block_dto(block_key)
        if not block:
            return SaveResultDTO(False, "Content block not found.")

        try:
            payload = apply_form_to_block_dto(block, form_data)
            row = WebsiteAdminProvider.save_block(block_key, payload)
            ok = WebsiteAdminProvider.safe_commit(
                action="website.block.update",
                resource_type="content_block",
                resource_id=block_key,
                details=f"Updated content block: {row.title}",
                user_id=current_user.id,
                ip=ip_address or "",
            )
            if not ok:
                return SaveResultDTO(False, "Failed to save block.")

            page_slug = form_data.get("page_slug") or None
            section_id = form_data.get("section_id")
            redirect = url_for("admin.website_block_edit", block_key=block_key)
            if page_slug and section_id:
                redirect = url_for(
                    "admin.website_block_edit",
                    block_key=block_key,
                    page_slug=page_slug,
                    section_id=section_id,
                )
            return SaveResultDTO(True, "Content block saved successfully.", redirect_url=redirect)
        except Exception:
            WebsiteAdminProvider.rollback()
            return SaveResultDTO(False, "Failed to save block.")

    @staticmethod
    def save_block_item(block_key: str, form_data: dict, *, ip_address: str | None) -> SaveResultDTO:
        block = WebsiteAdminProvider.get_block_dto(block_key)
        if not block:
            return SaveResultDTO(False, "Content block not found.")

        item_id_raw = form_data.get("item_id", "")
        item_id = int(item_id_raw) if str(item_id_raw).isdigit() and int(item_id_raw) > 0 else None

        if item_id:
            row_existing = WebsiteAdminProvider.get_block_item(item_id)
            if not row_existing:
                return SaveResultDTO(False, "Item not found.")
            item_dto = WebsiteAdminProvider.item_to_dto(row_existing, block_key)
        else:
            from app.schemas.content import ContentBlockItemDTO

            item_dto = ContentBlockItemDTO(id=0, block_key=block_key, item_key="", title="")

        try:
            payload = apply_form_to_item_dto(item_dto, form_data)
            row = WebsiteAdminProvider.save_block_item(block_key=block_key, item_id=item_id, payload=payload)
            audit = "website.block_item.update" if item_id else "website.block_item.create"
            ok = WebsiteAdminProvider.safe_commit(
                action=audit,
                resource_type="content_block_item",
                resource_id=str(row.id),
                details=f"{'Updated' if item_id else 'Created'} item {row.title} in {block_key}",
                user_id=current_user.id,
                ip=ip_address or "",
            )
            if not ok:
                return SaveResultDTO(False, "Failed to save item.")
            return SaveResultDTO(
                True,
                "Block item saved successfully.",
                resource_id=row.id,
                redirect_url=url_for("admin.website_block_edit", block_key=block_key, tab="items"),
            )
        except Exception:
            WebsiteAdminProvider.rollback()
            return SaveResultDTO(False, "Failed to save item.")

    @staticmethod
    def block_item_action(item_id: int, action: str, *, ip_address: str | None) -> SaveResultDTO:
        row = WebsiteAdminProvider.get_block_item(item_id)
        if not row:
            return SaveResultDTO(False, "Item not found.")

        block_key = row.block.block_key if row.block else ""
        if action == "delete":
            WebsiteAdminProvider.delete_block_item(item_id)
            audit = "website.block_item.delete"
            details = f"Deleted block item {item_id} from {block_key}"
        elif action == "toggle":
            WebsiteAdminProvider.toggle_block_item(item_id)
            audit = "website.block_item.update"
            details = f"Toggled item {item_id} in {block_key}"
        elif action in ("up", "down"):
            if not WebsiteAdminProvider.move_block_item(item_id, action):
                return SaveResultDTO(False, "Cannot move item further.")
            audit = "website.block_item.update"
            details = f"Reordered item {item_id} in {block_key}"
        else:
            return SaveResultDTO(False, "Unknown action.")

        ok = WebsiteAdminProvider.safe_commit(
            action=audit,
            resource_type="content_block_item",
            resource_id=str(item_id),
            details=details,
            user_id=current_user.id,
            ip=ip_address or "",
        )
        if not ok:
            return SaveResultDTO(False, "Action failed.")
        return SaveResultDTO(
            True,
            "Item updated.",
            redirect_url=url_for("admin.website_block_edit", block_key=block_key, tab="items"),
        )

    @staticmethod
    def save_hero_slide(form_data: dict, *, ip_address: str | None) -> SaveResultDTO:
        slide_id_raw = form_data.get("slide_id", "")
        slide_id = int(slide_id_raw) if str(slide_id_raw).isdigit() and int(slide_id_raw) > 0 else None
        try:
            row = WebsiteAdminProvider.save_hero_slide(
                slide_id=slide_id,
                title=form_data.get("title", ""),
                subtitle=form_data.get("subtitle", ""),
                description=form_data.get("description", ""),
                image=form_data.get("image", ""),
                cta_text=form_data.get("cta_text", ""),
                cta_url=form_data.get("cta_url", ""),
                secondary_cta_text=form_data.get("secondary_cta_text", ""),
                secondary_cta_url=form_data.get("secondary_cta_url", ""),
                overlay_opacity=form_data.get("overlay_opacity", "0.65"),
                text_alignment=form_data.get("text_alignment", "left"),
                sort_order=int(form_data.get("sort_order") or 0),
                is_active=form_data.get("is_active") in ("1", "true", "on", "yes", "y", True),
            )
            if row == "limit":
                return SaveResultDTO(False, "Maximum of 5 hero slides allowed.")
            if not row:
                return SaveResultDTO(False, "Hero slide not found.")

            ok = WebsiteAdminProvider.safe_commit(
                action="website.hero_slide.update" if slide_id else "website.hero_slide.create",
                resource_type="hero_slide",
                resource_id=str(row.id),
                details=f"Saved hero slide: {row.title}",
                user_id=current_user.id,
                ip=ip_address or "",
            )
            if not ok:
                return SaveResultDTO(False, "Failed to save hero slide.")
            return SaveResultDTO(
                True,
                "Hero slide saved.",
                resource_id=row.id,
                redirect_url=url_for("admin.website_page", slug="home"),
            )
        except Exception:
            WebsiteAdminProvider.rollback()
            return SaveResultDTO(False, "Failed to save hero slide.")

    @staticmethod
    def hero_slide_action(slide_id: int, action: str, *, ip_address: str | None) -> SaveResultDTO:
        try:
            if action == "delete":
                if not WebsiteAdminProvider.delete_hero_slide(slide_id):
                    return SaveResultDTO(False, "Hero slide not found.")
                detail = f"Deleted hero slide #{slide_id}"
            elif action in ("up", "down"):
                if not WebsiteAdminProvider.reorder_hero_slide(slide_id, action):
                    return SaveResultDTO(False, "Cannot reorder slide.")
                detail = f"Reordered hero slide #{slide_id} ({action})"
            elif action == "toggle":
                if not WebsiteAdminProvider.toggle_hero_slide(slide_id):
                    return SaveResultDTO(False, "Hero slide not found.")
                detail = f"Toggled hero slide #{slide_id}"
            else:
                return SaveResultDTO(False, "Unknown action.")

            ok = WebsiteAdminProvider.safe_commit(
                action=f"website.hero_slide.{action}",
                resource_type="hero_slide",
                resource_id=str(slide_id),
                details=detail,
                user_id=current_user.id,
                ip=ip_address or "",
            )
            if not ok:
                return SaveResultDTO(False, "Action failed.")
            return SaveResultDTO(True, "Hero slide updated.", redirect_url=url_for("admin.website_page", slug="home"))
        except Exception:
            WebsiteAdminProvider.rollback()
            return SaveResultDTO(False, "Action failed.")

    @staticmethod
    def store_preview_draft(slug: str, draft_type: str, payload: dict) -> None:
        previews = session.get(WebsiteAdminService.PREVIEW_SESSION_KEY, {})
        previews[f"{slug}:{draft_type}"] = payload
        session[WebsiteAdminService.PREVIEW_SESSION_KEY] = previews
        session.modified = True

    @staticmethod
    def get_preview_draft(slug: str, draft_type: str) -> dict | None:
        previews = session.get(WebsiteAdminService.PREVIEW_SESSION_KEY, {})
        return previews.get(f"{slug}:{draft_type}")

    @staticmethod
    def clear_preview_draft(slug: str, draft_type: str) -> None:
        previews = session.get(WebsiteAdminService.PREVIEW_SESSION_KEY, {})
        previews.pop(f"{slug}:{draft_type}", None)
        session[WebsiteAdminService.PREVIEW_SESSION_KEY] = previews
        session.modified = True
