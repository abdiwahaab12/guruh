"""Media library data provider — filesystem + MySQL."""

from __future__ import annotations

import json
import mimetypes
import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from flask import current_app
from sqlalchemy import asc, desc, func, or_
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.constants.media_library import (
    ALL_ALLOWED_EXTENSIONS,
    ALLOWED_EXTENSIONS,
    MEDIA_FOLDER_SLUGS,
    MEDIA_FOLDERS,
    MEDIA_TYPE_SLUGS,
    MEDIA_TYPES,
    MIME_TO_MEDIA_TYPE,
)
from app.extensions import db
from app.models.media import MediaAsset
from app.providers.auth_provider import AuthProvider
from app.schemas.media_admin import MediaAssetDTO, MediaUsageDTO


def _folder_label(slug: str) -> str:
    for item in MEDIA_FOLDERS:
        if item["slug"] == slug:
            return item["label"]
    return slug.replace("-", " ").title()


def _type_label(slug: str) -> str:
    for item in MEDIA_TYPES:
        if item["slug"] == slug:
            return item["label"]
    return slug.title()


def _format_bytes(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    if size < 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024):.1f} MB"
    return f"{size / (1024 * 1024 * 1024):.2f} GB"


def _static_root() -> Path:
    return Path(current_app.static_folder or "static")


def _upload_root() -> str:
    return current_app.config.get("MEDIA_UPLOAD_ROOT", "uploads")


def _abs_path(storage_path: str) -> Path:
    return _static_root() / storage_path.replace("\\", "/")


def _extension(filename: str) -> str:
    if "." not in filename:
        return ""
    return filename.rsplit(".", 1)[1].lower()


def _detect_media_type(filename: str, mime_type: str, folder: str) -> str:
    if folder == "downloads" and mime_type == "application/pdf":
        return "pdf"
    if mime_type in MIME_TO_MEDIA_TYPE:
        detected = MIME_TO_MEDIA_TYPE[mime_type]
        if detected == "image" and folder == "general":
            ext = _extension(filename)
            # Only treat true icons as icon type — PNG/JPG stay selectable for hero backgrounds
            if ext in {"svg", "ico"}:
                return "icon"
        return detected
    ext = _extension(filename)
    for media_type, extensions in ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            return media_type
    return "document"


def _validate_file(file: FileStorage, folder: str) -> tuple[str | None, str | None]:
    if not file or not file.filename:
        return None, "No file selected."
    if folder not in MEDIA_FOLDER_SLUGS:
        return None, f"Invalid folder: {folder}"
    ext = _extension(file.filename)
    if ext not in ALL_ALLOWED_EXTENSIONS:
        return None, f"File type .{ext} is not allowed."
    mime = file.mimetype or mimetypes.guess_type(file.filename)[0] or "application/octet-stream"
    media_type = _detect_media_type(file.filename, mime, folder)
    if ext not in ALLOWED_EXTENSIONS.get(media_type, frozenset()):
        if ext not in ALL_ALLOWED_EXTENSIONS:
            return None, f"Extension .{ext} not permitted."
    max_size = current_app.config.get("MEDIA_MAX_FILE_SIZE", 20 * 1024 * 1024)
    file.stream.seek(0, os.SEEK_END)
    size = file.stream.tell()
    file.stream.seek(0)
    if size > max_size:
        return None, f"File exceeds maximum size of {_format_bytes(max_size)}."
    return media_type, None


