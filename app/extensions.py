"""Flask extensions — initialized in application factory."""

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

login_manager.login_view = "admin.login"
login_manager.login_message = "Please sign in to access the admin area."
login_manager.login_message_category = "warning"
login_manager.session_protection = "strong"
