"""Enterprise Website CMS admin routes — Step 23."""

from __future__ import annotations

import json

from flask import abort, flash, redirect, render_template, request, url_for

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
from app.forms.website_forms import (
    WebsiteBlockItemActionForm,
    WebsiteBlockItemForm,
    WebsiteHeroSlideActionForm,
    WebsiteHeroSlideForm,
    WebsitePageSeoForm,
    WebsiteSectionActionForm,
    WebsiteSectionForm,
)
from app.constants.public_nav import MAX_HERO_SLIDES
from app.providers.website_admin_provider import WebsiteAdminProvider
from app.services.website_admin_service import WebsiteAdminService
from app.utils.permissions import can_manage_pages


def _populate_section_form(form: WebsiteSectionForm) -> None:
    form.layout_type.choices = [(v, LAYOUT_TYPE_LABELS.get(v, v)) for v in LAYOUT_TYPES]
    form.background_style.choices = [(v, BACKGROUND_STYLE_LABELS.get(v, v)) for v in BACKGROUND_STYLES]
    form.spacing.choices = [(v, SPACING_LABELS.get(v, v)) for v in SPACING_PRESETS]
    form.animation.choices = [(v, ANIMATION_LABELS.get(v, v)) for v in ANIMATION_PRESETS]


def _fill_section_form(form: WebsiteSectionForm, section) -> None:
    form.page_slug.data = section.page_slug
    form.section_id.data = section.id
    form.section_key.data = section.section_key
    form.section_title.data = section.section_title
    form.block_key.data = section.block_key
    form.display_order.data = section.display_order
    form.layout_type.data = section.layout_type
    form.background_style.data = section.background_style
    form.spacing.data = section.spacing
    form.animation.data = section.animation
    form.seo_anchor.data = section.seo_anchor
    form.is_visible.data = section.is_visible
    form.is_active.data = section.is_active
    form.extra_json.data = json.dumps(section.extra or {}, indent=2)


def _fill_page_seo_form(form: WebsitePageSeoForm, editor) -> None:
    form.slug.data = editor.slug
    form.title.data = editor.title
    form.meta_title.data = editor.meta_title
    form.meta_description.data = editor.meta_description
    form.banner_subtitle.data = editor.banner_subtitle
    form.banner_image.data = editor.banner_image
    form.canonical_url.data = editor.canonical_url
    form.is_published.data = editor.is_published


