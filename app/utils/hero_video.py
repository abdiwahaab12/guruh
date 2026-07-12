"""Hero background video upload, validation, thumbnail, and file cleanup."""

from __future__ import annotations

import logging
import shutil
import subprocess
import uuid
from pathlib import Path

from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.constants.hero_video import (
    HERO_VIDEO_ALLOWED_EXTENSIONS,
    HERO_VIDEO_ALLOWED_MIME_TYPES,
    HERO_VIDEO_REJECTED_EXTENSIONS,
    HERO_VIDEO_STORAGE_DIR,
    HERO_VIDEO_THUMB_DIR,
)

logger = logging.getLogger(__name__)


def _static_root() -> Path:
    return Path(current_app.static_folder or "static")


def _max_bytes() -> int:
    return int(current_app.config.get("MEDIA_MAX_FILE_SIZE", 100 * 1024 * 1024))


def _format_bytes(size: int) -> str:
    if size >= 1024 * 1024:
        return f"{size / (1024 * 1024):.1f} MB"
    return f"{size / 1024:.1f} KB"


def _extension(filename: str) -> str:
    if "." not in filename:
        return ""
    return filename.rsplit(".", 1)[1].lower()


def validate_hero_video_file(file: FileStorage | None) -> tuple[bool, str]:
    """Validate hero video upload — extension, MIME, and size."""
    if not file or not file.filename:
        return False, "No video file selected."

    ext = _extension(file.filename)
    if ext in HERO_VIDEO_REJECTED_EXTENSIONS:
        return False, HERO_VIDEO_REJECTED_EXTENSIONS[ext]
    if ext not in HERO_VIDEO_ALLOWED_EXTENSIONS:
        return False, "Only MP4 and WEBM video formats are supported."

    mime = (file.mimetype or "").strip().lower()
    if mime and mime not in HERO_VIDEO_ALLOWED_MIME_TYPES:
        return False, f"Unsupported video MIME type ({mime}). Use MP4 or WEBM."

    file.stream.seek(0, 2)
    size = file.stream.tell()
    file.stream.seek(0)
    max_size = _max_bytes()
    if size > max_size:
        return False, f"Video exceeds maximum size of {_format_bytes(max_size)}."

    safe = secure_filename(file.filename)
    if not safe or ".." in safe or "/" in safe or "\\" in safe:
        return False, "Invalid video filename."

    return True, ""


def _ensure_dirs() -> tuple[Path, Path]:
    video_dir = _static_root() / HERO_VIDEO_STORAGE_DIR
    thumb_dir = _static_root() / HERO_VIDEO_THUMB_DIR
    video_dir.mkdir(parents=True, exist_ok=True)
    thumb_dir.mkdir(parents=True, exist_ok=True)
    return video_dir, thumb_dir


def _normalize_storage_path(path: str) -> str:
    cleaned = (path or "").strip().replace("\\", "/")
    if not cleaned or ".." in cleaned:
        return ""
    if not cleaned.startswith("uploads/hero_videos/"):
        return ""
    return cleaned


def save_hero_video_file(
    file: FileStorage,
    *,
    fallback_image: str = "",
) -> tuple[str, str, str | None]:
    """
    Save hero video with unique filename.

    Returns (video_path, thumbnail_path, error_message).
    """
    ok, err = validate_hero_video_file(file)
    if not ok:
        return "", "", err

    ext = _extension(file.filename)
    video_dir, thumb_dir = _ensure_dirs()
    unique = uuid.uuid4().hex
    filename = f"hero_{unique}.{ext}"
    dest = video_dir / filename

    file.save(dest)

    video_path = f"{HERO_VIDEO_STORAGE_DIR}/{filename}"
    thumb_path = generate_video_thumbnail(
        str(dest),
        fallback_image=fallback_image,
        unique_id=unique,
    )
    return video_path, thumb_path, None


def generate_video_thumbnail(
    video_abs_path: str,
    *,
    fallback_image: str = "",
    unique_id: str | None = None,
) -> str:
    """Generate poster thumbnail — ffmpeg frame or fallback image copy."""
    _, thumb_dir = _ensure_dirs()
    uid = unique_id or uuid.uuid4().hex
    thumb_filename = f"hero_{uid}.jpg"
    thumb_abs = thumb_dir / thumb_filename
    thumb_rel = f"{HERO_VIDEO_THUMB_DIR}/{thumb_filename}"

    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        try:
            result = subprocess.run(
                [
                    ffmpeg,
                    "-y",
                    "-i",
                    video_abs_path,
                    "-ss",
                    "00:00:01",
                    "-vframes",
                    "1",
                    "-q:v",
                    "2",
                    str(thumb_abs),
                ],
                capture_output=True,
                timeout=30,
                check=False,
            )
            if result.returncode == 0 and thumb_abs.is_file() and thumb_abs.stat().st_size > 0:
                return thumb_rel
        except (OSError, subprocess.TimeoutExpired) as exc:
            logger.warning("ffmpeg thumbnail failed: %s", exc)

    fallback = _normalize_storage_path(fallback_image) or (fallback_image or "").strip().replace("\\", "/")
    if fallback and not fallback.startswith(".."):
        src = _static_root() / fallback
        if src.is_file():
            try:
                shutil.copy2(src, thumb_abs)
                return thumb_rel
            except OSError as exc:
                logger.warning("fallback thumbnail copy failed: %s", exc)

    return ""


def delete_hero_video_files(video_path: str, thumbnail_path: str = "") -> None:
    """Remove hero video and thumbnail from disk."""
    for rel in (video_path, thumbnail_path):
        cleaned = _normalize_storage_path(rel) if "hero_videos" in rel else rel.replace("\\", "/")
        if not cleaned or ".." in cleaned:
            continue
        if not cleaned.startswith("uploads/"):
            continue
        abs_path = _static_root() / cleaned
        try:
            if abs_path.is_file():
                abs_path.unlink()
        except OSError as exc:
            logger.warning("Could not delete hero video file %s: %s", cleaned, exc)
