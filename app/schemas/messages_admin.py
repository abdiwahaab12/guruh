"""Messages / Inbox admin DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MessageListItemDTO:
    id: int
    tab: str
    name: str
    email: str
    summary: str
    is_read: bool
    is_starred: bool
    is_archived: bool
    is_deleted: bool
    created_at_label: str
    status_badges: list[str] = field(default_factory=list)


@dataclass
class MessageDetailDTO:
    id: int
    tab: str
    title: str
    name: str
    email: str
    phone: str
    subject: str
    body: str
    is_read: bool
    is_starred: bool
    is_archived: bool
    is_deleted: bool
    admin_notes: str
    reply_subject: str
    reply_body: str
    replied_at_label: str
    created_at_label: str
    updated_at_label: str
    extra_fields: dict[str, str] = field(default_factory=dict)
    job_position: str = ""
    job_listing_title: str = ""


@dataclass
class InboxStatsDTO:
    contacts_total: int
    contacts_unread: int
    quotes_total: int
    quotes_unread: int
    applications_total: int
    applications_unread: int


@dataclass
class InboxListPageDTO:
    items: list[MessageListItemDTO]
    total: int
    page: int
    per_page: int
    total_pages: int
    tab: str
    query: str
    status: str
    sort: str
    include_deleted: bool


@dataclass
class SaveResultDTO:
    success: bool
    message: str
    redirect_url: str | None = None
