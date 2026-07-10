"""
Create MySQL database and run full production setup.

Usage:
    python scripts/setup_mysql.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env", override=True)

import pymysql


def _db_name_from_url(url: str) -> str:
    parsed = urlparse(url.replace("mysql+pymysql://", "mysql://"))
    return parsed.path.lstrip("/").split("?")[0]


def _connect_server(url: str):
    parsed = urlparse(url.replace("mysql+pymysql://", "mysql://"))
    return pymysql.connect(
        host=parsed.hostname or "127.0.0.1",
        port=parsed.port or 3306,
        user=parsed.username or "root",
        password=parsed.password or "",
        charset="utf8mb4",
    )


def create_database_if_missing() -> None:
    import os

    url = os.environ.get("DATABASE_URL", "")
    if not url.startswith("mysql"):
        print(f"DATABASE_URL is not MySQL: {url}")
        raise SystemExit(1)

    db_name = _db_name_from_url(url)
    conn = _connect_server(url)
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        conn.commit()
        print(f"Database ready: {db_name}")
    finally:
        conn.close()


def run(script: str) -> None:
    print(f"\n>> {script}")
    result = subprocess.run([sys.executable, str(ROOT / script)], cwd=str(ROOT))
    if result.returncode != 0:
        raise SystemExit(f"Failed: {script}")


def main() -> None:
    create_database_if_missing()
    run("init_db.py")
    run("scripts/apply_all_migrations.py")
    run("scripts/seed_auth.py")
    run("scripts/seed_settings.py")
    run("seed_cms_blocks.py")
    run("seed_page_sections.py")
    print("\nMySQL setup complete.")


if __name__ == "__main__":
    main()
