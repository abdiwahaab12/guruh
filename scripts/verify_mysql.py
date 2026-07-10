"""
MySQL pre-deployment verification — schema, seeds, connectivity, smoke tests.

Usage:
    python scripts/verify_mysql.py
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env", override=True)

import app.models  # noqa: F401
from run import app
from app.extensions import db
from sqlalchemy import inspect, text

# Expected tables from app.models
EXPECTED_TABLES = sorted(
    {
        "about_sections",
        "audit_logs",
        "company_info",
        "contact_page_content",
        "contact_submission_details",
        "contact_submissions",
        "content_block_items",
        "content_blocks",
        "cta_sections",
        "equipment",
        "equipment_details",
        "footer_content",
        "gallery_details",
        "gallery_images",
        "hero_slides",
        "job_applications",
        "job_listing_details",
        "job_listings",
        "login_history",
        "media_assets",
        "nav_items",
        "office_locations",
        "page_sections",
        "pages",
        "partners",
        "password_resets",
        "permissions",
        "process_steps",
        "project_details",
        "projects",
        "quote_page_content",
        "quote_request_details",
        "quote_requests",
        "role_permissions",
        "roles",
        "section_headings",
        "service_details",
        "services",
        "site_settings",
        "social_links",
        "statistics",
        "team_details",
        "team_members",
        "testimonials",
        "trust_badges",
        "user_sessions",
        "users",
        "why_choose_us_items",
        "why_choose_us_sections",
        "working_process_sections",
    }
)

PUBLIC_ROUTES = (
    "/",
    "/about",
    "/services",
    "/projects",
    "/equipment",
    "/gallery",
    "/team",
    "/careers",
    "/testimonials",
    "/contact",
    "/request-quote",
    "/health",
)


def _sqlite_refs() -> list[str]:
    refs = []
    db_url = os.environ.get("DATABASE_URL", "")
    if "sqlite" in db_url.lower():
        refs.append(f"DATABASE_URL uses SQLite: {db_url}")
    if os.environ.get("DATABASE_ENABLED", "").lower() != "true":
        refs.append("DATABASE_ENABLED is not true")
    return refs


def main() -> None:
    report: dict = {
        "sqlite_references": [],
        "mysql_connection": "unknown",
        "database_enabled": os.environ.get("DATABASE_ENABLED"),
        "database_url_masked": "",
        "tables_expected": len(EXPECTED_TABLES),
        "tables_found": [],
        "tables_missing": [],
        "schema_issues": [],
        "seed_counts": {},
        "public_pages": {},
        "test_failures": [],
        "fixed_issues": [],
        "blockers": [],
    }

    url = os.environ.get("DATABASE_URL", "")
    if "@" in url:
        report["database_url_masked"] = url.split("@", 1)[1]
    else:
        report["database_url_masked"] = url

    report["sqlite_references"] = _sqlite_refs()

    with app.app_context():
        dialect = db.engine.dialect.name
        report["mysql_connection"] = f"OK ({dialect})" if dialect == "mysql" else f"FAIL ({dialect})"
        if dialect != "mysql":
            report["blockers"].append(f"Expected MySQL dialect, got {dialect}")

        try:
            db.session.execute(text("SELECT 1")).scalar()
        except Exception as exc:
            report["mysql_connection"] = f"FAIL: {exc}"
            report["blockers"].append(str(exc))

        insp = inspect(db.engine)
        found = set(insp.get_table_names())
        report["tables_found"] = sorted(found)
        missing = sorted(set(EXPECTED_TABLES) - found)
        report["tables_missing"] = missing
        if missing:
            report["blockers"].append(f"Missing tables: {', '.join(missing)}")

        # Critical column checks
        project_cols = {c["name"] for c in insp.get_columns("projects")} if "projects" in found else set()
        for col in ("country", "county"):
            if "projects" in found and col not in project_cols:
                report["schema_issues"].append(f"projects.{col} missing")
                report["blockers"].append(f"projects.{col} column missing")

        from app.models.auth import Permission, Role, User
        from app.models.content_blocks import ContentBlock
        from app.models.page_sections import PageSection
        from app.models.site import CompanyInfo, SiteSetting

        report["seed_counts"] = {
            "roles": Role.query.count(),
            "permissions": Permission.query.count(),
            "users": User.query.count(),
            "company_info": CompanyInfo.query.count(),
            "site_settings": SiteSetting.query.count(),
            "content_blocks": ContentBlock.query.count(),
            "page_sections": PageSection.query.count(),
        }

        if report["seed_counts"]["users"] < 1:
            report["blockers"].append("No admin user seeded")
        if report["seed_counts"]["permissions"] < 1:
            report["blockers"].append("No permissions seeded")

        provider = app.extensions.get("content_provider")
        provider_name = type(provider).__name__ if provider else "none"
        report["content_provider"] = provider_name
        if os.environ.get("DATABASE_ENABLED", "").lower() == "true" and "Database" not in provider_name:
            report["blockers"].append(f"DATABASE_ENABLED=true but provider is {provider_name}")

        client = app.test_client()
        for route in PUBLIC_ROUTES:
            r = client.get(route)
            report["public_pages"][route] = r.status_code
            if r.status_code != 200:
                report["blockers"].append(f"Public route {route} returned {r.status_code}")

    # Run test suite
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "test_release.py")],
        cwd=str(ROOT),
        env={**os.environ},
    )
    if result.returncode != 0:
        report["test_failures"].append("test_release.py failed")
        report["blockers"].append("One or more test suites failed")

    # Print report
    print("\n" + "=" * 60)
    print("MYSQL PRE-DEPLOYMENT VERIFICATION REPORT")
    print("=" * 60)
    print(f"\nDATABASE_ENABLED: {report['database_enabled']}")
    print(f"Connection:       {report['mysql_connection']}")
    print(f"Database URL:     ...@{report['database_url_masked']}")
    print(f"Content provider: {report.get('content_provider', 'n/a')}")

    print(f"\nSQLite/config issues ({len(report['sqlite_references'])}):")
    for item in report["sqlite_references"] or ["None"]:
        print(f"  - {item}")

    print(f"\nTables: {len(report['tables_found'])}/{report['tables_expected']} expected")
    if report["tables_missing"]:
        print("Missing:", ", ".join(report["tables_missing"]))
    if report["schema_issues"]:
        print("Schema issues:", ", ".join(report["schema_issues"]))

    print("\nSeed data:")
    for key, val in report["seed_counts"].items():
        print(f"  {key}: {val}")

    print("\nPublic pages:")
    for route, status in report["public_pages"].items():
        mark = "OK" if status == 200 else "FAIL"
        print(f"  [{mark}] {route} -> {status}")

    print(f"\nTest suite: {'PASS' if not report['test_failures'] else 'FAIL'}")

    if report["blockers"]:
        print(f"\nDEPLOYMENT BLOCKERS ({len(report['blockers'])}):")
        for b in report["blockers"]:
            print(f"  ! {b}")
        raise SystemExit(1)

    print("\nVERDICT: MySQL production verification PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
