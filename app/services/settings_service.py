"""Website Settings business logic — Route → SettingsService → Provider → DTO."""

from __future__ import annotations

from flask import url_for
from flask_login import current_user

from app.constants.settings_keys import (
    ANALYTICS_KEYS,
    BUSINESS_KEYS,
    KEY_ANALYTICS_ENABLE_DASHBOARD,
    KEY_MAINTENANCE_ENABLED,
    KEY_MAPS_DEFAULT_LAT,
    KEY_MAPS_DEFAULT_LNG,
    KEY_MAPS_DEFAULT_ZOOM,
    KEY_SMTP_PORT,
    KEY_SMTP_USE_TLS,
    KEY_THEME_ENABLE_DARK,
    LOCALE_KEYS,
    MAINTENANCE_KEYS,
    MAPS_KEYS,
    SEO_KEYS,
    SMTP_KEYS,
    THEME_KEYS,
    bool_to_str,
    parse_bool,
)
from app.constants.settings_sections import SETTINGS_SECTIONS, SETTINGS_SECTION_BY_SLUG
from app.providers.admin_dashboard_provider import AdminDashboardProvider
from app.providers.settings_provider import SettingsProvider
from app.schemas.admin import BreadcrumbItemDTO
from app.schemas.settings import (
    CompanySettingsDTO,
    ContactSettingsDTO,
    OfficeAdminDTO,
    SaveResultDTO,
    SocialLinkAdminDTO,
)


