"""Enterprise Careers Management admin routes — Step 22."""

from __future__ import annotations

from flask import abort, flash, redirect, render_template, request, url_for

from app.forms.careers_forms import CareersBulkForm, CareersDeleteForm, JobListingForm
from app.services.careers_admin_service import CareersAdminService
from app.utils.permissions import can_manage_careers


def _fill_form_from_job(form: JobListingForm, job) -> None:
    form.job_id.data = job.id
    form.title.data = job.title
    form.slug.data = job.slug
    form.department.data = job.department
    form.location.data = job.location
    form.employment_type.data = job.employment_type
    form.status.data = job.status
    form.short_description.data = job.short_description
    form.sort_order.data = job.sort_order
    form.is_active.data = job.is_active
    form.description.data = job.description
    form.requirements.data = job.requirements
    form.experience_required.data = job.experience_required
    form.image.data = job.image
    form.responsibilities.data = "\n".join(job.responsibilities)
    form.qualifications.data = "\n".join(job.qualifications)
    form.skills.data = "\n".join(job.skills)
    form.benefits.data = "\n".join(job.benefits)
    form.deadline.data = job.deadline
    form.accept_applications.data = job.accept_applications
    form.is_featured.data = job.is_featured
    form.notify_email.data = job.notify_email
    form.auto_reply_enabled.data = job.auto_reply_enabled
    form.auto_reply_message.data = job.auto_reply_message
    form.meta_title.data = job.meta_title
    form.meta_description.data = job.meta_description
    form.og_image.data = job.og_image
    form.canonical_url.data = job.canonical_url


def register_careers_routes(admin_bp) -> None:
    """Register careers CRUD routes."""

    @admin_bp.route("/careers")
    @can_manage_careers
    def careers_dashboard():
        return render_template(
            "admin/careers/dashboard.html",
            **CareersAdminService.get_dashboard_context(),
        )

    @admin_bp.route("/careers/list")
    @can_manage_careers
    def careers_list():
        ctx = CareersAdminService.get_list_context(
            q=request.args.get("q", ""),
            department=request.args.get("department", ""),
            employment_type=request.args.get("employment_type", ""),
            location=request.args.get("location", ""),
            status=request.args.get("status", ""),
            sort=request.args.get("sort", "date_desc"),
            page=request.args.get("page", 1, type=int),
            include_deleted=request.args.get("deleted") == "1",
        )
        bulk_form = CareersBulkForm()
        bulk_form.action.choices = list(ctx["bulk_actions"].items())
        ctx["bulk_form"] = bulk_form
        return render_template("admin/careers/list.html", **ctx)

    @admin_bp.route("/careers/create", methods=["GET", "POST"])
    @can_manage_careers
    def careers_create():
        active_tab = request.args.get("tab", "general")
        ctx = CareersAdminService.get_form_context(job_id=None, active_tab=active_tab)
        form = JobListingForm()

        if form.validate_on_submit():
            dto = CareersAdminService.dto_from_form(form)
            result = CareersAdminService.save_job(dto, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success and result.job_id:
                return redirect(url_for("admin.careers_edit", job_id=result.job_id))

        ctx["form"] = form
        ctx["delete_form"] = CareersDeleteForm()
        return render_template("admin/careers/form.html", **ctx)

    @admin_bp.route("/careers/<int:job_id>/edit", methods=["GET", "POST"])
    @can_manage_careers
    def careers_edit(job_id: int):
        active_tab = request.args.get("tab", "general")
        ctx = CareersAdminService.get_form_context(job_id=job_id, active_tab=active_tab)
        if not ctx:
            abort(404)

        form = JobListingForm()
        if request.method == "GET":
            _fill_form_from_job(form, ctx["job"])

        if form.validate_on_submit():
            dto = CareersAdminService.dto_from_form(form)
            result = CareersAdminService.save_job(dto, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success:
                return redirect(url_for("admin.careers_edit", job_id=job_id, tab=active_tab))

        ctx["form"] = form
        ctx["delete_form"] = CareersDeleteForm()
        return render_template("admin/careers/form.html", **ctx)

    @admin_bp.route("/careers/<int:job_id>/delete", methods=["POST"])
    @can_manage_careers
    def careers_delete(job_id: int):
        form = CareersDeleteForm()
        if form.validate_on_submit():
            result = CareersAdminService.delete_job(job_id, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success:
                return redirect(url_for("admin.careers_list", deleted=1))
        return redirect(url_for("admin.careers_edit", job_id=job_id))

    @admin_bp.route("/careers/<int:job_id>/restore", methods=["POST"])
    @can_manage_careers
    def careers_restore(job_id: int):
        result = CareersAdminService.restore_job(job_id, ip_address=request.remote_addr)
        flash(result.message, "success" if result.success else "danger")
        return redirect(url_for("admin.careers_list"))

    @admin_bp.route("/careers/bulk", methods=["POST"])
    @can_manage_careers
    def careers_bulk():
        form = CareersBulkForm()
        from app.constants.careers_admin import BULK_ACTIONS

        form.action.choices = list(BULK_ACTIONS.items())
        if not form.validate_on_submit():
            flash("Invalid bulk action.", "danger")
            return redirect(url_for("admin.careers_list"))

        ids = [int(x) for x in request.form.getlist("job_ids") if x.isdigit()]
        result = CareersAdminService.bulk_action(ids, form.action.data, ip_address=request.remote_addr)
        flash(result.message, "success" if result.success else "danger")
        return redirect(url_for("admin.careers_list"))