class MediaProvider:
    """Database and filesystem operations for media assets."""

    @staticmethod
    def commit() -> bool:
        return AuthProvider.commit()

    @staticmethod
    def rollback() -> None:
        AuthProvider.rollback()

    @staticmethod
    def record_audit(**kwargs) -> None:
        AuthProvider.record_audit_event(**kwargs)

    @staticmethod
    def asset_to_dto(row: MediaAsset, usage: list[MediaUsageDTO] | None = None) -> MediaAssetDTO:
        uploader = ""
        if row.uploaded_by:
            uploader = row.uploaded_by.full_name
        created = row.created_at.strftime("%d %b %Y, %H:%M") if row.created_at else ""
        return MediaAssetDTO(
            id=row.id,
            filename=row.filename,
            original_filename=row.original_filename,
            storage_path=row.storage_path,
            public_url=f"/static/{row.storage_path}",
            folder=row.folder,
            folder_label=_folder_label(row.folder),
            media_type=row.media_type,
            media_type_label=_type_label(row.media_type),
            mime_type=row.mime_type,
            file_size=row.file_size,
            file_size_label=_format_bytes(row.file_size),
            title=row.title or row.original_filename,
            alt_text=row.alt_text or "",
            caption=row.caption or "",
            description=row.description or "",
            tags=row.tags or "",
            category=row.category or "",
            seo_title=row.seo_title or "",
            seo_description=row.seo_description or "",
            width=row.width,
            height=row.height,
            uploaded_by_name=uploader,
            created_at_label=created,
            is_active=row.is_active,
            usage=usage or [],
            is_image=row.media_type == "image" or row.media_type == "icon",
            is_video=row.media_type == "video",
            is_pdf=row.media_type == "pdf",
        )

    @staticmethod
    def get_asset(asset_id: int, include_inactive: bool = False) -> MediaAsset | None:
        try:
            query = MediaAsset.query.filter_by(id=asset_id)
            if not include_inactive:
                query = query.filter_by(is_active=True)
            return query.first()
        except SQLAlchemyError as exc:
            current_app.logger.error("get_asset failed: %s", exc)
            return None

    @staticmethod
    def save_upload(
        file: FileStorage,
        *,
        folder: str,
        uploaded_by_id: int | None,
        title: str = "",
        alt_text: str = "",
    ) -> tuple[MediaAsset | None, str | None]:
        media_type, error = _validate_file(file, folder)
        if error:
            return None, error

        original = secure_filename(file.filename)
        unique_name = f"{uuid.uuid4().hex[:12]}_{original}"
        storage_path = f"{_upload_root()}/{folder}/{unique_name}".replace("\\", "/")

        abs_path = _abs_path(storage_path)
        abs_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            file.save(abs_path)
        except OSError as exc:
            current_app.logger.error("save_upload filesystem failed: %s", exc)
            return None, "Failed to save file to disk."

        mime = file.mimetype or mimetypes.guess_type(original)[0] or "application/octet-stream"
        file_size = abs_path.stat().st_size if abs_path.exists() else 0

        asset = MediaAsset(
            filename=unique_name,
            original_filename=original,
            storage_path=storage_path,
            folder=folder,
            media_type=media_type or "document",
            mime_type=mime,
            file_size=file_size,
            title=title or os.path.splitext(original)[0].replace("-", " ").replace("_", " ").title(),
            alt_text=alt_text,
            uploaded_by_id=uploaded_by_id,
            is_active=True,
        )
        db.session.add(asset)
        return asset, None

    @staticmethod
    def query_library(
        *,
        q: str = "",
        folder: str = "",
        media_type: str = "",
        sort: str = "date_desc",
        page: int = 1,
        per_page: int = 24,
    ) -> tuple[list[MediaAsset], int]:
        try:
            query = MediaAsset.query.filter_by(is_active=True)

            if folder and folder in MEDIA_FOLDER_SLUGS:
                query = query.filter(MediaAsset.folder == folder)
            if media_type and media_type in MEDIA_TYPE_SLUGS:
                query = query.filter(MediaAsset.media_type == media_type)
            if q:
                term = f"%{q.strip()}%"
                query = query.filter(
                    or_(
                        MediaAsset.title.ilike(term),
                        MediaAsset.original_filename.ilike(term),
                        MediaAsset.filename.ilike(term),
                        MediaAsset.alt_text.ilike(term),
                        MediaAsset.tags.ilike(term),
                        MediaAsset.caption.ilike(term),
                    )
                )

            sort_map = {
                "date_desc": desc(MediaAsset.created_at),
                "date_asc": asc(MediaAsset.created_at),
                "name_asc": asc(MediaAsset.title),
                "name_desc": desc(MediaAsset.title),
                "size_desc": desc(MediaAsset.file_size),
                "size_asc": asc(MediaAsset.file_size),
                "type_asc": asc(MediaAsset.media_type),
            }
            query = query.order_by(sort_map.get(sort, desc(MediaAsset.created_at)))

            total = query.count()
            items = query.offset((page - 1) * per_page).limit(per_page).all()
            return items, total
        except SQLAlchemyError as exc:
            current_app.logger.error("query_library failed: %s", exc)
            return [], 0

    @staticmethod
    def get_stats() -> dict:
        try:
            total_files = MediaAsset.query.filter_by(is_active=True).count()
            total_storage = (
                db.session.query(func.coalesce(func.sum(MediaAsset.file_size), 0))
                .filter(MediaAsset.is_active.is_(True))
                .scalar()
            ) or 0

            by_type_rows = (
                db.session.query(MediaAsset.media_type, func.count(MediaAsset.id))
                .filter(MediaAsset.is_active.is_(True))
                .group_by(MediaAsset.media_type)
                .all()
            )
            by_folder_rows = (
                db.session.query(MediaAsset.folder, func.count(MediaAsset.id))
                .filter(MediaAsset.is_active.is_(True))
                .group_by(MediaAsset.folder)
                .all()
            )

            recent = (
                MediaAsset.query.filter_by(is_active=True)
                .order_by(desc(MediaAsset.created_at))
                .limit(8)
                .all()
            )

            return {
                "total_files": total_files,
                "total_storage": int(total_storage),
                "by_type": {row[0]: row[1] for row in by_type_rows},
                "by_folder": {row[0]: row[1] for row in by_folder_rows},
                "recent": recent,
            }
        except SQLAlchemyError as exc:
            current_app.logger.error("get_stats failed: %s", exc)
            return {
                "total_files": 0,
                "total_storage": 0,
                "by_type": {},
                "by_folder": {},
                "recent": [],
            }

    @staticmethod
    def update_metadata(asset: MediaAsset, data: dict) -> MediaAsset:
        asset.title = data.get("title", asset.title).strip()
        asset.alt_text = data.get("alt_text", asset.alt_text or "").strip()
        asset.caption = data.get("caption", asset.caption or "").strip()
        asset.description = data.get("description", asset.description or "").strip()
        asset.tags = data.get("tags", asset.tags or "").strip()
        asset.category = data.get("category", asset.category or "").strip()
        asset.seo_title = data.get("seo_title", asset.seo_title or "").strip()
        asset.seo_description = data.get("seo_description", asset.seo_description or "").strip()
        if data.get("original_filename"):
            asset.original_filename = secure_filename(data["original_filename"])
        return asset

    @staticmethod
    def move_asset(asset: MediaAsset, new_folder: str) -> tuple[MediaAsset | None, str | None]:
        if new_folder not in MEDIA_FOLDER_SLUGS:
            return None, "Invalid folder."
        if asset.folder == new_folder:
            return asset, None

        old_path = _abs_path(asset.storage_path)
        new_storage = f"{_upload_root()}/{new_folder}/{asset.filename}".replace("\\", "/")
        new_path = _abs_path(new_storage)
        new_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            if old_path.exists():
                shutil.move(str(old_path), str(new_path))
            asset.storage_path = new_storage
            asset.folder = new_folder
            return asset, None
        except OSError as exc:
            current_app.logger.error("move_asset failed: %s", exc)
            return None, "Failed to move file on disk."

    @staticmethod
    def copy_asset(asset: MediaAsset, uploaded_by_id: int | None) -> tuple[MediaAsset | None, str | None]:
        src = _abs_path(asset.storage_path)
        if not src.exists():
            return None, "Source file not found on disk."

        base, ext = os.path.splitext(asset.filename)
        copy_name = f"{base}-copy-{uuid.uuid4().hex[:6]}{ext}"
        new_storage = f"{_upload_root()}/{asset.folder}/{copy_name}".replace("\\", "/")
        dst = _abs_path(new_storage)
        dst.parent.mkdir(parents=True, exist_ok=True)

        try:
            shutil.copy2(str(src), str(dst))
        except OSError as exc:
            current_app.logger.error("copy_asset failed: %s", exc)
            return None, "Failed to copy file."

        copy = MediaAsset(
            filename=copy_name,
            original_filename=f"Copy of {asset.original_filename}",
            storage_path=new_storage,
            folder=asset.folder,
            media_type=asset.media_type,
            mime_type=asset.mime_type,
            file_size=dst.stat().st_size,
            title=f"Copy of {asset.title}",
            alt_text=asset.alt_text,
            caption=asset.caption,
            description=asset.description,
            tags=asset.tags,
            category=asset.category,
            seo_title=asset.seo_title,
            seo_description=asset.seo_description,
            width=asset.width,
            height=asset.height,
            uploaded_by_id=uploaded_by_id,
            is_active=True,
        )
        db.session.add(copy)
        return copy, None

    @staticmethod
    def replace_file(asset: MediaAsset, file: FileStorage) -> tuple[MediaAsset | None, str | None]:
        media_type, error = _validate_file(file, asset.folder)
        if error:
            return None, error

        abs_path = _abs_path(asset.storage_path)
        abs_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            file.save(abs_path)
        except OSError as exc:
            current_app.logger.error("replace_file failed: %s", exc)
            return None, "Failed to replace file."

        mime = file.mimetype or mimetypes.guess_type(file.filename)[0] or asset.mime_type
        asset.mime_type = mime
        asset.media_type = media_type or asset.media_type
        asset.file_size = abs_path.stat().st_size if abs_path.exists() else asset.file_size
        asset.original_filename = secure_filename(file.filename)
        return asset, None

    @staticmethod
    def soft_delete(asset: MediaAsset) -> None:
        asset.soft_delete()

    @staticmethod
    def scan_usage(storage_path: str) -> list[MediaUsageDTO]:
        """Scan CMS models for references to this storage path."""
        from app.models.catalog import GalleryImage, Project, Service, TeamMember, Testimonial
        from app.models.cms import AboutSection, HeroSlide, Page, Partner, WhyChooseUsSection
        from app.models.content_blocks import ContentBlock, ContentBlockItem
        from app.models.site import CompanyInfo

        usages: list[MediaUsageDTO] = []
        path = storage_path.replace("\\", "/")

        def add(location: str, label: str, resource_type: str, resource_id: str | int):
            usages.append(
                MediaUsageDTO(
                    location=location,
                    label=label,
                    resource_type=resource_type,
                    resource_id=resource_id,
                )
            )

        try:
            for slide in HeroSlide.query.filter(HeroSlide.image == path).limit(20).all():
                add("Home Hero", slide.title or "Hero Slide", "hero_slide", slide.id)
            for page in Page.query.filter(Page.banner_image == path).limit(20).all():
                add("Page Banner", page.title, "page", page.slug)
            for svc in Service.query.filter(Service.image == path).limit(20).all():
                add("Service", svc.title, "service", svc.slug)
            for proj in Project.query.filter(Project.cover_image == path).limit(20).all():
                add("Project", proj.title, "project", proj.slug)
            for img in GalleryImage.query.filter(GalleryImage.image == path).limit(20).all():
                add("Gallery", img.title, "gallery_image", img.id)
            for member in TeamMember.query.filter(TeamMember.photo == path).limit(20).all():
                add("Team", member.name, "team_member", member.id)
            for item in Testimonial.query.filter(Testimonial.photo == path).limit(20).all():
                add("Testimonial", item.client_name, "testimonial", item.id)
            for about in AboutSection.query.filter(AboutSection.image == path).limit(5).all():
                add("About Section", about.heading, "about_section", about.id)
            for partner in Partner.query.filter(Partner.logo == path).limit(20).all():
                add("Partner", partner.name, "partner", partner.id)
            for section in WhyChooseUsSection.query.filter(WhyChooseUsSection.image == path).limit(5).all():
                add("Why Choose Us", section.heading, "why_choose_us", section.id)
            for company in CompanyInfo.query.filter(CompanyInfo.logo_path == path).limit(1).all():
                add("Company Logo", company.name, "company_info", company.id)

            for block in ContentBlock.query.filter(
                or_(ContentBlock.hero_image == path, ContentBlock.og_image == path)
            ).limit(30).all():
                if block.hero_image == path:
                    add("Content Block Hero", block.title or block.block_key, "content_block", block.id)
                if block.og_image == path:
                    add("Content Block OG", block.title or block.block_key, "content_block", block.id)

            for block in ContentBlock.query.filter(ContentBlock.gallery_images.isnot(None)).limit(100).all():
                if not block.gallery_images:
                    continue
                images = block.gallery_images
                if isinstance(images, str):
                    try:
                        images = json.loads(images)
                    except json.JSONDecodeError:
                        continue
                if isinstance(images, list) and path in images:
                    add("Content Block Gallery", block.title or block.block_key, "content_block", block.id)

            for item in ContentBlockItem.query.filter(ContentBlockItem.image == path).limit(30).all():
                add("Block Item", item.title or "Item", "content_block_item", item.id)

        except SQLAlchemyError as exc:
            current_app.logger.error("scan_usage failed: %s", exc)

        return usages
