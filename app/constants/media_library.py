"""
Enterprise Media Library — folders, types, and upload rules.
"""

from __future__ import annotations

from typing import Final

MEDIA_FOLDERS: Final[list[dict[str, str]]] = [
    {"slug": "content", "label": "Website Content", "icon": "bi-layout-text-window-reverse"},
    {"slug": "projects", "label": "Projects", "icon": "bi-building"},
    {"slug": "services", "label": "Services", "icon": "bi-grid"},
    {"slug": "equipment", "label": "Equipment", "icon": "bi-truck"},
    {"slug": "gallery", "label": "Gallery", "icon": "bi-images"},
    {"slug": "team", "label": "Team", "icon": "bi-people"},
    {"slug": "careers", "label": "Careers", "icon": "bi-briefcase"},
    {"slug": "company", "label": "Company", "icon": "bi-building-check"},
    {"slug": "downloads", "label": "Downloads", "icon": "bi-download"},
    {"slug": "general", "label": "General", "icon": "bi-folder2"},
]

MEDIA_FOLDER_SLUGS: Final[frozenset[str]] = frozenset(f["slug"] for f in MEDIA_FOLDERS)

MEDIA_TYPES: Final[list[dict[str, str]]] = [
    {"slug": "image", "label": "Images", "icon": "bi-image"},
    {"slug": "video", "label": "Videos", "icon": "bi-camera-video"},
    {"slug": "pdf", "label": "PDF", "icon": "bi-file-earmark-pdf"},
    {"slug": "document", "label": "Documents", "icon": "bi-file-earmark-text"},
    {"slug": "icon", "label": "Icons", "icon": "bi-star"},
]

MEDIA_TYPE_SLUGS: Final[frozenset[str]] = frozenset(t["slug"] for t in MEDIA_TYPES)

ALLOWED_EXTENSIONS: Final[dict[str, frozenset[str]]] = {
    "image": frozenset({"jpg", "jpeg", "png", "gif", "webp", "svg", "bmp"}),
    "video": frozenset({"mp4", "webm", "mov", "avi", "mkv"}),
    "pdf": frozenset({"pdf"}),
    "document": frozenset({"doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt", "csv", "rtf"}),
    "icon": frozenset({"svg", "png", "ico"}),
}

ALL_ALLOWED_EXTENSIONS: Final[frozenset[str]] = frozenset().union(*ALLOWED_EXTENSIONS.values())

MIME_TO_MEDIA_TYPE: Final[dict[str, str]] = {
    "image/jpeg": "image",
    "image/png": "image",
    "image/gif": "image",
    "image/webp": "image",
    "image/svg+xml": "image",
    "image/bmp": "image",
    "image/x-icon": "icon",
    "video/mp4": "video",
    "video/webm": "video",
    "video/quicktime": "video",
    "video/x-msvideo": "video",
    "video/x-matroska": "video",
    "application/pdf": "pdf",
    "application/msword": "document",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "document",
    "application/vnd.ms-excel": "document",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "document",
    "application/vnd.ms-powerpoint": "document",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": "document",
    "text/plain": "document",
    "text/csv": "document",
    "application/rtf": "document",
}

DEFAULT_PER_PAGE: Final[int] = 24
MAX_PER_PAGE: Final[int] = 96
MAX_UPLOAD_BATCH: Final[int] = 20

SORT_OPTIONS: Final[dict[str, str]] = {
    "date_desc": "Newest first",
    "date_asc": "Oldest first",
    "name_asc": "Name A–Z",
    "name_desc": "Name Z–A",
    "size_desc": "Largest first",
    "size_asc": "Smallest first",
    "type_asc": "Type",
}
