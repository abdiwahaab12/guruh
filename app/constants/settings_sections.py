"""Admin Website Settings — section metadata for navigation and hub."""

from __future__ import annotations

from typing import Any, Final

SETTINGS_SECTIONS: Final[list[dict[str, Any]]] = [
    {
        "slug": "company",
        "label": "Company Information",
        "description": "Legal name, tagline, description, logo, and geography.",
        "icon": "bi-building",
        "endpoint": "admin.settings_company",
    },
    {
        "slug": "contact",
        "label": "Contact Information",
        "description": "Primary phone, email, address, and office hours.",
        "icon": "bi-telephone",
        "endpoint": "admin.settings_contact",
    },
    {
        "slug": "offices",
        "label": "Office Locations",
        "description": "Headquarters and branch offices shown on the contact page.",
        "icon": "bi-geo-alt",
        "endpoint": "admin.settings_offices",
    },
    {
        "slug": "business",
        "label": "Business Information",
        "description": "Vision, mission, overview, and directors message.",
        "icon": "bi-briefcase",
        "endpoint": "admin.settings_business",
    },
    {
        "slug": "social",
        "label": "Social Media",
        "description": "Social profile links for header and footer.",
        "icon": "bi-share",
        "endpoint": "admin.settings_social",
    },
    {
        "slug": "seo",
        "label": "SEO Settings",
        "description": "Default meta tags, Open Graph, and canonical URL.",
        "icon": "bi-search",
        "endpoint": "admin.settings_seo",
    },
    {
        "slug": "email",
        "label": "Email (SMTP)",
        "description": "Outbound mail server configuration for forms and alerts.",
        "icon": "bi-envelope-at",
        "endpoint": "admin.settings_email",
    },
    {
        "slug": "maps",
        "label": "Google Maps",
        "description": "API key and default map coordinates.",
        "icon": "bi-map",
        "endpoint": "admin.settings_maps",
    },
    {
        "slug": "localization",
        "label": "Localization",
        "description": "Default locale, timezone, date format, and currency.",
        "icon": "bi-translate",
        "endpoint": "admin.settings_localization",
    },
    {
        "slug": "theme",
        "label": "Theme Settings",
        "description": "Public site brand colors and typography.",
        "icon": "bi-palette",
        "endpoint": "admin.settings_theme",
    },
    {
        "slug": "maintenance",
        "label": "Maintenance Mode",
        "description": "Take the public site offline for maintenance.",
        "icon": "bi-cone-striped",
        "endpoint": "admin.settings_maintenance",
    },
    {
        "slug": "analytics",
        "label": "Analytics",
        "description": "Google Analytics, GTM, and tracking integrations.",
        "icon": "bi-graph-up-arrow",
        "endpoint": "admin.settings_analytics",
    },
]

SETTINGS_SECTION_BY_SLUG: Final[dict[str, dict[str, Any]]] = {
    section["slug"]: section for section in SETTINGS_SECTIONS
}
