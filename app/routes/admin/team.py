"""Enterprise Team Management admin routes — Step 20."""

from __future__ import annotations

from flask import abort, flash, redirect, render_template, request, url_for

from app.forms.team_forms import TeamBulkForm, TeamDeleteForm, TeamMemberForm
from app.services.team_admin_service import TeamAdminService
from app.utils.permissions import can_manage_team


def _populate_team_form(form: TeamMemberForm, ctx: dict) -> None:
    form.related_project_ids.choices = [(p.id, p.title) for p in ctx.get("projects", [])]
    form.related_service_slugs.choices = [(s.slug, s.title) for s in ctx.get("services", [])]
    form.related_equipment_ids.choices = [
        (e.id, e.name) for e in ctx.get("equipment_list", [])
    ]


def _fill_form_from_member(form: TeamMemberForm, member) -> None:
    form.team_member_id.data = member.id
    form.name.data = member.name
    form.slug.data = member.slug
    form.position.data = member.position
    form.department.data = member.department
    form.member_type.data = member.member_type
    form.email.data = member.email
    form.phone.data = member.phone
    form.sort_order.data = member.sort_order
    form.is_featured.data = member.is_featured
    form.is_active.data = member.is_active
    form.years_experience.data = member.years_experience
    form.education.data = member.education
    form.experience_summary.data = member.experience_summary
    form.bio.data = member.bio
    form.photo.data = member.photo
    form.related_project_ids.data = member.related_project_ids
    form.related_service_slugs.data = member.related_service_slugs
    form.related_equipment_ids.data = member.related_equipment_ids
    form.meta_title.data = member.meta_title
    form.meta_description.data = member.meta_description
    form.og_image.data = member.og_image
    form.canonical_url.data = member.canonical_url


def register_team_routes(admin_bp) -> None:
    """Register team CRUD routes."""

    @admin_bp.route("/team")
    @can_manage_team
    def team_dashboard():
        return render_template(
            "admin/team/dashboard.html",
            **TeamAdminService.get_dashboard_context(),
        )

    @admin_bp.route("/team/list")
    @can_manage_team
    def team_list():
        ctx = TeamAdminService.get_list_context(
            q=request.args.get("q", ""),
            department=request.args.get("department", ""),
            position=request.args.get("position", ""),
            member_type=request.args.get("member_type", ""),
            featured=request.args.get("featured", ""),
            status=request.args.get("status", ""),
            sort=request.args.get("sort", "date_desc"),
            page=request.args.get("page", 1, type=int),
            include_deleted=request.args.get("deleted") == "1",
        )
        bulk_form = TeamBulkForm()
        bulk_form.action.choices = list(ctx["bulk_actions"].items())
        ctx["bulk_form"] = bulk_form
        return render_template("admin/team/list.html", **ctx)

    @admin_bp.route("/team/create", methods=["GET", "POST"])
    @can_manage_team
    def team_create():
        active_tab = request.args.get("tab", "general")
        ctx = TeamAdminService.get_form_context(member_id=None, active_tab=active_tab)
        form = TeamMemberForm()
        _populate_team_form(form, ctx)

        if form.validate_on_submit():
            dto = TeamAdminService.dto_from_form(
                form,
                gallery_paths=request.form.getlist("gallery_paths"),
            )
            result = TeamAdminService.save_member(dto, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success and result.team_member_id:
                return redirect(url_for("admin.team_edit", team_member_id=result.team_member_id))

        ctx["form"] = form
        ctx["delete_form"] = TeamDeleteForm()
        return render_template("admin/team/form.html", **ctx)

    @admin_bp.route("/team/<int:team_member_id>/edit", methods=["GET", "POST"])
    @can_manage_team
    def team_edit(team_member_id: int):
        active_tab = request.args.get("tab", "general")
        ctx = TeamAdminService.get_form_context(member_id=team_member_id, active_tab=active_tab)
        if not ctx:
            abort(404)

        form = TeamMemberForm()
        _populate_team_form(form, ctx)
        if request.method == "GET":
            _fill_form_from_member(form, ctx["member"])
            form.social_links.data = ctx.get("social_links_text", "")

        if form.validate_on_submit():
            dto = TeamAdminService.dto_from_form(
                form,
                gallery_paths=request.form.getlist("gallery_paths"),
            )
            result = TeamAdminService.save_member(dto, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success:
                return redirect(
                    url_for("admin.team_edit", team_member_id=team_member_id, tab=active_tab)
                )

        ctx["form"] = form
        ctx["delete_form"] = TeamDeleteForm()
        return render_template("admin/team/form.html", **ctx)

    @admin_bp.route("/team/<int:team_member_id>/delete", methods=["POST"])
    @can_manage_team
    def team_delete(team_member_id: int):
        form = TeamDeleteForm()
        if form.validate_on_submit():
            result = TeamAdminService.delete_member(team_member_id, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success:
                return redirect(url_for("admin.team_list", deleted=1))
        return redirect(url_for("admin.team_edit", team_member_id=team_member_id))

    @admin_bp.route("/team/<int:team_member_id>/restore", methods=["POST"])
    @can_manage_team
    def team_restore(team_member_id: int):
        result = TeamAdminService.restore_member(team_member_id, ip_address=request.remote_addr)
        flash(result.message, "success" if result.success else "danger")
        return redirect(url_for("admin.team_list"))

    @admin_bp.route("/team/bulk", methods=["POST"])
    @can_manage_team
    def team_bulk():
        form = TeamBulkForm()
        from app.constants.team_admin import BULK_ACTIONS

        form.action.choices = list(BULK_ACTIONS.items())
        if not form.validate_on_submit():
            flash("Invalid bulk action.", "danger")
            return redirect(url_for("admin.team_list"))

        ids = [int(x) for x in request.form.getlist("team_member_ids") if x.isdigit()]
        result = TeamAdminService.bulk_action(ids, form.action.data, ip_address=request.remote_addr)
        flash(result.message, "success" if result.success else "danger")
        return redirect(url_for("admin.team_list"))
