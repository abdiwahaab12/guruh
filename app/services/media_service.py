"""Enterprise Media Manager business logic."""

from __future__ import annotations

import math

from flask import url_for
from flask_login import current_user

from app.constants.media_library import (
    DEFAULT_PER_PAGE,
    MAX_PER_PAGE,
    MEDIA_FOLDERS,
    MEDIA_TYPES,
    SORT_OPTIONS,
)
from app.providers.admin_dashboard_provider import AdminDashboardProvider
from app.providers.media_provider import MediaProvider, _format_bytes
from app.schemas.admin import BreadcrumbItemDTO
from app.schemas.media_admin import (
    MediaAssetDTO,
    MediaLibraryPageDTO,
    MediaStatsDTO,
    MediaUploadResultDTO,
    SaveResultDTO,
)


class MediaService:
    """Centralized media library service."""

    @staticmethod
    def get_shell_context(
        *,
        page_title: str,
        active_section: str | None = None,
        breadcrumbs: list[BreadcrumbItemDTO] | None = None,
    ) -> dict:
        dashboard = AdminDashboardProvider.get_dashboard()
        return {
            "page_title": page_title,
            "active_nav": "media",
            "media_active_section": active_section,
            "media_folders": MEDIA_FOLDERS,
            "media_types": MEDIA_TYPES,
            "sort_options": SORT_OPTIONS,
            "breadcrumbs": breadcrumbs
            or MediaService.build_breadcrumbs(page_title),
            "notifications": dashboard.notifications,
            "unread_notification_count": dashboard.unread_notification_count,
            "user": current_user,
        }

    @staticmethod
    def build_breadcrumbs(current_label: str) -> list[BreadcrumbItemDTO]:
        return [
            BreadcrumbItemDTO("Admin", url_for("admin.dashboard"), False),
            BreadcrumbItemDTO("Media Library", url_for("admin.media_dashboard"), False),
            BreadcrumbItemDTO(current_label, None, True),
        ]

    @staticmethod
    def asset_dto(row, *, with_usage: bool = False) -> MediaAssetDTO:
        usage = MediaProvider.scan_usage(row.storage_path) if with_usage else []
        return MediaProvider.asset_to_dto(row, usage)

    @staticmethod
    def get_dashboard_context() -> dict:
        stats_raw = MediaProvider.get_stats()
        ctx = MediaService.get_shell_context(
            page_title="Media Library",
            active_section="dashboard",
            breadcrumbs=[
                BreadcrumbItemDTO("Admin", url_for("admin.dashboard"), False),
                BreadcrumbItemDTO("Media Library", None, True),
            ],
        )
        ctx["stats"] = MediaStatsDTO(
            total_files=stats_raw["total_files"],
            total_storage_bytes=stats_raw["total_storage"],
            total_storage_label=_format_bytes(stats_raw["total_storage"]),
            by_type=stats_raw["by_type"],
            by_folder=stats_raw["by_folder"],
            recent_uploads=[MediaService.asset_dto(r) for r in stats_raw["recent"]],
        )
        return ctx

    @staticmethod
    def get_library_context(
        *,
        q: str = "",
        folder: str = "",
        media_type: str = "",
        sort: str = "date_desc",
        view: str = "grid",
        page: int = 1,
        per_page: int = DEFAULT_PER_PAGE,
    ) -> dict:
        per_page = min(max(per_page, 12), MAX_PER_PAGE)
        page = max(page, 1)
        items, total = MediaProvider.query_library(
            q=q,
            folder=folder,
            media_type=media_type,
            sort=sort,
            page=page,
            per_page=per_page,
        )
        total_pages = max(1, math.ceil(total / per_page)) if total else 1
        page = min(page, total_pages)

        ctx = MediaService.get_shell_context(
            page_title="Media Library",
            active_section="library",
        )
        ctx["library"] = MediaLibraryPageDTO(
            items=[MediaService.asset_dto(r) for r in items],
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
            query=q,
            folder=folder,
            media_type=media_type,
            sort=sort,
            view=view if view in {"grid", "list"} else "grid",
        )
        return ctx

    @staticmethod
    def get_upload_context(folder: str = "general") -> dict:
        ctx = MediaService.get_shell_context(
            page_title="Upload Media",
            active_section="upload",
        )
        ctx["default_folder"] = folder if folder else "general"
        return ctx

    @staticmethod
    def get_detail_context(asset_id: int) -> dict | None:
        row = MediaProvider.get_asset(asset_id)
        if not row:
            return None
        ctx = MediaService.get_shell_context(
            page_title=row.title or row.original_filename,
            active_section="library",
        )
        ctx["asset"] = MediaService.asset_dto(row, with_usage=True)
        return ctx

    @staticmethod
    def get_edit_context(asset_id: int) -> dict | None:
        row = MediaProvider.get_asset(asset_id)
        if not row:
            return None
        ctx = MediaService.get_shell_context(
            page_title="Edit Media",
            active_section="library",
        )
        ctx["asset"] = MediaService.asset_dto(row, with_usage=True)
        return ctx

    @staticmethod
    def upload_files(
        files,
        *,
        folder: str,
        ip_address: str | None,
        title: str = "",
        alt_text: str = "",
    ) -> list[MediaUploadResultDTO]:
        results: list[MediaUploadResultDTO] = []
        user_id = current_user.id if current_user.is_authenticated else None

        for file in files:
            if not file or not file.filename:
                continue
            asset, error = MediaProvider.save_upload(
                file,
                folder=folder,
                uploaded_by_id=user_id,
                title=title,
                alt_text=alt_text,
            )
            if error:
                results.append(MediaUploadResultDTO(False, error))
                continue

            MediaProvider.record_audit(
                user_id=user_id,
                action="media.upload",
                resource_type="media_asset",
                resource_id=str(asset.id) if asset.id else None,
                details=f"Uploaded {asset.original_filename} to {folder}",
                ip_address=ip_address,
            )
            if MediaProvider.commit():
                dto = MediaService.asset_dto(asset)
                results.append(
                    MediaUploadResultDTO(True, "Upload successful.", asset=dto)
                )
            else:
                MediaProvider.rollback()
                results.append(MediaUploadResultDTO(False, "Database save failed."))

        return results

    @staticmethod
    def save_metadata(asset_id: int, data: dict, *, ip_address: str | None) -> SaveResultDTO:
        row = MediaProvider.get_asset(asset_id)
        if not row:
            return SaveResultDTO(False, "Media asset not found.")
        try:
            MediaProvider.update_metadata(row, data)
            MediaProvider.record_audit(
                user_id=current_user.id,
                action="media.update",
                resource_type="media_asset",
                resource_id=str(asset_id),
                details=f"Updated metadata for {row.title}",
                ip_address=ip_address,
            )
            if MediaProvider.commit():
                return SaveResultDTO(True, "Media metadata saved.")
            return SaveResultDTO(False, "Unable to save metadata.")
        except Exception as exc:
            MediaProvider.rollback()
            return SaveResultDTO(False, str(exc))

    @staticmethod
    def move_asset(asset_id: int, new_folder: str, *, ip_address: str | None) -> SaveResultDTO:
        row = MediaProvider.get_asset(asset_id)
        if not row:
            return SaveResultDTO(False, "Media asset not found.")
        updated, error = MediaProvider.move_asset(row, new_folder)
        if error:
            MediaProvider.rollback()
            return SaveResultDTO(False, error)
        MediaProvider.record_audit(
            user_id=current_user.id,
            action="media.move",
            resource_type="media_asset",
            resource_id=str(asset_id),
            details=f"Moved to folder {new_folder}",
            ip_address=ip_address,
        )
        if MediaProvider.commit():
            return SaveResultDTO(True, f"Moved to {_folder_label(new_folder)}.")
        MediaProvider.rollback()
        return SaveResultDTO(False, "Move failed.")

    @staticmethod
    def copy_asset(asset_id: int, *, ip_address: str | None) -> SaveResultDTO:
        row = MediaProvider.get_asset(asset_id)
        if not row:
            return SaveResultDTO(False, "Media asset not found.")
        copy, error = MediaProvider.copy_asset(row, current_user.id)
        if error:
            MediaProvider.rollback()
            return SaveResultDTO(False, error)
        MediaProvider.record_audit(
            user_id=current_user.id,
            action="media.copy",
            resource_type="media_asset",
            resource_id=str(copy.id) if copy and copy.id else str(asset_id),
            details=f"Copied {row.title}",
            ip_address=ip_address,
        )
        if MediaProvider.commit():
            return SaveResultDTO(True, "Media file copied.")
        MediaProvider.rollback()
        return SaveResultDTO(False, "Copy failed.")

    @staticmethod
    def replace_asset(asset_id: int, file, *, ip_address: str | None) -> SaveResultDTO:
        row = MediaProvider.get_asset(asset_id)
        if not row:
            return SaveResultDTO(False, "Media asset not found.")
        updated, error = MediaProvider.replace_file(row, file)
        if error:
            MediaProvider.rollback()
            return SaveResultDTO(False, error)
        MediaProvider.record_audit(
            user_id=current_user.id,
            action="media.replace",
            resource_type="media_asset",
            resource_id=str(asset_id),
            details=f"Replaced file {row.original_filename}",
            ip_address=ip_address,
        )
        if MediaProvider.commit():
            return SaveResultDTO(True, "File replaced successfully.")
        MediaProvider.rollback()
        return SaveResultDTO(False, "Replace failed.")

    @staticmethod
    def delete_asset(asset_id: int, *, ip_address: str | None) -> SaveResultDTO:
        row = MediaProvider.get_asset(asset_id)
        if not row:
            return SaveResultDTO(False, "Media asset not found.")
        MediaProvider.soft_delete(row)
        MediaProvider.record_audit(
            user_id=current_user.id,
            action="media.delete",
            resource_type="media_asset",
            resource_id=str(asset_id),
            details=f"Soft-deleted {row.title}",
            ip_address=ip_address,
        )
        if MediaProvider.commit():
            return SaveResultDTO(True, "Media moved to trash (restore coming in a future step).")
        MediaProvider.rollback()
        return SaveResultDTO(False, "Delete failed.")

    @staticmethod
    def rename_asset(asset_id: int, title: str, original_filename: str, *, ip_address: str | None) -> SaveResultDTO:
        return MediaService.save_metadata(
            asset_id,
            {"title": title, "original_filename": original_filename},
            ip_address=ip_address,
        )


def _folder_label(slug: str) -> str:
    for item in MEDIA_FOLDERS:
        if item["slug"] == slug:
            return item["label"]
    return slug
