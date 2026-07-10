"""Services admin business logic."""

from __future__ import annotations

import math

from flask import url_for
from flask_login import current_user

from app.constants.services_admin import DEFAULT_PER_PAGE, MAX_PER_PAGE
from app.providers.admin_dashboard_provider import AdminDashboardProvider
from app.providers.services_admin_provider import ServicesAdminProvider
from app.schemas.admin import BreadcrumbItemDTO
from app.schemas.services_admin import (
    SaveResultDTO,
    ServiceAdminDTO,
    ServiceListPageDTO,
    ServiceStatsDTO,
)


class ServicesAdminService:
    """Enterprise services management service."""

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
            "active_nav": "services",
            "services_active_section": active_section,
            "breadcrumbs": breadcrumbs
            or ServicesAdminService.build_breadcrumbs(page_title),
            "notifications": dashboard.notifications,
            "unread_notification_count": dashboard.unread_notification_count,
            "user": current_user,
        }

    @staticmethod
    def build_breadcrumbs(current_label: str) -> list[BreadcrumbItemDTO]:
        return [
            BreadcrumbItemDTO("Admin", url_for("admin.dashboard"), False),
            BreadcrumbItemDTO("Services", url_for("admin.services_dashboard"), False),
            BreadcrumbItemDTO(current_label, None, True),
        ]

    @staticmethod
    def get_dashboard_context() -> dict:
        stats_raw = ServicesAdminProvider.get_stats()
        ctx = ServicesAdminService.get_shell_context(
            page_title="Services",
            active_section="dashboard",
            breadcrumbs=[
                BreadcrumbItemDTO("Admin", url_for("admin.dashboard"), False),
                BreadcrumbItemDTO("Services", None, True),
            ],
        )
        ctx["stats"] = ServiceStatsDTO(
            total=stats_raw["total"],
            active=stats_raw["active"],
            inactive=stats_raw["inactive"],
            featured=stats_raw["featured"],
            recent=[ServicesAdminProvider.to_list_item(s) for s in stats_raw["recent"]],
        )
        return ctx

    @staticmethod
    def get_list_context(
        *,
        q: str = "",
        featured: str = "",
        status: str = "",
        sort: str = "date_desc",
        page: int = 1,
        per_page: int = DEFAULT_PER_PAGE,
        include_deleted: bool = False,
    ) -> dict:
        per_page = min(max(per_page, 10), MAX_PER_PAGE)
        page = max(page, 1)
        items, total = ServicesAdminProvider.query_services(
            q=q,
            featured=featured,
            status=status,
            sort=sort,
            page=page,
            per_page=per_page,
            include_deleted=include_deleted,
        )
        total_pages = max(1, math.ceil(total / per_page)) if total else 1
        page = min(page, total_pages)

        ctx = ServicesAdminService.get_shell_context(
            page_title="All Services",
            active_section="list",
        )
        ctx["list_page"] = ServiceListPageDTO(
            items=[ServicesAdminProvider.to_list_item(s) for s in items],
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
            query=q,
            filters={"featured": featured, "status": status},
            sort=sort,
            include_deleted=include_deleted,
        )
        from app.constants.services_admin import (
            BULK_ACTIONS,
            FEATURED_FILTER_OPTIONS,
            SORT_OPTIONS,
            STATUS_FILTER_OPTIONS,
        )

        ctx.update(
            {
                "bulk_actions": BULK_ACTIONS,
                "sort_options": SORT_OPTIONS,
                "featured_filter_options": FEATURED_FILTER_OPTIONS,
                "status_filter_options": STATUS_FILTER_OPTIONS,
            }
        )
        return ctx

    @staticmethod
    def get_form_context(service_id: int | None = None, active_tab: str = "general") -> dict:
        if service_id:
            service = ServicesAdminProvider.get_service(service_id, include_inactive=True)
            if not service:
                return {}
            dto = ServicesAdminProvider.to_admin_dto(service)
            title = f"Edit — {dto.title}"
            is_edit = True
        else:
            dto = ServiceAdminDTO(
                id=None,
                title="",
                slug="",
                short_description="",
                description="",
                icon="bi-grid",
                image="",
                sort_order=0,
                is_featured=False,
                is_active=True,
            )
            title = "Create Service"
            is_edit = False

        ctx = ServicesAdminService.get_shell_context(page_title=title, active_section="form")
        ctx["service"] = dto
        ctx["is_edit"] = is_edit
        ctx["active_tab"] = active_tab
        ctx["projects"] = ServicesAdminProvider.list_projects()
        ctx["related_services"] = ServicesAdminProvider.list_services_for_related(service_id)
        ctx["team_members"] = ServicesAdminProvider.list_team()
        ctx["media_assets"] = ServicesAdminProvider.list_media_assets("services")

        from app.constants.services_admin import SERVICE_FORM_TABS, SERVICE_ICONS

        ctx.update(
            {
                "form_tabs": SERVICE_FORM_TABS,
                "service_icons": SERVICE_ICONS,
            }
        )
        return ctx

    @staticmethod
    def dto_from_form(
        form,
        *,
        gallery_paths: list[str] | None = None,
    ) -> ServiceAdminDTO:
        return ServiceAdminDTO(
            id=form.service_id.data or None,
            title=form.title.data,
            slug=form.slug.data or "",
            short_description=form.short_description.data,
            description=form.description.data,
            icon=form.icon.data or "",
            image=form.image.data or "",
            sort_order=int(form.sort_order.data or 0),
            is_featured=form.is_featured.data,
            is_active=form.is_active.data if form.service_id.data else True,
            meta_title=form.meta_title.data or "",
            meta_description=form.meta_description.data or "",
            og_image=form.og_image.data or "",
            canonical_url=form.canonical_url.data or "",
            scope_of_work=ServicesAdminProvider.lines_to_list(form.scope_of_work.data),
            benefits=ServicesAdminProvider.lines_to_list(form.benefits.data),
            equipment=ServicesAdminProvider.lines_to_list(form.equipment.data),
            related_project_ids=[int(x) for x in (form.related_project_ids.data or [])],
            related_service_slugs=form.related_service_slugs.data or [],
            team_member_ids=[int(x) for x in (form.team_member_ids.data or [])],
            gallery_paths=gallery_paths or [],
        )

    @staticmethod
    def save_service(dto: ServiceAdminDTO, *, ip_address: str | None) -> SaveResultDTO:
        try:
            is_new = not dto.id
            service = ServicesAdminProvider.save_from_dto(dto)
            action = "services.create" if is_new else "services.update"
            ServicesAdminProvider.record_audit(
                user_id=current_user.id,
                action=action,
                resource_type="service",
                resource_id=str(service.id),
                details=f"{'Created' if is_new else 'Updated'} service: {service.title}",
                ip_address=ip_address,
            )
            if ServicesAdminProvider.commit():
                return SaveResultDTO(True, "Service saved successfully.", service.id)
            return SaveResultDTO(False, "Unable to save service.")
        except ValueError as exc:
            ServicesAdminProvider.rollback()
            return SaveResultDTO(False, str(exc))
        except Exception as exc:
            ServicesAdminProvider.rollback()
            return SaveResultDTO(False, f"Save failed: {exc}")

    @staticmethod
    def delete_service(service_id: int, *, ip_address: str | None) -> SaveResultDTO:
        service = ServicesAdminProvider.get_service(service_id, include_inactive=True)
        if not service:
            return SaveResultDTO(False, "Service not found.")
        ServicesAdminProvider.soft_delete(service)
        ServicesAdminProvider.record_audit(
            user_id=current_user.id,
            action="services.delete",
            resource_type="service",
            resource_id=str(service_id),
            details=f"Soft-deleted service: {service.title}",
            ip_address=ip_address,
        )
        if ServicesAdminProvider.commit():
            return SaveResultDTO(True, "Service moved to trash.")
        ServicesAdminProvider.rollback()
        return SaveResultDTO(False, "Delete failed.")

    @staticmethod
    def restore_service(service_id: int, *, ip_address: str | None) -> SaveResultDTO:
        service = ServicesAdminProvider.get_service(service_id, include_inactive=True)
        if not service:
            return SaveResultDTO(False, "Service not found.")
        ServicesAdminProvider.restore(service)
        ServicesAdminProvider.record_audit(
            user_id=current_user.id,
            action="services.restore",
            resource_type="service",
            resource_id=str(service_id),
            details=f"Restored service: {service.title}",
            ip_address=ip_address,
        )
        if ServicesAdminProvider.commit():
            return SaveResultDTO(True, "Service restored.")
        ServicesAdminProvider.rollback()
        return SaveResultDTO(False, "Restore failed.")

    @staticmethod
    def bulk_action(service_ids: list[int], action: str, *, ip_address: str | None) -> SaveResultDTO:
        if not service_ids:
            return SaveResultDTO(False, "No services selected.")
        count = ServicesAdminProvider.bulk_update(service_ids, action)
        ServicesAdminProvider.record_audit(
            user_id=current_user.id,
            action=f"services.bulk_{action}",
            resource_type="service",
            resource_id=",".join(str(i) for i in service_ids[:10]),
            details=f"Bulk {action} on {count} service(s)",
            ip_address=ip_address,
        )
        if ServicesAdminProvider.commit():
            return SaveResultDTO(True, f"Bulk action applied to {count} service(s).")
        ServicesAdminProvider.rollback()
        return SaveResultDTO(False, "Bulk action failed.")
