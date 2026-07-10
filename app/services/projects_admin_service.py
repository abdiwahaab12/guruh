"""Projects admin business logic."""

from __future__ import annotations

import math

from flask import url_for
from flask_login import current_user

from app.constants.projects_admin import DEFAULT_PER_PAGE, MAX_PER_PAGE
from app.providers.admin_dashboard_provider import AdminDashboardProvider
from app.providers.projects_admin_provider import ProjectsAdminProvider
from app.schemas.admin import BreadcrumbItemDTO
from app.schemas.projects_admin import ProjectAdminDTO, ProjectListPageDTO, ProjectStatsDTO, SaveResultDTO


class ProjectsAdminService:
    """Enterprise projects management service."""

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
            "active_nav": "projects",
            "projects_active_section": active_section,
            "breadcrumbs": breadcrumbs
            or ProjectsAdminService.build_breadcrumbs(page_title),
            "notifications": dashboard.notifications,
            "unread_notification_count": dashboard.unread_notification_count,
            "user": current_user,
        }

    @staticmethod
    def build_breadcrumbs(current_label: str) -> list[BreadcrumbItemDTO]:
        return [
            BreadcrumbItemDTO("Admin", url_for("admin.dashboard"), False),
            BreadcrumbItemDTO("Projects", url_for("admin.projects_dashboard"), False),
            BreadcrumbItemDTO(current_label, None, True),
        ]

    @staticmethod
    def get_dashboard_context() -> dict:
        stats_raw = ProjectsAdminProvider.get_stats()
        ctx = ProjectsAdminService.get_shell_context(
            page_title="Projects",
            active_section="dashboard",
            breadcrumbs=[
                BreadcrumbItemDTO("Admin", url_for("admin.dashboard"), False),
                BreadcrumbItemDTO("Projects", None, True),
            ],
        )
        ctx["stats"] = ProjectStatsDTO(
            total=stats_raw["total"],
            active=stats_raw["active"],
            featured=stats_raw["featured"],
            by_country=stats_raw["by_country"],
            by_status=stats_raw["by_status"],
            recent=[ProjectsAdminProvider.to_list_item(p) for p in stats_raw["recent"]],
        )
        ctx["stats_json_country"] = stats_raw["by_country"]
        ctx["stats_json_status"] = stats_raw["by_status"]
        return ctx

    @staticmethod
    def get_list_context(
        *,
        q: str = "",
        country: str = "",
        county: str = "",
        status: str = "",
        category: str = "",
        service: str = "",
        client: str = "",
        year: str = "",
        sort: str = "date_desc",
        page: int = 1,
        per_page: int = DEFAULT_PER_PAGE,
        include_deleted: bool = False,
    ) -> dict:
        per_page = min(max(per_page, 10), MAX_PER_PAGE)
        page = max(page, 1)
        items, total = ProjectsAdminProvider.query_projects(
            q=q,
            country=country,
            county=county,
            status=status,
            category=category,
            service=service,
            client=client,
            year=year,
            sort=sort,
            page=page,
            per_page=per_page,
            include_deleted=include_deleted,
        )
        total_pages = max(1, math.ceil(total / per_page)) if total else 1
        page = min(page, total_pages)

        ctx = ProjectsAdminService.get_shell_context(
            page_title="All Projects",
            active_section="list",
        )
        ctx["list_page"] = ProjectListPageDTO(
            items=[ProjectsAdminProvider.to_list_item(p) for p in items],
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
            query=q,
            filters={
                "country": country,
                "county": county,
                "status": status,
                "category": category,
                "service": service,
                "client": client,
                "year": year,
            },
            sort=sort,
            include_deleted=include_deleted,
        )
        from app.constants.projects_admin import (
            BULK_ACTIONS,
            PROJECT_CATEGORIES,
            PROJECT_CLIENTS,
            PROJECT_COUNTIES,
            PROJECT_COUNTRIES,
            PROJECT_STATUSES,
            PROJECT_YEARS,
            SORT_OPTIONS,
        )
        from app.providers.projects_admin_provider import ProjectsAdminProvider as P

        ctx.update(
            {
                "bulk_actions": BULK_ACTIONS,
                "sort_options": SORT_OPTIONS,
                "filter_countries": PROJECT_COUNTRIES,
                "filter_counties": PROJECT_COUNTIES,
                "filter_statuses": PROJECT_STATUSES,
                "filter_categories": PROJECT_CATEGORIES,
                "filter_clients": PROJECT_CLIENTS,
                "filter_years": PROJECT_YEARS,
                "filter_services": P.list_services(),
            }
        )
        return ctx

    @staticmethod
    def get_form_context(project_id: int | None = None, active_tab: str = "general") -> dict:
        if project_id:
            project = ProjectsAdminProvider.get_project(project_id, include_inactive=True)
            if not project:
                return {}
            dto = ProjectsAdminProvider.to_admin_dto(project)
            title = f"Edit — {dto.title}"
            is_edit = True
        else:
            dto = ProjectAdminDTO(
                id=None,
                title="",
                slug="",
                description="",
                location="",
                country="Somalia",
                county="",
                status="Completed",
                client="",
                category="",
                cover_image="",
                completion_date="",
                sort_order=0,
                is_featured=False,
                is_active=True,
            )
            title = "Create Project"
            is_edit = False

        ctx = ProjectsAdminService.get_shell_context(page_title=title, active_section="form")
        ctx["project"] = dto
        ctx["is_edit"] = is_edit
        ctx["active_tab"] = active_tab
        ctx["services"] = ProjectsAdminProvider.list_services()
        ctx["team_members"] = ProjectsAdminProvider.list_team()
        ctx["related_projects"] = ProjectsAdminProvider.list_projects_for_related(project_id)
        ctx["media_assets"] = ProjectsAdminProvider.list_media_assets("projects")
        ctx["document_assets"] = ProjectsAdminProvider.list_media_assets("downloads")

        from app.constants.projects_admin import (
            PROJECT_CATEGORIES,
            PROJECT_CLIENTS,
            PROJECT_COUNTIES,
            PROJECT_COUNTRIES,
            PROJECT_FORM_TABS,
            PROJECT_STATUSES,
            PROJECT_YEARS,
            SOMALIA_COUNTIES,
        )

        ctx.update(
            {
                "form_tabs": PROJECT_FORM_TABS,
                "countries": PROJECT_COUNTRIES,
                "counties_ke": PROJECT_COUNTIES,
                "counties_so": SOMALIA_COUNTIES,
                "statuses": PROJECT_STATUSES,
                "categories": PROJECT_CATEGORIES,
                "clients": PROJECT_CLIENTS,
                "years": PROJECT_YEARS,
                "timeline_text": ProjectsAdminProvider.timeline_to_text(dto.timeline),
            }
        )
        return ctx

    @staticmethod
    def dto_from_form(form, *, gallery_paths: list[str] | None = None, document_paths: list[str] | None = None) -> ProjectAdminDTO:
        return ProjectAdminDTO(
            id=form.project_id.data or None,
            title=form.title.data,
            slug=form.slug.data or "",
            description=form.description.data,
            location=form.location.data or "",
            country=form.country.data,
            county=form.county.data or "",
            status=form.status.data or "",
            client=form.client.data or "",
            category=form.category.data or "",
            cover_image=form.cover_image.data or "",
            completion_date=form.completion_date.data or "",
            sort_order=int(form.sort_order.data or 0),
            is_featured=form.is_featured.data,
            is_active=form.is_active.data if form.project_id.data else True,
            meta_title=form.meta_title.data or "",
            meta_description=form.meta_description.data or "",
            og_image=form.og_image.data or "",
            canonical_url=form.canonical_url.data or "",
            overview=form.overview.data or "",
            consultant=form.consultant.data or "",
            duration=form.duration.data or "",
            completion_year=form.completion_year.data or "",
            challenges=ProjectsAdminProvider.lines_to_list(form.challenges.data),
            solutions=ProjectsAdminProvider.lines_to_list(form.solutions.data),
            scope_of_work=ProjectsAdminProvider.lines_to_list(form.scope_of_work.data),
            timeline=ProjectsAdminProvider.parse_timeline_text(form.timeline.data or ""),
            service_slugs=form.service_slugs.data or [],
            equipment=ProjectsAdminProvider.lines_to_list(form.equipment.data),
            team_member_ids=[int(x) for x in (form.team_member_ids.data or [])],
            related_project_ids=[int(x) for x in (form.related_project_ids.data or [])],
            related_service_slugs=form.related_service_slugs.data or [],
            document_paths=document_paths or [],
            gallery_paths=gallery_paths or [],
        )

    @staticmethod
    def save_project(dto: ProjectAdminDTO, *, ip_address: str | None) -> SaveResultDTO:
        try:
            is_new = not dto.id
            project = ProjectsAdminProvider.save_from_dto(dto)
            action = "projects.create" if is_new else "projects.update"
            ProjectsAdminProvider.record_audit(
                user_id=current_user.id,
                action=action,
                resource_type="project",
                resource_id=str(project.id),
                details=f"{'Created' if is_new else 'Updated'} project: {project.title}",
                ip_address=ip_address,
            )
            if ProjectsAdminProvider.commit():
                return SaveResultDTO(True, "Project saved successfully.", project.id)
            return SaveResultDTO(False, "Unable to save project.")
        except ValueError as exc:
            ProjectsAdminProvider.rollback()
            return SaveResultDTO(False, str(exc))
        except Exception as exc:
            ProjectsAdminProvider.rollback()
            return SaveResultDTO(False, f"Save failed: {exc}")

    @staticmethod
    def delete_project(project_id: int, *, ip_address: str | None) -> SaveResultDTO:
        project = ProjectsAdminProvider.get_project(project_id, include_inactive=True)
        if not project:
            return SaveResultDTO(False, "Project not found.")
        ProjectsAdminProvider.soft_delete(project)
        ProjectsAdminProvider.record_audit(
            user_id=current_user.id,
            action="projects.delete",
            resource_type="project",
            resource_id=str(project_id),
            details=f"Soft-deleted project: {project.title}",
            ip_address=ip_address,
        )
        if ProjectsAdminProvider.commit():
            return SaveResultDTO(True, "Project moved to trash.")
        ProjectsAdminProvider.rollback()
        return SaveResultDTO(False, "Delete failed.")

    @staticmethod
    def restore_project(project_id: int, *, ip_address: str | None) -> SaveResultDTO:
        project = ProjectsAdminProvider.get_project(project_id, include_inactive=True)
        if not project:
            return SaveResultDTO(False, "Project not found.")
        ProjectsAdminProvider.restore(project)
        ProjectsAdminProvider.record_audit(
            user_id=current_user.id,
            action="projects.restore",
            resource_type="project",
            resource_id=str(project_id),
            details=f"Restored project: {project.title}",
            ip_address=ip_address,
        )
        if ProjectsAdminProvider.commit():
            return SaveResultDTO(True, "Project restored.")
        ProjectsAdminProvider.rollback()
        return SaveResultDTO(False, "Restore failed.")

    @staticmethod
    def bulk_action(project_ids: list[int], action: str, *, ip_address: str | None) -> SaveResultDTO:
        if not project_ids:
            return SaveResultDTO(False, "No projects selected.")
        count = ProjectsAdminProvider.bulk_update(project_ids, action)
        ProjectsAdminProvider.record_audit(
            user_id=current_user.id,
            action=f"projects.bulk_{action}",
            resource_type="project",
            resource_id=",".join(str(i) for i in project_ids[:10]),
            details=f"Bulk {action} on {count} project(s)",
            ip_address=ip_address,
        )
        if ProjectsAdminProvider.commit():
            return SaveResultDTO(True, f"Bulk action applied to {count} project(s).")
        ProjectsAdminProvider.rollback()
        return SaveResultDTO(False, "Bulk action failed.")
