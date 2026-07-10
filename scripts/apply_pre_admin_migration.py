"""
Pre-Admin Dashboard schema migration (Migrations 1–3).

Applies column and index changes to existing MySQL/SQLite databases.
Fresh installs can use init_db.py instead.

Usage:
    python scripts/apply_pre_admin_migration.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import app.models  # noqa: F401 — register models
from run import app
from app.extensions import db
from sqlalchemy import inspect, text


def _table_exists(insp, table: str) -> bool:
    return table in insp.get_table_names()


def _column_names(insp, table: str) -> set[str]:
    if not _table_exists(insp, table):
        return set()
    return {col["name"] for col in insp.get_columns(table)}


def _index_names(insp, table: str) -> set[str]:
    if not _table_exists(insp, table):
        return set()
    return {idx["name"] for idx in insp.get_indexes(table)}


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "job"


def _add_column_if_missing(table: str, column: str, ddl: str) -> bool:
    insp = inspect(db.engine)
    if column in _column_names(insp, table):
        return False
    db.session.execute(text(f"ALTER TABLE {table} ADD COLUMN {ddl}"))
    return True


def _create_index_if_missing(table: str, index_name: str, columns: list[str]) -> bool:
    insp = inspect(db.engine)
    if index_name in _index_names(insp, table):
        return False
    cols = ", ".join(columns)
    db.session.execute(text(f"CREATE INDEX {index_name} ON {table} ({cols})"))
    return True


def _is_mysql() -> bool:
    return db.engine.dialect.name == "mysql"


def migrate_content_block_extra() -> None:
    ddl = "extra JSON NULL" if _is_mysql() else "extra JSON"
    if _add_column_if_missing("content_blocks", "extra", ddl):
        print("Added content_blocks.extra")


def migrate_job_listing_slug() -> None:
    insp = inspect(db.engine)
    if "slug" not in _column_names(insp, "job_listings"):
        ddl = "slug VARCHAR(150) NULL"
        db.session.execute(text(f"ALTER TABLE job_listings ADD COLUMN {ddl}"))
        print("Added job_listings.slug (nullable for backfill)")

        from app.data.careers_catalog import JOBS_CATALOG
        from app.models.catalog import JobListing

        slug_by_title = {job["title"]: job["slug"] for job in JOBS_CATALOG}
        used: set[str] = set()
        for row in JobListing.query.all():
            slug = slug_by_title.get(row.title) or _slugify(row.title)
            base = slug
            n = 2
            while slug in used:
                slug = f"{base}-{n}"
                n += 1
            row.slug = slug
            used.add(slug)
        db.session.flush()

        if _is_mysql():
            db.session.execute(
                text("ALTER TABLE job_listings MODIFY COLUMN slug VARCHAR(150) NOT NULL")
            )
            db.session.execute(text("CREATE UNIQUE INDEX ix_job_listings_slug ON job_listings (slug)"))
        else:
            db.session.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS ix_job_listings_slug ON job_listings (slug)"))
        print("Backfilled job_listings.slug and added unique index")
    elif "ix_job_listings_slug" not in _index_names(insp, "job_listings"):
        _create_index_if_missing("job_listings", "ix_job_listings_slug", ["slug"])
        print("Ensured job_listings slug index")


def migrate_projects_country() -> None:
    """Add country/county columns required by Project model (pre-2026 schemas)."""
    if _add_column_if_missing("projects", "country", "country VARCHAR(100) DEFAULT 'Kenya'"):
        print("Added projects.country")
    if _add_column_if_missing("projects", "county", "county VARCHAR(100) DEFAULT NULL"):
        print("Added projects.county")


def migrate_admin_indexes() -> None:
    specs = [
        ("contact_submissions", "ix_contact_submissions_is_read_created_at", ["is_read", "created_at"]),
        ("quote_requests", "ix_quote_requests_is_read_created_at", ["is_read", "created_at"]),
        ("audit_logs", "ix_audit_logs_resource_type_resource_id", ["resource_type", "resource_id"]),
        ("login_history", "ix_login_history_user_id_created_at", ["user_id", "created_at"]),
        ("projects", "ix_projects_country_is_active", ["country", "is_active"]),
    ]
    for table, index_name, columns in specs:
        if _create_index_if_missing(table, index_name, columns):
            print(f"Created index {index_name} on {table}")


def apply_pre_admin_migration() -> None:
    with app.app_context():
        migrate_content_block_extra()
        migrate_job_listing_slug()
        migrate_projects_country()
        migrate_admin_indexes()
        db.session.commit()
        print("Pre-admin migration completed successfully.")


if __name__ == "__main__":
    apply_pre_admin_migration()