def register_website_routes(admin_bp) -> None:
    """Register Website CMS routes."""

    @admin_bp.route("/website")
    @can_manage_pages
    def website_dashboard():
        return render_template(
            "admin/website/index.html",
            **WebsiteAdminService.get_dashboard_context(),
        )

    @admin_bp.route("/website/pages/<slug>", methods=["GET", "POST"])
    @can_manage_pages
    def website_page(slug: str):
        ctx = WebsiteAdminService.get_page_context(slug)
        if not ctx:
            abort(404)

        seo_form = WebsitePageSeoForm()
        section_action_form = WebsiteSectionActionForm()
        editor = ctx["page_editor"]

        if request.method == "GET":
            _fill_page_seo_form(seo_form, editor)

        if seo_form.validate_on_submit() and seo_form.submit.data:
            result = WebsiteAdminService.save_page_seo(
                request.form.to_dict(flat=True),
                ip_address=request.remote_addr,
            )
            flash(result.message, "success" if result.success else "danger")
            if result.success and result.redirect_url:
                return redirect(result.redirect_url)

        ctx["seo_form"] = seo_form
        ctx["section_action_form"] = section_action_form
        return render_template("admin/website/page_editor.html", **ctx)

    @admin_bp.route("/website/pages/home/hero-slides/create", methods=["GET", "POST"])
    @admin_bp.route("/website/pages/home/hero-slides/<int:slide_id>/edit", methods=["GET", "POST"])
    @can_manage_pages
    def website_hero_slide_edit(slide_id: int | None = None):
        if slide_id is None and WebsiteAdminProvider.count_hero_slides() >= MAX_HERO_SLIDES:
            flash(f"Maximum of {MAX_HERO_SLIDES} hero slides allowed.", "warning")
            return redirect(url_for("admin.website_page", slug="home"))

        ctx = WebsiteAdminService.get_hero_slide_context(slide_id)
        if ctx is None:
            abort(404)

        form = ctx["form"]
        slide = ctx.get("slide")

        if request.method == "GET":
            if slide:
                WebsiteAdminService.fill_hero_slide_form(form, slide)
            else:
                form.sort_order.data = len(WebsiteAdminProvider.list_hero_slides_admin()) + 1
                form.is_active.data = True
                form.overlay_opacity.data = "0.65"

        if form.validate_on_submit() and form.submit.data:
            form_data = request.form.to_dict(flat=True)
            if slide_id:
                form_data["slide_id"] = str(slide_id)
            result = WebsiteAdminService.save_hero_slide(
                form_data,
                files=request.files,
                ip_address=request.remote_addr,
            )
            flash(result.message, "success" if result.success else "danger")
            if result.success and result.redirect_url:
                return redirect(result.redirect_url)

        ctx["form"] = form
        return render_template("admin/website/hero_slide_edit.html", **ctx)

    @admin_bp.route("/website/pages/home/hero-slides/<int:slide_id>/video/delete", methods=["POST"])
    @can_manage_pages
    def website_hero_slide_video_delete(slide_id: int):
        form = WebsiteHeroSlideActionForm()
        if not form.validate_on_submit():
            flash("Invalid request.", "danger")
            return redirect(url_for("admin.website_hero_slide_edit", slide_id=slide_id))
        result = WebsiteAdminService.delete_hero_slide_video(
            slide_id,
            ip_address=request.remote_addr,
        )
        flash(result.message, "success" if result.success else "danger")
        if result.redirect_url:
            return redirect(result.redirect_url)
        return redirect(url_for("admin.website_hero_slide_edit", slide_id=slide_id))

    @admin_bp.route("/website/pages/home/hero-slides/<int:slide_id>/<action>", methods=["POST"])
    @can_manage_pages
    def website_hero_slide_action(slide_id: int, action: str):
        form = WebsiteHeroSlideActionForm()
        if not form.validate_on_submit():
            flash("Invalid request.", "danger")
            return redirect(url_for("admin.website_page", slug="home"))
        result = WebsiteAdminService.hero_slide_action(slide_id, action, ip_address=request.remote_addr)
        flash(result.message, "success" if result.success else "danger")
        return redirect(url_for("admin.website_page", slug="home"))

    @admin_bp.route("/website/pages/<slug>/sections/<int:section_id>/edit", methods=["GET", "POST"])
    @can_manage_pages
    def website_section_edit(slug: str, section_id: int):
        ctx = WebsiteAdminService.get_section_context(slug, section_id)
        if not ctx:
            abort(404)

        form = WebsiteSectionForm()
        _populate_section_form(form)
        section = ctx["section"]

        if request.method == "GET":
            _fill_section_form(form, section)

        if form.validate_on_submit():
            if form.preview.data:
                WebsiteAdminService.store_preview_draft(
                    slug,
                    f"section:{section_id}",
                    request.form.to_dict(flat=True),
                )
                flash("Preview draft stored. Open the public page to review saved content; unsaved preview is session-only.", "info")
                return redirect(
                    url_for(
                        "admin.website_preview",
                        slug=slug,
                        draft_type=f"section:{section_id}",
                    )
                )

            result = WebsiteAdminService.save_section(
                request.form.to_dict(flat=True),
                ip_address=request.remote_addr,
            )
            flash(result.message, "success" if result.success else "danger")
            if result.success and result.redirect_url:
                return redirect(result.redirect_url)

        ctx["form"] = form
        return render_template("admin/website/section_editor.html", **ctx)

    @admin_bp.route("/website/pages/<slug>/sections/<int:section_id>/<action>", methods=["POST"])
    @can_manage_pages
    def website_section_action(slug: str, section_id: int, action: str):
        form = WebsiteSectionActionForm()
        if not form.validate_on_submit():
            flash("Invalid request.", "danger")
            return redirect(url_for("admin.website_page", slug=slug))

        if action == "preview":
            return redirect(ctx_public_preview(slug))

        result = WebsiteAdminService.section_action(section_id, action, ip_address=request.remote_addr)
        flash(result.message, "success" if result.success else "danger")
        if result.redirect_url:
            return redirect(result.redirect_url)
        return redirect(url_for("admin.website_page", slug=slug))

    @admin_bp.route("/website/blocks/<block_key>/edit", methods=["GET", "POST"])
    @can_manage_pages
    def website_block_edit(block_key: str):
        page_slug = request.args.get("page_slug") or request.form.get("page_slug")
        section_id_raw = request.args.get("section_id") or request.form.get("section_id")
        section_id = int(section_id_raw) if section_id_raw and str(section_id_raw).isdigit() else None
        active_tab = request.args.get("tab", "content")

        ctx = WebsiteAdminService.get_block_context(
            block_key,
            page_slug=page_slug,
            section_id=section_id,
            active_tab=active_tab,
        )
        if not ctx:
            abort(404)

        if request.method == "POST":
            submit_preview = request.form.get("preview") == "Preview"
            form_data = request.form.to_dict(flat=True)
            form_data["page_slug"] = page_slug or ""
            form_data["section_id"] = section_id_raw or ""

            if submit_preview:
                WebsiteAdminService.store_preview_draft(
                    page_slug or block_key,
                    f"block:{block_key}",
                    form_data,
                )
                flash("Preview draft stored in session.", "info")
                return redirect(
                    url_for(
                        "admin.website_preview",
                        slug=page_slug or "about",
                        draft_type=f"block:{block_key}",
                    )
                )

            result = WebsiteAdminService.save_block(block_key, form_data, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success and result.redirect_url:
                return redirect(result.redirect_url)

        ctx["item_action_form"] = WebsiteBlockItemActionForm()
        return render_template("admin/website/block_editor.html", **ctx)

    @admin_bp.route("/website/blocks/<block_key>/items/create", methods=["GET", "POST"])
    @admin_bp.route("/website/blocks/<block_key>/items/<int:item_id>/edit", methods=["GET", "POST"])
    @can_manage_pages
    def website_block_item_edit(block_key: str, item_id: int | None = None):
        ctx = WebsiteAdminService.get_block_item_context(block_key, item_id)
        if not ctx:
            abort(404)

        form = WebsiteBlockItemForm()
        form.block_key.data = block_key
        form.item_id.data = item_id or 0
        item = ctx["item_editor"].item
        if request.method == "GET" and item_id:
            form.item_key.data = item.item_key
            form.is_active.data = item.is_active

        if form.validate_on_submit():
            data = request.form.to_dict(flat=True)
            for field in ctx["item_editor"].fields:
                if field.name not in data:
                    if field.field_type == "checkbox":
                        data[field.name] = ""
                    else:
                        data[field.name] = field.value if field.value is not None else ""

            if form.preview.data:
                WebsiteAdminService.store_preview_draft(block_key, f"item:{item_id or 'new'}", data)
                flash("Item preview draft stored.", "info")
                return redirect(url_for("admin.website_block_edit", block_key=block_key, tab="items"))

            result = WebsiteAdminService.save_block_item(block_key, data, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success and result.redirect_url:
                return redirect(result.redirect_url)

        ctx["form"] = form
        return render_template("admin/website/block_item_form.html", **ctx)

    @admin_bp.route("/website/blocks/items/<int:item_id>/<action>", methods=["POST"])
    @can_manage_pages
    def website_block_item_action(item_id: int, action: str):
        form = WebsiteBlockItemActionForm()
        if not form.validate_on_submit():
            flash("Invalid request.", "danger")
            return redirect(url_for("admin.website_dashboard"))

        result = WebsiteAdminService.block_item_action(item_id, action, ip_address=request.remote_addr)
        flash(result.message, "success" if result.success else "danger")
        if result.redirect_url:
            return redirect(result.redirect_url)
        return redirect(url_for("admin.website_dashboard"))

    @admin_bp.route("/website/preview/<slug>")
    @can_manage_pages
    def website_preview(slug: str):
        draft_type = request.args.get("draft_type", "")
        draft = WebsiteAdminService.get_preview_draft(slug, draft_type) if draft_type else None
        ctx = WebsiteAdminService.get_page_context(slug)
        if not ctx:
            abort(404)
        ctx["preview_draft"] = draft
        ctx["preview_draft_type"] = draft_type
        return render_template("admin/website/preview.html", **ctx)


def ctx_public_preview(slug: str) -> str:
    from app.constants.website_admin import MANAGED_PAGES

    for page in MANAGED_PAGES:
        if page["slug"] == slug:
            return page["public_path"]
    return url_for("admin.website_page", slug=slug)
