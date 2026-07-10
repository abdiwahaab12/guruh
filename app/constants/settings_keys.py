"""
SiteSetting key registry — grouped by admin settings section.

Values are stored as text in `site_settings.value`. Booleans use 'true'/'false'.
"""

from __future__ import annotations

from typing import Any, Final

# ---------------------------------------------------------------------------
# Business information (SiteSetting keys)
# ---------------------------------------------------------------------------
KEY_BUSINESS_OVERVIEW: Final[str] = "business.company_overview"
KEY_BUSINESS_INTRODUCTION: Final[str] = "business.company_introduction"
KEY_BUSINESS_ABOUT: Final[str] = "business.about_the_company"
KEY_BUSINESS_HISTORY: Final[str] = "business.company_history"
KEY_BUSINESS_VISION: Final[str] = "business.vision"
KEY_BUSINESS_MISSION: Final[str] = "business.mission"
KEY_BUSINESS_DIRECTORS_MESSAGE: Final[str] = "business.directors_message"

BUSINESS_KEYS: Final[tuple[str, ...]] = (
    KEY_BUSINESS_OVERVIEW,
    KEY_BUSINESS_INTRODUCTION,
    KEY_BUSINESS_ABOUT,
    KEY_BUSINESS_HISTORY,
    KEY_BUSINESS_VISION,
    KEY_BUSINESS_MISSION,
    KEY_BUSINESS_DIRECTORS_MESSAGE,
)

# ---------------------------------------------------------------------------
# SEO
# ---------------------------------------------------------------------------
KEY_SEO_SITE_TITLE: Final[str] = "seo.site_title"
KEY_SEO_META_DESCRIPTION: Final[str] = "seo.meta_description"
KEY_SEO_META_KEYWORDS: Final[str] = "seo.meta_keywords"
KEY_SEO_OG_IMAGE: Final[str] = "seo.og_image"
KEY_SEO_ROBOTS: Final[str] = "seo.robots"
KEY_SEO_CANONICAL_BASE: Final[str] = "seo.canonical_base_url"

SEO_KEYS: Final[tuple[str, ...]] = (
    KEY_SEO_SITE_TITLE,
    KEY_SEO_META_DESCRIPTION,
    KEY_SEO_META_KEYWORDS,
    KEY_SEO_OG_IMAGE,
    KEY_SEO_ROBOTS,
    KEY_SEO_CANONICAL_BASE,
)

# ---------------------------------------------------------------------------
# SMTP
# ---------------------------------------------------------------------------
KEY_SMTP_HOST: Final[str] = "smtp.host"
KEY_SMTP_PORT: Final[str] = "smtp.port"
KEY_SMTP_USERNAME: Final[str] = "smtp.username"
KEY_SMTP_PASSWORD: Final[str] = "smtp.password"
KEY_SMTP_USE_TLS: Final[str] = "smtp.use_tls"
KEY_SMTP_FROM_EMAIL: Final[str] = "smtp.from_email"
KEY_SMTP_FROM_NAME: Final[str] = "smtp.from_name"

SMTP_KEYS: Final[tuple[str, ...]] = (
    KEY_SMTP_HOST,
    KEY_SMTP_PORT,
    KEY_SMTP_USERNAME,
    KEY_SMTP_PASSWORD,
    KEY_SMTP_USE_TLS,
    KEY_SMTP_FROM_EMAIL,
    KEY_SMTP_FROM_NAME,
)

# ---------------------------------------------------------------------------
# Google Maps
# ---------------------------------------------------------------------------
KEY_MAPS_API_KEY: Final[str] = "maps.api_key"
KEY_MAPS_DEFAULT_LAT: Final[str] = "maps.default_latitude"
KEY_MAPS_DEFAULT_LNG: Final[str] = "maps.default_longitude"
KEY_MAPS_DEFAULT_ZOOM: Final[str] = "maps.default_zoom"
KEY_MAPS_EMBED_URL: Final[str] = "maps.embed_url"
KEY_MAPS_PROVIDER: Final[str] = "maps.provider"

MAPS_KEYS: Final[tuple[str, ...]] = (
    KEY_MAPS_API_KEY,
    KEY_MAPS_DEFAULT_LAT,
    KEY_MAPS_DEFAULT_LNG,
    KEY_MAPS_DEFAULT_ZOOM,
    KEY_MAPS_EMBED_URL,
    KEY_MAPS_PROVIDER,
)

# ---------------------------------------------------------------------------
# Localization
# ---------------------------------------------------------------------------
KEY_LOCALE_DEFAULT: Final[str] = "locale.default"
KEY_LOCALE_AVAILABLE: Final[str] = "locale.available"
KEY_LOCALE_TIMEZONE: Final[str] = "locale.timezone"
KEY_LOCALE_DATE_FORMAT: Final[str] = "locale.date_format"
KEY_LOCALE_CURRENCY: Final[str] = "locale.currency"

