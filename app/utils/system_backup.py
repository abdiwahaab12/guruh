"""Database backup and restore utilities."""

from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlparse

from flask import current_app
from sqlalchemy import inspect, text

from app.extensions import db


def _backup_root() -> Path:
    root = Path(current_app.instance_path) / "backups"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _format_bytes(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{round(size / 1024, 1)} KB"
    if size < 1024 * 1024 * 1024:
        return f"{round(size / (1024 * 1024), 1)} MB"
    return f"{round(size / (1024 * 1024 * 1024), 2)} GB"


def _sqlite_db_path(uri: str) -> Path | None:
    if not uri.startswith("sqlite"):
        return None
    raw = uri.replace("sqlite:///", "").split("?")[0]
    if raw == ":memory:":
        return None
    return Path(raw)


def _mysql_dump(uri: str, dest: Path) -> bool:
    parsed = urlparse(uri)
    if parsed.scheme not in ("mysql", "mysql+pymysql"):
        return False
    mysqldump = shutil.which("mysqldump")
    if not mysqldump:
        return False
    db_name = parsed.path.lstrip("/")
    cmd = [
        mysqldump,
        f"--host={parsed.hostname or 'localhost'}",
        f"--port={parsed.port or 3306}",
        f"--user={unquote(parsed.username or 'root')}",
        db_name,
    ]
    env = None
    if parsed.password:
        env = {"MYSQL_PWD": unquote(parsed.password)}
    with dest.open("w", encoding="utf-8") as handle:
        result = subprocess.run(cmd, stdout=handle, stderr=subprocess.PIPE, env=env, check=False)
    return result.returncode == 0 and dest.stat().st_size > 0


def _sqlalchemy_sql_dump(dest: Path) -> None:
    engine = db.engine
    inspector = inspect(engine)
    lines = ["-- GURUH CMS SQL backup", f"-- Generated {datetime.utcnow().isoformat()} UTC", ""]
    with engine.connect() as conn:
        for table in inspector.get_table_names():
            lines.append(f"-- Table: {table}")
            rows = conn.execute(text(f"SELECT * FROM `{table}`")).mappings().all()
            if not rows:
                lines.append("")
                continue
            columns = list(rows[0].keys())
            col_list = ", ".join(f"`{c}`" for c in columns)
            for row in rows:
                values = []
                for col in columns:
                    val = row[col]
                    if val is None:
                        values.append("NULL")
                    elif isinstance(val, (int, float)):
                        values.append(str(val))
                    else:
                        escaped = str(val).replace("'", "''")
                        values.append(f"'{escaped}'")
                lines.append(f"INSERT INTO `{table}` ({col_list}) VALUES ({', '.join(values)});")
            lines.append("")
    dest.write_text("\n".join(lines), encoding="utf-8")


def create_backup() -> tuple[str, str]:
    """Create backup file. Returns (filename, backup_type)."""
    uri = current_app.config.get("SQLALCHEMY_DATABASE_URI", "")
    stamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    root = _backup_root()

    sqlite_path = _sqlite_db_path(uri)
    if sqlite_path and sqlite_path.is_file():
        filename = f"guruh-backup-{stamp}.db"
        shutil.copy2(sqlite_path, root / filename)
        meta = {"type": "sqlite", "source": str(sqlite_path)}
        (root / f"{filename}.meta.json").write_text(json.dumps(meta), encoding="utf-8")
        return filename, "sqlite"

    filename = f"guruh-backup-{stamp}.sql"
    dest = root / filename
    if _mysql_dump(uri, dest):
        backup_type = "mysql"
    else:
        _sqlalchemy_sql_dump(dest)
        backup_type = "sql"

    meta = {"type": backup_type, "uri_scheme": urlparse(uri).scheme}
    (root / f"{filename}.meta.json").write_text(json.dumps(meta), encoding="utf-8")
    return filename, backup_type


def list_backups() -> list[dict]:
    root = _backup_root()
    items = []
    for path in sorted(root.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
        if path.suffix == ".json" or path.name.endswith(".meta.json"):
            continue
        if not path.is_file():
            continue
        stat = path.stat()
        meta_path = root / f"{path.name}.meta.json"
        backup_type = "unknown"
        if meta_path.is_file():
            try:
                backup_type = json.loads(meta_path.read_text(encoding="utf-8")).get("type", "unknown")
            except (json.JSONDecodeError, OSError):
                pass
        items.append(
            {
                "filename": path.name,
                "size_bytes": stat.st_size,
                "size_label": _format_bytes(stat.st_size),
                "created_at_label": datetime.utcfromtimestamp(stat.st_mtime).strftime("%d %b %Y %H:%M UTC"),
                "backup_type": backup_type,
            }
        )
    return items


def get_backup_path(filename: str) -> Path | None:
    safe = Path(filename).name
    path = _backup_root() / safe
    if path.is_file() and path.parent == _backup_root():
        return path
    return None


def restore_backup(filename: str) -> None:
    path = get_backup_path(filename)
    if not path:
        raise FileNotFoundError("Backup file not found.")

    uri = current_app.config.get("SQLALCHEMY_DATABASE_URI", "")
    sqlite_path = _sqlite_db_path(uri)

    if sqlite_path and path.suffix == ".db":
        db.session.remove()
        shutil.copy2(path, sqlite_path)
        return

    if path.suffix == ".sql":
        sql = path.read_text(encoding="utf-8")
        statements = [s.strip() for s in sql.split(";") if s.strip() and not s.strip().startswith("--")]
        with db.engine.begin() as conn:
            for stmt in statements:
                if stmt.upper().startswith("INSERT INTO"):
                    conn.execute(text(stmt))
        return

    raise ValueError("Unsupported backup format for restore.")
