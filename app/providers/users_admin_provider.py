"""Users & RBAC admin data provider."""

from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy import asc, desc, func, or_
from sqlalchemy.exc import SQLAlchemyError

from app.constants.rbac import ROLE_SUPER_ADMIN
from app.constants.users_admin import PROTECTED_ROLE_SLUGS
from app.extensions import db
from app.models.auth import AuditLog, LoginHistory, Permission, Role, RolePermission, User, UserSession
from app.providers.auth_provider import AuthProvider
from app.schemas.users_admin import (
    AuditLogAdminDTO,
    LoginHistoryAdminDTO,
    PermissionAdminDTO,
    RoleAdminDTO,
    SessionAdminDTO,
    UserAdminDTO,
    UsersStatsDTO,
)


class UsersAdminProvider:
    """Database operations for users and RBAC administration."""

    @staticmethod
    def commit() -> bool:
        return AuthProvider.commit()

    @staticmethod
    def rollback() -> None:
        AuthProvider.rollback()

    @staticmethod
    def record_audit(**kwargs) -> None:
        AuthProvider.record_audit_event(**kwargs)

    @staticmethod
    def _format_dt(value: datetime | None) -> str:
        return value.strftime("%d %b %Y, %H:%M") if value else "—"

    @staticmethod
    def get_user(user_id: int) -> User | None:
        return User.query.get(user_id)

    @staticmethod
    def count_super_admins(*, active_only: bool = True) -> int:
        query = User.query.join(Role).filter(Role.slug == ROLE_SUPER_ADMIN)
        if active_only:
            query = query.filter(User.is_active.is_(True))
        return query.count()

    @staticmethod
    def to_user_dto(user: User, *, can_edit: bool = True) -> UserAdminDTO:
        role = user.role
        return UserAdminDTO(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            full_name=user.full_name,
            role_id=user.role_id,
            role_slug=role.slug if role else "",
            role_name=role.name if role else "",
            is_active=user.is_active,
            is_locked=user.is_locked,
            failed_login_attempts=user.failed_login_attempts or 0,
            last_login_at_label=UsersAdminProvider._format_dt(user.last_login_at),
            last_login_ip=user.last_login_ip or "",
            created_at_label=UsersAdminProvider._format_dt(user.created_at),
            is_super_admin=bool(role and role.slug == ROLE_SUPER_ADMIN),
            can_edit=can_edit,
        )

    @staticmethod
    def query_users(
        *,
        q: str = "",
        role_slug: str = "",
        status: str = "",
        sort: str = "newest",
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[UserAdminDTO], int]:
        query = User.query.join(Role)
        if q:
            like = f"%{q}%"
            query = query.filter(
                or_(
                    User.email.ilike(like),
                    User.first_name.ilike(like),
                    User.last_name.ilike(like),
                )
            )
        if role_slug:
            query = query.filter(Role.slug == role_slug)
        if status == "active":
            query = query.filter(User.is_active.is_(True))
        elif status == "inactive":
            query = query.filter(User.is_active.is_(False))
        elif status == "locked":
            query = query.filter(User.locked_until.isnot(None), User.locked_until > datetime.utcnow())

        if sort == "oldest":
            query = query.order_by(asc(User.created_at))
        elif sort == "name_asc":
            query = query.order_by(asc(User.first_name), asc(User.last_name))
        elif sort == "name_desc":
            query = query.order_by(desc(User.first_name), desc(User.last_name))
        elif sort == "email_asc":
            query = query.order_by(asc(User.email))
        else:
            query = query.order_by(desc(User.created_at))

        total = query.count()
        rows = query.offset((page - 1) * per_page).limit(per_page).all()
        return [UsersAdminProvider.to_user_dto(r) for r in rows], total

    @staticmethod
    def create_user(
        *,
        email: str,
        first_name: str,
        last_name: str,
        role_id: int,
        password: str,
        is_active: bool = True,
    ) -> User:
        user = User(
            email=email.lower().strip(),
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            role_id=role_id,
            is_active=is_active,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.flush()
        return user

    @staticmethod
    def update_user(
        user: User,
        *,
        email: str,
        first_name: str,
        last_name: str,
        role_id: int,
        is_active: bool,
        new_password: str | None = None,
    ) -> User:
        user.email = email.lower().strip()
        user.first_name = first_name.strip()
        user.last_name = last_name.strip()
        user.role_id = role_id
        user.is_active = is_active
        if new_password:
            user.set_password(new_password)
        return user

    @staticmethod
    def reset_user_password(user: User, new_password: str) -> None:
        user.set_password(new_password)
        AuthProvider.reset_failed_login(user)

    @staticmethod
    def unlock_user(user: User) -> None:
        AuthProvider.reset_failed_login(user)

    @staticmethod
    def apply_user_bulk(user_ids: list[int], action: str) -> int:
        updated = 0
        for user_id in user_ids:
            user = User.query.get(user_id)
            if not user:
                continue
            if action == "activate":
                user.is_active = True
                updated += 1
            elif action == "deactivate":
                user.is_active = False
                updated += 1
            elif action == "unlock":
                UsersAdminProvider.unlock_user(user)
                updated += 1
            elif action == "revoke_sessions":
                AuthProvider.deactivate_user_sessions(user)
                updated += 1
        return updated

    @staticmethod
    def list_roles() -> list[RoleAdminDTO]:
        roles = Role.query.order_by(Role.name).all()
        result = []
        for role in roles:
            perm_slugs = [p.slug for p in role.permissions]
            result.append(
                RoleAdminDTO(
                    id=role.id,
                    slug=role.slug,
                    name=role.name,
                    description=role.description or "",
                    is_active=role.is_active,
                    user_count=User.query.filter_by(role_id=role.id).count(),
                    permission_slugs=perm_slugs,
                    is_protected=role.slug in PROTECTED_ROLE_SLUGS,
                )
            )
        return result

    @staticmethod
    def get_role(role_id: int) -> Role | None:
        return Role.query.get(role_id)

    @staticmethod
    def sync_role_permissions(role: Role, permission_ids: list[int]) -> None:
        if role.slug in PROTECTED_ROLE_SLUGS:
            return
        desired = set(permission_ids)
        existing = {rp.permission_id: rp for rp in role.role_permissions}
        for pid, rp in list(existing.items()):
            if pid not in desired:
                db.session.delete(rp)
        for pid in desired:
            if pid not in existing:
                db.session.add(RolePermission(role_id=role.id, permission_id=pid))

    @staticmethod
    def list_permissions() -> list[PermissionAdminDTO]:
        rows = Permission.query.order_by(Permission.slug).all()
        result = []
        for perm in rows:
            role_count = RolePermission.query.filter_by(permission_id=perm.id).count()
            result.append(
                PermissionAdminDTO(
                    id=perm.id,
                    slug=perm.slug,
                    name=perm.name,
                    description=perm.description or "",
                    is_active=perm.is_active,
                    role_count=role_count,
                )
            )
        return result

    @staticmethod
    def query_sessions(
        *,
        q: str = "",
        status: str = "",
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[SessionAdminDTO], int]:
        query = UserSession.query.join(User)
        if q:
            like = f"%{q}%"
            query = query.filter(or_(User.email.ilike(like), UserSession.ip_address.ilike(like)))
        if status == "active":
            query = query.filter(UserSession.is_active.is_(True))
        elif status == "inactive":
            query = query.filter(UserSession.is_active.is_(False))

        query = query.order_by(desc(UserSession.created_at))
        total = query.count()
        rows = query.offset((page - 1) * per_page).limit(per_page).all()
        items = []
        for row in rows:
            user = row.user
            items.append(
                SessionAdminDTO(
                    id=row.id,
                    user_id=row.user_id,
                    user_email=user.email if user else "",
                    user_name=user.full_name if user else "",
                    ip_address=row.ip_address or "",
                    user_agent=(row.user_agent or "")[:120],
                    is_active=row.is_active,
                    expires_at_label=UsersAdminProvider._format_dt(row.expires_at),
                    logged_out_at_label=UsersAdminProvider._format_dt(row.logged_out_at),
                    created_at_label=UsersAdminProvider._format_dt(row.created_at),
                )
            )
        return items, total

    @staticmethod
    def revoke_session(session_id: int) -> bool:
        row = UserSession.query.get(session_id)
        if not row or not row.is_active:
            return False
        row.is_active = False
        row.logged_out_at = datetime.utcnow()
        return True

    @staticmethod
    def query_login_history(
        *,
        q: str = "",
        status: str = "",
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[LoginHistoryAdminDTO], int]:
        query = LoginHistory.query.outerjoin(User)
        if q:
            like = f"%{q}%"
            query = query.filter(or_(LoginHistory.email_attempted.ilike(like), LoginHistory.ip_address.ilike(like)))
        if status == "success":
            query = query.filter(LoginHistory.success.is_(True))
        elif status == "failed":
            query = query.filter(LoginHistory.success.is_(False))

        query = query.order_by(desc(LoginHistory.created_at))
        total = query.count()
        rows = query.offset((page - 1) * per_page).limit(per_page).all()
        items = []
        for row in rows:
            items.append(
                LoginHistoryAdminDTO(
                    id=row.id,
                    email_attempted=row.email_attempted,
                    user_name=row.user.full_name if row.user else "",
                    ip_address=row.ip_address or "",
                    success=row.success,
                    failure_reason=row.failure_reason or "",
                    created_at_label=UsersAdminProvider._format_dt(row.created_at),
                )
            )
        return items, total

    @staticmethod
    def query_audit_logs(
        *,
        q: str = "",
        action: str = "",
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[AuditLogAdminDTO], int]:
        query = AuditLog.query.outerjoin(User, AuditLog.user_id == User.id)
        if q:
            like = f"%{q}%"
            query = query.filter(
                or_(
                    AuditLog.action.ilike(like),
                    AuditLog.resource_type.ilike(like),
                    AuditLog.details.ilike(like),
                    User.email.ilike(like),
                )
            )
        if action:
            query = query.filter(AuditLog.action.ilike(f"%{action}%"))

        query = query.order_by(desc(AuditLog.created_at))
        total = query.count()
        rows = query.offset((page - 1) * per_page).limit(per_page).all()
        items = []
        for row in rows:
            items.append(
                AuditLogAdminDTO(
                    id=row.id,
                    action=row.action,
                    resource_type=row.resource_type or "",
                    resource_id=row.resource_id or "",
                    details=(row.details or "")[:200],
                    user_email=row.user.email if row.user else "System",
                    ip_address=row.ip_address or "",
                    created_at_label=UsersAdminProvider._format_dt(row.created_at),
                )
            )
        return items, total

    @staticmethod
    def get_stats() -> UsersStatsDTO:
        since = datetime.utcnow() - timedelta(hours=24)
        return UsersStatsDTO(
            total_users=User.query.count(),
            active_users=User.query.filter_by(is_active=True).count(),
            inactive_users=User.query.filter_by(is_active=False).count(),
            locked_users=User.query.filter(User.locked_until.isnot(None), User.locked_until > datetime.utcnow()).count(),
            total_roles=Role.query.filter_by(is_active=True).count(),
            active_sessions=UserSession.query.filter_by(is_active=True).count(),
            failed_logins_24h=LoginHistory.query.filter(
                LoginHistory.success.is_(False),
                LoginHistory.created_at >= since,
            ).count(),
            audit_events_24h=AuditLog.query.filter(AuditLog.created_at >= since).count(),
        )

    @staticmethod
    def list_assignable_roles() -> list[Role]:
        return Role.query.filter_by(is_active=True).order_by(Role.name).all()

    @staticmethod
    def safe_commit(action: str, resource_type: str, resource_id: str, details: str, user_id: int, ip: str) -> bool:
        try:
            UsersAdminProvider.record_audit(
                user_id=user_id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                details=details,
                ip_address=ip,
            )
            return UsersAdminProvider.commit()
        except SQLAlchemyError:
            UsersAdminProvider.rollback()
            return False