LOCALE_KEYS: Final[tuple[str, ...]] = (
    KEY_LOCALE_DEFAULT,
    KEY_LOCALE_AVAILABLE,
    KEY_LOCALE_TIMEZONE,
    KEY_LOCALE_DATE_FORMAT,
    KEY_LOCALE_CURRENCY,
)

# ---------------------------------------------------------------------------
# Theme (public site branding)
# ---------------------------------------------------------------------------
KEY_THEME_PRIMARY: Final[str] = "theme.primary_color"
KEY_THEME_ACCENT: Final[str] = "theme.accent_color"
KEY_THEME_FONT: Final[str] = "theme.font_family"
KEY_THEME_ENABLE_DARK: Final[str] = "theme.enable_dark_mode"

THEME_KEYS: Final[tuple[str, ...]] = (
    KEY_THEME_PRIMARY,
    KEY_THEME_ACCENT,
    KEY_THEME_FONT,
    KEY_THEME_ENABLE_DARK,
)

# ---------------------------------------------------------------------------
# Maintenance mode
# ---------------------------------------------------------------------------
KEY_MAINTENANCE_ENABLED: Final[str] = "maintenance.enabled"
KEY_MAINTENANCE_MESSAGE: Final[str] = "maintenance.message"
KEY_MAINTENANCE_ALLOWED_IPS: Final[str] = "maintenance.allowed_ips"

MAINTENANCE_KEYS: Final[tuple[str, ...]] = (
    KEY_MAINTENANCE_ENABLED,
    KEY_MAINTENANCE_MESSAGE,
    KEY_MAINTENANCE_ALLOWED_IPS,
)

# ---------------------------------------------------------------------------
# Analytics
# ---------------------------------------------------------------------------
KEY_ANALYTICS_GA_ID: Final[str] = "analytics.google_analytics_id"
KEY_ANALYTICS_GTM_ID: Final[str] = "analytics.google_tag_manager_id"
KEY_ANALYTICS_FB_PIXEL: Final[str] = "analytics.facebook_pixel_id"
KEY_ANALYTICS_ENABLE_DASHBOARD: Final[str] = "analytics.enable_dashboard_widgets"

ANALYTICS_KEYS: Final[tuple[str, ...]] = (
    KEY_ANALYTICS_GA_ID,
    KEY_ANALYTICS_GTM_ID,
    KEY_ANALYTICS_FB_PIXEL,
    KEY_ANALYTICS_ENABLE_DASHBOARD,
)

SETTING_DESCRIPTIONS: Final[dict[str, str]] = {
    KEY_BUSINESS_OVERVIEW: "Company overview paragraph",
    KEY_BUSINESS_INTRODUCTION: "Company introduction paragraph",
    KEY_BUSINESS_ABOUT: "About the company paragraph",
    KEY_BUSINESS_HISTORY: "Company history paragraph",
    KEY_BUSINESS_VISION: "Vision statement",
    KEY_BUSINESS_MISSION: "Mission statement",
    KEY_BUSINESS_DIRECTORS_MESSAGE: "Directors message summary",
    KEY_SEO_SITE_TITLE: "Default site title suffix",
    KEY_SEO_META_DESCRIPTION: "Default meta description",
    KEY_SEO_META_KEYWORDS: "Default meta keywords",
    KEY_SEO_OG_IMAGE: "Default Open Graph image path",
    KEY_SEO_ROBOTS: "Default robots directive",
    KEY_SEO_CANONICAL_BASE: "Canonical base URL",
    KEY_SMTP_HOST: "SMTP server hostname",
    KEY_SMTP_PORT: "SMTP server port",
    KEY_SMTP_USERNAME: "SMTP username",
    KEY_SMTP_PASSWORD: "SMTP password",
    KEY_SMTP_USE_TLS: "Use TLS for SMTP",
    KEY_SMTP_FROM_EMAIL: "Default from email address",
    KEY_SMTP_FROM_NAME: "Default from display name",
    KEY_MAPS_API_KEY: "Google Maps API key",
    KEY_MAPS_DEFAULT_LAT: "Default map latitude",
    KEY_MAPS_DEFAULT_LNG: "Default map longitude",
    KEY_MAPS_DEFAULT_ZOOM: "Default map zoom level",
    KEY_MAPS_EMBED_URL: "Optional map embed URL",
    KEY_MAPS_PROVIDER: "Map provider identifier",
    KEY_LOCALE_DEFAULT: "Default locale code",
    KEY_LOCALE_AVAILABLE: "Comma-separated available locales",
    KEY_LOCALE_TIMEZONE: "Site timezone",
    KEY_LOCALE_DATE_FORMAT: "Date display format",
    KEY_LOCALE_CURRENCY: "Default currency code",
    KEY_THEME_PRIMARY: "Primary brand color (hex)",
    KEY_THEME_ACCENT: "Accent brand color (hex)",
    KEY_THEME_FONT: "Primary font family",
    KEY_THEME_ENABLE_DARK: "Enable public dark mode toggle",
    KEY_MAINTENANCE_ENABLED: "Maintenance mode enabled",
    KEY_MAINTENANCE_MESSAGE: "Maintenance page message",
    KEY_MAINTENANCE_ALLOWED_IPS: "IPs allowed during maintenance",
    KEY_ANALYTICS_GA_ID: "Google Analytics measurement ID",
    KEY_ANALYTICS_GTM_ID: "Google Tag Manager container ID",
    KEY_ANALYTICS_FB_PIXEL: "Facebook Pixel ID",
    KEY_ANALYTICS_ENABLE_DASHBOARD: "Enable live analytics on admin dashboard",
}


