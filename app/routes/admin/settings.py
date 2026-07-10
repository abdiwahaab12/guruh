"""Website Settings admin routes — Step 15."""

from __future__ import annotations

from flask import flash, redirect, render_template, request, url_for

from app.constants.settings_keys import (
    ANALYTICS_KEYS,
    BUSINESS_KEYS,
    KEY_ANALYTICS_ENABLE_DASHBOARD,
    KEY_ANALYTICS_FB_PIXEL,
    KEY_ANALYTICS_GA_ID,
    KEY_ANALYTICS_GTM_ID,
    KEY_BUSINESS_ABOUT,
    KEY_BUSINESS_DIRECTORS_MESSAGE,
    KEY_BUSINESS_HISTORY,
    KEY_BUSINESS_INTRODUCTION,
    KEY_BUSINESS_MISSION,
    KEY_BUSINESS_OVERVIEW,
    KEY_BUSINESS_VISION,
    KEY_LOCALE_AVAILABLE,
    KEY_LOCALE_CURRENCY,
    KEY_LOCALE_DATE_FORMAT,
    KEY_LOCALE_DEFAULT,
    KEY_LOCALE_TIMEZONE,
    KEY_MAINTENANCE_ALLOWED_IPS,
    KEY_MAINTENANCE_ENABLED,
    KEY_MAINTENANCE_MESSAGE,
    KEY_MAPS_API_KEY,
    KEY_MAPS_DEFAULT_LAT,
    KEY_MAPS_DEFAULT_LNG,
    KEY_MAPS_DEFAULT_ZOOM,
    KEY_MAPS_EMBED_URL,
    KEY_MAPS_PROVIDER,
    KEY_SEO_CANONICAL_BASE,
    KEY_SEO_META_DESCRIPTION,
    KEY_SEO_META_KEYWORDS,
    KEY_SEO_OG_IMAGE,
    KEY_SEO_ROBOTS,
    KEY_SEO_SITE_TITLE,
    KEY_SMTP_FROM_EMAIL,
    KEY_SMTP_FROM_NAME,
    KEY_SMTP_HOST,
    KEY_SMTP_PASSWORD,
    KEY_SMTP_PORT,
    KEY_SMTP_USERNAME,
    KEY_SMTP_USE_TLS,
    KEY_THEME_ACCENT,
    KEY_THEME_ENABLE_DARK,
    KEY_THEME_FONT,
    KEY_THEME_PRIMARY,
    bool_to_str,
    parse_bool,
)
from app.forms.settings_forms import (
    AnalyticsForm,
    BusinessInfoForm,
    CompanyInfoForm,
    ContactInfoForm,
    DeleteConfirmForm,
    LocalizationForm,
    MaintenanceForm,
    MapsSettingsForm,
    OfficeLocationForm,
    SeoSettingsForm,
    SocialLinkForm,
    SmtpSettingsForm,
    ThemeSettingsForm,
)
from app.schemas.settings import CompanySettingsDTO, ContactSettingsDTO
from app.services.settings_service import SettingsService
from app.utils.permissions import can_manage_settings


