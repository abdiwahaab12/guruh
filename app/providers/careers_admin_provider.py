"""Careers admin data provider — MySQL / SQLAlchemy."""

from __future__ import annotations

import json
import re
import unicodedata

from flask import current_app
from sqlalchemy import asc, desc, or_
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models.catalog import JobListing
from app.models.job_listing_detail import JobListingDetail
from app.providers.auth_provider import AuthProvider
from app.schemas.careers_admin import JobAdminDTO, JobListItemDTO


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-")


def _json_list(raw: str | None) -> list:
    if not raw:
        return []
    try:
        data = json.loads(raw)
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def _dump_json(data: list) -> str:
    return json.dumps(data)


def _lines_to_list(text: str) -> list[str]:
    return [line.strip() for line in (text or "").splitlines() if line.strip()]


class CareersAdminProvider:
    """Database operations for job listing CRUD."""

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
    def get_or_create_detail(job: JobListing) -> JobListingDetail:
        if job.detail:
            return job.detail
        detail = JobListingDetail(job_listing_id=job.id)
        db.session.add(detail)
        return detail

    @staticmethod
    def to_admin_dto(job: JobListing) -> JobAdminDTO:
        detail = job.detail
        created = job.created_at.strftime("%d %b %Y") if job.created_at else ""
        updated = job.updated_at.strftime("%d %b %Y") if job.updated_at else ""
        return JobAdminDTO(
            id=job.id,
            title=job.title,
            slug=job.slug,
            department=job.department or "",
            location=job.location or "",
            employment_type=job.employment_type or "",
            description=job.description or "",
            requirements=job.requirements or "",
            deadline=job.deadline or "",
            sort_order=job.sort_order or 0,
            is_active=job.is_active,
            status=detail.status if detail else "draft",
            short_description=detail.short_description if detail else "",
            experience_required=detail.experience_required if detail else "",
            image=detail.image if detail else "",
            responsibilities=_json_list(detail.responsibilities_json if detail else "[]"),
            qualifications=_json_list(detail.qualifications_json if detail else "[]"),
            skills=_json_list(detail.skills_json if detail else "[]"),
            benefits=_json_list(detail.benefits_json if detail else "[]"),
            is_featured=detail.is_featured if detail else False,
            accept_applications=detail.accept_applications if detail else True,
            notify_email=detail.notify_email if detail else "",
            auto_reply_enabled=detail.auto_reply_enabled if detail else False,
            auto_reply_message=detail.auto_reply_message if detail else "",
            meta_title=detail.meta_title if detail else "",
            meta_description=detail.meta_description if detail else "",
            og_image=detail.og_image if detail else "",
            canonical_url=detail.canonical_url if detail else "",
            created_at_label=created,
            updated_at_label=updated,
        )

    @staticmethod
    def to_list_item(job: JobListing) -> JobListItemDTO:
        detail = job.detail
        updated = job.updated_at.strftime("%d %b %Y") if job.updated_at else ""
        return JobListItemDTO(
            id=job.id,
            title=job.title,
            slug=job.slug,
            department=job.department or "",
            location=job.location or "",
            employment_type=job.employment_type or "",
            deadline=job.deadline or "",
            status=detail.status if detail else "draft",
            sort_order=job.sort_order or 0,
            is_featured=detail.is_featured if detail else False,
            is_active=job.is_active,
            updated_at_label=updated,
        )

    @staticmethod
    def get_job(job_id: int, include_inactive: bool = False) -> JobListing | None:
        try:
            query = JobListing.query.filter_by(id=job_id)
            if not include_inactive:
                query = query.filter_by(is_active=True)
            return query.first()
        except SQLAlchemyError as exc:
            current_app.logger.error("get_job failed: %s", exc)
            return None

    @staticmethod
    def get_by_slug(slug: str, exclude_id: int | None = None) -> JobListing | None:
        query = JobListing.query.filter_by(slug=slug)
        if exclude_id:
            query = query.filter(JobListing.id != exclude_id)
        return query.first()

    @staticmethod
    def ensure_unique_slug(base: str, exclude_id: int | None = None) -> str:
        slug = slugify(base) or "job"
        candidate = slug
        counter = 2
        while CareersAdminProvider.get_by_slug(candidate, exclude_id=exclude_id):
            candidate = f"{slug}-{counter}"
            counter += 1
        return candidate

    @staticmethod
    def query_jobs(
        *,
        q: str = "",
        department: str = "",
        employment_type: str = "",
        location: str = "",
        status: str = "",
        sort: str = "date_desc",
        page: int = 1,
        per_page: int = 20,
        include_deleted: bool = False,
    ) -> tuple[list[JobListing], int]:
        try:
            query = JobListing.query.outerjoin(
                JobListingDetail, JobListingDetail.job_listing_id == JobListing.id
            )

            if include_deleted:
                query = query.filter(JobListing.is_active.is_(False))
            else:
                query = query.filter(JobListing.is_active.is_(True))
                if status == "draft":
                    query = query.filter(JobListingDetail.status == "draft")
                elif status == "active":
                    query = query.filter(JobListingDetail.status == "active")
                elif status == "closed":
                    query = query.filter(JobListingDetail.status == "closed")

            if q:
                term = f"%{q.strip()}%"
                query = query.filter(
                    or_(
                        JobListing.title.ilike(term),
                        JobListing.slug.ilike(term),
                        JobListing.department.ilike(term),
                        JobListing.location.ilike(term),
                        JobListingDetail.short_description.ilike(term),
                    )
                )
            if department:
                query = query.filter(JobListing.department == department)
            if employment_type:
                query = query.filter(JobListing.employment_type == employment_type)
            if location:
                query = query.filter(JobListing.location == location)

            sort_map = {
                "date_desc": desc(JobListing.updated_at),
                "date_asc": asc(JobListing.updated_at),
                "title_asc": asc(JobListing.title),
                "title_desc": desc(JobListing.title),
                "sort_order": asc(JobListing.sort_order),
                "deadline_asc": asc(JobListing.deadline),
            }
            query = query.order_by(sort_map.get(sort, desc(JobListing.updated_at)))

            total = query.count()
            items = query.offset((page - 1) * per_page).limit(per_page).all()
            return items, total
        except SQLAlchemyError as exc:
            current_app.logger.error("query_jobs failed: %s", exc)
            return [], 0

    @staticmethod
    def get_stats() -> dict:
        try:
            total = JobListing.query.count()
            base = db.session.query(JobListing).join(
                JobListingDetail, JobListingDetail.job_listing_id == JobListing.id
            )
            active = base.filter(
                JobListing.is_active.is_(True), JobListingDetail.status == "active"
            ).count()
            closed = base.filter(
                JobListing.is_active.is_(True), JobListingDetail.status == "closed"
            ).count()
            draft = base.filter(
                JobListing.is_active.is_(True), JobListingDetail.status == "draft"
            ).count()
            recent = JobListing.query.order_by(desc(JobListing.updated_at)).limit(6).all()
            return {
                "total": total,
                "active": active,
                "closed": closed,
                "draft": draft,
                "recent": recent,
            }
        except SQLAlchemyError as exc:
            current_app.logger.error("get_stats failed: %s", exc)
            return {"total": 0, "active": 0, "closed": 0, "draft": 0, "recent": []}

    @staticmethod
    def save_from_dto(dto: JobAdminDTO) -> JobListing:
        slug = CareersAdminProvider.ensure_unique_slug(dto.slug or dto.title, dto.id)

        if dto.id:
            job = CareersAdminProvider.get_job(dto.id, include_inactive=True)
            if not job:
                raise ValueError("Job listing not found.")
        else:
            job = JobListing(
                title=dto.title.strip(),
                slug=slug,
                description=dto.description.strip(),
            )
            db.session.add(job)

        job.title = dto.title.strip()
        job.slug = slug
        job.department = dto.department.strip()
        job.location = dto.location.strip()
        job.employment_type = dto.employment_type.strip()
        job.description = dto.description.strip()
        job.requirements = dto.requirements.strip()
        job.deadline = dto.deadline.strip()
        job.sort_order = dto.sort_order

        status = dto.status.strip() or "draft"
        job.is_active = dto.is_active
        if status == "active":
            job.is_active = True

        db.session.flush()

        detail = CareersAdminProvider.get_or_create_detail(job)
        detail.status = status
        detail.short_description = dto.short_description.strip()
        detail.experience_required = dto.experience_required.strip()
        detail.image = dto.image.strip()
        detail.responsibilities_json = _dump_json(dto.responsibilities)
        detail.qualifications_json = _dump_json(dto.qualifications)
        detail.skills_json = _dump_json(dto.skills)
        detail.benefits_json = _dump_json(dto.benefits)
        detail.is_featured = dto.is_featured
        detail.accept_applications = dto.accept_applications
        detail.notify_email = dto.notify_email.strip()
        detail.auto_reply_enabled = dto.auto_reply_enabled
        detail.auto_reply_message = dto.auto_reply_message.strip()
        detail.meta_title = dto.meta_title.strip()
        detail.meta_description = dto.meta_description.strip()
        detail.og_image = dto.og_image.strip()
        detail.canonical_url = dto.canonical_url.strip()

        return job

    @staticmethod
    def soft_delete(job: JobListing) -> None:
        job.is_active = False
        detail = CareersAdminProvider.get_or_create_detail(job)
        detail.mark_deleted()

    @staticmethod
    def restore(job: JobListing) -> None:
        job.is_active = True
        if job.detail:
            job.detail.restore()
            if job.detail.status not in ("active", "closed", "draft"):
                job.detail.status = "draft"

    @staticmethod
    def bulk_update(job_ids: list[int], action: str) -> int:
        count = 0
        jobs = JobListing.query.filter(JobListing.id.in_(job_ids)).all()
        for job in jobs:
            detail = CareersAdminProvider.get_or_create_detail(job)
            if action == "feature":
                detail.is_featured = True
                count += 1
            elif action == "unfeature":
                detail.is_featured = False
                count += 1
            elif action == "activate":
                job.is_active = True
                detail.status = "active"
                detail.restore()
                count += 1
            elif action == "close":
                detail.status = "closed"
                count += 1
            elif action == "deactivate":
                CareersAdminProvider.soft_delete(job)
                count += 1
            elif action == "restore":
                CareersAdminProvider.restore(job)
                count += 1
        return count

    @staticmethod
    def lines_to_list(text: str) -> list[str]:
        return _lines_to_list(text)
