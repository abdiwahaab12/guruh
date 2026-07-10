"""System Administration log file helpers."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from flask import current_app

from app.constants.system_admin import LOG_FILES, MAX_LOG_LINES


def _log_root() -> Path:
    root = Path(current_app.instance_path) / "logs"
    root.mkdir(parents=True, exist_ok=True)
    return root


def append_log(level: str, message: str) -> None:
    root = _log_root()
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} [{level.upper()}] {message}\n"
    app_log = root / LOG_FILES["application"]
    with app_log.open("a", encoding="utf-8") as handle:
        handle.write(line)
    if level.lower() in ("error", "critical"):
        err_log = root / LOG_FILES["error"]
        with err_log.open("a", encoding="utf-8") as handle:
            handle.write(line)


def tail_log(log_key: str, limit: int = MAX_LOG_LINES) -> list[tuple[int, str, str]]:
    filename = LOG_FILES.get(log_key)
    if not filename:
        return []
    path = _log_root() / filename
    if not path.is_file():
        return []

    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    tail = lines[-limit:]
    result = []
    start = len(lines) - len(tail) + 1
    for idx, content in enumerate(tail, start=start):
        level = "info"
        if "[ERROR]" in content or "[CRITICAL]" in content:
            level = "error"
        elif "[WARNING]" in content:
            level = "warning"
        result.append((idx, content, level))
    return result
