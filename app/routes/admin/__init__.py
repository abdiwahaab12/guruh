"""
Admin routes — authentication, middleware, and dashboard foundation.

CRUD modules will be added in future steps without changing this shell.
"""

from flask import Blueprint

from app.routes.admin.auth import register_auth_routes
from app.routes.admin.dashboard import register_dashboard_routes
from app.routes.admin.middleware import register_admin_middleware
from app.routes.admin.settings import register_settings_routes
from app.routes.admin.media import register_media_routes
from app.routes.admin.projects import register_projects_routes
from app.routes.admin.services import register_services_routes
from app.routes.admin.equipment import register_equipment_routes
from app.routes.admin.team import register_team_routes
from app.routes.admin.gallery import register_gallery_routes
from app.routes.admin.careers import register_careers_routes
from app.routes.admin.website import register_website_routes
from app.routes.admin.messages import register_messages_routes
from app.routes.admin.users import register_users_routes
from app.routes.admin.reports import register_reports_routes
from app.routes.admin.system import register_system_routes
from app.services.admin_service import AdminDashboardService

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

register_admin_middleware(admin_bp)
register_auth_routes(admin_bp)
register_settings_routes(admin_bp)
register_media_routes(admin_bp)
register_projects_routes(admin_bp)
register_services_routes(admin_bp)
register_equipment_routes(admin_bp)
register_team_routes(admin_bp)
register_gallery_routes(admin_bp)
register_careers_routes(admin_bp)
register_website_routes(admin_bp)
register_messages_routes(admin_bp)
register_users_routes(admin_bp)
register_reports_routes(admin_bp)
register_system_routes(admin_bp)
register_dashboard_routes(admin_bp)


@admin_bp.context_processor
def inject_admin_context():
    """Shared admin shell context for layout templates."""
    return {
        "admin_nav": AdminDashboardService.get_sidebar_nav(),
    }
