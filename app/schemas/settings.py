"""Website Settings DTOs — admin module data transfer."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SettingsSectionDTO:
    slug: str
    label: str
    description: str
    icon: str
    endpoint: str


@dataclass
class SaveResultDTO:
    success: bool
    message: str


@dataclass
class CompanySettingsDTO:
    id: int | None
    name: str
    short_name: str
    tagline: str
    description: str
    logo_path: str
    founded_country: str
    founded_country_code: str
    operating_country: str
    operating_country_code: str
    headquarters: str


@dataclass
class ContactSettingsDTO:
    id: int | None
    phone: str
    email: str
    address: str
    office_hours: str


@dataclass
class OfficeAdminDTO:
    id: int | None
    slug: str
    name: str
    office_label: str
    address: str
    postal_address: str
    address_area: str
    address_district: str
    address_locality: str
    country: str
    country_code: str
    phone_primary: str
    phone_secondary: str
    email: str
    office_hours: str
    is_headquarters: bool
    show_on_contact_page: bool
    map_latitude: float | None
    map_longitude: float | None
    map_zoom: int
    sort_order: int
    is_active: bool


@dataclass
class SocialLinkAdminDTO:
    id: int | None
    platform: str
    label: str
    icon: str
    url: str
    sort_order: int
    is_active: bool


@dataclass
class KeyValueSettingsDTO:
    """Grouped key-value settings for a section."""

    values: dict[str, str] = field(default_factory=dict)
