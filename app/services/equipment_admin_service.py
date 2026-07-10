"""Equipment admin business logic."""

from __future__ import annotations

import math

from flask import url_for
from flask_login import current_user

from app.constants.equipment_admin import DEFAULT_PER_PAGE, MAX_PER_PAGE
from app.providers.admin_dashboard_provider import AdminDashboardProvider
from app.providers.equipment_admin_provider import EquipmentAdminProvider
from app.schemas.admin import BreadcrumbItemDTO
from app.schemas.equipment_admin import (
    EquipmentAdminDTO,
    EquipmentListPageDTO,
    EquipmentStatsDTO,
    SaveResultDTO,
)


class EquipmentAdminService:
    """Enterprise equipment management service."""

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
            "active_nav": "equipment",
            "equipment_active_section": active_section,
            "breadcrumbs": breadcrumbs
            or EquipmentAdminService.build_breadcrumbs(page_title),
            "notifications": dashboard.notifications,
            "unread_notification_count": dashboard.unread_notification_count,
            "user": current_user,
        }

    @staticmethod
    def build_breadcrumbs(current_label: str) -> list[BreadcrumbItemDTO]:
        return [
            BreadcrumbItemDTO("Admin", url_for("admin.dashboard"), False),
            BreadcrumbItemDTO("Equipment", url_for("admin.equipment_dashboard"), False),
            BreadcrumbItemDTO(current_label, None, True),
        ]

    @staticmethod
    def get_dashboard_context() -> dict:
        stats_raw = EquipmentAdminProvider.get_stats()
        ctx = EquipmentAdminService.get_shell_context(
            page_title="Equipment",
            active_section="dashboard",
            breadcrumbs=[
                BreadcrumbItemDTO("Admin", url_for("admin.dashboard"), False),
                BreadcrumbItemDTO("Equipment", None, True),
            ],
        )
        ctx["stats"] = EquipmentStatsDTO(
            total=stats_raw["total"],
            active=stats_raw["active"],
            inactive=stats_raw["inactive"],
            featured=stats_raw["featured"],
            recent=[EquipmentAdminProvider.to_list_item(e) for e in stats_raw["recent"]],
        )
        return ctx

    @staticmethod
    def get_list_context(
        *,
        q: str = "",
        category: str = "",
        featured: str = "",
        status: str = "",
        sort: str = "date_desc",
        page: int = 1,
        per_page: int = DEFAULT_PER_PAGE,
        include_deleted: bool = False,
    ) -> dict:
        per_page = min(max(per_page, 10), MAX_PER_PAGE)
        page = max(page, 1)
        items, total = EquipmentAdminProvider.query_equipment(
            q=q,
            category=category,
            featured=featured,
            status=status,
            sort=sort,
            page=page,
            per_page=per_page,
            include_deleted=include_deleted,
        )
        total_pages = max(1, math.ceil(total / per_page)) if total else 1
        page = min(page, total_pages)

        ctx = EquipmentAdminService.get_shell_context(
            page_title="All Equipment",
            active_section="list",
        )
        ctx["list_page"] = EquipmentListPageDTO(
            items=[EquipmentAdminProvider.to_list_item(e) for e in items],
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
            query=q,
            filters={"category": category, "featured": featured, "status": status},
            sort=sort,
            include_deleted=include_deleted,
        )
        from app.constants.equipment_admin import (
            BULK_ACTIONS,
            EQUIPMENT_CATEGORY_TITLES,
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
                "filter_categories": EQUIPMENT_CATEGORY_TITLES,
            }
        )
        return ctx

    @staticmethod
    def get_form_context(equipment_id: int | None = None, active_tab: str = "general") -> dict:
        from app.constants.equipment_admin import (
            CONDITION_OPTIONS,
            EQUIPMENT_CATEGORY_TITLES,
            EQUIPMENT_FORM_TABS,
        )

        if equipment_id:
            row = EquipmentAdminProvider.get_equipment(equipment_id, include_inactive=True)
            if not row:
                return {}
            dto = EquipmentAdminProvider.to_admin_dto(row)
            title = f"Edit — {dto.name}"
            is_edit = True
        else:
            dto = EquipmentAdminDTO(
                id=None,
                name="",
                slug="",
                category=EQUIPMENT_CATEGORY_TITLES[0] if EQUIPMENT_CATEGORY_TITLES else "",
                short_description="",
                description="",
                image="",
                capacity="",
                condition="Operational",
                maintenance_status="",
                usage="",
                sort_order=0,
                is_featured=False,
                is_active=True,
            )
            title = "Create Equipment"
            is_edit = False

        ctx = EquipmentAdminService.get_shell_context(page_title=title, active_section="form")
        ctx["equipment"] = dto
        ctx["is_edit"] = is_edit
        ctx["active_tab"] = active_tab
        ctx["projects"] = EquipmentAdminProvider.list_projects()
        ctx["services"] = EquipmentAdminProvider.list_services()
        ctx["team_members"] = EquipmentAdminProvider.list_team()
        ctx["media_assets"] = EquipmentAdminProvider.list_media_assets("equipment")

        ctx.update(
            {
                "form_tabs": EQUIPMENT_FORM_TABS,
                "categories": EQUIPMENT_CATEGORY_TITLES,
                "condition_options": CONDITION_OPTIONS,
                "specifications_text": EquipmentAdminProvider.specs_to_text(dto.specifications),
            }
        )
        return ctx

    @staticmethod
    def dto_from_form(
        form,
        *,
        gallery_paths: list[str] | None = None,
    ) -> EquipmentAdminDTO:
        return EquipmentAdminDTO(
            id=form.equipment_id.data or None,
            name=form.name.data,
            slug=form.slug.data or "",
            category=form.category.data,
            short_description=form.short_description.data,
            description=form.description.data,
            image=form.image.data or "",
            capacity=form.capacity.data or "",
            condition=form.condition.data or "Operational",
            maintenance_status=form.maintenance_status.data or "",
            usage=form.usage.data or "",
            sort_order=int(form.sort_order.data or 0),
            is_featured=form.is_featured.data,
            is_active=form.is_active.data if form.equipment_id.data else True,
            meta_title=form.meta_title.data or "",
            meta_description=form.meta_description.data or "",
            og_image=form.og_image.data or "",
            canonical_url=form.canonical_url.data or "",
            specifications=EquipmentAdminProvider.parse_specs_text(form.specifications.data or ""),
            related_project_ids=[int(x) for x in (form.related_project_ids.data or [])],
            related_service_slugs=form.related_service_slugs.data or [],
            team_member_ids=[int(x) for x in (form.team_member_ids.data or [])],
            gallery_paths=gallery_paths or [],
        )

    @staticmethod
    def save_equipment(dto: EquipmentAdminDTO, *, ip_address: str | None) -> SaveResultDTO:
        try:
            is_new = not dto.id
            row = EquipmentAdminProvider.save_from_dto(dto)
            action = "equipment.create" if is_new else "equipment.update"
            EquipmentAdminProvider.record_audit(
                user_id=current_user.id,
                action=action,
                resource_type="equipment",
                resource_id=str(row.id),
                details=f"{'Created' if is_new else 'Updated'} equipment: {row.name}",
                ip_address=ip_address,
            )
            if EquipmentAdminProvider.commit():
                return SaveResultDTO(True, "Equipment saved successfully.", row.id)
            return SaveResultDTO(False, "Unable to save equipment.")
        except ValueError as exc:
            EquipmentAdminProvider.rollback()
            return SaveResultDTO(False, str(exc))
        except Exception as exc:
            EquipmentAdminProvider.rollback()
            return SaveResultDTO(False, f"Save failed: {exc}")

    @staticmethod
    def delete_equipment(equipment_id: int, *, ip_address: str | None) -> SaveResultDTO:
        row = EquipmentAdminProvider.get_equipment(equipment_id, include_inactive=True)
        if not row:
            return SaveResultDTO(False, "Equipment not found.")
        EquipmentAdminProvider.soft_delete(row)
        EquipmentAdminProvider.record_audit(
            user_id=current_user.id,
            action="equipment.delete",
            resource_type="equipment",
            resource_id=str(equipment_id),
            details=f"Soft-deleted equipment: {row.name}",
            ip_address=ip_address,
        )
        if EquipmentAdminProvider.commit():
            return SaveResultDTO(True, "Equipment moved to trash.")
        EquipmentAdminProvider.rollback()
        return SaveResultDTO(False, "Delete failed.")

    @staticmethod
    def restore_equipment(equipment_id: int, *, ip_address: str | None) -> SaveResultDTO:
        row = EquipmentAdminProvider.get_equipment(equipment_id, include_inactive=True)
        if not row:
            return SaveResultDTO(False, "Equipment not found.")
        EquipmentAdminProvider.restore(row)
        EquipmentAdminProvider.record_audit(
            user_id=current_user.id,
            action="equipment.restore",
            resource_type="equipment",
            resource_id=str(equipment_id),
            details=f"Restored equipment: {row.name}",
            ip_address=ip_address,
        )
        if EquipmentAdminProvider.commit():
            return SaveResultDTO(True, "Equipment restored.")
        EquipmentAdminProvider.rollback()
        return SaveResultDTO(False, "Restore failed.")

    @staticmethod
    def bulk_action(equipment_ids: list[int], action: str, *, ip_address: str | None) -> SaveResultDTO:
        if not equipment_ids:
            return SaveResultDTO(False, "No equipment selected.")
        count = EquipmentAdminProvider.bulk_update(equipment_ids, action)
        EquipmentAdminProvider.record_audit(
            user_id=current_user.id,
            action=f"equipment.bulk_{action}",
            resource_type="equipment",
            resource_id=",".join(str(i) for i in equipment_ids[:10]),
            details=f"Bulk {action} on {count} equipment item(s)",
            ip_address=ip_address,
        )
        if EquipmentAdminProvider.commit():
            return SaveResultDTO(True, f"Bulk action applied to {count} equipment item(s).")
        EquipmentAdminProvider.rollback()
        return SaveResultDTO(False, "Bulk action failed.")
