"""Careers admin module DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class JobAdminDTO:
    id: int | None
    title: str
    slug: str
    department: str
    location: str
    employment_type: str
    description: str
    requirements: str
    deadline: str
    sort_order: int
    is_active: bool
    status: str = "draft"
    short_description: str = ""
    experience_required: str = ""
    image: str = ""
    responsibilities: list[str] = field(default_factory=list)
    qualifications: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    benefits: list[str] = field(default_factory=list)
    is_featured: bool = False
    accept_applications: bool = True
    notify_email: str = ""
    auto_reply_enabled: bool = False
    auto_reply_message: str = ""
    meta_title: str = ""
    meta_description: str = ""
    og_image: str = ""
    canonical_url: str = ""
    created_at_label: str = ""
    updated_at_label: str = ""


@dataclass
class JobListItemDTO:
    id: int
    title: str
    slug: str
    department: str
    location: str
    employment_type: str
    deadline: str
    status: str
    sort_order: int
    is_featured: bool
    is_active: bool
    updated_at_label: str


@dataclass
class JobStatsDTO:
    total: int
    active: int
    closed: int
    draft: int
    recent: list[JobListItemDTO]


@dataclass
class JobListPageDTO:
    items: list[JobListItemDTO]
    total: int
    page: int
    per_page: int
    total_pages: int
    query: str
    filters: dict[str, str]
    sort: str
    include_deleted: bool


@dataclass
class SaveResultDTO:
    success: bool
    message: str
    job_id: int | None = None