def default_settings_from_profile() -> dict[str, str]:
    """Bootstrap SiteSetting defaults from static company profile."""
    from app.data.company_profile import COMPANY_PROFILE

    contact = COMPANY_PROFILE["contact"]
    msg = COMPANY_PROFILE["directors_message"]
    map_data = contact.get("map", {})

    return {
        KEY_BUSINESS_OVERVIEW: COMPANY_PROFILE["company_overview"],
        KEY_BUSINESS_INTRODUCTION: COMPANY_PROFILE["company_introduction"],
        KEY_BUSINESS_ABOUT: COMPANY_PROFILE["about_the_company"],
        KEY_BUSINESS_HISTORY: COMPANY_PROFILE["company_history"],
        KEY_BUSINESS_VISION: COMPANY_PROFILE["vision"],
        KEY_BUSINESS_MISSION: COMPANY_PROFILE["mission"],
        KEY_BUSINESS_DIRECTORS_MESSAGE: msg["summary"],
        KEY_SEO_SITE_TITLE: contact["company_name"],
        KEY_SEO_META_DESCRIPTION: (
            "GURUH Construction — professional construction services in Somalia "
            "and East Africa."
        ),
        KEY_SEO_META_KEYWORDS: "construction, civil engineering, Somalia, GURUH",
        KEY_SEO_OG_IMAGE: "img/logo.png",
        KEY_SEO_ROBOTS: "index,follow",
        KEY_SEO_CANONICAL_BASE: "",
        KEY_SMTP_HOST: "",
        KEY_SMTP_PORT: "587",
        KEY_SMTP_USERNAME: "",
        KEY_SMTP_PASSWORD: "",
        KEY_SMTP_USE_TLS: "true",
        KEY_SMTP_FROM_EMAIL: contact["email"],
        KEY_SMTP_FROM_NAME: contact["short_name"],
        KEY_MAPS_API_KEY: "",
        KEY_MAPS_DEFAULT_LAT: str(map_data.get("latitude", 2.0469)),
        KEY_MAPS_DEFAULT_LNG: str(map_data.get("longitude", 45.3182)),
        KEY_MAPS_DEFAULT_ZOOM: str(map_data.get("zoom", 16)),
        KEY_MAPS_EMBED_URL: map_data.get("embed_url", ""),
        KEY_MAPS_PROVIDER: map_data.get("map_provider", "google-maps"),
        KEY_LOCALE_DEFAULT: "en",
        KEY_LOCALE_AVAILABLE: "en,so",
        KEY_LOCALE_TIMEZONE: "Africa/Mogadishu",
        KEY_LOCALE_DATE_FORMAT: "DD MMM YYYY",
        KEY_LOCALE_CURRENCY: "USD",
        KEY_THEME_PRIMARY: "#33A8FF",
        KEY_THEME_ACCENT: "#E91E63",
        KEY_THEME_FONT: "Inter, sans-serif",
        KEY_THEME_ENABLE_DARK: "false",
        KEY_MAINTENANCE_ENABLED: "false",
        KEY_MAINTENANCE_MESSAGE: (
            "We are performing scheduled maintenance. Please check back shortly."
        ),
        KEY_MAINTENANCE_ALLOWED_IPS: "127.0.0.1",
        KEY_ANALYTICS_GA_ID: "",
        KEY_ANALYTICS_GTM_ID: "",
        KEY_ANALYTICS_FB_PIXEL: "",
        KEY_ANALYTICS_ENABLE_DASHBOARD: "false",
    }


def parse_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def bool_to_str(value: bool) -> str:
    return "true" if value else "false"
