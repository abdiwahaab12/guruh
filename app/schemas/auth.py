"""Authentication DTOs — service layer data transfer."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class RoleDTO:
    id: int
    slug: str
    name: str
    description: str = ""
    is_active: bool = True


@dataclass
class PermissionDTO:
    id: int
    slug: str
    name: str
    description: str = ""
    is_active: bool = True


@dataclass
class UserDTO:
    id: int
    email: str
    first_name: str
    last_name: str
    role: RoleDTO
    is_active: bool = True
    last_login_at: datetime | None = None
    last_login_ip: str | None = None
    permission_slugs: list[str] = field(default_factory=list)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip() or self.email


@dataclass
class LoginResultDTO:
    success: bool
    user: UserDTO | None = None
    message: str = ""
    failure_code: str = ""


@dataclass
class PasswordResetResultDTO:
    success: bool
    message: str = ""
    reset_token: str = ""


@dataclass
class SessionInfoDTO:
    session_token: str
    ip_address: str | None = None
    user_agent: str | None = None
    expires_at: datetime | None = None
