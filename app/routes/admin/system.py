"""Enterprise System Administration routes — Step 27."""

from __future__ import annotations

from flask import Response, flash, redirect, render_template, request, url_for

from app.constants.system_admin import DEFAULT_TAB, LOG_TAB_APPLICATION, TAB_MAINTENANCE
from app.forms.system_forms import BackupRestoreForm, LogSearchForm, MaintenanceForm
from app.services.system_admin_service import SystemAdminService
from app.utils.permissions import super_admin_required
from app.utils.system_backup import get_backup_path


def register_system_routes(admin_bp) -> None:
    """Register system administration routes — super admin only."""

    @admin_bp.route("/system")
    @admin_bp.route("/system/dashboard")
    @super_admin_required
    def system_dashboard():
        tab = request.args.get("tab", DEFAULT_TAB)
        ctx = SystemAdminService.get_dashboard_context(
            tab=tab,
            log_tab=request.args.get("log_tab", LOG_TAB_APPLICATION),
            q=request.args.get("q", ""),
            page=request.args.get("page", 1, type=int),
        )
        ctx["maintenance_form"] = MaintenanceForm()
        ctx["maintenance_form"].message.data = ctx["maintenance"].message
        ctx["restore_form"] = BackupRestoreForm()
        ctx["log_search_form"] = LogSearchForm()
        ctx["log_search_form"].q.data = ctx["log_query"]
        return render_template("admin/system/dashboard.html", **ctx)

    @admin_bp.route("/system/maintenance/enable", methods=["POST"])
    @super_admin_required
    def system_maintenance_enable():
        form = MaintenanceForm()
        if form.validate_on_submit() and form.submit_enable.data:
            result = SystemAdminService.enable_maintenance(
                message=form.message.data or "",
                ip_address=request.remote_addr,
            )
            flash(result.message, "success" if result.success else "danger")
        return redirect(url_for("admin.system_dashboard", tab=TAB_MAINTENANCE))

    @admin_bp.route("/system/maintenance/disable", methods=["POST"])
    @super_admin_required
    def system_maintenance_disable():
        form = MaintenanceForm()
        if form.validate_on_submit() and form.submit_disable.data:
            result = SystemAdminService.disable_maintenance(ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
        return redirect(url_for("admin.system_dashboard", tab=TAB_MAINTENANCE))

    @admin_bp.route("/system/maintenance/message", methods=["POST"])
    @super_admin_required
    def system_maintenance_message():
        form = MaintenanceForm()
        if form.validate_on_submit() and form.submit_message.data:
            result = SystemAdminService.update_maintenance_message(
                message=form.message.data or "",
                ip_address=request.remote_addr,
            )
            flash(result.message, "success" if result.success else "danger")
        return redirect(url_for("admin.system_dashboard", tab=TAB_MAINTENANCE))

    @admin_bp.route("/system/backup/create", methods=["POST"])
    @super_admin_required
    def system_backup_create():
        from flask_wtf import FlaskForm

        form = FlaskForm()
        if form.validate_on_submit():
            result = SystemAdminService.create_backup(ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
        return redirect(url_for("admin.system_dashboard", tab="backup"))

    @admin_bp.route("/system/backup/download/<path:filename>")
    @super_admin_required
    def system_backup_download(filename: str):
        from flask_login import current_user

        from app.providers.system_admin_provider import SystemAdminProvider

        path = get_backup_path(filename)
        if not path:
            flash("Backup file not found.", "danger")
            return redirect(url_for("admin.system_dashboard", tab="backup"))

        SystemAdminProvider.record_audit(
            user_id=current_user.id,
            action="system.backup.download",
            resource_type="system",
            resource_id=filename,
            details=f"Downloaded backup {filename}",
            ip_address=request.remote_addr,
        )
        SystemAdminProvider.commit()

        return Response(
            path.read_bytes(),
            mimetype="application/octet-stream",
            headers={"Content-Disposition": f'attachment; filename="{path.name}"'},
        )

    @admin_bp.route("/system/backup/restore", methods=["POST"])
    @super_admin_required
    def system_backup_restore():
        form = BackupRestoreForm()
        if form.validate_on_submit() and form.confirm.data.strip().upper() == "RESTORE":
            result = SystemAdminService.restore_backup(
                filename=form.filename.data,
                ip_address=request.remote_addr,
            )
            flash(result.message, "success" if result.success else "danger")
        else:
            flash("Restore cancelled — type RESTORE to confirm.", "warning")
        return redirect(url_for("admin.system_dashboard", tab="backup"))

    @admin_bp.route("/system/health/run", methods=["POST"])
    @super_admin_required
    def system_health_run():
        from flask_wtf import FlaskForm

        form = FlaskForm()
        if form.validate_on_submit():
            result = SystemAdminService.run_health_checks(ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "warning")
        return redirect(url_for("admin.system_dashboard", tab="health"))

    @admin_bp.route("/system/cache/clear", methods=["POST"])
    @super_admin_required
    def system_cache_clear():
        from flask_wtf import FlaskForm

        form = FlaskForm()
        if form.validate_on_submit():
            result = SystemAdminService.clear_cache(ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
        return redirect(url_for("admin.system_dashboard", tab="cache"))

    @admin_bp.route("/system/cache/rebuild", methods=["POST"])
    @super_admin_required
    def system_cache_rebuild():
        from flask_wtf import FlaskForm

        form = FlaskForm()
        if form.validate_on_submit():
            result = SystemAdminService.rebuild_cache(ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
        return redirect(url_for("admin.system_dashboard", tab="cache"))
