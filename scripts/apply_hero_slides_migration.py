"""Apply hero_slides CMS columns — secondary CTA + overlay opacity — and clear legacy SVG placeholder paths."""

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


def _add_column_if_missing(table: str, column: str, ddl: str) -> bool:
    if column in _column_names(table):
        return False
    db.session.execute(text(f"ALTER TABLE {table} ADD COLUMN {ddl}"))
    return True


def _clear_svg_placeholder_paths() -> None:
    """Replace legacy SVG placeholder paths with empty strings.

    Public templates render a brand gradient / smart fallback when the stored
    path is empty, so clearing these removes hard-coded SVG artwork while
    leaving any real Media Library uploads untouched.
    """
    tables = inspect(db.engine).get_table_names()
    statements = []
    if "hero_slides" in tables:
        statements.append("UPDATE hero_slides SET image = '' WHERE image LIKE 'img/fallbacks/%'")
    if "pages" in tables:
        statements.append("UPDATE pages SET banner_image = '' WHERE banner_image LIKE 'img/fallbacks/%'")
    if "content_blocks" in tables:
        cols = _column_names("content_blocks")
        if "hero_image" in cols:
            statements.append("UPDATE content_blocks SET hero_image = '' WHERE hero_image LIKE 'img/fallbacks/%'")
        if "og_image" in cols:
            statements.append("UPDATE content_blocks SET og_image = '' WHERE og_image LIKE 'img/fallbacks/%'")

    cleared = 0
    for stmt in statements:
        cleared += db.session.execute(text(stmt)).rowcount or 0
    if cleared:
        db.session.commit()
        print(f"Cleared {cleared} legacy SVG placeholder path(s) from CMS tables.")
    else:
        print("No legacy SVG placeholder paths found.")


def main() -> None:
    with app.app_context():
        if "hero_slides" not in inspect(db.engine).get_table_names():
            print("hero_slides table missing — run init_db / setup_mysql first.")
            raise SystemExit(1)

        is_mysql = db.engine.dialect.name == "mysql"
        overlay_ddl = (
            "overlay_opacity FLOAT NOT NULL DEFAULT 0.65"
            if is_mysql
            else "overlay_opacity REAL NOT NULL DEFAULT 0.65"
        )

        changes = 0
        if _add_column_if_missing("hero_slides", "secondary_cta_text", "secondary_cta_text VARCHAR(100)"):
            changes += 1
            print("Added hero_slides.secondary_cta_text")
        if _add_column_if_missing("hero_slides", "secondary_cta_url", "secondary_cta_url VARCHAR(255)"):
            changes += 1
            print("Added hero_slides.secondary_cta_url")
        if _add_column_if_missing("hero_slides", "overlay_opacity", overlay_ddl):
            changes += 1
            print("Added hero_slides.overlay_opacity")
        if _add_column_if_missing("hero_slides", "text_alignment", "text_alignment VARCHAR(20) NOT NULL DEFAULT 'left'"):
            changes += 1
            print("Added hero_slides.text_alignment")

        if changes:
            db.session.commit()
            print(f"Hero slides migration applied ({changes} column(s)).")
        else:
            print("Hero slides columns already present — skipping.")

        _clear_svg_placeholder_paths()


if __name__ == "__main__":
    main()
