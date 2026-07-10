"""Users & RBAC admin DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class UserAdminDTO:
    id: int
    email: str
    first_name: str
    last_name: str
    full_name: str
    role_id: int
    role_slug: str
    role_name: str
    is_active: bool
    is_locked: bool
    failed_login_attempts: int
    last_login_at_label: str
    last_login_ip: str
    created_at_label: str
    is_super_admin: bool = False
    can_edit: bool = True


@dataclass
class RoleAdminDTO:
    id: int
    slug: str
    name: str
    description: str
    is_active: bool
    user_count: int
    permission_slugs: list[str] = field(default_factory=list)
    is_protected: bool = False


@dataclass
class PermissionAdminDTO:
    id: int
    slug: str
    name: str
    description: str
    is_active: bool
    role_count: int


@dataclass
class SessionAdminDTO:
    id: int
    user_id: int
    user_email: str
    user_name: str
    ip_address: str
    user_agent: str
    is_active: bool
    expires_at_label: str
    logged_out_at_label: str
    created_at_label: str


@dataclass
class LoginHistoryAdminDTO:
    id: int
    email_attempted: str
    user_name: str
    ip_address: str
    success: bool
    failure_reason: str
    created_at_label: str


@dataclass
class AuditLogAdminDTO:
    id: int
    action: str
    resource_type: str
    resource_id: str
    details: str
    user_email: str
    ip_address: str
    created_at_label: str


@dataclass
class UsersStatsDTO:
    total_users: int
    active_users: int
    inactive_users: int
    locked_users: int
    total_roles: int
    active_sessions: int
    failed_logins_24h: int
    audit_events_24h: int


@dataclass
class UsersListPageDTO:
    items: list
    total: int
    page: int
    per_page: int
    total_pages: int
    tab: str
    query: str
    filters: dict[str, str]
    sort: str


@dataclass
class SaveResultDTO:
    success: bool
    message: str
    user_id: int | None = None
    redirect_url: str | None = None
    reset_url: str | None = None
