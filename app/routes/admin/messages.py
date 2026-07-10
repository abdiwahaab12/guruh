"""Enterprise Messages / Inbox admin routes — Step 24."""

from __future__ import annotations

from flask import Response, abort, flash, redirect, render_template, request, url_for

from app.constants.messages_admin import BULK_ACTIONS, TAB_CONTACTS, TAB_QUOTES, TAB_APPLICATIONS
from app.forms.messages_forms import MessageActionForm, MessageReplyForm, MessagesBulkForm
from app.services.messages_admin_service import MessagesAdminService
from app.utils.permissions import (
    can_access_messages,
    can_manage_contacts,
    can_manage_job_applications,
    can_manage_quotes,
)


def _tab_guard(tab: str):
    guards = {
        TAB_CONTACTS: can_manage_contacts,
        TAB_QUOTES: can_manage_quotes,
        TAB_APPLICATIONS: can_manage_job_applications,
    }
    return guards.get(tab, can_access_messages)


def register_messages_routes(admin_bp) -> None:
    """Register messages inbox routes."""

    @admin_bp.route("/messages")
    @admin_bp.route("/messages/inbox")
    @can_access_messages
    def messages_inbox():
        tab = request.args.get("tab") or MessagesAdminService.default_tab()
        ctx = MessagesAdminService.get_inbox_context(
            tab=tab,
            q=request.args.get("q", ""),
            status=request.args.get("status", ""),
            sort=request.args.get("sort", "newest"),
            page=request.args.get("page", 1, type=int),
            include_deleted=request.args.get("deleted") == "1",
        )
        if not ctx:
            abort(403)

        bulk_form = MessagesBulkForm()
        bulk_form.action.choices = list(BULK_ACTIONS.items())
        ctx["bulk_form"] = bulk_form
        ctx["action_form"] = MessageActionForm()
        return render_template("admin/messages/inbox.html", **ctx)

    @admin_bp.route("/messages/<tab>/<int:item_id>", methods=["GET", "POST"])
    @can_access_messages
    def messages_detail(tab: str, item_id: int):
        if not MessagesAdminService.can_access_tab(tab):
            abort(403)
        ctx = MessagesAdminService.get_detail_context(tab, item_id)
        if not ctx:
            abort(404)

        reply_form = MessageReplyForm()
        message = ctx["message"]
        if request.method == "GET":
            reply_form.reply_subject.data = message.reply_subject
            reply_form.reply_body.data = message.reply_body
            reply_form.admin_notes.data = message.admin_notes

        if reply_form.validate_on_submit():
            result = MessagesAdminService.save_reply(
                tab,
                item_id,
                request.form.to_dict(flat=True),
                ip_address=request.remote_addr,
            )
            flash(result.message, "success" if result.success else "danger")
            if result.success and result.redirect_url:
                return redirect(result.redirect_url)

        ctx["reply_form"] = reply_form
        ctx["action_form"] = MessageActionForm()
        return render_template("admin/messages/detail.html", **ctx)

    @admin_bp.route("/messages/<tab>/<int:item_id>/action/<action>", methods=["POST"])
    @can_access_messages
    def messages_item_action(tab: str, item_id: int, action: str):
        form = MessageActionForm()
        if not form.validate_on_submit():
            flash("Invalid request.", "danger")
            return redirect(url_for("admin.messages_inbox", tab=tab))

        result = MessagesAdminService.item_action(tab, item_id, action, ip_address=request.remote_addr)
        flash(result.message, "success" if result.success else "danger")
        if result.redirect_url:
            return redirect(result.redirect_url)
        return redirect(url_for("admin.messages_detail", tab=tab, item_id=item_id))

    @admin_bp.route("/messages/bulk", methods=["POST"])
    @can_access_messages
    def messages_bulk():
        tab = request.form.get("tab", TAB_CONTACTS)
        if not MessagesAdminService.can_access_tab(tab):
            abort(403)

        form = MessagesBulkForm()
        form.action.choices = list(BULK_ACTIONS.items())
        if not form.validate_on_submit():
            flash("Invalid bulk action.", "danger")
            return redirect(url_for("admin.messages_inbox", tab=tab))

        ids = [int(x) for x in request.form.getlist("message_ids") if x.isdigit()]
        result = MessagesAdminService.bulk_action(
            tab,
            ids,
            form.action.data,
            ip_address=request.remote_addr,
        )
        flash(result.message, "success" if result.success else "danger")
        return redirect(url_for("admin.messages_inbox", tab=tab))

    @admin_bp.route("/messages/export")
    @can_access_messages
    def messages_export():
        tab = request.args.get("tab", TAB_CONTACTS)
        if not MessagesAdminService.can_access_tab(tab):
            abort(403)

        ids_raw = request.args.get("ids", "")
        ids = [int(x) for x in ids_raw.split(",") if x.isdigit()] if ids_raw else None
        csv_data = MessagesAdminService.export_csv(tab, ids)
        if csv_data is None:
            abort(403)

        filename = f"guruh-{tab}-{request.args.get('export_ts', 'export')}.csv"
        return Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
