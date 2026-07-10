"""Messages / Inbox admin business logic."""

from __future__ import annotations

import math

from flask import url_for
from flask_login import current_user

from app.constants.messages_admin import (
    BULK_ACTIONS,
    DEFAULT_PER_PAGE,
    DEFAULT_TAB,
    INBOX_TABS,
    MAX_PER_PAGE,
    SORT_OPTIONS,
    STATUS_FILTER_OPTIONS,
    TAB_APPLICATIONS,
    TAB_CONTACTS,
    TAB_QUOTES,
)
from app.constants.rbac import (
    PERMISSION_MANAGE_CONTACTS,
    PERMISSION_MANAGE_JOB_APPLICATIONS,
    PERMISSION_MANAGE_QUOTES,
)
from app.providers.admin_dashboard_provider import AdminDashboardProvider
from app.providers.messages_admin_provider import MessagesAdminProvider
from app.schemas.admin import BreadcrumbItemDTO
from app.schemas.messages_admin import InboxListPageDTO, SaveResultDTO


class MessagesAdminService:
    """Unified messages inbox service."""

    @staticmethod
    def user_tabs() -> list[dict]:
        tabs = []
        for tab in INBOX_TABS:
            if current_user.has_permission(tab["permission"]):
                tabs.append(tab)
        return tabs

    @staticmethod
    def default_tab() -> str:
        tabs = MessagesAdminService.user_tabs()
        return tabs[0]["slug"] if tabs else DEFAULT_TAB

    @staticmethod
    def can_access_tab(tab: str) -> bool:
        perm = {
            TAB_CONTACTS: PERMISSION_MANAGE_CONTACTS,
            TAB_QUOTES: PERMISSION_MANAGE_QUOTES,
            TAB_APPLICATIONS: PERMISSION_MANAGE_JOB_APPLICATIONS,
        }.get(tab)
        return bool(perm and current_user.has_permission(perm))

    @staticmethod
    def get_shell_context(
        *,
        page_title: str,
        active_section: str | None = None,
        breadcrumbs: list[BreadcrumbItemDTO] | None = None,
    ) -> dict:
        dashboard = AdminDashboardProvider.get_dashboard()
        return {
            "page_title": page_title,
            "active_nav": "messages",
            "messages_active_section": active_section,
            "breadcrumbs": breadcrumbs
            or MessagesAdminService.build_breadcrumbs(page_title),
            "notifications": dashboard.notifications,
            "unread_notification_count": dashboard.unread_notification_count,
            "user": current_user,
            "inbox_tabs": MessagesAdminService.user_tabs(),
        }

    @staticmethod
    def build_breadcrumbs(current_label: str) -> list[BreadcrumbItemDTO]:
        return [
            BreadcrumbItemDTO("Admin", url_for("admin.dashboard"), False),
            BreadcrumbItemDTO("Messages", url_for("admin.messages_inbox"), False),
            BreadcrumbItemDTO(current_label, None, True),
        ]

    @staticmethod
    def get_inbox_context(
        *,
        tab: str | None = None,
        q: str = "",
        status: str = "",
        sort: str = "newest",
        page: int = 1,
        per_page: int = DEFAULT_PER_PAGE,
        include_deleted: bool = False,
    ) -> dict | None:
        tab = tab or MessagesAdminService.default_tab()
        if not MessagesAdminService.can_access_tab(tab):
            return None

        per_page = min(max(per_page, 10), MAX_PER_PAGE)
        page = max(page, 1)

        if tab == TAB_CONTACTS:
            items, total = MessagesAdminProvider.query_contacts(
                q=q, status=status, sort=sort, page=page, per_page=per_page, include_deleted=include_deleted
            )
        elif tab == TAB_QUOTES:
            items, total = MessagesAdminProvider.query_quotes(
                q=q, status=status, sort=sort, page=page, per_page=per_page, include_deleted=include_deleted
            )
        else:
            items, total = MessagesAdminProvider.query_applications(
                q=q, status=status, sort=sort, page=page, per_page=per_page, include_deleted=include_deleted
            )

        total_pages = max(1, math.ceil(total / per_page)) if total else 1
        page = min(page, total_pages)

        ctx = MessagesAdminService.get_shell_context(
            page_title="Inbox",
            active_section="inbox",
            breadcrumbs=[
                BreadcrumbItemDTO("Admin", url_for("admin.dashboard"), False),
                BreadcrumbItemDTO("Messages", None, True),
            ],
        )
        ctx["stats"] = MessagesAdminProvider.get_stats()
        ctx["list_page"] = InboxListPageDTO(
            items=items,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
            tab=tab,
            query=q,
            status=status,
            sort=sort,
            include_deleted=include_deleted,
        )
        ctx.update(
            {
                "bulk_actions": BULK_ACTIONS,
                "status_filter_options": STATUS_FILTER_OPTIONS,
                "sort_options": SORT_OPTIONS,
                "active_tab": tab,
            }
        )
        return ctx

    @staticmethod
    def get_detail_context(tab: str, item_id: int) -> dict | None:
        if not MessagesAdminService.can_access_tab(tab):
            return None

        if tab == TAB_CONTACTS:
            detail = MessagesAdminProvider.get_contact_detail(item_id, mark_read=True)
        elif tab == TAB_QUOTES:
            detail = MessagesAdminProvider.get_quote_detail(item_id, mark_read=True)
        else:
            detail = MessagesAdminProvider.get_application_detail(item_id, mark_read=True)

        if not detail:
            return None

        MessagesAdminProvider.commit()

        ctx = MessagesAdminService.get_shell_context(
            page_title=detail.title,
            active_section="detail",
            breadcrumbs=MessagesAdminService.build_breadcrumbs(detail.title),
        )
        ctx["message"] = detail
        ctx["active_tab"] = tab
        return ctx

    @staticmethod
    def save_reply(tab: str, item_id: int, form_data: dict, *, ip_address: str | None) -> SaveResultDTO:
        if not MessagesAdminService.can_access_tab(tab):
            return SaveResultDTO(False, "Permission denied.")

        ok = MessagesAdminProvider.save_reply(
            tab,
            item_id,
            subject=form_data.get("reply_subject", ""),
            body=form_data.get("reply_body", ""),
            admin_notes=form_data.get("admin_notes", ""),
            user_id=current_user.id,
        )
        if not ok:
            return SaveResultDTO(False, "Message not found.")

        committed = MessagesAdminProvider.safe_commit(
            action="messages.reply",
            resource_type=f"message_{tab}",
            resource_id=str(item_id),
            details=f"Reply saved for {tab} #{item_id}",
            user_id=current_user.id,
            ip=ip_address or "",
        )
        if not committed:
            return SaveResultDTO(False, "Failed to save reply.")
        return SaveResultDTO(
            True,
            "Reply saved successfully.",
            redirect_url=url_for("admin.messages_detail", tab=tab, item_id=item_id),
        )

    @staticmethod
    def bulk_action(tab: str, ids: list[int], action: str, *, ip_address: str | None) -> SaveResultDTO:
        if not MessagesAdminService.can_access_tab(tab):
            return SaveResultDTO(False, "Permission denied.")
        if action not in BULK_ACTIONS:
            return SaveResultDTO(False, "Invalid bulk action.")

        count = MessagesAdminProvider.apply_bulk(tab, ids, action)
        committed = MessagesAdminProvider.safe_commit(
            action=f"messages.bulk_{action}",
            resource_type=f"message_{tab}",
            resource_id=",".join(str(i) for i in ids[:20]),
            details=f"Bulk {action} on {count} {tab} message(s)",
            user_id=current_user.id,
            ip=ip_address or "",
        )
        if not committed:
            return SaveResultDTO(False, "Bulk action failed.")
        return SaveResultDTO(
            True,
            f"Updated {count} message(s).",
            redirect_url=url_for("admin.messages_inbox", tab=tab),
        )

    @staticmethod
    def item_action(tab: str, item_id: int, action: str, *, ip_address: str | None) -> SaveResultDTO:
        if not MessagesAdminService.can_access_tab(tab):
            return SaveResultDTO(False, "Permission denied.")
        if action not in BULK_ACTIONS:
            return SaveResultDTO(False, "Invalid action.")

        if not MessagesAdminProvider._apply_action(tab, item_id, action):
            return SaveResultDTO(False, "Message not found or action failed.")

        committed = MessagesAdminProvider.safe_commit(
            action=f"messages.{action}",
            resource_type=f"message_{tab}",
            resource_id=str(item_id),
            details=f"{action} on {tab} #{item_id}",
            user_id=current_user.id,
            ip=ip_address or "",
        )
        if not committed:
            return SaveResultDTO(False, "Action failed.")
        return SaveResultDTO(
            True,
            "Message updated.",
            redirect_url=url_for("admin.messages_inbox", tab=tab),
        )

    @staticmethod
    def export_csv(tab: str, ids: list[int] | None = None) -> str | None:
        if not MessagesAdminService.can_access_tab(tab):
            return None
        return MessagesAdminProvider.export_csv(tab, ids)
