"""Enterprise Gallery Management admin routes — Step 21."""

from __future__ import annotations

from flask import abort, flash, redirect, render_template, request, url_for

from app.forms.gallery_forms import GalleryBulkForm, GalleryDeleteForm, GalleryItemForm
from app.services.gallery_admin_service import GalleryAdminService
from app.utils.permissions import can_manage_gallery


def _populate_gallery_form(form: GalleryItemForm, ctx: dict) -> None:
    form.project_id.choices = [(0, "—")] + [(p.id, p.title) for p in ctx.get("projects", [])]
    form.service_slug.choices = [("", "—")] + [(s.slug, s.title) for s in ctx.get("services", [])]
    form.equipment_slug.choices = [("", "—")] + [
        (e.slug, e.name) for e in ctx.get("equipment_list", [])
    ]
    form.team_member_ids.choices = [(m.id, m.name) for m in ctx.get("team_members", [])]


def _fill_form_from_item(form: GalleryItemForm, item) -> None:
    form.gallery_item_id.data = item.id
    form.title.data = item.title
    form.slug.data = item.slug
    form.category.data = item.category
    form.media_type.data = item.media_type
    form.album.data = item.album
    form.caption.data = item.caption
    form.location.data = item.location
    form.county.data = item.county
    form.country.data = item.country
    form.media_date.data = item.media_date
    form.year.data = item.year
    form.sort_order.data = item.sort_order
    form.is_featured.data = item.is_featured
    form.is_active.data = item.is_active
    form.image.data = item.image
    form.video_provider.data = item.video_provider
    form.video_id.data = item.video_id
    form.embed_url.data = item.embed_url
    form.project_id.data = item.project_id or 0
    form.service_slug.data = item.service_slug
    form.equipment_slug.data = item.equipment_slug
    form.team_member_ids.data = item.team_member_ids
    form.meta_title.data = item.meta_title
    form.meta_description.data = item.meta_description
    form.og_image.data = item.og_image
    form.canonical_url.data = item.canonical_url


def register_gallery_routes(admin_bp) -> None:
    """Register gallery CRUD routes."""

    @admin_bp.route("/gallery")
    @can_manage_gallery
    def gallery_dashboard():
        return render_template(
            "admin/gallery/dashboard.html",
            **GalleryAdminService.get_dashboard_context(),
        )

    @admin_bp.route("/gallery/list")
    @can_manage_gallery
    def gallery_list():
        project_raw = request.args.get("project_id", "")
        project_id = int(project_raw) if project_raw.isdigit() else None
        ctx = GalleryAdminService.get_list_context(
            q=request.args.get("q", ""),
            album=request.args.get("album", ""),
            category=request.args.get("category", ""),
            project_id=project_id,
            service=request.args.get("service", ""),
            country=request.args.get("country", ""),
            featured=request.args.get("featured", ""),
            status=request.args.get("status", ""),
            sort=request.args.get("sort", "date_desc"),
            page=request.args.get("page", 1, type=int),
            include_deleted=request.args.get("deleted") == "1",
        )
        bulk_form = GalleryBulkForm()
        bulk_form.action.choices = list(ctx["bulk_actions"].items())
        ctx["bulk_form"] = bulk_form
        return render_template("admin/gallery/list.html", **ctx)

    @admin_bp.route("/gallery/create", methods=["GET", "POST"])
    @can_manage_gallery
    def gallery_create():
        active_tab = request.args.get("tab", "general")
        ctx = GalleryAdminService.get_form_context(item_id=None, active_tab=active_tab)
        form = GalleryItemForm()
        _populate_gallery_form(form, ctx)

        if form.validate_on_submit():
            dto = GalleryAdminService.dto_from_form(form)
            result = GalleryAdminService.save_item(dto, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success and result.gallery_item_id:
                return redirect(url_for("admin.gallery_edit", gallery_item_id=result.gallery_item_id))

        ctx["form"] = form
        ctx["delete_form"] = GalleryDeleteForm()
        return render_template("admin/gallery/form.html", **ctx)

    @admin_bp.route("/gallery/<int:gallery_item_id>/edit", methods=["GET", "POST"])
    @can_manage_gallery
    def gallery_edit(gallery_item_id: int):
        active_tab = request.args.get("tab", "general")
        ctx = GalleryAdminService.get_form_context(item_id=gallery_item_id, active_tab=active_tab)
        if not ctx:
            abort(404)

        form = GalleryItemForm()
        _populate_gallery_form(form, ctx)
        if request.method == "GET":
            _fill_form_from_item(form, ctx["gallery_item"])

        if form.validate_on_submit():
            dto = GalleryAdminService.dto_from_form(form)
            result = GalleryAdminService.save_item(dto, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success:
                return redirect(
                    url_for("admin.gallery_edit", gallery_item_id=gallery_item_id, tab=active_tab)
                )

        ctx["form"] = form
        ctx["delete_form"] = GalleryDeleteForm()
        return render_template("admin/gallery/form.html", **ctx)

    @admin_bp.route("/gallery/<int:gallery_item_id>/delete", methods=["POST"])
    @can_manage_gallery
    def gallery_delete(gallery_item_id: int):
        form = GalleryDeleteForm()
        if form.validate_on_submit():
            result = GalleryAdminService.delete_item(gallery_item_id, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success:
                return redirect(url_for("admin.gallery_list", deleted=1))
        return redirect(url_for("admin.gallery_edit", gallery_item_id=gallery_item_id))

    @admin_bp.route("/gallery/<int:gallery_item_id>/restore", methods=["POST"])
    @can_manage_gallery
    def gallery_restore(gallery_item_id: int):
        result = GalleryAdminService.restore_item(gallery_item_id, ip_address=request.remote_addr)
        flash(result.message, "success" if result.success else "danger")
        return redirect(url_for("admin.gallery_list"))

    @admin_bp.route("/gallery/bulk", methods=["POST"])
    @can_manage_gallery
    def gallery_bulk():
        form = GalleryBulkForm()
        from app.constants.gallery_admin import BULK_ACTIONS

        form.action.choices = list(BULK_ACTIONS.items())
        if not form.validate_on_submit():
            flash("Invalid bulk action.", "danger")
            return redirect(url_for("admin.gallery_list"))

        ids = [int(x) for x in request.form.getlist("gallery_item_ids") if x.isdigit()]
        result = GalleryAdminService.bulk_action(ids, form.action.data, ip_address=request.remote_addr)
        flash(result.message, "success" if result.success else "danger")
        return redirect(url_for("admin.gallery_list"))
