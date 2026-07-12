"""Apply hero_slides video background columns."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env", override=True)

import app.models  # noqa: F401
from app.extensions import db
from run import app
from sqlalchemy import inspect, text


def _column_names(table: str) -> set[str]:
    insp = inspect(db.engine)
    if table not in insp.get_table_names():
        return set()
    return {col["name"] for col in insp.get_columns(table)}


def _quote_identifier(name: str, *, is_mysql: bool) -> str:
    return f"`{name}`" if is_mysql else name


def _add_column_if_missing(table: str, column: str, ddl: str, *, is_mysql: bool) -> bool:
    if column in _column_names(table):
        return False
    table_ref = _quote_identifier(table, is_mysql=is_mysql)
    db.session.execute(text(f"ALTER TABLE {table_ref} ADD COLUMN {ddl}"))
    return True


def main() -> None:
    with app.app_context():
        if "hero_slides" not in inspect(db.engine).get_table_names():
            print("hero_slides table missing — run init_db / setup_mysql first.")
            raise SystemExit(1)

        is_mysql = db.engine.dialect.name == "mysql"
        bool_type = "BOOLEAN" if is_mysql else "INTEGER"

        bool_default = "1" if not is_mysql else "TRUE"
        columns = [
            ("background_type", f"{_quote_identifier('background_type', is_mysql=is_mysql)} VARCHAR(10) NOT NULL DEFAULT 'image'"),
            ("video_path", f"{_quote_identifier('video_path', is_mysql=is_mysql)} VARCHAR(255) NOT NULL DEFAULT ''"),
            ("video_thumbnail", f"{_quote_identifier('video_thumbnail', is_mysql=is_mysql)} VARCHAR(255) NOT NULL DEFAULT ''"),
            ("autoplay", f"{_quote_identifier('autoplay', is_mysql=is_mysql)} {bool_type} NOT NULL DEFAULT {bool_default}"),
            ("loop", f"{_quote_identifier('loop', is_mysql=is_mysql)} {bool_type} NOT NULL DEFAULT {bool_default}"),
            ("muted", f"{_quote_identifier('muted', is_mysql=is_mysql)} {bool_type} NOT NULL DEFAULT {bool_default}"),
            ("plays_inline", f"{_quote_identifier('plays_inline', is_mysql=is_mysql)} {bool_type} NOT NULL DEFAULT {bool_default}"),
        ]

        changes = 0
        for name, ddl in columns:
            if _add_column_if_missing("hero_slides", name, ddl, is_mysql=is_mysql):
                changes += 1
                print(f"Added hero_slides.{name}")

        if changes:
            db.session.commit()
            print(f"Hero video migration applied ({changes} column(s)).")
        else:
            print("Hero video columns already present — skipping.")


if __name__ == "__main__":
    main()
