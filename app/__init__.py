"""
GURUH Construction Company Limited — Flask Application Factory.
"""

from pathlib import Path

from flask import Flask, redirect, render_template, request, session, url_for
from flask_login import current_user, logout_user

from app.config import config_by_name
from app.env_loader import load_project_dotenv
from app.extensions import csrf, db, login_manager

BASE_DIR = Path(__file__).resolve().parent.parent

# Admin routes exempt from idle session timeout checks
_AUTH_EXEMPT_ENDPOINTS = frozenset(
    {
        "admin.login",
        "admin.forgot_password",
        "admin.reset_password",
        "admin.unauthorized_page",
        "admin.forbidden_page",
        "static",
    }
)


def create_app(config_name: str = "development") -> Flask:
    """Create and configure the Flask application."""
    load_project_dotenv()

    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
    )

    cfg = config_by_name[config_name]
    if config_name in ("production", "development"):
        app.config.from_object(cfg())
    else:
        app.config.from_object(cfg)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str):
        from app.services.auth_service import AuthService

        try:
            return AuthService.get_user_by_id(int(user_id))
        except (TypeError, ValueError):
            return None

    @login_manager.unauthorized_handler
    def handle_unauthorized():
        if request.path.startswith("/admin"):
            return redirect(url_for("admin.login", next=request.url))
        return render_template("admin/401.html"), 401

    @app.errorhandler(403)
    def handle_forbidden(error):
        if request.path.startswith("/admin"):
            return render_template("admin/403.html"), 403
        return error

    @app.before_request
    def enforce_admin_session_timeout():
        """Idle session timeout for authenticated admin users."""
        if not request.path.startswith("/admin"):
            return None
        if request.endpoint in _AUTH_EXEMPT_ENDPOINTS:
            return None
        if not current_user.is_authenticated:
            return None

        from app.services.auth_service import AuthService

        if not AuthService.touch_session(session):
            AuthService.logout_user(current_user)
            logout_user()
            session.clear()
            from flask import flash

            flash("Your session has expired due to inactivity. Please sign in again.", "warning")
            return redirect(url_for("admin.login"))

        return None

    # Initialize content provider (placeholder or MySQL)
    from app.providers import init_content_provider

    init_content_provider(app)

    # Register blueprints
    from app.routes.main import main_bp

    app.register_blueprint(main_bp)

    from app.routes.admin import admin_bp

    app.register_blueprint(admin_bp)

    # Inject dynamic site data into all templates
    @app.context_processor
    def inject_site_context():
        from app.services import SiteService

        return SiteService.get_global_context()

    from app.utils.template_filters import register_template_filters

    register_template_filters(app)

    # Trust reverse-proxy headers on shared hosting (Apache/Passenger + SSL)
    if config_name == "production":
        from werkzeug.middleware.proxy_fix import ProxyFix

        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    return app
