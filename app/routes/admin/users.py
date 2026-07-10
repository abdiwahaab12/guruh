"""Enterprise Users & RBAC admin routes — Step 25."""

from __future__ import annotations

from flask import abort, flash, redirect, render_template, request, url_for

from app.constants.users_admin import TAB_USERS, USER_BULK_ACTIONS
from app.forms.users_forms import ResetPasswordForm, RolePermissionsForm, SessionActionForm, UserForm, UsersBulkForm
from app.services.users_admin_service import UsersAdminService
from app.utils.permissions import super_admin_required


def register_users_routes(admin_bp) -> None:
    """Register users and RBAC administration routes."""

    @admin_bp.route("/users")
    @admin_bp.route("/users/dashboard")
    @super_admin_required
    def users_dashboard():
        tab = request.args.get("tab", TAB_USERS)
        ctx = UsersAdminService.get_dashboard_context(
            tab=tab,
            q=request.args.get("q", ""),
            role_slug=request.args.get("role_slug", ""),
            status=request.args.get("status", ""),
            action=request.args.get("action", ""),
            sort=request.args.get("sort", "newest"),
            page=request.args.get("page", 1, type=int),
        )
        bulk_form = UsersBulkForm()
        bulk_form.action.choices = list(USER_BULK_ACTIONS.items())
        ctx["bulk_form"] = bulk_form
        ctx["session_action_form"] = SessionActionForm()
        return render_template("admin/users/dashboard.html", **ctx)

    @admin_bp.route("/users/create", methods=["GET", "POST"])
    @super_admin_required
    def users_create():
        ctx = UsersAdminService.get_user_form_context(user_id=None)
        if not ctx:
            abort(404)
        form = UserForm()
        form.role_id.choices = [(r.id, r.name) for r in ctx["roles"]]

        if form.validate_on_submit():
            data = request.form.to_dict(flat=True)
            result = UsersAdminService.save_user(data, user_id=None, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success and result.redirect_url:
                return redirect(result.redirect_url)

        ctx["form"] = form
        return render_template("admin/users/form.html", **ctx)

    @admin_bp.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
    @super_admin_required
    def users_edit(user_id: int):
        ctx = UsersAdminService.get_user_form_context(user_id=user_id)
        if not ctx:
            abort(404)

        form = UserForm()
        form.role_id.choices = [(r.id, r.name) for r in ctx["roles"]]
        admin_user = ctx["admin_user"]
        reset_form = ResetPasswordForm()

        if request.method == "GET" and admin_user:
            form.user_id.data = admin_user.id
            form.email.data = admin_user.email
            form.first_name.data = admin_user.first_name
            form.last_name.data = admin_user.last_name
            form.role_id.data = admin_user.role_id
            form.is_active.data = admin_user.is_active

        if form.validate_on_submit() and form.submit.data:
            data = request.form.to_dict(flat=True)
            result = UsersAdminService.save_user(data, user_id=user_id, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success and result.redirect_url:
                return redirect(result.redirect_url)

        ctx["form"] = form
        ctx["reset_form"] = reset_form
        return render_template("admin/users/form.html", **ctx)

    @admin_bp.route("/users/<int:user_id>/reset-password", methods=["POST"])
    @super_admin_required
    def users_reset_password(user_id: int):
        form = ResetPasswordForm()
        if form.validate_on_submit():
            result = UsersAdminService.reset_password(
                user_id,
                form.new_password.data or "",
                ip_address=request.remote_addr,
            )
            flash(result.message, "success" if result.success else "danger")
        else:
            flash("Invalid password.", "danger")
        return redirect(url_for("admin.users_edit", user_id=user_id))

    @admin_bp.route("/users/<int:user_id>/reset-link", methods=["POST"])
    @super_admin_required
    def users_reset_link(user_id: int):
        result = UsersAdminService.admin_reset_link(user_id, ip_address=request.remote_addr)
        flash(result.message, "success" if result.success else "danger")
        if result.reset_url:
            flash(f"Reset link: {result.reset_url}", "info")
        return redirect(url_for("admin.users_edit", user_id=user_id))

    @admin_bp.route("/users/bulk", methods=["POST"])
    @super_admin_required
    def users_bulk():
        form = UsersBulkForm()
        form.action.choices = list(USER_BULK_ACTIONS.items())
        tab = request.form.get("tab", TAB_USERS)
        if not form.validate_on_submit():
            flash("Invalid bulk action.", "danger")
            return redirect(url_for("admin.users_dashboard", tab=tab))

        ids = [int(x) for x in request.form.getlist("item_ids") if x.isdigit()]
        result = UsersAdminService.bulk_users(ids, form.action.data, ip_address=request.remote_addr)
        flash(result.message, "success" if result.success else "danger")
        return redirect(url_for("admin.users_dashboard", tab=tab))

    @admin_bp.route("/users/roles/<int:role_id>/edit", methods=["GET", "POST"])
    @super_admin_required
    def users_role_edit(role_id: int):
        ctx = UsersAdminService.get_role_edit_context(role_id)
        if not ctx:
            abort(404)
        form = RolePermissionsForm()
        selected = set(ctx["role"].permission_slugs)

        if form.validate_on_submit():
            permission_ids = [int(x) for x in request.form.getlist("permission_ids") if x.isdigit()]
            result = UsersAdminService.save_role_permissions(role_id, permission_ids, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success and result.redirect_url:
                return redirect(result.redirect_url)

        ctx["form"] = form
        ctx["selected_permissions"] = selected
        return render_template("admin/users/role_form.html", **ctx)

    @admin_bp.route("/users/sessions/<int:session_id>/revoke", methods=["POST"])
    @super_admin_required
    def users_session_revoke(session_id: int):
        form = SessionActionForm()
        if not form.validate_on_submit():
            flash("Invalid request.", "danger")
            return redirect(url_for("admin.users_dashboard", tab="sessions"))
        result = UsersAdminService.revoke_session(session_id, ip_address=request.remote_addr)
        flash(result.message, "success" if result.success else "danger")
        return redirect(url_for("admin.users_dashboard", tab="sessions"))
