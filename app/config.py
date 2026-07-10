"""
Application configuration profiles.

Production (Namecheap cPanel + Passenger + MySQL):
  FLASK_ENV=production, DATABASE_ENABLED=true, MySQL only.

Local development: copy .env.development.example to .env — never deploy that file.
"""

from __future__ import annotations

import os
from datetime import timedelta

from app.env_loader import (
    assert_production_database_url,
    assert_production_enabled,
    resolve_database_url,
)


class Config:
    """Base configuration shared across all environments."""

    # Resolved at access time so DB_* components can build DATABASE_URL
    @staticmethod
    def _database_uri() -> str:
        return resolve_database_url()

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-change-me-in-production")

    DATABASE_ENABLED = os.environ.get("DATABASE_ENABLED", "false").lower() == "true"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # Session & cookie security
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    REMEMBER_COOKIE_DURATION = timedelta(days=30)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = "Lax"

    # CSRF (Flask-WTF)
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None

    # Authentication
    SESSION_IDLE_TIMEOUT_MINUTES = int(os.environ.get("SESSION_IDLE_TIMEOUT_MINUTES", "30"))
    MAX_LOGIN_ATTEMPTS = int(os.environ.get("MAX_LOGIN_ATTEMPTS", "5"))
    LOCKOUT_DURATION_MINUTES = int(os.environ.get("LOCKOUT_DURATION_MINUTES", "15"))
    PASSWORD_RESET_EXPIRY_HOURS = int(os.environ.get("PASSWORD_RESET_EXPIRY_HOURS", "1"))
    PASSWORD_MIN_LENGTH = int(os.environ.get("PASSWORD_MIN_LENGTH", "8"))

    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@guruh.com")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "GuruhAdmin2026!")
    ADMIN_FIRST_NAME = os.environ.get("ADMIN_FIRST_NAME", "Super")
    ADMIN_LAST_NAME = os.environ.get("ADMIN_LAST_NAME", "Admin")

    MEDIA_UPLOAD_ROOT = os.environ.get("MEDIA_UPLOAD_ROOT", "uploads")
    MEDIA_MAX_FILE_SIZE = int(os.environ.get("MEDIA_MAX_FILE_SIZE", str(20 * 1024 * 1024)))
    MEDIA_MAX_BATCH = int(os.environ.get("MEDIA_MAX_BATCH", "20"))


class DevelopmentConfig(Config):
    """Local development only — not used on Namecheap production."""

    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        url = resolve_database_url()
        if url:
            return url
        return "mysql+pymysql://root:@127.0.0.1:3306/guruh_construction?charset=utf8mb4"


class ProductionConfig(Config):
    """Namecheap / cPanel production — MySQL required, debug off."""

    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True

    @property
    def DATABASE_ENABLED(self) -> bool:
        return assert_production_enabled()

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return assert_production_database_url(resolve_database_url())

    @property
    def SECRET_KEY(self) -> str:
        key = os.environ.get("SECRET_KEY", "").strip()
        if not key or key == "dev-change-me-in-production" or key == "your-secret-key-here":
            raise ValueError("SECRET_KEY environment variable is required in production.")
        return key


class TestingConfig(Config):
    """Automated tests only — in-memory SQLite, never used in deployment."""

    DEBUG = False
    TESTING = True
    DATABASE_ENABLED = False
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL",
        "sqlite:///:memory:",
    )


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
