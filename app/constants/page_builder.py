"""
Page Builder constants — layout, spacing, and animation presets.

Used by models, seed data, admin dashboard, and dynamic page templates.
"""

from typing import Final

# Section layout templates (maps to frontend component variants)
LAYOUT_TYPES: Final[tuple[str, ...]] = (
    "hero-banner",
    "default",
    "split-columns",
    "timeline",
    "card-grid",
    "stats-row",
    "logo-grid",
    "team-grid",
    "cta-banner",
    "rich-text",
    "feature-list",
    "two-column",
    "services-grid",
    "service-detail",
    "process-steps",
    "projects-showcase",
    "faq-accordion",
    "projects-portfolio",
    "areas-map",
    "testimonials-grid",
    "project-hero",
    "project-gallery",
    "project-detail-overview",
    "project-challenges",
    "project-related",
    "equipment-categories",
    "equipment-grid",
    "equipment-hero",
    "equipment-detail-overview",
    "equipment-related",
    "team-leadership",
    "org-chart",
    "team-staff-grid",
    "join-team",
    "contact-office-info",
    "google-maps",
    "contact-form",
    "department-contacts",
    "emergency-contact",
    "social-media",
    "quote-form",
    "quote-multistep-form",
    "job-openings",
    "job-detail-overview",
    "job-apply-form",
    "gallery-filters",
    "gallery-media-grid",
    "featured-albums",
    "video-gallery",
    "before-after",
    "progress-gallery",
    "awards-gallery",
    "download-center",
)

LAYOUT_TYPE_LABELS: Final[dict[str, str]] = {
    "hero-banner": "Hero Banner",
    "default": "Default Section",
    "split-columns": "Split Columns",
    "timeline": "Timeline",
    "card-grid": "Card Grid",
    "stats-row": "Statistics Row",
    "logo-grid": "Logo Grid",
    "team-grid": "Team Grid",
    "cta-banner": "Call To Action Banner",
    "rich-text": "Rich Text",
    "feature-list": "Feature List",
    "two-column": "Two Column",
    "services-grid": "Services Grid",
    "service-detail": "Service Detail",
    "process-steps": "Process Steps",
    "projects-showcase": "Projects Showcase",
    "faq-accordion": "FAQ Accordion",
    "projects-portfolio": "Projects Portfolio",
    "areas-map": "Areas Map",
    "testimonials-grid": "Testimonials Grid",
    "project-hero": "Project Hero",
    "project-gallery": "Project Gallery",
    "project-detail-overview": "Project Detail Overview",
    "project-challenges": "Project Challenges",
    "project-related": "Project Related",
    "equipment-categories": "Equipment Categories",
    "equipment-grid": "Equipment Grid",
    "equipment-hero": "Equipment Hero",
    "equipment-detail-overview": "Equipment Detail Overview",
    "equipment-related": "Equipment Related",
    "team-leadership": "Team Leadership",
    "org-chart": "Organization Chart",
    "team-staff-grid": "Team Staff Grid",
    "join-team": "Join Team",
    "contact-office-info": "Contact Office Info",
    "google-maps": "Google Maps",
    "contact-form": "Contact Form",
    "department-contacts": "Department Contacts",
    "emergency-contact": "Emergency Contact",
    "social-media": "Social Media Links",
    "quote-form": "Quote Request Form",
    "quote-multistep-form": "Multi-Step Quote Form",
    "job-openings": "Job Openings Grid",
    "job-detail-overview": "Job Detail Overview",
    "job-apply-form": "Job Application Form",
    "gallery-filters": "Gallery Filters",
    "gallery-media-grid": "Gallery Media Grid",
    "featured-albums": "Featured Albums",
    "video-gallery": "Video Gallery",
    "before-after": "Before & After Gallery",
    "progress-gallery": "Project Progress Gallery",
    "awards-gallery": "Awards & Events Gallery",
    "download-center": "Download Center",
}

BACKGROUND_STYLES: Final[tuple[str, ...]] = (
    "default",
    "light",
    "dark",
    "brand",
    "muted",
    "image",
)

BACKGROUND_STYLE_LABELS: Final[dict[str, str]] = {
    "default": "Default",
    "light": "Light",
    "dark": "Dark",
    "brand": "Brand Primary",
    "muted": "Muted",
    "image": "Background Image",
}

SPACING_PRESETS: Final[tuple[str, ...]] = (
    "default",
    "compact",
    "relaxed",
    "none",
)

SPACING_LABELS: Final[dict[str, str]] = {
    "default": "Default",
    "compact": "Compact",
    "relaxed": "Relaxed",
    "none": "No Spacing",
}

ANIMATION_PRESETS: Final[tuple[str, ...]] = (
    "none",
    "fade-up",
    "fade-in",
    "slide-up",
    "stagger",
)

ANIMATION_LABELS: Final[dict[str, str]] = {
    "none": "None",
    "fade-up": "Fade Up",
    "fade-in": "Fade In",
    "slide-up": "Slide Up",
    "stagger": "Stagger Children",
}

# Section keys that do not bind to a single CMS content block
SYSTEM_SECTION_KEYS: Final[frozenset[str]] = frozenset({"hero_banner"})