class SettingsService:
    """Enterprise website settings service."""

    @staticmethod
    def get_shell_context(
        *,
        page_title: str,
        active_section: str | None = None,
        breadcrumbs: list[BreadcrumbItemDTO] | None = None,
    ) -> dict:
        dashboard = AdminDashboardProvider.get_dashboard()
        return {
            "page_title": page_title,
            "active_nav": "settings",
            "settings_active_section": active_section,
            "settings_sections": SETTINGS_SECTIONS,
            "breadcrumbs": breadcrumbs
            or SettingsService.build_breadcrumbs(page_title),
            "notifications": dashboard.notifications,
            "unread_notification_count": dashboard.unread_notification_count,
            "user": current_user,
        }

    @staticmethod
    def build_breadcrumbs(current_label: str) -> list[BreadcrumbItemDTO]:
        return [
            BreadcrumbItemDTO("Admin", url_for("admin.dashboard"), False),
            BreadcrumbItemDTO("Website Settings", url_for("admin.settings_hub"), False),
            BreadcrumbItemDTO(current_label, None, True),
        ]

    @staticmethod
    def get_hub_context() -> dict:
        ctx = SettingsService.get_shell_context(
            page_title="Website Settings",
            active_section=None,
            breadcrumbs=[
                BreadcrumbItemDTO("Admin", url_for("admin.dashboard"), False),
                BreadcrumbItemDTO("Website Settings", None, True),
            ],
        )
        ctx["sections"] = SETTINGS_SECTIONS
        return ctx

    @staticmethod
    def get_company_context() -> dict:
        row = SettingsProvider.get_active_company()
        ctx = SettingsService.get_shell_context(
            page_title="Company Information",
            active_section="company",
        )
        ctx["company"] = SettingsProvider.company_to_dto(row)
        return ctx

    @staticmethod
    def save_company(data: CompanySettingsDTO, *, ip_address: str | None) -> SaveResultDTO:
        try:
            row = SettingsProvider.update_company_info(data)
            SettingsProvider.record_audit(
                user_id=current_user.id,
                action="settings.company.update",
                resource_type="company_info",
                resource_id=str(row.id) if row.id else None,
                details=f"Updated company profile: {data.name}",
                ip_address=ip_address,
            )
            if SettingsProvider.commit():
                return SaveResultDTO(True, "Company information saved successfully.")
            return SaveResultDTO(False, "Unable to save company information. Please try again.")
        except Exception as exc:
            SettingsProvider.rollback()
            return SaveResultDTO(False, f"Save failed: {exc}")

    @staticmethod
    def get_contact_context() -> dict:
        row = SettingsProvider.get_active_company()
        ctx = SettingsService.get_shell_context(
            page_title="Contact Information",
            active_section="contact",
        )
        ctx["contact"] = SettingsProvider.contact_to_dto(row)
        return ctx

    @staticmethod
    def save_contact(data: ContactSettingsDTO, *, ip_address: str | None) -> SaveResultDTO:
        try:
            row = SettingsProvider.update_contact_info(data)
            SettingsProvider.record_audit(
                user_id=current_user.id,
                action="settings.contact.update",
                resource_type="company_info",
                resource_id=str(row.id) if row.id else None,
                details=f"Updated contact info: {data.email}",
                ip_address=ip_address,
            )
            if SettingsProvider.commit():
                return SaveResultDTO(True, "Contact information saved successfully.")
            return SaveResultDTO(False, "Unable to save contact information.")
        except Exception as exc:
            SettingsProvider.rollback()
            return SaveResultDTO(False, f"Save failed: {exc}")

    @staticmethod
    def get_offices_context() -> dict:
        offices = SettingsProvider.list_offices(include_inactive=True)
        ctx = SettingsService.get_shell_context(
            page_title="Office Locations",
            active_section="offices",
        )
        ctx["offices"] = [SettingsProvider.office_to_dto(o) for o in offices]
        return ctx

    @staticmethod
    def get_office_form_context(office_id: int | None) -> dict:
        if office_id:
            row = SettingsProvider.get_office(office_id)
            office = SettingsProvider.office_to_dto(row)
            title = f"Edit Office — {office.name}" if office else "Edit Office"
        else:
            office = SettingsProvider.default_office_dto()
            title = "Add Office Location"
        ctx = SettingsService.get_shell_context(page_title=title, active_section="offices")
        ctx["office"] = office
        ctx["is_edit"] = office_id is not None
        return ctx

    @staticmethod
    def save_office(data: OfficeAdminDTO, *, ip_address: str | None) -> SaveResultDTO:
        try:
            row = SettingsProvider.save_office(data)
            action = "settings.office.update" if data.id else "settings.office.create"
            SettingsProvider.record_audit(
                user_id=current_user.id,
                action=action,
                resource_type="office_location",
                resource_id=str(row.id) if row.id else None,
                details=f"Saved office: {data.name}",
                ip_address=ip_address,
            )
            if SettingsProvider.commit():
                return SaveResultDTO(True, "Office location saved successfully.")
            return SaveResultDTO(False, "Unable to save office location.")
        except ValueError as exc:
            SettingsProvider.rollback()
            return SaveResultDTO(False, str(exc))
        except Exception as exc:
            SettingsProvider.rollback()
            return SaveResultDTO(False, f"Save failed: {exc}")

    @staticmethod
    def delete_office(office_id: int, *, ip_address: str | None) -> SaveResultDTO:
        try:
            row = SettingsProvider.deactivate_office(office_id)
            if not row:
                return SaveResultDTO(False, "Office not found.")
            SettingsProvider.record_audit(
                user_id=current_user.id,
                action="settings.office.deactivate",
                resource_type="office_location",
                resource_id=str(office_id),
                details=f"Deactivated office: {row.name}",
                ip_address=ip_address,
            )
            if SettingsProvider.commit():
                return SaveResultDTO(True, "Office location removed.")
            return SaveResultDTO(False, "Unable to remove office location.")
        except Exception as exc:
            SettingsProvider.rollback()
            return SaveResultDTO(False, f"Delete failed: {exc}")

    @staticmethod
    def get_business_context() -> dict:
        values = SettingsProvider.get_settings(BUSINESS_KEYS)
        ctx = SettingsService.get_shell_context(
            page_title="Business Information",
            active_section="business",
        )
        ctx["settings"] = values
        return ctx

    @staticmethod
    def save_key_value_section(
        *,
        section_slug: str,
        values: dict[str, str],
        audit_action: str,
        ip_address: str | None,
    ) -> SaveResultDTO:
        section = SETTINGS_SECTION_BY_SLUG.get(section_slug)
        label = section["label"] if section else section_slug
        try:
            SettingsProvider.upsert_settings(values)
            SettingsProvider.record_audit(
                user_id=current_user.id,
                action=audit_action,
                resource_type="site_settings",
                resource_id=section_slug,
                details=f"Updated {label}",
                ip_address=ip_address,
            )
            if SettingsProvider.commit():
                return SaveResultDTO(True, f"{label} saved successfully.")
            return SaveResultDTO(False, f"Unable to save {label}.")
        except Exception as exc:
            SettingsProvider.rollback()
            return SaveResultDTO(False, f"Save failed: {exc}")

    @staticmethod
    def get_social_context() -> dict:
        links = SettingsProvider.list_social_links(include_inactive=True)
        ctx = SettingsService.get_shell_context(
            page_title="Social Media",
            active_section="social",
        )
        ctx["social_links"] = [SettingsProvider.social_to_dto(link) for link in links]
        return ctx

    @staticmethod
    def get_social_form_context(link_id: int | None) -> dict:
        if link_id:
            row = SettingsProvider.get_social_link(link_id)
            link = SettingsProvider.social_to_dto(row)
            title = f"Edit Social Link — {link.label}" if link else "Edit Social Link"
        else:
            link = SettingsProvider.default_social_dto()
            title = "Add Social Link"
        ctx = SettingsService.get_shell_context(page_title=title, active_section="social")
        ctx["link"] = link
        ctx["is_edit"] = link_id is not None
        return ctx

    @staticmethod
    def save_social(data: SocialLinkAdminDTO, *, ip_address: str | None) -> SaveResultDTO:
        try:
            row = SettingsProvider.save_social_link(data)
            action = "settings.social.update" if data.id else "settings.social.create"
            SettingsProvider.record_audit(
                user_id=current_user.id,
                action=action,
                resource_type="social_link",
                resource_id=str(row.id) if row.id else None,
                details=f"Saved social link: {data.platform}",
                ip_address=ip_address,
            )
            if SettingsProvider.commit():
                return SaveResultDTO(True, "Social link saved successfully.")
            return SaveResultDTO(False, "Unable to save social link.")
        except ValueError as exc:
            SettingsProvider.rollback()
            return SaveResultDTO(False, str(exc))
        except Exception as exc:
            SettingsProvider.rollback()
            return SaveResultDTO(False, f"Save failed: {exc}")

    @staticmethod
    def delete_social(link_id: int, *, ip_address: str | None) -> SaveResultDTO:
        try:
            row = SettingsProvider.deactivate_social_link(link_id)
            if not row:
                return SaveResultDTO(False, "Social link not found.")
            SettingsProvider.record_audit(
                user_id=current_user.id,
                action="settings.social.deactivate",
                resource_type="social_link",
                resource_id=str(link_id),
                details=f"Deactivated social link: {row.platform}",
                ip_address=ip_address,
            )
            if SettingsProvider.commit():
                return SaveResultDTO(True, "Social link removed.")
            return SaveResultDTO(False, "Unable to remove social link.")
        except Exception as exc:
            SettingsProvider.rollback()
            return SaveResultDTO(False, f"Delete failed: {exc}")

    @staticmethod
    def get_seo_context() -> dict:
        ctx = SettingsService.get_shell_context(page_title="SEO Settings", active_section="seo")
        ctx["settings"] = SettingsProvider.get_settings(SEO_KEYS)
        return ctx

    @staticmethod
    def get_email_context() -> dict:
        ctx = SettingsService.get_shell_context(
            page_title="Email (SMTP)",
            active_section="email",
        )
        settings = SettingsProvider.get_settings(SMTP_KEYS)
        settings[KEY_SMTP_USE_TLS] = "true" if parse_bool(settings.get(KEY_SMTP_USE_TLS)) else "false"
        ctx["settings"] = settings
        return ctx

    @staticmethod
    def get_maps_context() -> dict:
        ctx = SettingsService.get_shell_context(
            page_title="Google Maps",
            active_section="maps",
        )
        ctx["settings"] = SettingsProvider.get_settings(MAPS_KEYS)
        return ctx

    @staticmethod
    def get_localization_context() -> dict:
        ctx = SettingsService.get_shell_context(
            page_title="Localization",
            active_section="localization",
        )
        ctx["settings"] = SettingsProvider.get_settings(LOCALE_KEYS)
        return ctx

    @staticmethod
    def get_theme_context() -> dict:
        ctx = SettingsService.get_shell_context(
            page_title="Theme Settings",
            active_section="theme",
        )
        settings = SettingsProvider.get_settings(THEME_KEYS)
        settings[KEY_THEME_ENABLE_DARK] = (
            "true" if parse_bool(settings.get(KEY_THEME_ENABLE_DARK)) else "false"
        )
        ctx["settings"] = settings
        return ctx

    @staticmethod
    def get_maintenance_context() -> dict:
        ctx = SettingsService.get_shell_context(
            page_title="Maintenance Mode",
            active_section="maintenance",
        )
        settings = SettingsProvider.get_settings(MAINTENANCE_KEYS)
        settings[KEY_MAINTENANCE_ENABLED] = (
            "true" if parse_bool(settings.get(KEY_MAINTENANCE_ENABLED)) else "false"
        )
        ctx["settings"] = settings
        return ctx

    @staticmethod
    def get_analytics_context() -> dict:
        ctx = SettingsService.get_shell_context(
            page_title="Analytics",
            active_section="analytics",
        )
        settings = SettingsProvider.get_settings(ANALYTICS_KEYS)
        settings[KEY_ANALYTICS_ENABLE_DASHBOARD] = (
            "true" if parse_bool(settings.get(KEY_ANALYTICS_ENABLE_DASHBOARD)) else "false"
        )
        ctx["settings"] = settings
        return ctx

    @staticmethod
    def office_from_form(form) -> OfficeAdminDTO:
        lat = form.map_latitude.data
        lng = form.map_longitude.data
        return OfficeAdminDTO(
            id=form.office_id.data or None,
            slug=form.slug.data or "",
            name=form.name.data,
            office_label=form.office_label.data,
            address=form.address.data,
            postal_address=form.postal_address.data or "",
            address_area=form.address_area.data or "",
            address_district=form.address_district.data or "",
            address_locality=form.address_locality.data or "",
            country=form.country.data,
            country_code=form.country_code.data,
            phone_primary=form.phone_primary.data,
            phone_secondary=form.phone_secondary.data or "",
            email=form.email.data,
            office_hours=form.office_hours.data or "",
            is_headquarters=form.is_headquarters.data,
            show_on_contact_page=form.show_on_contact_page.data,
            map_latitude=float(lat) if lat is not None and lat != "" else None,
            map_longitude=float(lng) if lng is not None and lng != "" else None,
            map_zoom=int(form.map_zoom.data or 16),
            sort_order=int(form.sort_order.data or 0),
            is_active=form.is_active.data,
        )

    @staticmethod
    def social_from_form(form) -> SocialLinkAdminDTO:
        return SocialLinkAdminDTO(
            id=form.link_id.data or None,
            platform=form.platform.data,
            label=form.label.data,
            icon=form.icon.data,
            url=form.url.data,
            sort_order=int(form.sort_order.data or 0),
            is_active=form.is_active.data,
        )

    @staticmethod
    def validate_maps_coordinates(values: dict[str, str]) -> str | None:
        try:
            lat = float(values.get(KEY_MAPS_DEFAULT_LAT, "") or 0)
            lng = float(values.get(KEY_MAPS_DEFAULT_LNG, "") or 0)
            zoom = int(values.get(KEY_MAPS_DEFAULT_ZOOM, "16") or 16)
        except ValueError:
            return "Map coordinates and zoom must be valid numbers."
        if not -90 <= lat <= 90:
            return "Latitude must be between -90 and 90."
        if not -180 <= lng <= 180:
            return "Longitude must be between -180 and 180."
        if not 1 <= zoom <= 21:
            return "Zoom must be between 1 and 21."
        return None

    @staticmethod
    def normalize_smtp_values(values: dict[str, str]) -> dict[str, str]:
        port = values.get(KEY_SMTP_PORT, "587").strip() or "587"
        values[KEY_SMTP_PORT] = port
        values[KEY_SMTP_USE_TLS] = bool_to_str(parse_bool(values.get(KEY_SMTP_USE_TLS)))
        return values

    @staticmethod
    def normalize_bool_values(values: dict[str, str], *keys: str) -> dict[str, str]:
        for key in keys:
            if key in values:
                values[key] = bool_to_str(parse_bool(values.get(key)))
        return values