def register_settings_routes(admin_bp) -> None:
    """Register Website Settings module routes."""

    @admin_bp.route("/settings")
    @can_manage_settings
    def settings_hub():
        return render_template("admin/settings/hub.html", **SettingsService.get_hub_context())

    @admin_bp.route("/settings/company", methods=["GET", "POST"])
    @can_manage_settings
    def settings_company():
        form = CompanyInfoForm()
        company = SettingsService.get_company_context()["company"]
        if request.method == "GET":
            form.name.data = company.name
            form.short_name.data = company.short_name
            form.tagline.data = company.tagline
            form.description.data = company.description
            form.logo_path.data = company.logo_path
            form.founded_country.data = company.founded_country
            form.founded_country_code.data = company.founded_country_code
            form.operating_country.data = company.operating_country
            form.operating_country_code.data = company.operating_country_code
            form.headquarters.data = company.headquarters

        if form.validate_on_submit():
            dto = CompanySettingsDTO(
                id=company.id,
                name=form.name.data,
                short_name=form.short_name.data,
                tagline=form.tagline.data,
                description=form.description.data,
                logo_path=form.logo_path.data,
                founded_country=form.founded_country.data,
                founded_country_code=form.founded_country_code.data,
                operating_country=form.operating_country.data,
                operating_country_code=form.operating_country_code.data,
                headquarters=form.headquarters.data or "",
            )
            result = SettingsService.save_company(dto, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success:
                return redirect(url_for("admin.settings_company"))

        ctx = SettingsService.get_company_context()
        ctx["form"] = form
        return render_template("admin/settings/company.html", **ctx)

    @admin_bp.route("/settings/contact", methods=["GET", "POST"])
    @can_manage_settings
    def settings_contact():
        form = ContactInfoForm()
        contact = SettingsService.get_contact_context()["contact"]
        if request.method == "GET":
            form.phone.data = contact.phone
            form.email.data = contact.email
            form.address.data = contact.address
            form.office_hours.data = contact.office_hours

        if form.validate_on_submit():
            dto = ContactSettingsDTO(
                id=contact.id,
                phone=form.phone.data,
                email=form.email.data,
                address=form.address.data,
                office_hours=form.office_hours.data,
            )
            result = SettingsService.save_contact(dto, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success:
                return redirect(url_for("admin.settings_contact"))

        ctx = SettingsService.get_contact_context()
        ctx["form"] = form
        return render_template("admin/settings/contact.html", **ctx)

    @admin_bp.route("/settings/offices")
    @can_manage_settings
    def settings_offices():
        ctx = SettingsService.get_offices_context()
        ctx["delete_form"] = DeleteConfirmForm()
        return render_template("admin/settings/offices.html", **ctx)

    @admin_bp.route("/settings/offices/new", methods=["GET", "POST"])
    @admin_bp.route("/settings/offices/<int:office_id>/edit", methods=["GET", "POST"])
    @can_manage_settings
    def settings_office_form(office_id: int | None = None):
        form = OfficeLocationForm()
        ctx = SettingsService.get_office_form_context(office_id)
        office = ctx["office"]

        if request.method == "GET" and office:
            form.office_id.data = office.id
            form.slug.data = office.slug
            form.name.data = office.name
            form.office_label.data = office.office_label
            form.address.data = office.address
            form.postal_address.data = office.postal_address
            form.address_area.data = office.address_area
            form.address_district.data = office.address_district
            form.address_locality.data = office.address_locality
            form.country.data = office.country
            form.country_code.data = office.country_code
            form.phone_primary.data = office.phone_primary
            form.phone_secondary.data = office.phone_secondary
            form.email.data = office.email
            form.office_hours.data = office.office_hours
            form.map_latitude.data = office.map_latitude
            form.map_longitude.data = office.map_longitude
            form.map_zoom.data = office.map_zoom
            form.sort_order.data = office.sort_order
            form.is_headquarters.data = office.is_headquarters
            form.show_on_contact_page.data = office.show_on_contact_page
            form.is_active.data = office.is_active

        if form.validate_on_submit():
            dto = SettingsService.office_from_form(form)
            result = SettingsService.save_office(dto, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success:
                return redirect(url_for("admin.settings_offices"))

        ctx["form"] = form
        return render_template("admin/settings/office_form.html", **ctx)

    @admin_bp.route("/settings/offices/<int:office_id>/delete", methods=["POST"])
    @can_manage_settings
    def settings_office_delete(office_id: int):
        form = DeleteConfirmForm()
        if not form.validate_on_submit():
            flash("Invalid delete request.", "danger")
            return redirect(url_for("admin.settings_offices"))
        result = SettingsService.delete_office(office_id, ip_address=request.remote_addr)
        flash(result.message, "success" if result.success else "danger")
        return redirect(url_for("admin.settings_offices"))

    @admin_bp.route("/settings/business", methods=["GET", "POST"])
    @can_manage_settings
    def settings_business():
        form = BusinessInfoForm()
        settings = SettingsService.get_business_context()["settings"]
        if request.method == "GET":
            form.company_overview.data = settings.get(KEY_BUSINESS_OVERVIEW, "")
            form.company_introduction.data = settings.get(KEY_BUSINESS_INTRODUCTION, "")
            form.about_the_company.data = settings.get(KEY_BUSINESS_ABOUT, "")
            form.company_history.data = settings.get(KEY_BUSINESS_HISTORY, "")
            form.vision.data = settings.get(KEY_BUSINESS_VISION, "")
            form.mission.data = settings.get(KEY_BUSINESS_MISSION, "")
            form.directors_message.data = settings.get(KEY_BUSINESS_DIRECTORS_MESSAGE, "")

        if form.validate_on_submit():
            values = {
                KEY_BUSINESS_OVERVIEW: form.company_overview.data,
                KEY_BUSINESS_INTRODUCTION: form.company_introduction.data,
                KEY_BUSINESS_ABOUT: form.about_the_company.data,
                KEY_BUSINESS_HISTORY: form.company_history.data,
                KEY_BUSINESS_VISION: form.vision.data,
                KEY_BUSINESS_MISSION: form.mission.data,
                KEY_BUSINESS_DIRECTORS_MESSAGE: form.directors_message.data,
            }
            result = SettingsService.save_key_value_section(
                section_slug="business",
                values=values,
                audit_action="settings.business.update",
                ip_address=request.remote_addr,
            )
            flash(result.message, "success" if result.success else "danger")
            if result.success:
                return redirect(url_for("admin.settings_business"))

        ctx = SettingsService.get_business_context()
        ctx["form"] = form
        return render_template("admin/settings/business.html", **ctx)

    @admin_bp.route("/settings/social")
    @can_manage_settings
    def settings_social():
        ctx = SettingsService.get_social_context()
        ctx["delete_form"] = DeleteConfirmForm()
        return render_template("admin/settings/social.html", **ctx)

    @admin_bp.route("/settings/social/new", methods=["GET", "POST"])
    @admin_bp.route("/settings/social/<int:link_id>/edit", methods=["GET", "POST"])
    @can_manage_settings
    def settings_social_form(link_id: int | None = None):
        form = SocialLinkForm()
        ctx = SettingsService.get_social_form_context(link_id)
        link = ctx["link"]

        if request.method == "GET" and link:
            form.link_id.data = link.id
            form.platform.data = link.platform
            form.label.data = link.label
            form.icon.data = link.icon
            form.url.data = link.url
            form.sort_order.data = link.sort_order
            form.is_active.data = link.is_active

        if form.validate_on_submit():
            dto = SettingsService.social_from_form(form)
            result = SettingsService.save_social(dto, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success:
                return redirect(url_for("admin.settings_social"))

        ctx["form"] = form
        return render_template("admin/settings/social_form.html", **ctx)

    @admin_bp.route("/settings/social/<int:link_id>/delete", methods=["POST"])
    @can_manage_settings
    def settings_social_delete(link_id: int):
        form = DeleteConfirmForm()
        if not form.validate_on_submit():
            flash("Invalid delete request.", "danger")
            return redirect(url_for("admin.settings_social"))
        result = SettingsService.delete_social(link_id, ip_address=request.remote_addr)
        flash(result.message, "success" if result.success else "danger")
        return redirect(url_for("admin.settings_social"))

    @admin_bp.route("/settings/seo", methods=["GET", "POST"])
    @can_manage_settings
    def settings_seo():
        form = SeoSettingsForm()
        settings = SettingsService.get_seo_context()["settings"]
        if request.method == "GET":
            form.site_title.data = settings.get(KEY_SEO_SITE_TITLE, "")
            form.meta_description.data = settings.get(KEY_SEO_META_DESCRIPTION, "")
            form.meta_keywords.data = settings.get(KEY_SEO_META_KEYWORDS, "")
            form.og_image.data = settings.get(KEY_SEO_OG_IMAGE, "")
            form.robots.data = settings.get(KEY_SEO_ROBOTS, "")
            form.canonical_base_url.data = settings.get(KEY_SEO_CANONICAL_BASE, "") or None

        if form.validate_on_submit():
            values = {
                KEY_SEO_SITE_TITLE: form.site_title.data,
                KEY_SEO_META_DESCRIPTION: form.meta_description.data,
                KEY_SEO_META_KEYWORDS: form.meta_keywords.data or "",
                KEY_SEO_OG_IMAGE: form.og_image.data or "",
                KEY_SEO_ROBOTS: form.robots.data,
                KEY_SEO_CANONICAL_BASE: form.canonical_base_url.data or "",
            }
            result = SettingsService.save_key_value_section(
                section_slug="seo",
                values=values,
                audit_action="settings.seo.update",
                ip_address=request.remote_addr,
            )
            flash(result.message, "success" if result.success else "danger")
            if result.success:
                return redirect(url_for("admin.settings_seo"))

        ctx = SettingsService.get_seo_context()
        ctx["form"] = form
        return render_template("admin/settings/seo.html", **ctx)

    @admin_bp.route("/settings/email", methods=["GET", "POST"])
    @can_manage_settings
    def settings_email():
        form = SmtpSettingsForm()
        settings = SettingsService.get_email_context()["settings"]
        if request.method == "GET":
            form.host.data = settings.get(KEY_SMTP_HOST, "")
            form.port.data = int(settings.get(KEY_SMTP_PORT, "587") or 587)
            form.username.data = settings.get(KEY_SMTP_USERNAME, "")
            form.password.data = settings.get(KEY_SMTP_PASSWORD, "")
            form.use_tls.data = parse_bool(settings.get(KEY_SMTP_USE_TLS))
            form.from_email.data = settings.get(KEY_SMTP_FROM_EMAIL, "") or None
            form.from_name.data = settings.get(KEY_SMTP_FROM_NAME, "")

        if form.validate_on_submit():
            values = {
                KEY_SMTP_HOST: form.host.data or "",
                KEY_SMTP_PORT: str(form.port.data or 587),
                KEY_SMTP_USERNAME: form.username.data or "",
                KEY_SMTP_PASSWORD: form.password.data or "",
                KEY_SMTP_USE_TLS: bool_to_str(form.use_tls.data),
                KEY_SMTP_FROM_EMAIL: form.from_email.data or "",
                KEY_SMTP_FROM_NAME: form.from_name.data or "",
            }
            values = SettingsService.normalize_smtp_values(values)
            result = SettingsService.save_key_value_section(
                section_slug="email",
                values=values,
                audit_action="settings.email.update",
                ip_address=request.remote_addr,
            )
            flash(result.message, "success" if result.success else "danger")
            if result.success:
                return redirect(url_for("admin.settings_email"))

        ctx = SettingsService.get_email_context()
        ctx["form"] = form
        return render_template("admin/settings/email.html", **ctx)

    @admin_bp.route("/settings/maps", methods=["GET", "POST"])
    @can_manage_settings
    def settings_maps():
        form = MapsSettingsForm()
        settings = SettingsService.get_maps_context()["settings"]
        if request.method == "GET":
            form.api_key.data = settings.get(KEY_MAPS_API_KEY, "")
            lat = settings.get(KEY_MAPS_DEFAULT_LAT, "")
            lng = settings.get(KEY_MAPS_DEFAULT_LNG, "")
            form.default_latitude.data = float(lat) if lat not in ("", None) else None
            form.default_longitude.data = float(lng) if lng not in ("", None) else None
            form.default_zoom.data = int(settings.get(KEY_MAPS_DEFAULT_ZOOM, "16") or 16)
            form.embed_url.data = settings.get(KEY_MAPS_EMBED_URL, "")
            form.provider.data = settings.get(KEY_MAPS_PROVIDER, "")

        if form.validate_on_submit():
            values = {
                KEY_MAPS_API_KEY: form.api_key.data or "",
                KEY_MAPS_DEFAULT_LAT: str(form.default_latitude.data or ""),
                KEY_MAPS_DEFAULT_LNG: str(form.default_longitude.data or ""),
                KEY_MAPS_DEFAULT_ZOOM: str(form.default_zoom.data or 16),
                KEY_MAPS_EMBED_URL: form.embed_url.data or "",
                KEY_MAPS_PROVIDER: form.provider.data or "google-maps",
            }
            error = SettingsService.validate_maps_coordinates(values)
            if error:
                flash(error, "danger")
            else:
                result = SettingsService.save_key_value_section(
                    section_slug="maps",
                    values=values,
                    audit_action="settings.maps.update",
                    ip_address=request.remote_addr,
                )
                flash(result.message, "success" if result.success else "danger")
                if result.success:
                    return redirect(url_for("admin.settings_maps"))

        ctx = SettingsService.get_maps_context()
        ctx["form"] = form
        return render_template("admin/settings/maps.html", **ctx)

    @admin_bp.route("/settings/localization", methods=["GET", "POST"])
    @can_manage_settings
    def settings_localization():
        form = LocalizationForm()
        settings = SettingsService.get_localization_context()["settings"]
        if request.method == "GET":
            form.default_locale.data = settings.get(KEY_LOCALE_DEFAULT, "")
            form.available_locales.data = settings.get(KEY_LOCALE_AVAILABLE, "")
            form.timezone.data = settings.get(KEY_LOCALE_TIMEZONE, "")
            form.date_format.data = settings.get(KEY_LOCALE_DATE_FORMAT, "")
            form.currency.data = settings.get(KEY_LOCALE_CURRENCY, "")

        if form.validate_on_submit():
            values = {
                KEY_LOCALE_DEFAULT: form.default_locale.data,
                KEY_LOCALE_AVAILABLE: form.available_locales.data,
                KEY_LOCALE_TIMEZONE: form.timezone.data,
                KEY_LOCALE_DATE_FORMAT: form.date_format.data,
                KEY_LOCALE_CURRENCY: form.currency.data,
            }
            result = SettingsService.save_key_value_section(
                section_slug="localization",
                values=values,
                audit_action="settings.localization.update",
                ip_address=request.remote_addr,
            )
            flash(result.message, "success" if result.success else "danger")
            if result.success:
                return redirect(url_for("admin.settings_localization"))

        ctx = SettingsService.get_localization_context()
        ctx["form"] = form
        return render_template("admin/settings/localization.html", **ctx)

    @admin_bp.route("/settings/theme", methods=["GET", "POST"])
    @can_manage_settings
    def settings_theme():
        form = ThemeSettingsForm()
        settings = SettingsService.get_theme_context()["settings"]
        if request.method == "GET":
            form.primary_color.data = settings.get(KEY_THEME_PRIMARY, "")
            form.accent_color.data = settings.get(KEY_THEME_ACCENT, "")
            form.font_family.data = settings.get(KEY_THEME_FONT, "")
            form.enable_dark_mode.data = parse_bool(settings.get(KEY_THEME_ENABLE_DARK))

        if form.validate_on_submit():
            values = {
                KEY_THEME_PRIMARY: form.primary_color.data,
                KEY_THEME_ACCENT: form.accent_color.data,
                KEY_THEME_FONT: form.font_family.data,
                KEY_THEME_ENABLE_DARK: bool_to_str(form.enable_dark_mode.data),
            }
            result = SettingsService.save_key_value_section(
                section_slug="theme",
                values=values,
                audit_action="settings.theme.update",
                ip_address=request.remote_addr,
            )
            flash(result.message, "success" if result.success else "danger")
            if result.success:
                return redirect(url_for("admin.settings_theme"))

        ctx = SettingsService.get_theme_context()
        ctx["form"] = form
        return render_template("admin/settings/theme.html", **ctx)

    @admin_bp.route("/settings/maintenance", methods=["GET", "POST"])
    @can_manage_settings
    def settings_maintenance():
        form = MaintenanceForm()
        settings = SettingsService.get_maintenance_context()["settings"]
        if request.method == "GET":
            form.enabled.data = parse_bool(settings.get(KEY_MAINTENANCE_ENABLED))
            form.message.data = settings.get(KEY_MAINTENANCE_MESSAGE, "")
            form.allowed_ips.data = settings.get(KEY_MAINTENANCE_ALLOWED_IPS, "")

        if form.validate_on_submit():
            values = {
                KEY_MAINTENANCE_ENABLED: bool_to_str(form.enabled.data),
                KEY_MAINTENANCE_MESSAGE: form.message.data,
                KEY_MAINTENANCE_ALLOWED_IPS: form.allowed_ips.data or "",
            }
            result = SettingsService.save_key_value_section(
                section_slug="maintenance",
                values=values,
                audit_action="settings.maintenance.update",
                ip_address=request.remote_addr,
            )
            flash(result.message, "success" if result.success else "danger")
            if result.success:
                return redirect(url_for("admin.settings_maintenance"))

        ctx = SettingsService.get_maintenance_context()
        ctx["form"] = form
        return render_template("admin/settings/maintenance.html", **ctx)

    @admin_bp.route("/settings/analytics", methods=["GET", "POST"])
    @can_manage_settings
    def settings_analytics():
        form = AnalyticsForm()
        settings = SettingsService.get_analytics_context()["settings"]
        if request.method == "GET":
            form.google_analytics_id.data = settings.get(KEY_ANALYTICS_GA_ID, "")
            form.google_tag_manager_id.data = settings.get(KEY_ANALYTICS_GTM_ID, "")
            form.facebook_pixel_id.data = settings.get(KEY_ANALYTICS_FB_PIXEL, "")
            form.enable_dashboard_widgets.data = parse_bool(
                settings.get(KEY_ANALYTICS_ENABLE_DASHBOARD)
            )

        if form.validate_on_submit():
            values = {
                KEY_ANALYTICS_GA_ID: form.google_analytics_id.data or "",
                KEY_ANALYTICS_GTM_ID: form.google_tag_manager_id.data or "",
                KEY_ANALYTICS_FB_PIXEL: form.facebook_pixel_id.data or "",
                KEY_ANALYTICS_ENABLE_DASHBOARD: bool_to_str(form.enable_dashboard_widgets.data),
            }
            result = SettingsService.save_key_value_section(
                section_slug="analytics",
                values=values,
                audit_action="settings.analytics.update",
                ip_address=request.remote_addr,
            )
            flash(result.message, "success" if result.success else "danger")
            if result.success:
                return redirect(url_for("admin.settings_analytics"))

        ctx = SettingsService.get_analytics_context()
        ctx["form"] = form
        return render_template("admin/settings/analytics.html", **ctx)
