"""
Database initialization script.

Creates all tables defined in app/models/. Run on the server after MySQL is configured:
    python init_db.py

Requires production .env (copy from .env.production).
"""

import os

import app.models  # noqa: F401 — register models before app import

from app.env_loader import load_project_dotenv
from app import create_app
from app.extensions import db

load_project_dotenv()

config_name = os.environ.get("FLASK_ENV", "production")
app = create_app(config_name)


def init_database():
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")


if __name__ == "__main__":
    init_database()
