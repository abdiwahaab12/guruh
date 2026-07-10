"""Enterprise Projects Management admin routes — Step 17."""

from __future__ import annotations

from flask import abort, flash, redirect, render_template, request, url_for

from app.forms.projects_forms import ProjectBulkForm, ProjectDeleteForm, ProjectForm
from app.providers.projects_admin_provider import ProjectsAdminProvider
from app.services.projects_admin_service import ProjectsAdminService
from app.utils.permissions import can_manage_projects


def _populate_project_form(form: ProjectForm, ctx: dict) -> None:
    services = ctx.get("services", [])
    form.service_slugs.choices = [(s.slug, s.title) for s in services]
    form.related_service_slugs.choices = [(s.slug, s.title) for s in services]
    form.team_member_ids.choices = [(m.id, m.name) for m in ctx.get("team_members", [])]
    form.related_project_ids.choices = [(p.id, p.title) for p in ctx.get("related_projects", [])]


def _fill_form_from_project(form: ProjectForm, project) -> None:
    form.project_id.data = project.id
    form.title.data = project.title
    form.slug.data = project.slug
    form.description.data = project.description
    form.overview.data = project.overview
    form.consultant.data = project.consultant
    form.duration.data = project.duration
    form.completion_date.data = project.completion_date
    form.completion_year.data = project.completion_year
    form.sort_order.data = project.sort_order
    form.is_featured.data = project.is_featured
    form.is_active.data = project.is_active
    form.location.data = project.location
    form.country.data = project.country
    form.county.data = project.county
    form.status.data = project.status
    form.client.data = project.client
    form.category.data = project.category
    form.service_slugs.data = project.service_slugs
    form.equipment.data = "\n".join(project.equipment)
    form.team_member_ids.data = project.team_member_ids
    form.meta_title.data = project.meta_title
    form.meta_description.data = project.meta_description
    form.og_image.data = project.og_image
    form.canonical_url.data = project.canonical_url
    form.cover_image.data = project.cover_image
    form.challenges.data = "\n".join(project.challenges)
    form.solutions.data = "\n".join(project.solutions)
    form.scope_of_work.data = "\n".join(project.scope_of_work)
    form.timeline.data = ProjectsAdminProvider.timeline_to_text(project.timeline)
    form.related_project_ids.data = project.related_project_ids
    form.related_service_slugs.data = project.related_service_slugs


def register_projects_routes(admin_bp) -> None:
    """Register projects CRUD routes."""

    @admin_bp.route("/projects")
    @can_manage_projects
    def projects_dashboard():
        return render_template(
            "admin/projects/dashboard.html",
            **ProjectsAdminService.get_dashboard_context(),
        )

    @admin_bp.route("/projects/list")
    @can_manage_projects
    def projects_list():
        ctx = ProjectsAdminService.get_list_context(
            q=request.args.get("q", ""),
            country=request.args.get("country", ""),
            county=request.args.get("county", ""),
            status=request.args.get("status", ""),
            category=request.args.get("category", ""),
            service=request.args.get("service", ""),
            client=request.args.get("client", ""),
            year=request.args.get("year", ""),
            sort=request.args.get("sort", "date_desc"),
            page=request.args.get("page", 1, type=int),
            include_deleted=request.args.get("deleted") == "1",
        )
        bulk_form = ProjectBulkForm()
        bulk_form.action.choices = list(ctx["bulk_actions"].items())
        ctx["bulk_form"] = bulk_form
        return render_template("admin/projects/list.html", **ctx)

    @admin_bp.route("/projects/create", methods=["GET", "POST"])
    @can_manage_projects
    def projects_create():
        active_tab = request.args.get("tab", "general")
        ctx = ProjectsAdminService.get_form_context(project_id=None, active_tab=active_tab)
        form = ProjectForm()
        _populate_project_form(form, ctx)

        if form.validate_on_submit():
            dto = ProjectsAdminService.dto_from_form(
                form,
                gallery_paths=request.form.getlist("gallery_paths"),
                document_paths=request.form.getlist("document_paths"),
            )
            result = ProjectsAdminService.save_project(dto, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success and result.project_id:
                return redirect(url_for("admin.projects_edit", project_id=result.project_id))

        ctx["form"] = form
        ctx["delete_form"] = ProjectDeleteForm()
        return render_template("admin/projects/form.html", **ctx)

    @admin_bp.route("/projects/<int:project_id>/edit", methods=["GET", "POST"])
    @can_manage_projects
    def projects_edit(project_id: int):
        active_tab = request.args.get("tab", "general")
        ctx = ProjectsAdminService.get_form_context(project_id=project_id, active_tab=active_tab)
        if not ctx:
            abort(404)

        form = ProjectForm()
        _populate_project_form(form, ctx)
        if request.method == "GET":
            _fill_form_from_project(form, ctx["project"])
            form.timeline.data = ctx.get("timeline_text", "")

        if form.validate_on_submit():
            dto = ProjectsAdminService.dto_from_form(
                form,
                gallery_paths=request.form.getlist("gallery_paths"),
                document_paths=request.form.getlist("document_paths"),
            )
            result = ProjectsAdminService.save_project(dto, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success:
                return redirect(url_for("admin.projects_edit", project_id=project_id, tab=active_tab))

        ctx["form"] = form
        ctx["delete_form"] = ProjectDeleteForm()
        return render_template("admin/projects/form.html", **ctx)

    @admin_bp.route("/projects/<int:project_id>/delete", methods=["POST"])
    @can_manage_projects
    def projects_delete(project_id: int):
        form = ProjectDeleteForm()
        if form.validate_on_submit():
            result = ProjectsAdminService.delete_project(project_id, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success:
                return redirect(url_for("admin.projects_list", deleted=1))
        return redirect(url_for("admin.projects_edit", project_id=project_id))

    @admin_bp.route("/projects/<int:project_id>/restore", methods=["POST"])
    @can_manage_projects
    def projects_restore(project_id: int):
        result = ProjectsAdminService.restore_project(project_id, ip_address=request.remote_addr)
        flash(result.message, "success" if result.success else "danger")
        return redirect(url_for("admin.projects_list"))

    @admin_bp.route("/projects/bulk", methods=["POST"])
    @can_manage_projects
    def projects_bulk():
        form = ProjectBulkForm()
        from app.constants.projects_admin import BULK_ACTIONS

        form.action.choices = list(BULK_ACTIONS.items())
        if not form.validate_on_submit():
            flash("Invalid bulk action.", "danger")
            return redirect(url_for("admin.projects_list"))

        ids = [int(x) for x in request.form.getlist("project_ids") if x.isdigit()]
        result = ProjectsAdminService.bulk_action(
            ids, form.action.data, ip_address=request.remote_addr
        )
        flash(result.message, "success" if result.success else "danger")
        return redirect(url_for("admin.projects_list"))
