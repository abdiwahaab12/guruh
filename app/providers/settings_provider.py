"""Website Settings data provider — MySQL / SQLAlchemy write layer."""

from __future__ import annotations

import re
import unicodedata

from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

from app.constants.settings_keys import SETTING_DESCRIPTIONS, default_settings_from_profile
from app.data.company_profile import COMPANY_PROFILE
from app.extensions import db
from app.models.site import CompanyInfo, OfficeLocation, SiteSetting, SocialLink
from app.providers.auth_provider import AuthProvider
from app.schemas.settings import (
    CompanySettingsDTO,
    ContactSettingsDTO,
    OfficeAdminDTO,
    SocialLinkAdminDTO,
)


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-")


class SettingsProvider:
    """Database access for website settings CRUD."""

    @staticmethod
    def commit() -> bool:
        return AuthProvider.commit()

    @staticmethod
    def rollback() -> None:
        AuthProvider.rollback()

    @staticmethod
    def record_audit(
        *,
        user_id: int | None,
        action: str,
        resource_type: str,
        resource_id: str | None = None,
        details: str | None = None,
        ip_address: str | None = None,
    ) -> None:
        AuthProvider.record_audit_event(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
        )

    # ------------------------------------------------------------------
    # Company & contact (CompanyInfo singleton)
    # ------------------------------------------------------------------

    @staticmethod
    def _company_defaults() -> dict:
        contact = COMPANY_PROFILE["contact"]
        geo = COMPANY_PROFILE.get("geography", {})
        hq = COMPANY_PROFILE.get("headquarters", {})
        return {
            "name": contact["company_name"],
            "short_name": contact["short_name"],
            "tagline": contact["tagline"],
            "description": COMPANY_PROFILE["company_overview"],
            "phone": contact["phone_primary"],
            "email": contact["email"],
            "address": contact["address"],
            "office_hours": contact["office_hours"],
            "logo_path": "img/logo.png",
            "founded_country": geo.get("founded_country", "Kenya"),
            "founded_country_code": geo.get("founded_country_code", "KE"),
            "operating_country": geo.get("operating_country", "Somalia"),
            "operating_country_code": geo.get("operating_country_code", "SO"),
            "headquarters": hq.get("summary", ""),
        }

    @staticmethod
    def get_active_company() -> CompanyInfo | None:
        try:
            return CompanyInfo.query.filter_by(is_active=True).first()
        except SQLAlchemyError as exc:
            current_app.logger.error("get_active_company failed: %s", exc)
            return None

    @staticmethod
    def get_or_create_company() -> CompanyInfo:
        row = SettingsProvider.get_active_company()
        if row:
            return row
        defaults = SettingsProvider._company_defaults()
        row = CompanyInfo(**defaults, is_active=True)
        db.session.add(row)
        return row

    @staticmethod
    def company_to_dto(row: CompanyInfo | None) -> CompanySettingsDTO:
        defaults = SettingsProvider._company_defaults()
        if not row:
            return CompanySettingsDTO(
                id=None,
                name=defaults["name"],
                short_name=defaults["short_name"],
                tagline=defaults["tagline"],
                description=defaults["description"],
                logo_path=defaults["logo_path"],
                founded_country=defaults["founded_country"],
                founded_country_code=defaults["founded_country_code"],
                operating_country=defaults["operating_country"],
                operating_country_code=defaults["operating_country_code"],
                headquarters=defaults["headquarters"],
            )
        return CompanySettingsDTO(
            id=row.id,
            name=row.name,
            short_name=row.short_name,
            tagline=row.tagline,
            description=row.description,
            logo_path=row.logo_path or "img/logo.png",
            founded_country=row.founded_country,
            founded_country_code=row.founded_country_code,
            operating_country=row.operating_country,
            operating_country_code=row.operating_country_code,
            headquarters=row.headquarters or "",
        )

    @staticmethod
    def contact_to_dto(row: CompanyInfo | None) -> ContactSettingsDTO:
        defaults = SettingsProvider._company_defaults()
        if not row:
            return ContactSettingsDTO(
                id=None,
                phone=defaults["phone"],
                email=defaults["email"],
                address=defaults["address"],
                office_hours=defaults["office_hours"],
            )
        return ContactSettingsDTO(
            id=row.id,
            phone=row.phone,
            email=row.email,
            address=row.address,
            office_hours=row.office_hours,
        )

    @staticmethod
    def update_company_info(data: CompanySettingsDTO) -> CompanyInfo:
        row = SettingsProvider.get_or_create_company()
        row.name = data.name.strip()
        row.short_name = data.short_name.strip()
        row.tagline = data.tagline.strip()
        row.description = data.description.strip()
        row.logo_path = data.logo_path.strip() or "img/logo.png"
        row.founded_country = data.founded_country.strip()
        row.founded_country_code = data.founded_country_code.strip().upper()[:2]
        row.operating_country = data.operating_country.strip()
        row.operating_country_code = data.operating_country_code.strip().upper()[:2]
        row.headquarters = data.headquarters.strip()
        return row

    @staticmethod
    def update_contact_info(data: ContactSettingsDTO) -> CompanyInfo:
        row = SettingsProvider.get_or_create_company()
        row.phone = data.phone.strip()
        row.email = data.email.strip().lower()
        row.address = data.address.strip()
        row.office_hours = data.office_hours.strip()
        return row

    # ------------------------------------------------------------------
    # SiteSetting key-value
    # ------------------------------------------------------------------

    @staticmethod
    def get_setting(key: str, default: str = "") -> str:
        try:
            row = SiteSetting.query.filter_by(key=key).first()
            if row:
                return row.value
        except SQLAlchemyError as exc:
            current_app.logger.error("get_setting(%s) failed: %s", key, exc)
        profile_defaults = default_settings_from_profile()
        return profile_defaults.get(key, default)

    @staticmethod
    def get_settings(keys: tuple[str, ...] | list[str]) -> dict[str, str]:
        result: dict[str, str] = {}
        profile_defaults = default_settings_from_profile()
        try:
            rows = SiteSetting.query.filter(SiteSetting.key.in_(keys)).all()
            found = {row.key: row.value for row in rows}
            for key in keys:
                result[key] = found.get(key, profile_defaults.get(key, ""))
        except SQLAlchemyError as exc:
            current_app.logger.error("get_settings failed: %s", exc)
            for key in keys:
                result[key] = profile_defaults.get(key, "")
        return result

    @staticmethod
    def upsert_settings(values: dict[str, str]) -> None:
        for key, value in values.items():
            row = SiteSetting.query.filter_by(key=key).first()
            if row:
                row.value = value
            else:
                db.session.add(
                    SiteSetting(
                        key=key,
                        value=value,
                        description=SETTING_DESCRIPTIONS.get(key),
                    )
                )

    # ------------------------------------------------------------------
    # Office locations
    # ------------------------------------------------------------------

    @staticmethod
    def list_offices(include_inactive: bool = False) -> list[OfficeLocation]:
        try:
            query = OfficeLocation.query
            if not include_inactive:
                query = query.filter_by(is_active=True)
            return query.order_by(OfficeLocation.sort_order, OfficeLocation.name).all()
        except SQLAlchemyError as exc:
            current_app.logger.error("list_offices failed: %s", exc)
            return []

    @staticmethod
    def get_office(office_id: int) -> OfficeLocation | None:
        try:
            return OfficeLocation.query.get(office_id)
        except SQLAlchemyError as exc:
            current_app.logger.error("get_office failed: %s", exc)
            return None

    @staticmethod
    def office_to_dto(row: OfficeLocation | None) -> OfficeAdminDTO | None:
        if not row:
            return None
        return OfficeAdminDTO(
            id=row.id,
            slug=row.slug,
            name=row.name,
            office_label=row.office_label,
            address=row.address,
            postal_address=row.postal_address or "",
            address_area=row.address_area or "",
            address_district=row.address_district or "",
            address_locality=row.address_locality or "",
            country=row.country,
            country_code=row.country_code,
            phone_primary=row.phone_primary,
            phone_secondary=row.phone_secondary or "",
            email=row.email,
            office_hours=row.office_hours or "",
            is_headquarters=row.is_headquarters,
            show_on_contact_page=row.show_on_contact_page,
            map_latitude=row.map_latitude,
            map_longitude=row.map_longitude,
            map_zoom=row.map_zoom or 16,
            sort_order=row.sort_order,
            is_active=row.is_active,
        )

    @staticmethod
    def default_office_dto() -> OfficeAdminDTO:
        office = COMPANY_PROFILE["offices"][0]
        map_data = office.get("map", {})
        return OfficeAdminDTO(
            id=None,
            slug=office["slug"],
            name=office["name"],
            office_label=office["office_label"],
            address=office["address"],
            postal_address=office.get("postal_address", ""),
            address_area=office.get("address_area", ""),
            address_district=office.get("address_district", ""),
            address_locality=office.get("address_locality", ""),
            country=office["country"],
            country_code=office["country_code"],
            phone_primary=office["phone_primary"],
            phone_secondary=office.get("phone_secondary", ""),
            email=office["email"],
            office_hours=office.get("office_hours", ""),
            is_headquarters=office.get("is_headquarters", False),
            show_on_contact_page=office.get("show_on_contact_page", True),
            map_latitude=map_data.get("latitude"),
            map_longitude=map_data.get("longitude"),
            map_zoom=map_data.get("zoom", 16),
            sort_order=office.get("sort_order", 0),
            is_active=True,
        )

    @staticmethod
    def _ensure_unique_office_slug(base_slug: str, exclude_id: int | None = None) -> str:
        slug = base_slug
        counter = 2
        while True:
            query = OfficeLocation.query.filter_by(slug=slug)
            if exclude_id:
                query = query.filter(OfficeLocation.id != exclude_id)
            if not query.first():
                return slug
            slug = f"{base_slug}-{counter}"
            counter += 1

    @staticmethod
    def save_office(data: OfficeAdminDTO) -> OfficeLocation:
        if data.is_headquarters:
            query = OfficeLocation.query.filter(OfficeLocation.is_headquarters.is_(True))
            if data.id:
                query = query.filter(OfficeLocation.id != data.id)
            query.update({"is_headquarters": False})

        if data.id:
            row = SettingsProvider.get_office(data.id)
            if not row:
                raise ValueError("Office not found.")
        else:
            row = OfficeLocation()
            db.session.add(row)

        base_slug = slugify(data.slug or data.name)
        row.slug = SettingsProvider._ensure_unique_office_slug(base_slug, data.id)
        row.name = data.name.strip()
        row.office_label = data.office_label.strip() or "Office"
        row.address = data.address.strip()
        row.postal_address = data.postal_address.strip()
        row.address_area = data.address_area.strip()
        row.address_district = data.address_district.strip()
        row.address_locality = data.address_locality.strip()
        row.country = data.country.strip()
        row.country_code = data.country_code.strip().upper()[:2]
        row.phone_primary = data.phone_primary.strip()
        row.phone_secondary = data.phone_secondary.strip()
        row.email = data.email.strip().lower()
        row.office_hours = data.office_hours.strip()
        row.is_headquarters = data.is_headquarters
        row.show_on_contact_page = data.show_on_contact_page
        row.map_latitude = data.map_latitude
        row.map_longitude = data.map_longitude
        row.map_zoom = data.map_zoom or 16
        row.sort_order = data.sort_order
        row.is_active = data.is_active
        return row

    @staticmethod
    def deactivate_office(office_id: int) -> OfficeLocation | None:
        row = SettingsProvider.get_office(office_id)
        if row:
            row.is_active = False
        return row

    # ------------------------------------------------------------------
    # Social links
    # ------------------------------------------------------------------

    @staticmethod
    def list_social_links(include_inactive: bool = False) -> list[SocialLink]:
        try:
            query = SocialLink.query
            if not include_inactive:
                query = query.filter_by(is_active=True)
            return query.order_by(SocialLink.sort_order, SocialLink.platform).all()
        except SQLAlchemyError as exc:
            current_app.logger.error("list_social_links failed: %s", exc)
            return []

    @staticmethod
    def get_social_link(link_id: int) -> SocialLink | None:
        try:
            return SocialLink.query.get(link_id)
        except SQLAlchemyError as exc:
            current_app.logger.error("get_social_link failed: %s", exc)
            return None

    @staticmethod
    def social_to_dto(row: SocialLink | None) -> SocialLinkAdminDTO | None:
        if not row:
            return None
        return SocialLinkAdminDTO(
            id=row.id,
            platform=row.platform,
            label=row.label,
            icon=row.icon,
            url=row.url,
            sort_order=row.sort_order,
            is_active=row.is_active,
        )

    @staticmethod
    def default_social_dto() -> SocialLinkAdminDTO:
        return SocialLinkAdminDTO(
            id=None,
            platform="",
            label="",
            icon="bi-link",
            url="https://",
            sort_order=0,
            is_active=True,
        )

    @staticmethod
    def save_social_link(data: SocialLinkAdminDTO) -> SocialLink:
        if data.id:
            row = SettingsProvider.get_social_link(data.id)
            if not row:
                raise ValueError("Social link not found.")
        else:
            row = SocialLink()
            db.session.add(row)

        row.platform = data.platform.strip().lower()
        row.label = data.label.strip()
        row.icon = data.icon.strip() or "bi-link"
        row.url = data.url.strip()
        row.sort_order = data.sort_order
        row.is_active = data.is_active
        return row

    @staticmethod
    def deactivate_social_link(link_id: int) -> SocialLink | None:
        row = SettingsProvider.get_social_link(link_id)
        if row:
            row.is_active = False
        return row
