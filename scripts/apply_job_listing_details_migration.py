"""Apply migration 008 — job_listing_details table."""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sqlalchemy import inspect, text

import app.models  # noqa: F401
from app.extensions import db
from run import app

MIGRATION_FILE = ROOT / "migrations" / "008_job_listing_details.py"


def main() -> None:
    with app.app_context():
        if "job_listing_details" in inspect(db.engine).get_table_names():
            print("job_listing_details table already exists — skipping.")
            return
        spec = importlib.util.spec_from_file_location("migration_008", MIGRATION_FILE)
        migration = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(migration)
        sql = migration.MYSQL_CREATE if db.engine.dialect.name == "mysql" else migration.SQLITE_CREATE
        for statement in sql.split(";"):
            stmt = statement.strip()
            if stmt:
                db.session.execute(text(stmt))
        db.session.commit()
        print("Migration 008 applied: job_listing_details table created.")


if __name__ == "__main__":
    main()
