"""Apply migration 009 — messages inbox tables."""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sqlalchemy import inspect, text

import app.models  # noqa: F401
from app.extensions import db
from run import app

MIGRATION_FILE = ROOT / "migrations" / "009_messages_inbox.py"
TABLES = ("contact_submission_details", "quote_request_details", "job_applications")


def main() -> None:
    with app.app_context():
        existing = set(inspect(db.engine).get_table_names())
        if all(t in existing for t in TABLES):
            print("Messages inbox tables already exist — skipping.")
            return
        spec = importlib.util.spec_from_file_location("migration_009", MIGRATION_FILE)
        migration = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(migration)
        sql = migration.MYSQL_CREATE if db.engine.dialect.name == "mysql" else migration.SQLITE_CREATE
        for statement in sql.split(";"):
            stmt = statement.strip()
            if stmt:
                db.session.execute(text(stmt))
        db.session.commit()
        print("Migration 009 applied: messages inbox tables created.")


if __name__ == "__main__":
    main()
