"""
Site-wide models: navigation, company info, social links, footer, settings.

All manageable from the Admin Dashboard.
"""

from app.extensions import db
from app.models.base import BaseModel


class NavItem(BaseModel):
    """Navigation menu item (header and/or footer)."""

    __tablename__ = "nav_items"

    label = db.Column(db.String(100), nullable=False)
    endpoint = db.Column(db.String(100), nullable=False)
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    show_in_header = db.Column(db.Boolean, default=True, nullable=False)
    show_in_footer = db.Column(db.Boolean, default=True, nullable=False)


class SocialLink(BaseModel):
    """Social media profile link."""

    __tablename__ = "social_links"

    platform = db.Column(db.String(50), nullable=False)
    label = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class CompanyInfo(BaseModel):
    """
    Singleton-style company profile (one active row expected).
    Admin can update all company-wide information here.
    """

    __tablename__ = "company_info"

    name = db.Column(db.String(200), nullable=False)
    short_name = db.Column(db.String(100), nullable=False)
    tagline = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    office_hours = db.Column(db.String(120), nullable=False)
    logo_path = db.Column(db.String(255), default="img/logo.png")
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # Corporate geography — founded vs current operations
    founded_country = db.Column(db.String(100), default="Kenya", nullable=False)
    founded_country_code = db.Column(db.String(2), default="KE", nullable=False)
    operating_country = db.Column(db.String(100), default="Somalia", nullable=False)
    operating_country_code = db.Column(db.String(2), default="SO", nullable=False)
    headquarters = db.Column(db.String(255), default="", nullable=False)


class OfficeLocation(BaseModel):
    """
    Company office — headquarters or branch.

    Supports multiple locations; contact page shows offices where show_on_contact_page=True.
    """

    __tablename__ = "office_locations"

    slug = db.Column(db.String(80), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    office_label = db.Column(db.String(100), default="Office", nullable=False)
    address = db.Column(db.String(255), nullable=False)
    postal_address = db.Column(db.String(255), default="")
    address_area = db.Column(db.String(120), default="")
    address_district = db.Column(db.String(120), default="")
    address_locality = db.Column(db.String(120), default="")
    country = db.Column(db.String(100), nullable=False)
    country_code = db.Column(db.String(2), nullable=False)
    phone_primary = db.Column(db.String(50), nullable=False)
    phone_secondary = db.Column(db.String(50), default="")
    email = db.Column(db.String(120), nullable=False)
    office_hours = db.Column(db.String(120), default="")
    is_headquarters = db.Column(db.Boolean, default=False, nullable=False)
    show_on_contact_page = db.Column(db.Boolean, default=True, nullable=False)
    map_latitude = db.Column(db.Float, nullable=True)
    map_longitude = db.Column(db.Float, nullable=True)
    map_zoom = db.Column(db.Integer, default=16)
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class FooterContent(BaseModel):
    """Footer text content managed from admin."""

    __tablename__ = "footer_content"

    about_text = db.Column(db.Text, nullable=False)
    copyright_text = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class SiteSetting(BaseModel):
    """Key-value store for website settings (SEO, feature flags, etc.)."""

    __tablename__ = "site_settings"

    key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    value = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(255))
