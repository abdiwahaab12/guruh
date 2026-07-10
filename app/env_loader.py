"""
Environment loading and database URL resolution.

Production (Passenger/wsgi) must use MySQL only — never SQLite.
Local development settings belong in .env.development.example, not .env.example.
"""

from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_project_dotenv() -> Path:
    """Load .env from project root; overrides stale shell variables."""
    load_dotenv(PROJECT_ROOT / ".env", override=True)
    return PROJECT_ROOT


def resolve_database_url() -> str:
    """
    Build SQLAlchemy URI from DATABASE_URL or DB_* component variables.

    Namecheap production (cPanel MySQL):
        DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
    """
    explicit = os.environ.get("DATABASE_URL", "").strip()
    if explicit:
        return explicit

    host = os.environ.get("DB_HOST", "").strip()
    port = os.environ.get("DB_PORT", "3306").strip() or "3306"
    name = os.environ.get("DB_NAME", "").strip()
    user = os.environ.get("DB_USER", "").strip()
    password = os.environ.get("DB_PASSWORD", "")

    if host and name and user:
        return (
            f"mysql+pymysql://{quote_plus(user)}:{quote_plus(password)}"
            f"@{host}:{port}/{name}?charset=utf8mb4"
        )
    return ""


def assert_production_database_url(url: str) -> str:
    """Reject SQLite and non-MySQL URIs in production."""
    if not url:
        raise ValueError(
            "Production requires DATABASE_URL or DB_HOST/DB_USER/DB_NAME/DB_PASSWORD."
        )
    lowered = url.lower()
    if lowered.startswith("sqlite"):
        raise ValueError("SQLite is not permitted in production. Configure MySQL.")
    if not lowered.startswith("mysql"):
        raise ValueError("Production requires a MySQL connection (mysql+pymysql://...).")
    return url


def assert_production_enabled() -> bool:
    enabled = os.environ.get("DATABASE_ENABLED", "true").lower() == "true"
    if not enabled:
        raise ValueError("DATABASE_ENABLED must be true in production.")
    return True
