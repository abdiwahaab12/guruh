"""Users & RBAC admin business logic."""

from __future__ import annotations

import math

from flask import url_for
from flask_login import current_user

from app.constants.rbac import ROLE_SUPER_ADMIN
from app.constants.users_admin import (
    DEFAULT_PER_PAGE,
    DEFAULT_TAB,
    LOGIN_STATUS_OPTIONS,
    MAX_PER_PAGE,
    SESSION_STATUS_OPTIONS,
    TAB_AUDIT_LOGS,
    TAB_LOGIN_HISTORY,
    TAB_PERMISSIONS,
    TAB_ROLES,
    TAB_SESSIONS,
    TAB_USERS,
    USER_BULK_ACTIONS,
    USER_SORT_OPTIONS,
    USER_STATUS_OPTIONS,
    USERS_TABS,
)
from app.providers.admin_dashboard_provider import AdminDashboardProvider
from app.providers.users_admin_provider import UsersAdminProvider
from app.schemas.admin import BreadcrumbItemDTO
from app.schemas.users_admin import SaveResultDTO, UsersListPageDTO
from app.services.auth_service import AuthService


class UsersAdminService:
    """Enterprise users and RBAC management."""

    @staticmethod
    def get_shell_context(
        *,
        page_title: str,
        active_section: str | None = None,
        breadcrumbs: list[BreadcrumbItemDTO] | None = None,
        active_tab: str = DEFAULT_TAB,
    ) -> dict:
        dashboard = AdminDashboardProvider.get_dashboard()
        return {
            "page_title": page_title,
            "active_nav": "users",
            "users_active_section": active_section,
            "active_tab": active_tab,
            "users_tabs": USERS_TABS,
            "breadcrumbs": breadcrumbs
            or UsersAdminService.build_breadcrumbs(page_title),
            "notifications": dashboard.notifications,
            "unread_notification_count": dashboard.unread_notification_count,
            "user": current_user,
        }

    @staticmethod
    def build_breadcrumbs(current_label: str) -> list[BreadcrumbItemDTO]:
        return [
            BreadcrumbItemDTO("Admin", url_for("admin.dashboard"), False),
            BreadcrumbItemDTO("Users & RBAC", url_for("admin.users_dashboard"), False),
            BreadcrumbItemDTO(current_label, None, True),
        ]

    @staticmethod
    def can_edit_target_user(target: UserAdminDTO | None) -> bool:
        if not target:
            return False
        if target.is_super_admin and current_user.role.slug != ROLE_SUPER_ADMIN:
            return False
        return True

    @staticmethod
    def _guard_target_user(user_id: int) -> tuple[SaveResultDTO | None, object | None]:
        from app.providers.users_admin_provider import UsersAdminProvider as P

        user = P.get_user(user_id)
        if not user:
            return SaveResultDTO(False, "User not found."), None
        dto = P.to_user_dto(user)
        if dto.is_super_admin and current_user.role.slug != ROLE_SUPER_ADMIN:
            return SaveResultDTO(False, "You cannot modify a Super Administrator account."), None
        if user_id == current_user.id and not user.is_active:
            return SaveResultDTO(False, "You cannot deactivate your own account."), None
        return None, user

    @staticmethod
    def get_dashboard_context(tab: str | None = None, **list_kwargs) -> dict:
        tab = tab or DEFAULT_TAB
        ctx = UsersAdminService.get_shell_context(
            page_title="Users & RBAC",
            active_section="dashboard",
            active_tab=tab,
            breadcrumbs=[
                BreadcrumbItemDTO("Admin", url_for("admin.dashboard"), False),
                BreadcrumbItemDTO("Users & RBAC", None, True),
            ],
        )
        ctx["stats"] = UsersAdminProvider.get_stats()
        ctx["list_page"] = UsersAdminService._build_list_page(tab, **list_kwargs)
        ctx.update(UsersAdminService._tab_extras(tab))
        return ctx

    @staticmethod
    def _tab_extras(tab: str) -> dict:
        extras = {
            "bulk_actions": USER_BULK_ACTIONS,
            "user_status_options": USER_STATUS_OPTIONS,
            "user_sort_options": USER_SORT_OPTIONS,
            "session_status_options": SESSION_STATUS_OPTIONS,
            "login_status_options": LOGIN_STATUS_OPTIONS,
            "filter_roles": UsersAdminProvider.list_assignable_roles(),
        }
        if tab == TAB_ROLES:
            extras["roles"] = UsersAdminProvider.list_roles()
        elif tab == TAB_PERMISSIONS:
            extras["permissions"] = UsersAdminProvider.list_permissions()
        return extras

    @staticmethod
    def _build_list_page(tab: str, **kwargs) -> UsersListPageDTO:
        page = max(kwargs.get("page", 1), 1)
        per_page = min(max(kwargs.get("per_page", DEFAULT_PER_PAGE), 10), MAX_PER_PAGE)
        q = kwargs.get("q", "")
        sort = kwargs.get("sort", "newest")

        if tab == TAB_USERS:
            items, total = UsersAdminProvider.query_users(
                q=q,
                role_slug=kwargs.get("role_slug", ""),
                status=kwargs.get("status", ""),
                sort=sort,
                page=page,
                per_page=per_page,
            )
            filters = {"role_slug": kwargs.get("role_slug", ""), "status": kwargs.get("status", "")}
        elif tab == TAB_SESSIONS:
            items, total = UsersAdminProvider.query_sessions(
                q=q,
                status=kwargs.get("status", ""),
                page=page,
                per_page=per_page,
            )
            filters = {"status": kwargs.get("status", "")}
        elif tab == TAB_LOGIN_HISTORY:
            items, total = UsersAdminProvider.query_login_history(
                q=q,
                status=kwargs.get("status", ""),
                page=page,
                per_page=per_page,
            )
            filters = {"status": kwargs.get("status", "")}
        elif tab == TAB_AUDIT_LOGS:
            items, total = UsersAdminProvider.query_audit_logs(
                q=q,
                action=kwargs.get("action", ""),
                page=page,
                per_page=per_page,
            )
            filters = {"action": kwargs.get("action", "")}
        else:
            items, total = [], 0
            filters = {}

        total_pages = max(1, math.ceil(total / per_page)) if total else 1
        page = min(page, total_pages)
        return UsersListPageDTO(
            items=items,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
            tab=tab,
            query=q,
            filters=filters,
            sort=sort,
        )

    @staticmethod
    def get_user_form_context(user_id: int | None = None) -> dict | None:
        roles = UsersAdminProvider.list_assignable_roles()
        if user_id:
            user = UsersAdminProvider.get_user(user_id)
            if not user:
                return None
            dto = UsersAdminProvider.to_user_dto(user)
            if dto.is_super_admin and current_user.id != user.id and current_user.role.slug != ROLE_SUPER_ADMIN:
                return None
            title = f"Edit — {dto.full_name}"
            is_edit = True
        else:
            from app.schemas.users_admin import UserAdminDTO

            default_role = roles[0] if roles else None
            dto = UserAdminDTO(
                id=0,
                email="",
                first_name="",
                last_name="",
                full_name="",
                role_id=default_role.id if default_role else 0,
                role_slug=default_role.slug if default_role else "",
                role_name=default_role.name if default_role else "",
                is_active=True,
                is_locked=False,
                failed_login_attempts=0,
                last_login_at_label="—",
                last_login_ip="",
                created_at_label="—",
            )
            title = "Create User"
            is_edit = False

        ctx = UsersAdminService.get_shell_context(page_title=title, active_section="form")
        ctx["admin_user"] = dto if is_edit else None
        ctx["is_edit"] = is_edit
        ctx["roles"] = roles
        return ctx

    @staticmethod
    def save_user(form_data: dict, *, user_id: int | None, ip_address: str | None) -> SaveResultDTO:
        email = form_data.get("email", "").strip()
        first_name = form_data.get("first_name", "").strip()
        last_name = form_data.get("last_name", "").strip()
        role_id = int(form_data.get("role_id") or 0)
        is_active = form_data.get("is_active") in ("1", "true", "on", "yes", "y")
        password = form_data.get("password", "")
        new_password = form_data.get("new_password", "")

        if not email or not first_name or not role_id:
            return SaveResultDTO(False, "Email, first name, and role are required.")

        role = UsersAdminProvider.get_role(role_id)
        if not role:
            return SaveResultDTO(False, "Invalid role selected.")

        if user_id:
            err, user = UsersAdminService._guard_target_user(user_id)
            if err:
                return err
            if user.id == current_user.id and not is_active:
                return SaveResultDTO(False, "You cannot deactivate your own account.")
            if user.role.slug == ROLE_SUPER_ADMIN and role.slug != ROLE_SUPER_ADMIN:
                if UsersAdminProvider.count_super_admins(active_only=True) <= 1:
                    return SaveResultDTO(False, "Cannot remove the last Super Administrator role.")
            if new_password:
                ok, msg = AuthService.validate_password_strength(new_password)
                if not ok:
                    return SaveResultDTO(False, msg)
            UsersAdminProvider.update_user(
                user,
                email=email,
                first_name=first_name,
                last_name=last_name,
                role_id=role_id,
                is_active=is_active,
                new_password=new_password or None,
            )
            action = "users.update"
            details = f"Updated user {email}"
        else:
            ok, msg = AuthService.validate_password_strength(password)
            if not ok:
                return SaveResultDTO(False, msg)
            from app.providers.auth_provider import AuthProvider

            if AuthProvider.get_user_by_email(email):
                return SaveResultDTO(False, "A user with this email already exists.")
            user = UsersAdminProvider.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                role_id=role_id,
                password=password,
                is_active=is_active,
            )
            action = "users.create"
            details = f"Created user {email}"

        committed = UsersAdminProvider.safe_commit(
            action=action,
            resource_type="user",
            resource_id=str(user.id),
            details=details,
            user_id=current_user.id,
            ip=ip_address or "",
        )
        if not committed:
            return SaveResultDTO(False, "Failed to save user.")
        return SaveResultDTO(
            True,
            "User saved successfully.",
            user_id=user.id,
            redirect_url=url_for("admin.users_edit", user_id=user.id),
        )

    @staticmethod
    def reset_password(user_id: int, new_password: str, *, ip_address: str | None) -> SaveResultDTO:
        err, user = UsersAdminService._guard_target_user(user_id)
        if err:
            return err
        ok, msg = AuthService.validate_password_strength(new_password)
        if not ok:
            return SaveResultDTO(False, msg)
        UsersAdminProvider.reset_user_password(user, new_password)
        from app.providers.auth_provider import AuthProvider

        AuthProvider.deactivate_user_sessions(user)
        committed = UsersAdminProvider.safe_commit(
            action="users.reset_password",
            resource_type="user",
            resource_id=str(user_id),
            details=f"Password reset for {user.email}",
            user_id=current_user.id,
            ip=ip_address or "",
        )
        if not committed:
            return SaveResultDTO(False, "Failed to reset password.")
        return SaveResultDTO(True, "Password reset successfully.", redirect_url=url_for("admin.users_edit", user_id=user_id))

    @staticmethod
    def admin_reset_link(user_id: int, *, ip_address: str | None) -> SaveResultDTO:
        from app.providers.auth_provider import AuthProvider
        from flask import url_for

        err, user = UsersAdminService._guard_target_user(user_id)
        if err:
            return err
        reset = AuthProvider.create_password_reset(user, ip_address=ip_address)
        committed = UsersAdminProvider.safe_commit(
            action="users.reset_password_link",
            resource_type="user",
            resource_id=str(user_id),
            details=f"Generated password reset link for {user.email}",
            user_id=current_user.id,
            ip=ip_address or "",
        )
        if not committed:
            return SaveResultDTO(False, "Failed to generate reset link.")
        reset_url = url_for("admin.reset_password", token=reset.token, _external=True)
        return SaveResultDTO(
            True,
            "Password reset link generated.",
            redirect_url=url_for("admin.users_edit", user_id=user_id),
            reset_url=reset_url,
        )

    @staticmethod
    def bulk_users(user_ids: list[int], action: str, *, ip_address: str | None) -> SaveResultDTO:
        if action not in USER_BULK_ACTIONS:
            return SaveResultDTO(False, "Invalid bulk action.")
        if current_user.id in user_ids and action == "deactivate":
            return SaveResultDTO(False, "You cannot deactivate your own account.")
        for uid in user_ids:
            user = UsersAdminProvider.get_user(uid)
            if user and user.role.slug == ROLE_SUPER_ADMIN and action == "deactivate":
                if UsersAdminProvider.count_super_admins(active_only=True) <= 1:
                    return SaveResultDTO(False, "Cannot deactivate the last Super Administrator.")
        count = UsersAdminProvider.apply_user_bulk(user_ids, action)
        committed = UsersAdminProvider.safe_commit(
            action=f"users.bulk_{action}",
            resource_type="user",
            resource_id=",".join(str(i) for i in user_ids[:20]),
            details=f"Bulk {action} on {count} user(s)",
            user_id=current_user.id,
            ip=ip_address or "",
        )
        if not committed:
            return SaveResultDTO(False, "Bulk action failed.")
        return SaveResultDTO(True, f"Updated {count} user(s).", redirect_url=url_for("admin.users_dashboard", tab=TAB_USERS))

    @staticmethod
    def save_role_permissions(role_id: int, permission_ids: list[int], *, ip_address: str | None) -> SaveResultDTO:
        role = UsersAdminProvider.get_role(role_id)
        if not role:
            return SaveResultDTO(False, "Role not found.")
        if role.slug in {ROLE_SUPER_ADMIN}:
            return SaveResultDTO(False, "Super Administrator permissions are managed in code and cannot be edited.")
        UsersAdminProvider.sync_role_permissions(role, permission_ids)
        committed = UsersAdminProvider.safe_commit(
            action="users.role.update",
            resource_type="role",
            resource_id=str(role_id),
            details=f"Updated permissions for role {role.slug}",
            user_id=current_user.id,
            ip=ip_address or "",
        )
        if not committed:
            return SaveResultDTO(False, "Failed to save role permissions.")
        return SaveResultDTO(True, "Role permissions saved.", redirect_url=url_for("admin.users_dashboard", tab=TAB_ROLES))

    @staticmethod
    def revoke_session(session_id: int, *, ip_address: str | None) -> SaveResultDTO:
        if not UsersAdminProvider.revoke_session(session_id):
            return SaveResultDTO(False, "Session not found or already revoked.")
        committed = UsersAdminProvider.safe_commit(
            action="users.session.revoke",
            resource_type="user_session",
            resource_id=str(session_id),
            details=f"Revoked session #{session_id}",
            user_id=current_user.id,
            ip=ip_address or "",
        )
        if not committed:
            return SaveResultDTO(False, "Failed to revoke session.")
        return SaveResultDTO(True, "Session revoked.", redirect_url=url_for("admin.users_dashboard", tab=TAB_SESSIONS))

    @staticmethod
    def get_role_edit_context(role_id: int) -> dict | None:
        role = UsersAdminProvider.get_role(role_id)
        if not role:
            return None
        dto = next((r for r in UsersAdminProvider.list_roles() if r.id == role_id), None)
        if not dto:
            return None
        ctx = UsersAdminService.get_shell_context(
            page_title=f"Role — {dto.name}",
            active_section="role",
            active_tab=TAB_ROLES,
        )
        ctx["role"] = dto
        ctx["all_permissions"] = UsersAdminProvider.list_permissions()
        return ctx
