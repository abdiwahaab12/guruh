"""Apply migration 002 — media_assets table."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sqlalchemy import inspect, text

import app.models  # noqa: F401
from app.extensions import db
from run import app

MIGRATION_FILE = ROOT / "migrations" / "002_media_assets.py"


def table_exists() -> bool:
    inspector = inspect(db.engine)
    return "media_assets" in inspector.get_table_names()


def main() -> None:
    with app.app_context():
        if table_exists():
            print("media_assets table already exists — skipping.")
            return

        dialect = db.engine.dialect.name
        import importlib.util

        spec = importlib.util.spec_from_file_location("migration_002", MIGRATION_FILE)
        migration = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(migration)
        sql = migration.MYSQL_CREATE if dialect == "mysql" else migration.SQLITE_CREATE
        for statement in sql.split(";"):
            stmt = statement.strip()
            if stmt:
                db.session.execute(text(stmt))
        db.session.commit()
        print("Migration 002 applied: media_assets table created.")


if __name__ == "__main__":
    main()
