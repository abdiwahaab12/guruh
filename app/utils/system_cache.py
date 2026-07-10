"""File-based application cache for System Administration."""

from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path

from flask import current_app


def _cache_root() -> Path:
    root = Path(current_app.instance_path) / "cache"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _meta_path() -> Path:
    return _cache_root() / "_meta.json"


def _load_meta() -> dict:
    path = _meta_path()
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _save_meta(meta: dict) -> None:
    _meta_path().write_text(json.dumps(meta, indent=2), encoding="utf-8")


def get_cache_stats() -> dict:
    root = _cache_root()
    entries = [p for p in root.glob("*.json") if p.name != "_meta.json"]
    total_bytes = sum(p.stat().st_size for p in entries if p.is_file())
    meta = _load_meta()
    return {
        "entry_count": len(entries),
        "total_bytes": total_bytes,
        "last_rebuilt_label": meta.get("last_rebuilt_label", "Never"),
    }


def clear_cache() -> int:
    root = _cache_root()
    removed = 0
    for path in root.glob("*.json"):
        if path.name == "_meta.json":
            continue
        try:
            path.unlink()
            removed += 1
        except OSError:
            pass
    return removed


def rebuild_cache() -> int:
    from app.providers.admin_dashboard_provider import AdminDashboardProvider

    root = _cache_root()
    payload = {
        "dashboard": AdminDashboardProvider.get_dashboard().__dict__,
        "rebuilt_at": datetime.utcnow().isoformat(),
    }
    cache_file = root / f"dashboard-{int(time.time())}.json"

    def _default(obj):
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        return str(obj)

    cache_file.write_text(json.dumps(payload, default=_default, indent=2), encoding="utf-8")
    label = datetime.utcnow().strftime("%d %b %Y %H:%M UTC")
    _save_meta({"last_rebuilt_label": label, "last_rebuilt_at": datetime.utcnow().isoformat()})
    return 1
