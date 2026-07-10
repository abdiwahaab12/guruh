"""
Public-facing routes — thin controllers.

Routes delegate all data fetching to the service layer.
No business logic or hardcoded content here.
"""

from flask import Blueprint, abort, render_template

from app.services import (
    AboutService,
    CatalogService,
    CareersService,
    ContactService,
    HomeService,
    ProjectsService,
    EquipmentService,
)

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Homepage — sections rendered from dynamic data."""
    context = HomeService.get_page_context()
    return render_template("pages/home.html", **context)


@main_bp.route("/about")
def about():
    context = AboutService.get_page_context()
    return render_template("pages/about.html", **context)


@main_bp.route("/services")
def services():
    context = CatalogService.get_services_page()
    return render_template("pages/services.html", **context)


@main_bp.route("/projects")
def projects():
    context = CatalogService.get_projects_page()
    return render_template("pages/projects.html", **context)


@main_bp.route("/projects/<slug>")
def project_detail(slug):
    context = ProjectsService.get_detail_context(slug)
    if not context:
        abort(404)
    return render_template("pages/project_detail.html", **context)


@main_bp.route("/equipment")
def equipment():
    context = CatalogService.get_equipment_page()
    return render_template("pages/equipment.html", **context)


@main_bp.route("/equipment/<slug>")
def equipment_detail(slug):
    context = EquipmentService.get_detail_context(slug)
    if not context:
        abort(404)
    return render_template("pages/equipment_detail.html", **context)


@main_bp.route("/gallery")
def gallery():
    context = CatalogService.get_gallery_page()
    return render_template("pages/gallery.html", **context)


@main_bp.route("/team")
def team():
    context = CatalogService.get_team_page()
    return render_template("pages/team.html", **context)


@main_bp.route("/careers")
def careers():
    context = CareersService.get_page_context()
    return render_template("pages/careers.html", **context)


@main_bp.route("/careers/<slug>")
def career_detail(slug):
    context = CareersService.get_detail_context(slug)
    if not context:
        abort(404)
    return render_template("pages/career_detail.html", **context)


@main_bp.route("/testimonials")
def testimonials():
    context = CatalogService.get_testimonials_page()
    return render_template("pages/testimonials.html", **context)


@main_bp.route("/contact")
def contact():
    context = ContactService.get_contact_page()
    return render_template("pages/contact.html", **context)


@main_bp.route("/request-quote")
def request_quote():
    context = ContactService.get_quote_page()
    return render_template("pages/request_quote.html", **context)


@main_bp.route("/health")
def health_check():
    return "OK", 200
