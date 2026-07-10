"""Admin authentication routes — login, logout, password reset."""

from __future__ import annotations

from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.forms.auth_forms import ForgotPasswordForm, LoginForm, ResetPasswordForm
from app.services.auth_service import AuthService


def register_auth_routes(admin_bp) -> None:
    """Register authentication routes on the admin blueprint."""

    @admin_bp.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("admin.dashboard"))

        form = LoginForm()
        if form.validate_on_submit():
            result = AuthService.authenticate(
                form.email.data,
                form.password.data,
                ip_address=request.remote_addr,
                user_agent=request.headers.get("User-Agent"),
                remember=form.remember.data,
            )
            if result.success:
                user = AuthService.get_user_by_id(result.user.id)
                login_user(user, remember=form.remember.data)
                session.pop("_last_activity", None)
                AuthService.touch_session(session)
                flash("Welcome back! You are now signed in.", "success")
                next_url = request.args.get("next")
                if next_url and next_url.startswith("/admin"):
                    return redirect(next_url)
                return redirect(url_for("admin.dashboard"))
            flash(result.message, "danger")

        return render_template("admin/login.html", form=form)

    @admin_bp.route("/logout")
    @login_required
    def logout():
        AuthService.logout_user(current_user)
        logout_user()
        session.clear()
        flash("You have been signed out.", "info")
        return redirect(url_for("admin.login"))

    @admin_bp.route("/forgot-password", methods=["GET", "POST"])
    def forgot_password():
        if current_user.is_authenticated:
            return redirect(url_for("admin.dashboard"))

        form = ForgotPasswordForm()
        if form.validate_on_submit():
            result = AuthService.request_password_reset(
                form.email.data,
                ip_address=request.remote_addr,
            )
            flash(result.message, "success" if result.success else "danger")
            if result.success:
                return redirect(url_for("admin.login"))

        return render_template("admin/forgot_password.html", form=form)

    @admin_bp.route("/reset-password/<token>", methods=["GET", "POST"])
    def reset_password(token):
        if current_user.is_authenticated:
            return redirect(url_for("admin.dashboard"))

        form = ResetPasswordForm()
        if form.validate_on_submit():
            valid, msg = AuthService.validate_password_strength(form.password.data)
            if not valid:
                flash(msg, "danger")
            else:
                result = AuthService.reset_password(token, form.password.data)
                flash(result.message, "success" if result.success else "danger")
                if result.success:
                    return redirect(url_for("admin.login"))

        return render_template("admin/reset_password.html", form=form, token=token)

    @admin_bp.route("/401")
    def unauthorized_page():
        return render_template("admin/401.html"), 401

    @admin_bp.route("/403")
    def forbidden_page():
        return render_template("admin/403.html"), 403
