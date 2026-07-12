"""Hero background video upload rules — MP4 and WEBM only."""

from __future__ import annotations

from typing import Final

HERO_VIDEO_STORAGE_DIR: Final[str] = "uploads/hero_videos"
HERO_VIDEO_THUMB_DIR: Final[str] = "uploads/hero_videos/thumbnails"

HERO_VIDEO_ALLOWED_EXTENSIONS: Final[frozenset[str]] = frozenset({"mp4", "webm"})

HERO_VIDEO_ALLOWED_MIME_TYPES: Final[frozenset[str]] = frozenset(
    {"video/mp4", "video/webm"}
)

HERO_VIDEO_REJECTED_EXTENSIONS: Final[dict[str, str]] = {
    "avi": "AVI video format is not supported. Please upload MP4 or WEBM.",
    "mov": "MOV video format is not supported. Please upload MP4 or WEBM.",
    "mkv": "MKV video format is not supported. Please upload MP4 or WEBM.",
    "wmv": "WMV video format is not supported. Please upload MP4 or WEBM.",
    "flv": "FLV video format is not supported. Please upload MP4 or WEBM.",
}

HERO_BACKGROUND_IMAGE: Final[str] = "image"
HERO_BACKGROUND_VIDEO: Final[str] = "video"

HERO_BACKGROUND_TYPES: Final[tuple[str, ...]] = (HERO_BACKGROUND_IMAGE, HERO_BACKGROUND_VIDEO)
