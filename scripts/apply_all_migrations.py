"""
Apply all database migrations in order (MySQL / MariaDB / SQLite).

Usage:
    python scripts/apply_all_migrations.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MIGRATION_SCRIPTS = (
    "scripts/apply_pre_admin_migration.py",
    "scripts/apply_media_migration.py",
    "scripts/apply_project_details_migration.py",
    "scripts/apply_service_details_migration.py",
    "scripts/apply_equipment_migration.py",
    "scripts/apply_team_details_migration.py",
    "scripts/apply_gallery_details_migration.py",
    "scripts/apply_job_listing_details_migration.py",
    "scripts/apply_messages_inbox_migration.py",
    "scripts/apply_hero_slides_migration.py",
    "scripts/apply_hero_video_migration.py",
)


def main() -> None:
    print("Applying all migrations...")
    for script in MIGRATION_SCRIPTS:
        path = ROOT / script
        print(f"\n--- {script} ---")
        result = subprocess.run([sys.executable, str(path)], cwd=str(ROOT))
        if result.returncode != 0:
            print(f"FAILED: {script}")
            raise SystemExit(1)
    print("\nAll migrations applied successfully.")


if __name__ == "__main__":
    main()
