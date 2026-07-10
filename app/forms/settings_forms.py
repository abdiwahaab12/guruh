"""Website Settings WTForms — CSRF protected dynamic admin forms."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DecimalField,
    EmailField,
    HiddenField,
    IntegerField,
    StringField,
    SubmitField,
    TextAreaField,
    URLField,
)
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, URL


class CompanyInfoForm(FlaskForm):
    name = StringField(
        "Legal Company Name",
        validators=[DataRequired(), Length(max=200)],
    )
    short_name = StringField(
        "Short Name",
        validators=[DataRequired(), Length(max=100)],
    )
    tagline = StringField(
        "Tagline",
        validators=[DataRequired(), Length(max=255)],
    )
    description = TextAreaField(
        "Company Description",
        validators=[DataRequired(), Length(max=5000)],
        render_kw={"rows": 5},
    )
    logo_path = StringField(
        "Logo Path",
        validators=[DataRequired(), Length(max=255)],
        description="Relative path under static/, e.g. img/logo.png",
    )
    founded_country = StringField(
        "Founded Country",
        validators=[DataRequired(), Length(max=100)],
    )
    founded_country_code = StringField(
        "Founded Country Code",
        validators=[DataRequired(), Length(min=2, max=2)],
    )
    operating_country = StringField(
        "Operating Country",
        validators=[DataRequired(), Length(max=100)],
    )
    operating_country_code = StringField(
        "Operating Country Code",
        validators=[DataRequired(), Length(min=2, max=2)],
    )
    headquarters = StringField(
        "Headquarters Summary",
        validators=[Optional(), Length(max=255)],
    )
    submit = SubmitField("Save Company Information")


class ContactInfoForm(FlaskForm):
    phone = StringField(
        "Primary Phone",
        validators=[DataRequired(), Length(max=50)],
    )
    email = EmailField(
        "Primary Email",
        validators=[DataRequired(), Email(), Length(max=120)],
    )
    address = StringField(
        "Primary Address",
        validators=[DataRequired(), Length(max=255)],
    )
    office_hours = StringField(
        "Office Hours",
        validators=[DataRequired(), Length(max=120)],
    )
    submit = SubmitField("Save Contact Information")


class BusinessInfoForm(FlaskForm):
    company_overview = TextAreaField("Company Overview", validators=[DataRequired()], render_kw={"rows": 4})
    company_introduction = TextAreaField("Company Introduction", validators=[DataRequired()], render_kw={"rows": 4})
    about_the_company = TextAreaField("About the Company", validators=[DataRequired()], render_kw={"rows": 4})
    company_history = TextAreaField("Company History", validators=[DataRequired()], render_kw={"rows": 4})
    vision = TextAreaField("Vision", validators=[DataRequired()], render_kw={"rows": 3})
    mission = TextAreaField("Mission", validators=[DataRequired()], render_kw={"rows": 3})
    directors_message = TextAreaField("Directors Message", validators=[DataRequired()], render_kw={"rows": 4})
    submit = SubmitField("Save Business Information")


class SeoSettingsForm(FlaskForm):
    site_title = StringField("Default Site Title", validators=[DataRequired(), Length(max=200)])
    meta_description = TextAreaField("Meta Description", validators=[DataRequired(), Length(max=500)], render_kw={"rows": 3})
    meta_keywords = StringField("Meta Keywords", validators=[Optional(), Length(max=500)])
    og_image = StringField("Open Graph Image", validators=[Optional(), Length(max=255)])
    robots = StringField("Robots Directive", validators=[DataRequired(), Length(max=100)])
    canonical_base_url = URLField("Canonical Base URL", validators=[Optional(), URL(require_tld=False)])
    submit = SubmitField("Save SEO Settings")


class SmtpSettingsForm(FlaskForm):
    host = StringField("SMTP Host", validators=[Optional(), Length(max=255)])
    port = IntegerField("SMTP Port", validators=[Optional(), NumberRange(min=1, max=65535)], default=587)
    username = StringField("SMTP Username", validators=[Optional(), Length(max=255)])
    password = StringField("SMTP Password", validators=[Optional(), Length(max=255)])
    use_tls = BooleanField("Use TLS", default=True)
    from_email = EmailField("From Email", validators=[Optional(), Email(), Length(max=120)])
    from_name = StringField("From Name", validators=[Optional(), Length(max=120)])
    submit = SubmitField("Save Email Settings")


class MapsSettingsForm(FlaskForm):
    api_key = StringField("Google Maps API Key", validators=[Optional(), Length(max=255)])
    default_latitude = DecimalField(
        "Default Latitude",
        validators=[Optional(), NumberRange(min=-90, max=90)],
        places=6,
    )
    default_longitude = DecimalField(
        "Default Longitude",
        validators=[Optional(), NumberRange(min=-180, max=180)],
        places=6,
    )
    default_zoom = IntegerField(
        "Default Zoom",
        validators=[Optional(), NumberRange(min=1, max=21)],
        default=16,
    )
    embed_url = StringField("Embed URL", validators=[Optional(), Length(max=500)])
    provider = StringField("Map Provider", validators=[Optional(), Length(max=50)])
    submit = SubmitField("Save Map Settings")


class LocalizationForm(FlaskForm):
    default_locale = StringField("Default Locale", validators=[DataRequired(), Length(max=10)])
    available_locales = StringField(
        "Available Locales",
        validators=[DataRequired(), Length(max=100)],
        description="Comma-separated locale codes, e.g. en,so",
    )
    timezone = StringField("Timezone", validators=[DataRequired(), Length(max=80)])
    date_format = StringField("Date Format", validators=[DataRequired(), Length(max=40)])
    currency = StringField("Currency Code", validators=[DataRequired(), Length(max=10)])
    submit = SubmitField("Save Localization Settings")


class ThemeSettingsForm(FlaskForm):
    primary_color = StringField("Primary Color", validators=[DataRequired(), Length(max=20)])
    accent_color = StringField("Accent Color", validators=[DataRequired(), Length(max=20)])
    font_family = StringField("Font Family", validators=[DataRequired(), Length(max=120)])
    enable_dark_mode = BooleanField("Enable Public Dark Mode Toggle", default=False)
    submit = SubmitField("Save Theme Settings")


class MaintenanceForm(FlaskForm):
    enabled = BooleanField("Enable Maintenance Mode", default=False)
    message = TextAreaField("Maintenance Message", validators=[DataRequired()], render_kw={"rows": 4})
    allowed_ips = TextAreaField(
        "Allowed IP Addresses",
        validators=[Optional()],
        description="One IP per line or comma-separated",
        render_kw={"rows": 3},
    )
    submit = SubmitField("Save Maintenance Settings")


class AnalyticsForm(FlaskForm):
    google_analytics_id = StringField("Google Analytics ID", validators=[Optional(), Length(max=50)])
    google_tag_manager_id = StringField("Google Tag Manager ID", validators=[Optional(), Length(max=50)])
    facebook_pixel_id = StringField("Facebook Pixel ID", validators=[Optional(), Length(max=50)])
    enable_dashboard_widgets = BooleanField("Enable Live Dashboard Analytics", default=False)
    submit = SubmitField("Save Analytics Settings")


class OfficeLocationForm(FlaskForm):
    office_id = HiddenField(validators=[Optional()])
    slug = StringField("Slug", validators=[Optional(), Length(max=80)])
    name = StringField("Office Name", validators=[DataRequired(), Length(max=200)])
    office_label = StringField("Office Label", validators=[DataRequired(), Length(max=100)])
    address = StringField("Street Address", validators=[DataRequired(), Length(max=255)])
    postal_address = StringField("Postal Address", validators=[Optional(), Length(max=255)])
    address_area = StringField("Area", validators=[Optional(), Length(max=120)])
    address_district = StringField("District", validators=[Optional(), Length(max=120)])
    address_locality = StringField("City / Locality", validators=[Optional(), Length(max=120)])
    country = StringField("Country", validators=[DataRequired(), Length(max=100)])
    country_code = StringField("Country Code", validators=[DataRequired(), Length(min=2, max=2)])
    phone_primary = StringField("Primary Phone", validators=[DataRequired(), Length(max=50)])
    phone_secondary = StringField("Secondary Phone", validators=[Optional(), Length(max=50)])
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    office_hours = StringField("Office Hours", validators=[Optional(), Length(max=120)])
    map_latitude = DecimalField("Latitude", validators=[Optional(), NumberRange(min=-90, max=90)], places=6)
    map_longitude = DecimalField("Longitude", validators=[Optional(), NumberRange(min=-180, max=180)], places=6)
    map_zoom = IntegerField("Map Zoom", validators=[Optional(), NumberRange(min=1, max=21)], default=16)
    sort_order = IntegerField("Sort Order", validators=[Optional()], default=0)
    is_headquarters = BooleanField("Headquarters", default=False)
    show_on_contact_page = BooleanField("Show on Contact Page", default=True)
    is_active = BooleanField("Active", default=True)
    submit = SubmitField("Save Office")


class SocialLinkForm(FlaskForm):
    link_id = HiddenField(validators=[Optional()])
    platform = StringField("Platform", validators=[DataRequired(), Length(max=50)])
    label = StringField("Label", validators=[DataRequired(), Length(max=100)])
    icon = StringField("Bootstrap Icon Class", validators=[DataRequired(), Length(max=50)])
    url = URLField("URL", validators=[DataRequired(), URL(require_tld=False)])
    sort_order = IntegerField("Sort Order", validators=[Optional()], default=0)
    is_active = BooleanField("Active", default=True)
    submit = SubmitField("Save Social Link")


class DeleteConfirmForm(FlaskForm):
    submit = SubmitField("Confirm Delete")
