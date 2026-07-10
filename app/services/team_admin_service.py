"""Team admin business logic."""

from __future__ import annotations

import math

from flask import url_for
from flask_login import current_user

from app.constants.team_admin import DEFAULT_PER_PAGE, MAX_PER_PAGE, MEMBER_TYPES
from app.providers.admin_dashboard_provider import AdminDashboardProvider
from app.providers.team_admin_provider import TeamAdminProvider
from app.schemas.admin import BreadcrumbItemDTO
from app.schemas.team_admin import SaveResultDTO, TeamAdminDTO, TeamListPageDTO, TeamStatsDTO


class TeamAdminService:
    """Enterprise team management service."""

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
            "active_nav": "team",
            "team_active_section": active_section,
            "breadcrumbs": breadcrumbs or TeamAdminService.build_breadcrumbs(page_title),
            "notifications": dashboard.notifications,
            "unread_notification_count": dashboard.unread_notification_count,
            "user": current_user,
        }

    @staticmethod
    def build_breadcrumbs(current_label: str) -> list[BreadcrumbItemDTO]:
        return [
            BreadcrumbItemDTO("Admin", url_for("admin.dashboard"), False),
            BreadcrumbItemDTO("Team", url_for("admin.team_dashboard"), False),
            BreadcrumbItemDTO(current_label, None, True),
        ]

    @staticmethod
    def get_dashboard_context() -> dict:
        stats_raw = TeamAdminProvider.get_stats()
        ctx = TeamAdminService.get_shell_context(
            page_title="Team",
            active_section="dashboard",
            breadcrumbs=[
                BreadcrumbItemDTO("Admin", url_for("admin.dashboard"), False),
                BreadcrumbItemDTO("Team", None, True),
            ],
        )
        ctx["stats"] = TeamStatsDTO(
            total=stats_raw["total"],
            active=stats_raw["active"],
            inactive=stats_raw["inactive"],
            directors=stats_raw["directors"],
            management=stats_raw["management"],
            staff=stats_raw["staff"],
            recent=[TeamAdminProvider.to_list_item(m) for m in stats_raw["recent"]],
        )
        ctx["member_type_labels"] = dict(MEMBER_TYPES)
        return ctx

    @staticmethod
    def get_list_context(
        *,
        q: str = "",
        department: str = "",
        position: str = "",
        member_type: str = "",
        featured: str = "",
        status: str = "",
        sort: str = "date_desc",
        page: int = 1,
        per_page: int = DEFAULT_PER_PAGE,
        include_deleted: bool = False,
    ) -> dict:
        per_page = min(max(per_page, 10), MAX_PER_PAGE)
        page = max(page, 1)
        items, total = TeamAdminProvider.query_members(
            q=q,
            department=department,
            position=position,
            member_type=member_type,
            featured=featured,
            status=status,
            sort=sort,
            page=page,
            per_page=per_page,
            include_deleted=include_deleted,
        )
        total_pages = max(1, math.ceil(total / per_page)) if total else 1
        page = min(page, total_pages)

        ctx = TeamAdminService.get_shell_context(
            page_title="All Team Members",
            active_section="list",
        )
        ctx["list_page"] = TeamListPageDTO(
            items=[TeamAdminProvider.to_list_item(m) for m in items],
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
            query=q,
            filters={
                "department": department,
                "position": position,
                "member_type": member_type,
                "featured": featured,
                "status": status,
            },
            sort=sort,
            include_deleted=include_deleted,
        )
        from app.constants.team_admin import (
            BULK_ACTIONS,
            FEATURED_FILTER_OPTIONS,
            SORT_OPTIONS,
            STATUS_FILTER_OPTIONS,
            TEAM_DEPARTMENTS,
            TEAM_POSITIONS,
        )

        ctx.update(
            {
                "bulk_actions": BULK_ACTIONS,
                "sort_options": SORT_OPTIONS,
                "featured_filter_options": FEATURED_FILTER_OPTIONS,
                "status_filter_options": STATUS_FILTER_OPTIONS,
                "filter_departments": TEAM_DEPARTMENTS,
                "filter_positions": TEAM_POSITIONS,
                "member_types": MEMBER_TYPES,
                "member_type_labels": dict(MEMBER_TYPES),
            }
        )
        return ctx

    @staticmethod
    def get_form_context(member_id: int | None = None, active_tab: str = "general") -> dict:
        from app.constants.team_admin import (
            MEMBER_TYPES,
            TEAM_DEPARTMENTS,
            TEAM_FORM_TABS,
            TEAM_POSITIONS,
        )

        if member_id:
            member = TeamAdminProvider.get_member(member_id, include_inactive=True)
            if not member:
                return {}
            dto = TeamAdminProvider.to_admin_dto(member)
            title = f"Edit — {dto.name}"
            is_edit = True
        else:
            dto = TeamAdminDTO(
                id=None,
                name="",
                slug="",
                position="",
                department=TEAM_DEPARTMENTS[0] if TEAM_DEPARTMENTS else "",
                member_type="staff",
                bio="",
                photo="",
                email="",
                phone="",
                years_experience="",
                education="",
                experience_summary="",
                sort_order=0,
                is_featured=False,
                is_active=True,
            )
            title = "Create Team Member"
            is_edit = False

        ctx = TeamAdminService.get_shell_context(page_title=title, active_section="form")
        ctx["member"] = dto
        ctx["is_edit"] = is_edit
        ctx["active_tab"] = active_tab
        ctx["projects"] = TeamAdminProvider.list_projects()
        ctx["services"] = TeamAdminProvider.list_services()
        ctx["equipment_list"] = TeamAdminProvider.list_equipment()
        ctx["media_assets"] = TeamAdminProvider.list_media_assets("team")
        ctx.update(
            {
                "form_tabs": TEAM_FORM_TABS,
                "departments": TEAM_DEPARTMENTS,
                "positions": TEAM_POSITIONS,
                "member_types": MEMBER_TYPES,
                "social_links_text": TeamAdminProvider.social_links_to_text(dto.social_links),
            }
        )
        return ctx

    @staticmethod
    def dto_from_form(
        form,
        *,
        gallery_paths: list[str] | None = None,
    ) -> TeamAdminDTO:
        return TeamAdminDTO(
            id=form.team_member_id.data or None,
            name=form.name.data,
            slug=form.slug.data or "",
            position=form.position.data,
            department=form.department.data or "",
            member_type=form.member_type.data or "staff",
            bio=form.bio.data or "",
            photo=form.photo.data or "",
            email=form.email.data or "",
            phone=form.phone.data or "",
            years_experience=form.years_experience.data or "",
            education=form.education.data or "",
            experience_summary=form.experience_summary.data or "",
            sort_order=int(form.sort_order.data or 0),
            is_featured=form.is_featured.data,
            is_active=form.is_active.data if form.team_member_id.data else True,
            meta_title=form.meta_title.data or "",
            meta_description=form.meta_description.data or "",
            og_image=form.og_image.data or "",
            canonical_url=form.canonical_url.data or "",
            social_links=TeamAdminProvider.parse_social_links_text(form.social_links.data or ""),
            related_project_ids=[int(x) for x in (form.related_project_ids.data or [])],
            related_service_slugs=form.related_service_slugs.data or [],
            related_equipment_ids=[int(x) for x in (form.related_equipment_ids.data or [])],
            gallery_paths=gallery_paths or [],
        )

    @staticmethod
    def save_member(dto: TeamAdminDTO, *, ip_address: str | None) -> SaveResultDTO:
        try:
            is_new = not dto.id
            member = TeamAdminProvider.save_from_dto(dto)
            action = "team.create" if is_new else "team.update"
            TeamAdminProvider.record_audit(
                user_id=current_user.id,
                action=action,
                resource_type="team_member",
                resource_id=str(member.id),
                details=f"{'Created' if is_new else 'Updated'} team member: {member.name}",
                ip_address=ip_address,
            )
            if TeamAdminProvider.commit():
                return SaveResultDTO(True, "Team member saved successfully.", member.id)
            return SaveResultDTO(False, "Unable to save team member.")
        except ValueError as exc:
            TeamAdminProvider.rollback()
            return SaveResultDTO(False, str(exc))
        except Exception as exc:
            TeamAdminProvider.rollback()
            return SaveResultDTO(False, f"Save failed: {exc}")

    @staticmethod
    def delete_member(member_id: int, *, ip_address: str | None) -> SaveResultDTO:
        member = TeamAdminProvider.get_member(member_id, include_inactive=True)
        if not member:
            return SaveResultDTO(False, "Team member not found.")
        TeamAdminProvider.soft_delete(member)
        TeamAdminProvider.record_audit(
            user_id=current_user.id,
            action="team.delete",
            resource_type="team_member",
            resource_id=str(member_id),
            details=f"Soft-deleted team member: {member.name}",
            ip_address=ip_address,
        )
        if TeamAdminProvider.commit():
            return SaveResultDTO(True, "Team member moved to trash.")
        TeamAdminProvider.rollback()
        return SaveResultDTO(False, "Delete failed.")

    @staticmethod
    def restore_member(member_id: int, *, ip_address: str | None) -> SaveResultDTO:
        member = TeamAdminProvider.get_member(member_id, include_inactive=True)
        if not member:
            return SaveResultDTO(False, "Team member not found.")
        TeamAdminProvider.restore(member)
        TeamAdminProvider.record_audit(
            user_id=current_user.id,
            action="team.restore",
            resource_type="team_member",
            resource_id=str(member_id),
            details=f"Restored team member: {member.name}",
            ip_address=ip_address,
        )
        if TeamAdminProvider.commit():
            return SaveResultDTO(True, "Team member restored.")
        TeamAdminProvider.rollback()
        return SaveResultDTO(False, "Restore failed.")

    @staticmethod
    def bulk_action(member_ids: list[int], action: str, *, ip_address: str | None) -> SaveResultDTO:
        if not member_ids:
            return SaveResultDTO(False, "No team members selected.")
        count = TeamAdminProvider.bulk_update(member_ids, action)
        TeamAdminProvider.record_audit(
            user_id=current_user.id,
            action=f"team.bulk_{action}",
            resource_type="team_member",
            resource_id=",".join(str(i) for i in member_ids[:10]),
            details=f"Bulk {action} on {count} team member(s)",
            ip_address=ip_address,
        )
        if TeamAdminProvider.commit():
            return SaveResultDTO(True, f"Bulk action applied to {count} team member(s).")
        TeamAdminProvider.rollback()
        return SaveResultDTO(False, "Bulk action failed.")
