"""
Catalog models: services, projects, gallery, team, testimonials, careers.
"""

from app.extensions import db
from app.models.base import BaseModel


class Service(BaseModel):
    __tablename__ = "services"

    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False, index=True)
    short_description = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50))
    image = db.Column(db.String(255))
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    is_featured = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class Project(BaseModel):
    __tablename__ = "projects"
    __table_args__ = (db.Index("ix_projects_country_is_active", "country", "is_active"),)

    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(150))
    country = db.Column(db.String(100), default="Kenya")
    county = db.Column(db.String(100))
    status = db.Column(db.String(50))
    client = db.Column(db.String(150))
    category = db.Column(db.String(100))
    cover_image = db.Column(db.String(255))
    completion_date = db.Column(db.String(50))
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    is_featured = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class GalleryImage(BaseModel):
    __tablename__ = "gallery_images"

    title = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100))
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=True)
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class TeamMember(BaseModel):
    __tablename__ = "team_members"

    name = db.Column(db.String(150), nullable=False)
    position = db.Column(db.String(150), nullable=False)
    bio = db.Column(db.Text)
    photo = db.Column(db.String(255))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class Testimonial(BaseModel):
    __tablename__ = "testimonials"

    client_name = db.Column(db.String(150), nullable=False)
    client_title = db.Column(db.String(150))
    company = db.Column(db.String(150))
    content = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(255))
    rating = db.Column(db.Integer, default=5)
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    is_featured = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class JobListing(BaseModel):
    __tablename__ = "job_listings"

    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False, index=True)
    department = db.Column(db.String(100))
    location = db.Column(db.String(150))
    employment_type = db.Column(db.String(50))
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)
    deadline = db.Column(db.String(50))
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class ContactPageContent(BaseModel):
    """Contact page content managed from admin."""

    __tablename__ = "contact_page_content"

    heading = db.Column(db.String(200), nullable=False)
    subheading = db.Column(db.String(255))
    intro = db.Column(db.Text)
    map_embed = db.Column(db.Text)
    form_heading = db.Column(db.String(200), default="Send Us a Message")
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class QuotePageContent(BaseModel):
    """Request quote page content managed from admin."""

    __tablename__ = "quote_page_content"

    heading = db.Column(db.String(200), nullable=False)
    subheading = db.Column(db.String(255))
    intro = db.Column(db.Text)
    form_heading = db.Column(db.String(200), default="Request a Project Quote")
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class ContactSubmission(BaseModel):
    """Stored contact form submissions."""

    __tablename__ = "contact_submissions"
    __table_args__ = (db.Index("ix_contact_submissions_is_read_created_at", "is_read", "created_at"),)

    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(50))
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)


class QuoteRequest(BaseModel):
    """Stored quote request form submissions."""

    __tablename__ = "quote_requests"
    __table_args__ = (db.Index("ix_quote_requests_is_read_created_at", "is_read", "created_at"),)

    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    project_type = db.Column(db.String(100))
    budget = db.Column(db.String(100))
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
