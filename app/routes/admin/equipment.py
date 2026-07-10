"""Enterprise Equipment Management admin routes — Step 19."""

from __future__ import annotations

from flask import abort, flash, redirect, render_template, request, url_for

from app.forms.equipment_forms import EquipmentBulkForm, EquipmentDeleteForm, EquipmentForm
from app.services.equipment_admin_service import EquipmentAdminService
from app.utils.permissions import can_manage_equipment


def _populate_equipment_form(form: EquipmentForm, ctx: dict) -> None:
    form.related_project_ids.choices = [(p.id, p.title) for p in ctx.get("projects", [])]
    form.related_service_slugs.choices = [(s.slug, s.title) for s in ctx.get("services", [])]
    form.team_member_ids.choices = [(m.id, m.name) for m in ctx.get("team_members", [])]


def _fill_form_from_equipment(form: EquipmentForm, equipment) -> None:
    form.equipment_id.data = equipment.id
    form.name.data = equipment.name
    form.slug.data = equipment.slug
    form.category.data = equipment.category
    form.short_description.data = equipment.short_description
    form.description.data = equipment.description
    form.image.data = equipment.image
    form.capacity.data = equipment.capacity
    form.condition.data = equipment.condition
    form.maintenance_status.data = equipment.maintenance_status
    form.usage.data = equipment.usage
    form.sort_order.data = equipment.sort_order
    form.is_featured.data = equipment.is_featured
    form.is_active.data = equipment.is_active
    form.related_project_ids.data = equipment.related_project_ids
    form.related_service_slugs.data = equipment.related_service_slugs
    form.team_member_ids.data = equipment.team_member_ids
    form.meta_title.data = equipment.meta_title
    form.meta_description.data = equipment.meta_description
    form.og_image.data = equipment.og_image
    form.canonical_url.data = equipment.canonical_url


def register_equipment_routes(admin_bp) -> None:
    """Register equipment CRUD routes."""

    @admin_bp.route("/equipment")
    @can_manage_equipment
    def equipment_dashboard():
        return render_template(
            "admin/equipment/dashboard.html",
            **EquipmentAdminService.get_dashboard_context(),
        )

    @admin_bp.route("/equipment/list")
    @can_manage_equipment
    def equipment_list():
        ctx = EquipmentAdminService.get_list_context(
            q=request.args.get("q", ""),
            category=request.args.get("category", ""),
            featured=request.args.get("featured", ""),
            status=request.args.get("status", ""),
            sort=request.args.get("sort", "date_desc"),
            page=request.args.get("page", 1, type=int),
            include_deleted=request.args.get("deleted") == "1",
        )
        bulk_form = EquipmentBulkForm()
        bulk_form.action.choices = list(ctx["bulk_actions"].items())
        ctx["bulk_form"] = bulk_form
        return render_template("admin/equipment/list.html", **ctx)

    @admin_bp.route("/equipment/create", methods=["GET", "POST"])
    @can_manage_equipment
    def equipment_create():
        active_tab = request.args.get("tab", "general")
        ctx = EquipmentAdminService.get_form_context(equipment_id=None, active_tab=active_tab)
        form = EquipmentForm()
        _populate_equipment_form(form, ctx)

        if form.validate_on_submit():
            dto = EquipmentAdminService.dto_from_form(
                form,
                gallery_paths=request.form.getlist("gallery_paths"),
            )
            result = EquipmentAdminService.save_equipment(dto, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success and result.equipment_id:
                return redirect(url_for("admin.equipment_edit", equipment_id=result.equipment_id))

        ctx["form"] = form
        ctx["delete_form"] = EquipmentDeleteForm()
        return render_template("admin/equipment/form.html", **ctx)

    @admin_bp.route("/equipment/<int:equipment_id>/edit", methods=["GET", "POST"])
    @can_manage_equipment
    def equipment_edit(equipment_id: int):
        active_tab = request.args.get("tab", "general")
        ctx = EquipmentAdminService.get_form_context(equipment_id=equipment_id, active_tab=active_tab)
        if not ctx:
            abort(404)

        form = EquipmentForm()
        _populate_equipment_form(form, ctx)
        if request.method == "GET":
            _fill_form_from_equipment(form, ctx["equipment"])
            form.specifications.data = ctx.get("specifications_text", "")

        if form.validate_on_submit():
            dto = EquipmentAdminService.dto_from_form(
                form,
                gallery_paths=request.form.getlist("gallery_paths"),
            )
            result = EquipmentAdminService.save_equipment(dto, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success:
                return redirect(url_for("admin.equipment_edit", equipment_id=equipment_id, tab=active_tab))

        ctx["form"] = form
        ctx["delete_form"] = EquipmentDeleteForm()
        return render_template("admin/equipment/form.html", **ctx)

    @admin_bp.route("/equipment/<int:equipment_id>/delete", methods=["POST"])
    @can_manage_equipment
    def equipment_delete(equipment_id: int):
        form = EquipmentDeleteForm()
        if form.validate_on_submit():
            result = EquipmentAdminService.delete_equipment(
                equipment_id, ip_address=request.remote_addr
            )
            flash(result.message, "success" if result.success else "danger")
            if result.success:
                return redirect(url_for("admin.equipment_list", deleted=1))
        return redirect(url_for("admin.equipment_edit", equipment_id=equipment_id))

    @admin_bp.route("/equipment/<int:equipment_id>/restore", methods=["POST"])
    @can_manage_equipment
    def equipment_restore(equipment_id: int):
        result = EquipmentAdminService.restore_equipment(
            equipment_id, ip_address=request.remote_addr
        )
        flash(result.message, "success" if result.success else "danger")
        return redirect(url_for("admin.equipment_list"))

    @admin_bp.route("/equipment/bulk", methods=["POST"])
    @can_manage_equipment
    def equipment_bulk():
        form = EquipmentBulkForm()
        from app.constants.equipment_admin import BULK_ACTIONS

        form.action.choices = list(BULK_ACTIONS.items())
        if not form.validate_on_submit():
            flash("Invalid bulk action.", "danger")
            return redirect(url_for("admin.equipment_list"))

        ids = [int(x) for x in request.form.getlist("equipment_ids") if x.isdigit()]
        result = EquipmentAdminService.bulk_action(
            ids, form.action.data, ip_address=request.remote_addr
        )
        flash(result.message, "success" if result.success else "danger")
        return redirect(url_for("admin.equipment_list"))
