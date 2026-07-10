"""Apply migration 005 — equipment and equipment_details tables."""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sqlalchemy import inspect, text

import app.models  # noqa: F401
from app.extensions import db
from run import app

MIGRATION_FILE = ROOT / "migrations" / "005_equipment.py"


def main() -> None:
    with app.app_context():
        tables = inspect(db.engine).get_table_names()
        if "equipment" in tables and "equipment_details" in tables:
            print("equipment tables already exist — skipping.")
            return
        spec = importlib.util.spec_from_file_location("migration_005", MIGRATION_FILE)
        migration = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(migration)
        sql = migration.MYSQL_CREATE if db.engine.dialect.name == "mysql" else migration.SQLITE_CREATE
        for statement in sql.split(";"):
            stmt = statement.strip()
            if stmt:
                db.session.execute(text(stmt))
        db.session.commit()
        print("Migration 005 applied: equipment and equipment_details tables created.")


if __name__ == "__main__":
    main()
