"""
Admin dashboard navigation — sidebar structure for Step 14 foundation.

Future CRUD modules will attach to these routes in later steps.
Labels use data-i18n keys for multi-language readiness.
"""

from __future__ import annotations

from typing import Any, Final

# Module slugs served by the placeholder view (no CRUD yet)
MODULE_SLUGS: Final[frozenset[str]] = frozenset()

MODULE_LABELS: Final[dict[str, str]] = {
    "content": "Content",
    "projects": "Projects",
    "services": "Services",
    "equipment": "Equipment",
    "gallery": "Gallery",
    "team": "Team",
    "careers": "Careers",
    "messages": "Messages",
    "forms": "Forms",
    "media": "Media",
    "users": "Users",
    "roles": "Roles",
    "audit-logs": "Audit Logs",
    "reports": "Reports",
    "system": "System",
}


def build_sidebar_nav() -> list[dict[str, Any]]:
    """Primary sidebar navigation items."""
    return [
        {
            "id": "dashboard",
            "label": "Dashboard",
            "i18n_key": "nav.dashboard",
            "icon": "bi-speedometer2",
            "endpoint": "admin.dashboard",
            "slug": None,
            "badge": None,
            "children": [],
        },
        {
            "id": "content",
            "label": "Content",
            "i18n_key": "nav.content",
            "icon": "bi-file-earmark-text",
            "endpoint": "admin.website_dashboard",
            "slug": None,
            "badge": None,
            "children": [
                {"label": "Pages", "i18n_key": "nav.pages", "endpoint": "admin.website_dashboard", "slug": None, "anchor": None},
            ],
        },
        {
            "id": "projects",
            "label": "Projects",
            "i18n_key": "nav.projects",
            "icon": "bi-building",
            "endpoint": "admin.projects_dashboard",
            "slug": None,
            "badge": None,
            "children": [],
        },
        {
            "id": "services",
            "label": "Services",
            "i18n_key": "nav.services",
            "icon": "bi-grid",
            "endpoint": "admin.services_dashboard",
            "slug": None,
            "badge": None,
            "children": [],
        },
        {
            "id": "equipment",
            "label": "Equipment",
            "i18n_key": "nav.equipment",
            "icon": "bi-truck",
            "endpoint": "admin.equipment_dashboard",
            "slug": None,
            "badge": None,
            "children": [],
        },
        {
            "id": "gallery",
            "label": "Gallery",
            "i18n_key": "nav.gallery",
            "icon": "bi-images",
            "endpoint": "admin.gallery_dashboard",
            "slug": None,
            "badge": None,
            "children": [],
        },
        {
            "id": "team",
            "label": "Team",
            "i18n_key": "nav.team",
            "icon": "bi-people",
            "endpoint": "admin.team_dashboard",
            "slug": None,
            "badge": None,
            "children": [],
        },
        {
            "id": "careers",
            "label": "Careers",
            "i18n_key": "nav.careers",
            "icon": "bi-briefcase",
            "endpoint": "admin.careers_dashboard",
            "slug": None,
            "badge": None,
            "children": [],
        },
        {
            "id": "messages",
            "label": "Messages",
            "i18n_key": "nav.messages",
            "icon": "bi-inbox",
            "endpoint": "admin.messages_inbox",
            "slug": None,
            "badge": None,
            "children": [
                {"label": "Contact Messages", "i18n_key": "nav.contact_messages", "endpoint": "admin.messages_inbox", "slug": None, "anchor": None, "query": {"tab": "contacts"}},
                {"label": "Quote Requests", "i18n_key": "nav.quote_requests", "endpoint": "admin.messages_inbox", "slug": None, "anchor": None, "query": {"tab": "quotes"}},
                {"label": "Job Applications", "i18n_key": "nav.job_applications", "endpoint": "admin.messages_inbox", "slug": None, "anchor": None, "query": {"tab": "applications"}},
            ],
        },
        {
            "id": "media",
            "label": "Media",
            "i18n_key": "nav.media",
            "icon": "bi-folder2-open",
            "endpoint": "admin.media_dashboard",
            "slug": None,
            "badge": None,
            "children": [],
        },
        {
            "id": "users",
            "label": "Users & RBAC",
            "i18n_key": "nav.users",
            "icon": "bi-person-badge",
            "endpoint": "admin.users_dashboard",
            "slug": None,
            "badge": None,
            "children": [
                {"label": "Users", "i18n_key": "nav.users_list", "endpoint": "admin.users_dashboard", "slug": None, "anchor": None, "query": {"tab": "users"}},
                {"label": "Roles", "i18n_key": "nav.roles", "endpoint": "admin.users_dashboard", "slug": None, "anchor": None, "query": {"tab": "roles"}},
                {"label": "Audit Logs", "i18n_key": "nav.audit_logs", "endpoint": "admin.users_dashboard", "slug": None, "anchor": None, "query": {"tab": "audit-logs"}},
            ],
        },
        {
            "id": "reports",
            "label": "Reports",
            "i18n_key": "nav.reports",
            "icon": "bi-bar-chart-line",
            "endpoint": "admin.reports_dashboard",
            "slug": None,
            "badge": None,
            "children": [],
        },
        {
            "id": "system",
            "label": "System",
            "i18n_key": "nav.system",
            "icon": "bi-hdd-stack",
            "endpoint": "admin.system_dashboard",
            "slug": None,
            "badge": None,
            "children": [],
        },
        {
            "id": "settings",
            "label": "Settings",
            "i18n_key": "nav.settings",
            "icon": "bi-gear",
            "endpoint": "admin.settings_hub",
            "slug": None,
            "badge": None,
            "children": [],
        },
    ]


def build_quick_actions() -> list[dict[str, Any]]:
    """Dashboard quick action cards — links to future modules."""
    return [
        {
            "label": "Add Project",
            "i18n_key": "actions.add_project",
            "icon": "bi-plus-circle",
            "description": "Create a new portfolio project",
            "endpoint": "admin.projects_create",
            "module_slug": None,
            "color": "primary",
        },
        {
            "label": "Add Service",
            "i18n_key": "actions.add_service",
            "icon": "bi-grid",
            "description": "Publish a new service offering",
            "endpoint": "admin.services_create",
            "module_slug": None,
            "color": "accent",
        },
        {
            "label": "Upload Media",
            "i18n_key": "actions.upload_media",
            "icon": "bi-cloud-upload",
            "description": "Add images, videos, or documents",
            "endpoint": "admin.media_upload",
            "module_slug": None,
            "color": "success",
        },
        {
            "label": "Create Career",
            "i18n_key": "actions.create_career",
            "icon": "bi-briefcase",
            "description": "Post a new job opening",
            "endpoint": "admin.careers_create",
            "module_slug": None,
            "color": "warning",
        },
        {
            "label": "Website Settings",
            "i18n_key": "actions.website_settings",
            "icon": "bi-sliders",
            "description": "Company info, offices, and SEO",
            "endpoint": "admin.settings_hub",
            "module_slug": None,
            "color": "info",
        },
    ]
