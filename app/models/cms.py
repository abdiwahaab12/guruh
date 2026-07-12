"""
CMS content models: pages, homepage sections, statistics, partners.
"""

from app.extensions import db
from app.models.base import BaseModel


class Page(BaseModel):
    """Dynamic page metadata for SEO and admin management."""

    __tablename__ = "pages"

    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    meta_title = db.Column(db.String(200), nullable=False)
    meta_description = db.Column(db.Text, nullable=False)
    banner_subtitle = db.Column(db.String(255))
    banner_image = db.Column(db.String(255))
    is_published = db.Column(db.Boolean, default=True, nullable=False)


class HeroSlide(BaseModel):
    """Homepage hero slider slide."""

    __tablename__ = "hero_slides"

    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(255))
    description = db.Column(db.Text)
    image = db.Column(db.String(255), default="", nullable=False)
    cta_text = db.Column(db.String(100))
    cta_url = db.Column(db.String(255))
    secondary_cta_text = db.Column(db.String(100))
    secondary_cta_url = db.Column(db.String(255))
    overlay_opacity = db.Column(db.Float, default=0.65, nullable=False)
    text_alignment = db.Column(db.String(20), default="left", nullable=False)
    background_type = db.Column(db.String(10), default="image", nullable=False)
    video_path = db.Column(db.String(255), default="", nullable=False)
    video_thumbnail = db.Column(db.String(255), default="", nullable=False)
    autoplay = db.Column(db.Boolean, default=True, nullable=False)
    loop = db.Column("loop", db.Boolean, default=True, nullable=False, quote=True)
    muted = db.Column(db.Boolean, default=True, nullable=False)
    plays_inline = db.Column(db.Boolean, default=True, nullable=False)
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class AboutSection(BaseModel):
    """About section content (homepage and/or about page)."""

    __tablename__ = "about_sections"

    page_slug = db.Column(db.String(100), default="home", index=True)
    heading = db.Column(db.String(200), nullable=False)
    subheading = db.Column(db.String(255))
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255))
    highlights = db.Column(db.JSON)
    cta_text = db.Column(db.String(100))
    cta_url = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class Statistic(BaseModel):
    """Company statistics counter (homepage)."""

    __tablename__ = "statistics"

    label = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(50), nullable=False)
    suffix = db.Column(db.String(20))
    icon = db.Column(db.String(50))
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class Partner(BaseModel):
    """Partner / client logo for homepage."""

    __tablename__ = "partners"

    name = db.Column(db.String(150), nullable=False)
    logo = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(500))
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class CTASection(BaseModel):
    """Call-to-action block (homepage or global)."""

    __tablename__ = "cta_sections"

    page_slug = db.Column(db.String(100), default="home", index=True)
    heading = db.Column(db.String(200), nullable=False)
    subheading = db.Column(db.String(255))
    button_text = db.Column(db.String(100), nullable=False)
    button_url = db.Column(db.String(255), nullable=False)
    secondary_button_text = db.Column(db.String(100))
    secondary_button_url = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class WhyChooseUsSection(BaseModel):
    """Why Choose Us section header content."""

    __tablename__ = "why_choose_us_sections"

    page_slug = db.Column(db.String(100), default="home", index=True)
    heading = db.Column(db.String(200), nullable=False)
    subheading = db.Column(db.String(255))
    intro = db.Column(db.Text)
    image = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class WhyChooseUsItem(BaseModel):
    """Individual feature in Why Choose Us section."""

    __tablename__ = "why_choose_us_items"

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50))
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class WorkingProcessSection(BaseModel):
    """Working process section header content."""

    __tablename__ = "working_process_sections"

    page_slug = db.Column(db.String(100), default="home", index=True)
    heading = db.Column(db.String(200), nullable=False)
    subheading = db.Column(db.String(255))
    intro = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class ProcessStep(BaseModel):
    """Single step in the working process timeline."""

    __tablename__ = "process_steps"

    page_slug = db.Column(db.String(100), default="home", index=True)
    step_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50))
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class TrustBadge(BaseModel):
    """Hero section trust badge — admin-manageable."""

    __tablename__ = "trust_badges"

    page_slug = db.Column(db.String(100), default="home", index=True)
    label = db.Column(db.String(150), nullable=False)
    icon = db.Column(db.String(50))
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class SectionHeading(BaseModel):
    """Configurable headings for homepage sections (admin-managed)."""

    __tablename__ = "section_headings"

    page_slug = db.Column(db.String(100), default="home", index=True)
    section_key = db.Column(db.String(100), nullable=False, index=True)
    heading = db.Column(db.String(200), nullable=False)
    subheading = db.Column(db.String(255))
    intro = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
