"""Gallery admin business logic."""

from __future__ import annotations

import math

from flask import url_for
from flask_login import current_user

from app.constants.gallery_admin import DEFAULT_PER_PAGE, MAX_PER_PAGE
from app.providers.admin_dashboard_provider import AdminDashboardProvider
from app.providers.gallery_admin_provider import GalleryAdminProvider
from app.schemas.admin import BreadcrumbItemDTO
from app.schemas.gallery_admin import GalleryAdminDTO, GalleryListPageDTO, GalleryStatsDTO, SaveResultDTO


class GalleryAdminService:
    """Enterprise gallery management service."""

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
            "active_nav": "gallery",
            "gallery_active_section": active_section,
            "breadcrumbs": breadcrumbs
            or GalleryAdminService.build_breadcrumbs(page_title),
            "notifications": dashboard.notifications,
            "unread_notification_count": dashboard.unread_notification_count,
            "user": current_user,
        }

    @staticmethod
    def build_breadcrumbs(current_label: str) -> list[BreadcrumbItemDTO]:
        return [
            BreadcrumbItemDTO("Admin", url_for("admin.dashboard"), False),
            BreadcrumbItemDTO("Gallery", url_for("admin.gallery_dashboard"), False),
            BreadcrumbItemDTO(current_label, None, True),
        ]

    @staticmethod
    def get_dashboard_context() -> dict:
        stats_raw = GalleryAdminProvider.get_stats()
        ctx = GalleryAdminService.get_shell_context(
            page_title="Gallery",
            active_section="dashboard",
            breadcrumbs=[
                BreadcrumbItemDTO("Admin", url_for("admin.dashboard"), False),
                BreadcrumbItemDTO("Gallery", None, True),
            ],
        )
        ctx["stats"] = GalleryStatsDTO(
            total=stats_raw["total"],
            albums=stats_raw["albums"],
            images=stats_raw["images"],
            videos=stats_raw["videos"],
            featured=stats_raw["featured"],
            active=stats_raw["active"],
            inactive=stats_raw["inactive"],
            recent=[GalleryAdminProvider.to_list_item(i) for i in stats_raw["recent"]],
        )
        return ctx

    @staticmethod
    def get_list_context(
        *,
        q: str = "",
        album: str = "",
        category: str = "",
        project_id: int | None = None,
        service: str = "",
        country: str = "",
        featured: str = "",
        status: str = "",
        sort: str = "date_desc",
        page: int = 1,
        per_page: int = DEFAULT_PER_PAGE,
        include_deleted: bool = False,
    ) -> dict:
        per_page = min(max(per_page, 12), MAX_PER_PAGE)
        page = max(page, 1)
        items, total = GalleryAdminProvider.query_gallery(
            q=q,
            album=album,
            category=category,
            project_id=project_id,
            service=service,
            country=country,
            featured=featured,
            status=status,
            sort=sort,
            page=page,
            per_page=per_page,
            include_deleted=include_deleted,
        )
        total_pages = max(1, math.ceil(total / per_page)) if total else 1
        page = min(page, total_pages)

        ctx = GalleryAdminService.get_shell_context(
            page_title="All Gallery Items",
            active_section="list",
        )
        ctx["list_page"] = GalleryListPageDTO(
            items=[GalleryAdminProvider.to_list_item(i) for i in items],
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
            query=q,
            filters={
                "album": album,
                "category": category,
                "project_id": str(project_id or ""),
                "service": service,
                "country": country,
                "featured": featured,
                "status": status,
            },
            sort=sort,
            include_deleted=include_deleted,
        )
        from app.constants.gallery_admin import (
            BULK_ACTIONS,
            FEATURED_FILTER_OPTIONS,
            GALLERY_ALBUMS,
            GALLERY_CATEGORIES,
            GALLERY_COUNTRIES,
            SORT_OPTIONS,
            STATUS_FILTER_OPTIONS,
        )

        ctx.update(
            {
                "bulk_actions": BULK_ACTIONS,
                "sort_options": SORT_OPTIONS,
                "featured_filter_options": FEATURED_FILTER_OPTIONS,
                "status_filter_options": STATUS_FILTER_OPTIONS,
                "filter_albums": GALLERY_ALBUMS,
                "filter_categories": GALLERY_CATEGORIES,
                "filter_countries": GALLERY_COUNTRIES,
                "filter_projects": GalleryAdminProvider.list_projects(),
                "filter_services": GalleryAdminProvider.list_services(),
            }
        )
        return ctx

    @staticmethod
    def get_form_context(item_id: int | None = None, active_tab: str = "general") -> dict:
        from app.constants.gallery_admin import (
            GALLERY_ALBUMS,
            GALLERY_CATEGORIES,
            GALLERY_COUNTIES,
            GALLERY_COUNTRIES,
            GALLERY_FORM_TABS,
            GALLERY_YEARS,
            MEDIA_TYPES,
            VIDEO_PROVIDERS,
        )

        if item_id:
            item = GalleryAdminProvider.get_item(item_id, include_inactive=True)
            if not item:
                return {}
            dto = GalleryAdminProvider.to_admin_dto(item)
            title = f"Edit — {dto.title}"
            is_edit = True
        else:
            dto = GalleryAdminDTO(
                id=None,
                title="",
                slug="",
                image="",
                category=GALLERY_CATEGORIES[0] if GALLERY_CATEGORIES else "",
                project_id=None,
                sort_order=0,
                is_active=True,
            )
            title = "Create Gallery Item"
            is_edit = False

        ctx = GalleryAdminService.get_shell_context(page_title=title, active_section="form")
        ctx["gallery_item"] = dto
        ctx["is_edit"] = is_edit
        ctx["active_tab"] = active_tab
        ctx["projects"] = GalleryAdminProvider.list_projects()
        ctx["services"] = GalleryAdminProvider.list_services()
        ctx["equipment_list"] = GalleryAdminProvider.list_equipment()
        ctx["team_members"] = GalleryAdminProvider.list_team()
        ctx["media_assets"] = GalleryAdminProvider.list_media_assets("gallery")
        ctx["video_media_assets"] = GalleryAdminProvider.list_media_assets("general")
        ctx.update(
            {
                "form_tabs": GALLERY_FORM_TABS,
                "categories": GALLERY_CATEGORIES,
                "albums": GALLERY_ALBUMS,
                "countries": GALLERY_COUNTRIES,
                "counties": GALLERY_COUNTIES,
                "years": GALLERY_YEARS,
                "media_types": MEDIA_TYPES,
                "video_providers": VIDEO_PROVIDERS,
            }
        )
        return ctx

    @staticmethod
    def dto_from_form(form) -> GalleryAdminDTO:
        project_id = form.project_id.data
        return GalleryAdminDTO(
            id=form.gallery_item_id.data or None,
            title=form.title.data,
            slug=form.slug.data or "",
            image=form.image.data or "",
            category=form.category.data or "",
            project_id=int(project_id) if project_id else None,
            sort_order=int(form.sort_order.data or 0),
            is_active=form.is_active.data if form.gallery_item_id.data else True,
            media_type=form.media_type.data or "image",
            album=form.album.data or "",
            caption=form.caption.data or "",
            location=form.location.data or "",
            county=form.county.data or "",
            country=form.country.data or "Somalia",
            media_date=form.media_date.data or "",
            year=form.year.data or "",
            is_featured=form.is_featured.data,
            meta_title=form.meta_title.data or "",
            meta_description=form.meta_description.data or "",
            og_image=form.og_image.data or "",
            canonical_url=form.canonical_url.data or "",
            service_slug=form.service_slug.data or "",
            equipment_slug=form.equipment_slug.data or "",
            team_member_ids=[int(x) for x in (form.team_member_ids.data or [])],
            video_provider=form.video_provider.data or "",
            video_id=form.video_id.data or "",
            embed_url=form.embed_url.data or "",
        )

    @staticmethod
    def save_item(dto: GalleryAdminDTO, *, ip_address: str | None) -> SaveResultDTO:
        try:
            is_new = not dto.id
            item = GalleryAdminProvider.save_from_dto(dto)
            action = "gallery.create" if is_new else "gallery.update"
            GalleryAdminProvider.record_audit(
                user_id=current_user.id,
                action=action,
                resource_type="gallery",
                resource_id=str(item.id),
                details=f"{'Created' if is_new else 'Updated'} gallery item: {item.title}",
                ip_address=ip_address,
            )
            if GalleryAdminProvider.commit():
                return SaveResultDTO(True, "Gallery item saved successfully.", item.id)
            return SaveResultDTO(False, "Unable to save gallery item.")
        except ValueError as exc:
            GalleryAdminProvider.rollback()
            return SaveResultDTO(False, str(exc))
        except Exception as exc:
            GalleryAdminProvider.rollback()
            return SaveResultDTO(False, f"Save failed: {exc}")

    @staticmethod
    def delete_item(item_id: int, *, ip_address: str | None) -> SaveResultDTO:
        item = GalleryAdminProvider.get_item(item_id, include_inactive=True)
        if not item:
            return SaveResultDTO(False, "Gallery item not found.")
        GalleryAdminProvider.soft_delete(item)
        GalleryAdminProvider.record_audit(
            user_id=current_user.id,
            action="gallery.delete",
            resource_type="gallery",
            resource_id=str(item_id),
            details=f"Soft-deleted gallery item: {item.title}",
            ip_address=ip_address,
        )
        if GalleryAdminProvider.commit():
            return SaveResultDTO(True, "Gallery item moved to trash.")
        GalleryAdminProvider.rollback()
        return SaveResultDTO(False, "Delete failed.")

    @staticmethod
    def restore_item(item_id: int, *, ip_address: str | None) -> SaveResultDTO:
        item = GalleryAdminProvider.get_item(item_id, include_inactive=True)
        if not item:
            return SaveResultDTO(False, "Gallery item not found.")
        GalleryAdminProvider.restore(item)
        GalleryAdminProvider.record_audit(
            user_id=current_user.id,
            action="gallery.restore",
            resource_type="gallery",
            resource_id=str(item_id),
            details=f"Restored gallery item: {item.title}",
            ip_address=ip_address,
        )
        if GalleryAdminProvider.commit():
            return SaveResultDTO(True, "Gallery item restored.")
        GalleryAdminProvider.rollback()
        return SaveResultDTO(False, "Restore failed.")

    @staticmethod
    def bulk_action(item_ids: list[int], action: str, *, ip_address: str | None) -> SaveResultDTO:
        if not item_ids:
            return SaveResultDTO(False, "No gallery items selected.")
        count = GalleryAdminProvider.bulk_update(item_ids, action)
        GalleryAdminProvider.record_audit(
            user_id=current_user.id,
            action=f"gallery.bulk_{action}",
            resource_type="gallery",
            resource_id=",".join(str(i) for i in item_ids[:10]),
            details=f"Bulk {action} on {count} gallery item(s)",
            ip_address=ip_address,
        )
        if GalleryAdminProvider.commit():
            return SaveResultDTO(True, f"Bulk action applied to {count} gallery item(s).")
        GalleryAdminProvider.rollback()
        return SaveResultDTO(False, "Bulk action failed.")
