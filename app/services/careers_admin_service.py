"""Careers admin business logic."""

from __future__ import annotations

import math

from flask import url_for
from flask_login import current_user

from app.constants.careers_admin import DEFAULT_PER_PAGE, JOB_STATUSES, MAX_PER_PAGE
from app.providers.admin_dashboard_provider import AdminDashboardProvider
from app.providers.careers_admin_provider import CareersAdminProvider
from app.schemas.admin import BreadcrumbItemDTO
from app.schemas.careers_admin import JobAdminDTO, JobListPageDTO, JobStatsDTO, SaveResultDTO


class CareersAdminService:
    """Enterprise careers management service."""

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
            "active_nav": "careers",
            "careers_active_section": active_section,
            "breadcrumbs": breadcrumbs
            or CareersAdminService.build_breadcrumbs(page_title),
            "notifications": dashboard.notifications,
            "unread_notification_count": dashboard.unread_notification_count,
            "user": current_user,
        }

    @staticmethod
    def build_breadcrumbs(current_label: str) -> list[BreadcrumbItemDTO]:
        return [
            BreadcrumbItemDTO("Admin", url_for("admin.dashboard"), False),
            BreadcrumbItemDTO("Careers", url_for("admin.careers_dashboard"), False),
            BreadcrumbItemDTO(current_label, None, True),
        ]

    @staticmethod
    def get_dashboard_context() -> dict:
        stats_raw = CareersAdminProvider.get_stats()
        ctx = CareersAdminService.get_shell_context(
            page_title="Careers",
            active_section="dashboard",
            breadcrumbs=[
                BreadcrumbItemDTO("Admin", url_for("admin.dashboard"), False),
                BreadcrumbItemDTO("Careers", None, True),
            ],
        )
        ctx["stats"] = JobStatsDTO(
            total=stats_raw["total"],
            active=stats_raw["active"],
            closed=stats_raw["closed"],
            draft=stats_raw["draft"],
            recent=[CareersAdminProvider.to_list_item(j) for j in stats_raw["recent"]],
        )
        ctx["status_labels"] = dict(JOB_STATUSES)
        return ctx

    @staticmethod
    def get_list_context(
        *,
        q: str = "",
        department: str = "",
        employment_type: str = "",
        location: str = "",
        status: str = "",
        sort: str = "date_desc",
        page: int = 1,
        per_page: int = DEFAULT_PER_PAGE,
        include_deleted: bool = False,
    ) -> dict:
        per_page = min(max(per_page, 10), MAX_PER_PAGE)
        page = max(page, 1)
        items, total = CareersAdminProvider.query_jobs(
            q=q,
            department=department,
            employment_type=employment_type,
            location=location,
            status=status,
            sort=sort,
            page=page,
            per_page=per_page,
            include_deleted=include_deleted,
        )
        total_pages = max(1, math.ceil(total / per_page)) if total else 1
        page = min(page, total_pages)

        ctx = CareersAdminService.get_shell_context(
            page_title="All Jobs",
            active_section="list",
        )
        ctx["list_page"] = JobListPageDTO(
            items=[CareersAdminProvider.to_list_item(j) for j in items],
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
            query=q,
            filters={
                "department": department,
                "employment_type": employment_type,
                "location": location,
                "status": status,
            },
            sort=sort,
            include_deleted=include_deleted,
        )
        from app.constants.careers_admin import (
            BULK_ACTIONS,
            EMPLOYMENT_TYPES,
            JOB_DEPARTMENTS,
            JOB_LOCATIONS,
            JOB_STATUSES,
            SORT_OPTIONS,
            STATUS_FILTER_OPTIONS,
        )

        ctx.update(
            {
                "bulk_actions": BULK_ACTIONS,
                "sort_options": SORT_OPTIONS,
                "status_filter_options": STATUS_FILTER_OPTIONS,
                "filter_departments": JOB_DEPARTMENTS,
                "filter_locations": JOB_LOCATIONS,
                "filter_employment_types": EMPLOYMENT_TYPES,
                "job_statuses": JOB_STATUSES,
                "status_labels": dict(JOB_STATUSES),
            }
        )
        return ctx

    @staticmethod
    def get_form_context(job_id: int | None = None, active_tab: str = "general") -> dict:
        from app.constants.careers_admin import (
            CAREERS_FORM_TABS,
            EMPLOYMENT_TYPES,
            EXPERIENCE_LEVELS,
            JOB_DEPARTMENTS,
            JOB_LOCATIONS,
            JOB_STATUSES,
        )

        if job_id:
            job = CareersAdminProvider.get_job(job_id, include_inactive=True)
            if not job:
                return {}
            dto = CareersAdminProvider.to_admin_dto(job)
            title = f"Edit — {dto.title}"
            is_edit = True
        else:
            dto = JobAdminDTO(
                id=None,
                title="",
                slug="",
                department=JOB_DEPARTMENTS[0] if JOB_DEPARTMENTS else "",
                location=JOB_LOCATIONS[0] if JOB_LOCATIONS else "",
                employment_type="Full-time",
                description="",
                requirements="",
                deadline="",
                sort_order=0,
                is_active=True,
                status="draft",
                accept_applications=True,
            )
            title = "Create Job"
            is_edit = False

        ctx = CareersAdminService.get_shell_context(page_title=title, active_section="form")
        ctx["job"] = dto
        ctx["is_edit"] = is_edit
        ctx["active_tab"] = active_tab
        ctx.update(
            {
                "form_tabs": CAREERS_FORM_TABS,
                "departments": JOB_DEPARTMENTS,
                "locations": JOB_LOCATIONS,
                "employment_types": EMPLOYMENT_TYPES,
                "experience_levels": EXPERIENCE_LEVELS,
                "job_statuses": JOB_STATUSES,
            }
        )
        return ctx

    @staticmethod
    def dto_from_form(form) -> JobAdminDTO:
        return JobAdminDTO(
            id=form.job_id.data or None,
            title=form.title.data,
            slug=form.slug.data or "",
            department=form.department.data or "",
            location=form.location.data or "",
            employment_type=form.employment_type.data or "",
            description=form.description.data,
            requirements=form.requirements.data or "",
            deadline=form.deadline.data or "",
            sort_order=int(form.sort_order.data or 0),
            is_active=form.is_active.data if form.job_id.data else True,
            status=form.status.data or "draft",
            short_description=form.short_description.data or "",
            experience_required=form.experience_required.data or "",
            image=form.image.data or "",
            responsibilities=CareersAdminProvider.lines_to_list(form.responsibilities.data),
            qualifications=CareersAdminProvider.lines_to_list(form.qualifications.data),
            skills=CareersAdminProvider.lines_to_list(form.skills.data),
            benefits=CareersAdminProvider.lines_to_list(form.benefits.data),
            is_featured=form.is_featured.data,
            accept_applications=form.accept_applications.data if form.job_id.data else True,
            notify_email=form.notify_email.data or "",
            auto_reply_enabled=form.auto_reply_enabled.data,
            auto_reply_message=form.auto_reply_message.data or "",
            meta_title=form.meta_title.data or "",
            meta_description=form.meta_description.data or "",
            og_image=form.og_image.data or "",
            canonical_url=form.canonical_url.data or "",
        )

    @staticmethod
    def save_job(dto: JobAdminDTO, *, ip_address: str | None) -> SaveResultDTO:
        try:
            is_new = not dto.id
            job = CareersAdminProvider.save_from_dto(dto)
            action = "careers.create" if is_new else "careers.update"
            CareersAdminProvider.record_audit(
                user_id=current_user.id,
                action=action,
                resource_type="job_listing",
                resource_id=str(job.id),
                details=f"{'Created' if is_new else 'Updated'} job: {job.title}",
                ip_address=ip_address,
            )
            if CareersAdminProvider.commit():
                return SaveResultDTO(True, "Job saved successfully.", job.id)
            return SaveResultDTO(False, "Unable to save job.")
        except ValueError as exc:
            CareersAdminProvider.rollback()
            return SaveResultDTO(False, str(exc))
        except Exception as exc:
            CareersAdminProvider.rollback()
            return SaveResultDTO(False, f"Save failed: {exc}")

    @staticmethod
    def delete_job(job_id: int, *, ip_address: str | None) -> SaveResultDTO:
        job = CareersAdminProvider.get_job(job_id, include_inactive=True)
        if not job:
            return SaveResultDTO(False, "Job not found.")
        CareersAdminProvider.soft_delete(job)
        CareersAdminProvider.record_audit(
            user_id=current_user.id,
            action="careers.delete",
            resource_type="job_listing",
            resource_id=str(job_id),
            details=f"Soft-deleted job: {job.title}",
            ip_address=ip_address,
        )
        if CareersAdminProvider.commit():
            return SaveResultDTO(True, "Job moved to trash.")
        CareersAdminProvider.rollback()
        return SaveResultDTO(False, "Delete failed.")

    @staticmethod
    def restore_job(job_id: int, *, ip_address: str | None) -> SaveResultDTO:
        job = CareersAdminProvider.get_job(job_id, include_inactive=True)
        if not job:
            return SaveResultDTO(False, "Job not found.")
        CareersAdminProvider.restore(job)
        CareersAdminProvider.record_audit(
            user_id=current_user.id,
            action="careers.restore",
            resource_type="job_listing",
            resource_id=str(job_id),
            details=f"Restored job: {job.title}",
            ip_address=ip_address,
        )
        if CareersAdminProvider.commit():
            return SaveResultDTO(True, "Job restored.")
        CareersAdminProvider.rollback()
        return SaveResultDTO(False, "Restore failed.")

    @staticmethod
    def bulk_action(job_ids: list[int], action: str, *, ip_address: str | None) -> SaveResultDTO:
        if not job_ids:
            return SaveResultDTO(False, "No jobs selected.")
        count = CareersAdminProvider.bulk_update(job_ids, action)
        CareersAdminProvider.record_audit(
            user_id=current_user.id,
            action=f"careers.bulk_{action}",
            resource_type="job_listing",
            resource_id=",".join(str(i) for i in job_ids[:10]),
            details=f"Bulk {action} on {count} job(s)",
            ip_address=ip_address,
        )
        if CareersAdminProvider.commit():
            return SaveResultDTO(True, f"Bulk action applied to {count} job(s).")
        CareersAdminProvider.rollback()
        return SaveResultDTO(False, "Bulk action failed.")
