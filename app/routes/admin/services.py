"""Enterprise Services Management admin routes — Step 18."""

from __future__ import annotations

from flask import abort, flash, redirect, render_template, request, url_for

from app.forms.services_forms import ServiceBulkForm, ServiceDeleteForm, ServiceForm
from app.services.services_admin_service import ServicesAdminService
from app.utils.permissions import can_manage_services


def _populate_service_form(form: ServiceForm, ctx: dict) -> None:
    form.related_project_ids.choices = [(p.id, p.title) for p in ctx.get("projects", [])]
    form.related_service_slugs.choices = [
        (s.slug, s.title) for s in ctx.get("related_services", [])
    ]
    form.team_member_ids.choices = [(m.id, m.name) for m in ctx.get("team_members", [])]


def _fill_form_from_service(form: ServiceForm, service) -> None:
    form.service_id.data = service.id
    form.title.data = service.title
    form.slug.data = service.slug
    form.short_description.data = service.short_description
    form.description.data = service.description
    form.icon.data = service.icon
    form.image.data = service.image
    form.sort_order.data = service.sort_order
    form.is_featured.data = service.is_featured
    form.is_active.data = service.is_active
    form.scope_of_work.data = "\n".join(service.scope_of_work)
    form.benefits.data = "\n".join(service.benefits)
    form.equipment.data = "\n".join(service.equipment)
    form.team_member_ids.data = service.team_member_ids
    form.related_project_ids.data = service.related_project_ids
    form.related_service_slugs.data = service.related_service_slugs
    form.meta_title.data = service.meta_title
    form.meta_description.data = service.meta_description
    form.og_image.data = service.og_image
    form.canonical_url.data = service.canonical_url


def register_services_routes(admin_bp) -> None:
    """Register services CRUD routes."""

    @admin_bp.route("/services")
    @can_manage_services
    def services_dashboard():
        return render_template(
            "admin/services/dashboard.html",
            **ServicesAdminService.get_dashboard_context(),
        )

    @admin_bp.route("/services/list")
    @can_manage_services
    def services_list():
        ctx = ServicesAdminService.get_list_context(
            q=request.args.get("q", ""),
            featured=request.args.get("featured", ""),
            status=request.args.get("status", ""),
            sort=request.args.get("sort", "date_desc"),
            page=request.args.get("page", 1, type=int),
            include_deleted=request.args.get("deleted") == "1",
        )
        bulk_form = ServiceBulkForm()
        bulk_form.action.choices = list(ctx["bulk_actions"].items())
        ctx["bulk_form"] = bulk_form
        return render_template("admin/services/list.html", **ctx)

    @admin_bp.route("/services/create", methods=["GET", "POST"])
    @can_manage_services
    def services_create():
        active_tab = request.args.get("tab", "general")
        ctx = ServicesAdminService.get_form_context(service_id=None, active_tab=active_tab)
        form = ServiceForm()
        _populate_service_form(form, ctx)

        if form.validate_on_submit():
            dto = ServicesAdminService.dto_from_form(
                form,
                gallery_paths=request.form.getlist("gallery_paths"),
            )
            result = ServicesAdminService.save_service(dto, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success and result.service_id:
                return redirect(url_for("admin.services_edit", service_id=result.service_id))

        ctx["form"] = form
        ctx["delete_form"] = ServiceDeleteForm()
        return render_template("admin/services/form.html", **ctx)

    @admin_bp.route("/services/<int:service_id>/edit", methods=["GET", "POST"])
    @can_manage_services
    def services_edit(service_id: int):
        active_tab = request.args.get("tab", "general")
        ctx = ServicesAdminService.get_form_context(service_id=service_id, active_tab=active_tab)
        if not ctx:
            abort(404)

        form = ServiceForm()
        _populate_service_form(form, ctx)
        if request.method == "GET":
            _fill_form_from_service(form, ctx["service"])

        if form.validate_on_submit():
            dto = ServicesAdminService.dto_from_form(
                form,
                gallery_paths=request.form.getlist("gallery_paths"),
            )
            result = ServicesAdminService.save_service(dto, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success:
                return redirect(url_for("admin.services_edit", service_id=service_id, tab=active_tab))

        ctx["form"] = form
        ctx["delete_form"] = ServiceDeleteForm()
        return render_template("admin/services/form.html", **ctx)

    @admin_bp.route("/services/<int:service_id>/delete", methods=["POST"])
    @can_manage_services
    def services_delete(service_id: int):
        form = ServiceDeleteForm()
        if form.validate_on_submit():
            result = ServicesAdminService.delete_service(service_id, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success:
                return redirect(url_for("admin.services_list", deleted=1))
        return redirect(url_for("admin.services_edit", service_id=service_id))

    @admin_bp.route("/services/<int:service_id>/restore", methods=["POST"])
    @can_manage_services
    def services_restore(service_id: int):
        result = ServicesAdminService.restore_service(service_id, ip_address=request.remote_addr)
        flash(result.message, "success" if result.success else "danger")
        return redirect(url_for("admin.services_list"))

    @admin_bp.route("/services/bulk", methods=["POST"])
    @can_manage_services
    def services_bulk():
        form = ServiceBulkForm()
        from app.constants.services_admin import BULK_ACTIONS

        form.action.choices = list(BULK_ACTIONS.items())
        if not form.validate_on_submit():
            flash("Invalid bulk action.", "danger")
            return redirect(url_for("admin.services_list"))

        ids = [int(x) for x in request.form.getlist("service_ids") if x.isdigit()]
        result = ServicesAdminService.bulk_action(
            ids, form.action.data, ip_address=request.remote_addr
        )
        flash(result.message, "success" if result.success else "danger")
        return redirect(url_for("admin.services_list"))
