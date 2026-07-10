"""Projects admin data provider — MySQL / SQLAlchemy."""

from __future__ import annotations

import json
import re
import unicodedata
from datetime import datetime

from flask import current_app
from sqlalchemy import asc, desc, func, or_
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models.catalog import GalleryImage, Project, Service, TeamMember
from app.models.project_detail import ProjectDetail
from app.providers.auth_provider import AuthProvider
from app.schemas.projects_admin import (
    ProjectAdminDTO,
    ProjectListItemDTO,
    ProjectTimelineItemDTO,
)


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


def _parse_timeline(raw: str | None) -> list[ProjectTimelineItemDTO]:
    items = []
    for entry in _json_list(raw):
        if isinstance(entry, dict):
            items.append(
                ProjectTimelineItemDTO(
                    date=str(entry.get("date", "")),
                    title=str(entry.get("title", "")),
                    description=str(entry.get("description", "")),
                )
            )
    return items


def _lines_to_list(text: str) -> list[str]:
    return [line.strip() for line in (text or "").splitlines() if line.strip()]


class ProjectsAdminProvider:
    """Database operations for project CRUD."""

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
    def get_or_create_detail(project: Project) -> ProjectDetail:
        if project.detail:
            return project.detail
        detail = ProjectDetail(project_id=project.id)
        db.session.add(detail)
        return detail

    @staticmethod
    def to_admin_dto(project: Project) -> ProjectAdminDTO:
        detail = project.detail
        gallery = (
            GalleryImage.query.filter_by(project_id=project.id, is_active=True)
            .order_by(GalleryImage.sort_order)
            .all()
        )
        created = project.created_at.strftime("%d %b %Y") if project.created_at else ""
        updated = project.updated_at.strftime("%d %b %Y") if project.updated_at else ""
        return ProjectAdminDTO(
            id=project.id,
            title=project.title,
            slug=project.slug,
            description=project.description,
            location=project.location or "",
            country=project.country or "",
            county=project.county or "",
            status=project.status or "",
            client=project.client or "",
            category=project.category or "",
            cover_image=project.cover_image or "",
            completion_date=project.completion_date or "",
            sort_order=project.sort_order or 0,
            is_featured=project.is_featured,
            is_active=project.is_active,
            meta_title=detail.meta_title if detail else "",
            meta_description=detail.meta_description if detail else "",
            og_image=detail.og_image if detail else "",
            canonical_url=detail.canonical_url if detail else "",
            overview=detail.overview if detail else "",
            consultant=detail.consultant if detail else "",
            duration=detail.duration if detail else "",
            completion_year=detail.completion_year if detail else "",
            challenges=_json_list(detail.challenges_json if detail else "[]"),
            solutions=_json_list(detail.solutions_json if detail else "[]"),
            scope_of_work=_json_list(detail.scope_of_work_json if detail else "[]"),
            timeline=_parse_timeline(detail.timeline_json if detail else "[]"),
            service_slugs=_json_list(detail.service_slugs_json if detail else "[]"),
            equipment=_json_list(detail.equipment_json if detail else "[]"),
            team_member_ids=[int(x) for x in _json_list(detail.team_member_ids_json if detail else "[]") if str(x).isdigit()],
            related_project_ids=[int(x) for x in _json_list(detail.related_project_ids_json if detail else "[]") if str(x).isdigit()],
            related_service_slugs=_json_list(detail.related_service_slugs_json if detail else "[]"),
            document_paths=_json_list(detail.document_paths_json if detail else "[]"),
            gallery_paths=[g.image for g in gallery],
            created_at_label=created,
            updated_at_label=updated,
        )

    @staticmethod
    def to_list_item(project: Project) -> ProjectListItemDTO:
        year = ""
        if project.detail and project.detail.completion_year:
            year = project.detail.completion_year
        elif project.completion_date:
            year = project.completion_date[:4]
        return ProjectListItemDTO(
            id=project.id,
            title=project.title,
            slug=project.slug,
            country=project.country or "",
            county=project.county or "",
            status=project.status or "",
            category=project.category or "",
            client=project.client or "",
            completion_year=year,
            is_featured=project.is_featured,
            is_active=project.is_active,
            cover_image=project.cover_image or "",
            sort_order=project.sort_order or 0,
        )

    @staticmethod
    def get_project(project_id: int, include_inactive: bool = False) -> Project | None:
        try:
            query = Project.query.filter_by(id=project_id)
            if not include_inactive:
                query = query.filter_by(is_active=True)
            return query.first()
        except SQLAlchemyError as exc:
            current_app.logger.error("get_project failed: %s", exc)
            return None

    @staticmethod
    def get_by_slug(slug: str, exclude_id: int | None = None) -> Project | None:
        query = Project.query.filter_by(slug=slug)
        if exclude_id:
            query = query.filter(Project.id != exclude_id)
        return query.first()

    @staticmethod
    def ensure_unique_slug(base: str, exclude_id: int | None = None) -> str:
        slug = slugify(base) or "project"
        candidate = slug
        counter = 2
        while ProjectsAdminProvider.get_by_slug(candidate, exclude_id=exclude_id):
            candidate = f"{slug}-{counter}"
            counter += 1
        return candidate

    @staticmethod
    def query_projects(
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
        per_page: int = 20,
        include_deleted: bool = False,
    ) -> tuple[list[Project], int]:
        try:
            query = Project.query
            if include_deleted:
                query = query.filter(Project.is_active.is_(False))
            else:
                query = query.filter(Project.is_active.is_(True))

            if q:
                term = f"%{q.strip()}%"
                query = query.filter(
                    or_(
                        Project.title.ilike(term),
                        Project.slug.ilike(term),
                        Project.client.ilike(term),
                        Project.location.ilike(term),
                    )
                )
            if country:
                query = query.filter(Project.country == country)
            if county:
                query = query.filter(Project.county == county)
            if status:
                query = query.filter(Project.status == status)
            if category:
                query = query.filter(Project.category == category)
            if client:
                query = query.filter(Project.client == client)
            if service or year:
                query = query.outerjoin(ProjectDetail, ProjectDetail.project_id == Project.id)
            if service:
                query = query.filter(ProjectDetail.service_slugs_json.ilike(f'%{service}%'))
            if year:
                query = query.filter(
                    or_(
                        ProjectDetail.completion_year == year,
                        Project.completion_date.ilike(f"{year}%"),
                    )
                )

            sort_map = {
                "date_desc": desc(Project.created_at),
                "date_asc": asc(Project.created_at),
                "title_asc": asc(Project.title),
                "title_desc": desc(Project.title),
                "sort_order": asc(Project.sort_order),
            }
            query = query.order_by(sort_map.get(sort, desc(Project.created_at)))

            total = query.count()
            items = query.offset((page - 1) * per_page).limit(per_page).all()
            return items, total
        except SQLAlchemyError as exc:
            current_app.logger.error("query_projects failed: %s", exc)
            return [], 0

    @staticmethod
    def get_stats() -> dict:
        try:
            total = Project.query.count()
            active = Project.query.filter_by(is_active=True).count()
            featured = Project.query.filter_by(is_active=True, is_featured=True).count()
            by_country = dict(
                db.session.query(Project.country, func.count(Project.id))
                .filter(Project.is_active.is_(True))
                .group_by(Project.country)
                .all()
            )
            by_status = dict(
                db.session.query(Project.status, func.count(Project.id))
                .filter(Project.is_active.is_(True))
                .group_by(Project.status)
                .all()
            )
            recent = (
                Project.query.filter_by(is_active=True)
                .order_by(desc(Project.updated_at))
                .limit(6)
                .all()
            )
            return {
                "total": total,
                "active": active,
                "featured": featured,
                "by_country": by_country,
                "by_status": by_status,
                "recent": recent,
            }
        except SQLAlchemyError as exc:
            current_app.logger.error("get_stats failed: %s", exc)
            return {"total": 0, "active": 0, "featured": 0, "by_country": {}, "by_status": {}, "recent": []}

    @staticmethod
    def save_from_dto(dto: ProjectAdminDTO) -> Project:
        slug = ProjectsAdminProvider.ensure_unique_slug(dto.slug or dto.title, dto.id)

        if dto.id:
            project = ProjectsAdminProvider.get_project(dto.id, include_inactive=True)
            if not project:
                raise ValueError("Project not found.")
        else:
            project = Project(
                title=dto.title.strip(),
                slug=slug,
                description=dto.description.strip(),
            )
            db.session.add(project)

        project.title = dto.title.strip()
        project.slug = slug
        project.description = dto.description.strip()
        project.location = dto.location.strip()
        project.country = dto.country.strip()
        project.county = dto.county.strip()
        project.status = dto.status.strip()
        project.client = dto.client.strip()
        project.category = dto.category.strip()
        project.cover_image = dto.cover_image.strip()
        project.completion_date = dto.completion_date.strip() or dto.completion_year
        project.sort_order = dto.sort_order
        project.is_featured = dto.is_featured
        project.is_active = dto.is_active

        db.session.flush()

        detail = ProjectsAdminProvider.get_or_create_detail(project)
        detail.meta_title = dto.meta_title.strip()
        detail.meta_description = dto.meta_description.strip()
        detail.og_image = dto.og_image.strip()
        detail.canonical_url = dto.canonical_url.strip()
        detail.overview = dto.overview.strip()
        detail.consultant = dto.consultant.strip()
        detail.duration = dto.duration.strip()
        detail.completion_year = dto.completion_year.strip()
        detail.challenges_json = _dump_json(dto.challenges)
        detail.solutions_json = _dump_json(dto.solutions)
        detail.scope_of_work_json = _dump_json(dto.scope_of_work)
        detail.timeline_json = _dump_json(
            [{"date": t.date, "title": t.title, "description": t.description} for t in dto.timeline]
        )
        detail.service_slugs_json = _dump_json(dto.service_slugs)
        detail.equipment_json = _dump_json(dto.equipment)
        detail.team_member_ids_json = _dump_json(dto.team_member_ids)
        detail.related_project_ids_json = _dump_json(dto.related_project_ids)
        detail.related_service_slugs_json = _dump_json(dto.related_service_slugs)
        detail.document_paths_json = _dump_json(dto.document_paths)

        ProjectsAdminProvider.sync_gallery(project, dto.gallery_paths)
        return project

    @staticmethod
    def sync_gallery(project: Project, paths: list[str]) -> None:
        paths = [p.strip() for p in paths if p and p.strip()]
        existing = GalleryImage.query.filter_by(project_id=project.id).all()
        existing_map = {g.image: g for g in existing}

        for idx, path in enumerate(paths):
            if path in existing_map:
                row = existing_map[path]
                row.is_active = True
                row.sort_order = idx
            else:
                db.session.add(
                    GalleryImage(
                        title=f"{project.title} — Image {idx + 1}",
                        image=path,
                        category=project.category or "",
                        project_id=project.id,
                        sort_order=idx,
                        is_active=True,
                    )
                )

        for image, row in existing_map.items():
            if image not in paths:
                row.is_active = False

    @staticmethod
    def soft_delete(project: Project) -> None:
        project.is_active = False
        detail = ProjectsAdminProvider.get_or_create_detail(project)
        detail.mark_deleted()
        GalleryImage.query.filter_by(project_id=project.id).update({"is_active": False})

    @staticmethod
    def restore(project: Project) -> None:
        project.is_active = True
        if project.detail:
            project.detail.restore()
        GalleryImage.query.filter_by(project_id=project.id).update({"is_active": True})

    @staticmethod
    def list_services() -> list[Service]:
        return Service.query.filter_by(is_active=True).order_by(Service.title).all()

    @staticmethod
    def list_team() -> list[TeamMember]:
        return TeamMember.query.filter_by(is_active=True).order_by(TeamMember.name).all()

    @staticmethod
    def list_projects_for_related(exclude_id: int | None = None) -> list[Project]:
        query = Project.query.filter_by(is_active=True).order_by(Project.title)
        if exclude_id:
            query = query.filter(Project.id != exclude_id)
        return query.all()

    @staticmethod
    def list_media_assets(folder: str = "projects") -> list:
        from app.models.media import MediaAsset

        return (
            MediaAsset.query.filter_by(is_active=True, folder=folder)
            .order_by(desc(MediaAsset.created_at))
            .limit(200)
            .all()
        )

    @staticmethod
    def bulk_update(project_ids: list[int], action: str) -> int:
        count = 0
        projects = Project.query.filter(Project.id.in_(project_ids)).all()
        for project in projects:
            if action == "feature":
                project.is_featured = True
                count += 1
            elif action == "unfeature":
                project.is_featured = False
                count += 1
            elif action == "activate":
                ProjectsAdminProvider.restore(project)
                count += 1
            elif action == "deactivate":
                ProjectsAdminProvider.soft_delete(project)
                count += 1
            elif action == "restore":
                ProjectsAdminProvider.restore(project)
                count += 1
        return count

    @staticmethod
    def lines_to_list(text: str) -> list[str]:
        return _lines_to_list(text)

    @staticmethod
    def parse_timeline_text(text: str) -> list[ProjectTimelineItemDTO]:
        items = []
        for line in _lines_to_list(text):
            parts = line.split("|", 2)
            if len(parts) == 3:
                items.append(ProjectTimelineItemDTO(parts[0].strip(), parts[1].strip(), parts[2].strip()))
            elif len(parts) == 2:
                items.append(ProjectTimelineItemDTO(parts[0].strip(), parts[1].strip(), ""))
        return items

    @staticmethod
    def timeline_to_text(timeline: list[ProjectTimelineItemDTO]) -> str:
        lines = []
        for item in timeline:
            lines.append(f"{item.date}|{item.title}|{item.description}")
        return "\n".join(lines)
