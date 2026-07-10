"""Team admin data provider — MySQL / SQLAlchemy."""

from __future__ import annotations

import json
import re
import unicodedata

from flask import current_app
from sqlalchemy import asc, desc, func, or_
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models.catalog import Project, Service, TeamMember
from app.models.equipment import Equipment
from app.models.team_detail import TeamDetail
from app.providers.auth_provider import AuthProvider
from app.schemas.team_admin import TeamAdminDTO, TeamListItemDTO, TeamSocialLinkDTO


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


def _parse_social_links(raw: str | None) -> list[TeamSocialLinkDTO]:
    items = []
    for entry in _json_list(raw):
        if isinstance(entry, dict):
            items.append(
                TeamSocialLinkDTO(
                    platform=str(entry.get("platform", "")),
                    url=str(entry.get("url", "")),
                    icon=str(entry.get("icon", "")),
                )
            )
    return items


class TeamAdminProvider:
    """Database operations for team member CRUD."""

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
    def get_or_create_detail(member: TeamMember, slug: str = "") -> TeamDetail:
        if member.detail:
            return member.detail
        detail = TeamDetail(
            team_member_id=member.id,
            slug=slug or slugify(member.name) or f"member-{member.id}",
        )
        db.session.add(detail)
        return detail

    @staticmethod
    def to_admin_dto(member: TeamMember) -> TeamAdminDTO:
        detail = member.detail
        created = member.created_at.strftime("%d %b %Y") if member.created_at else ""
        updated = member.updated_at.strftime("%d %b %Y") if member.updated_at else ""
        return TeamAdminDTO(
            id=member.id,
            name=member.name,
            slug=detail.slug if detail else "",
            position=member.position or "",
            department=detail.department if detail else "",
            member_type=detail.member_type if detail else "staff",
            bio=member.bio or "",
            photo=member.photo or "",
            email=member.email or "",
            phone=member.phone or "",
            years_experience=detail.years_experience if detail else "",
            education=detail.education if detail else "",
            experience_summary=detail.experience_summary if detail else "",
            sort_order=member.sort_order or 0,
            is_featured=detail.is_featured if detail else False,
            is_active=member.is_active,
            meta_title=detail.meta_title if detail else "",
            meta_description=detail.meta_description if detail else "",
            og_image=detail.og_image if detail else "",
            canonical_url=detail.canonical_url if detail else "",
            social_links=_parse_social_links(detail.social_links_json if detail else "[]"),
            gallery_paths=_json_list(detail.gallery_paths_json if detail else "[]"),
            related_project_ids=[
                int(x)
                for x in _json_list(detail.related_project_ids_json if detail else "[]")
                if str(x).isdigit()
            ],
            related_service_slugs=_json_list(detail.related_service_slugs_json if detail else "[]"),
            related_equipment_ids=[
                int(x)
                for x in _json_list(detail.related_equipment_ids_json if detail else "[]")
                if str(x).isdigit()
            ],
            created_at_label=created,
            updated_at_label=updated,
        )

    @staticmethod
    def to_list_item(member: TeamMember) -> TeamListItemDTO:
        detail = member.detail
        updated = member.updated_at.strftime("%d %b %Y") if member.updated_at else ""
        return TeamListItemDTO(
            id=member.id,
            name=member.name,
            slug=detail.slug if detail else "",
            position=member.position or "",
            department=detail.department if detail else "",
            member_type=detail.member_type if detail else "",
            photo=member.photo or "",
            sort_order=member.sort_order or 0,
            is_featured=detail.is_featured if detail else False,
            is_active=member.is_active,
            updated_at_label=updated,
        )

    @staticmethod
    def get_member(member_id: int, include_inactive: bool = False) -> TeamMember | None:
        try:
            query = TeamMember.query.filter_by(id=member_id)
            if not include_inactive:
                query = query.filter_by(is_active=True)
            return query.first()
        except SQLAlchemyError as exc:
            current_app.logger.error("get_member failed: %s", exc)
            return None

    @staticmethod
    def get_by_slug(slug: str, exclude_id: int | None = None) -> TeamDetail | None:
        query = TeamDetail.query.filter_by(slug=slug)
        if exclude_id:
            query = query.filter(TeamDetail.team_member_id != exclude_id)
        return query.first()

    @staticmethod
    def ensure_unique_slug(base: str, exclude_member_id: int | None = None) -> str:
        slug = slugify(base) or "team-member"
        candidate = slug
        counter = 2
        while TeamAdminProvider.get_by_slug(candidate, exclude_id=exclude_member_id):
            candidate = f"{slug}-{counter}"
            counter += 1
        return candidate

    @staticmethod
    def query_members(
        *,
        q: str = "",
        department: str = "",
        position: str = "",
        member_type: str = "",
        featured: str = "",
        status: str = "",
        sort: str = "date_desc",
        page: int = 1,
        per_page: int = 20,
        include_deleted: bool = False,
    ) -> tuple[list[TeamMember], int]:
        try:
            query = TeamMember.query.outerjoin(TeamDetail, TeamDetail.team_member_id == TeamMember.id)

            if include_deleted:
                query = query.filter(TeamMember.is_active.is_(False))
            elif status == "all":
                pass
            elif status == "inactive":
                query = query.filter(TeamMember.is_active.is_(False))
            else:
                query = query.filter(TeamMember.is_active.is_(True))

            if q:
                term = f"%{q.strip()}%"
                query = query.filter(
                    or_(
                        TeamMember.name.ilike(term),
                        TeamMember.position.ilike(term),
                        TeamMember.email.ilike(term),
                        TeamDetail.slug.ilike(term),
                        TeamDetail.department.ilike(term),
                    )
                )
            if department:
                query = query.filter(TeamDetail.department == department)
            if position:
                query = query.filter(TeamMember.position == position)
            if member_type:
                query = query.filter(TeamDetail.member_type == member_type)
            if featured == "yes":
                query = query.filter(TeamDetail.is_featured.is_(True))
            elif featured == "no":
                query = query.filter(TeamDetail.is_featured.is_(False))

            sort_map = {
                "date_desc": desc(TeamMember.updated_at),
                "date_asc": asc(TeamMember.updated_at),
                "name_asc": asc(TeamMember.name),
                "name_desc": desc(TeamMember.name),
                "sort_order": asc(TeamMember.sort_order),
            }
            query = query.order_by(sort_map.get(sort, desc(TeamMember.updated_at)))

            total = query.count()
            items = query.offset((page - 1) * per_page).limit(per_page).all()
            return items, total
        except SQLAlchemyError as exc:
            current_app.logger.error("query_members failed: %s", exc)
            return [], 0

    @staticmethod
    def get_stats() -> dict:
        try:
            total = TeamMember.query.count()
            active = TeamMember.query.filter_by(is_active=True).count()
            inactive = total - active

            def _count_type(member_type: str) -> int:
                return (
                    db.session.query(func.count(TeamMember.id))
                    .join(TeamDetail, TeamDetail.team_member_id == TeamMember.id)
                    .filter(TeamMember.is_active.is_(True), TeamDetail.member_type == member_type)
                    .scalar()
                    or 0
                )

            directors = _count_type("director")
            management = _count_type("executive")
            staff = _count_type("staff")
            recent = TeamMember.query.order_by(desc(TeamMember.updated_at)).limit(6).all()
            return {
                "total": total,
                "active": active,
                "inactive": inactive,
                "directors": directors,
                "management": management,
                "staff": staff,
                "recent": recent,
            }
        except SQLAlchemyError as exc:
            current_app.logger.error("get_stats failed: %s", exc)
            return {
                "total": 0,
                "active": 0,
                "inactive": 0,
                "directors": 0,
                "management": 0,
                "staff": 0,
                "recent": [],
            }

    @staticmethod
    def save_from_dto(dto: TeamAdminDTO) -> TeamMember:
        slug = TeamAdminProvider.ensure_unique_slug(dto.slug or dto.name, dto.id)

        if dto.id:
            member = TeamAdminProvider.get_member(dto.id, include_inactive=True)
            if not member:
                raise ValueError("Team member not found.")
        else:
            member = TeamMember(
                name=dto.name.strip(),
                position=dto.position.strip(),
                bio=dto.bio.strip(),
            )
            db.session.add(member)

        member.name = dto.name.strip()
        member.position = dto.position.strip()
        member.bio = dto.bio.strip()
        member.photo = dto.photo.strip()
        member.email = dto.email.strip()
        member.phone = dto.phone.strip()
        member.sort_order = dto.sort_order
        member.is_active = dto.is_active

        db.session.flush()

        detail = TeamAdminProvider.get_or_create_detail(member, slug)
        detail.slug = slug
        detail.department = dto.department.strip()
        detail.member_type = dto.member_type.strip() or "staff"
        detail.years_experience = dto.years_experience.strip()
        detail.education = dto.education.strip()
        detail.experience_summary = dto.experience_summary.strip()
        detail.is_featured = dto.is_featured
        detail.meta_title = dto.meta_title.strip()
        detail.meta_description = dto.meta_description.strip()
        detail.og_image = dto.og_image.strip()
        detail.canonical_url = dto.canonical_url.strip()
        detail.social_links_json = _dump_json(
            [{"platform": s.platform, "url": s.url, "icon": s.icon} for s in dto.social_links]
        )
        detail.gallery_paths_json = _dump_json(dto.gallery_paths)
        detail.related_project_ids_json = _dump_json(dto.related_project_ids)
        detail.related_service_slugs_json = _dump_json(dto.related_service_slugs)
        detail.related_equipment_ids_json = _dump_json(dto.related_equipment_ids)

        return member

    @staticmethod
    def soft_delete(member: TeamMember) -> None:
        member.is_active = False
        detail = TeamAdminProvider.get_or_create_detail(member)
        detail.mark_deleted()

    @staticmethod
    def restore(member: TeamMember) -> None:
        member.is_active = True
        if member.detail:
            member.detail.restore()

    @staticmethod
    def list_projects() -> list[Project]:
        return Project.query.filter_by(is_active=True).order_by(Project.title).all()

    @staticmethod
    def list_services() -> list[Service]:
        return Service.query.filter_by(is_active=True).order_by(Service.title).all()

    @staticmethod
    def list_equipment() -> list[Equipment]:
        return Equipment.query.filter_by(is_active=True).order_by(Equipment.name).all()

    @staticmethod
    def list_media_assets(folder: str = "team") -> list:
        from app.models.media import MediaAsset

        return (
            MediaAsset.query.filter_by(is_active=True, folder=folder)
            .order_by(desc(MediaAsset.created_at))
            .limit(200)
            .all()
        )

    @staticmethod
    def bulk_update(member_ids: list[int], action: str) -> int:
        count = 0
        members = TeamMember.query.filter(TeamMember.id.in_(member_ids)).all()
        for member in members:
            if action == "feature":
                detail = TeamAdminProvider.get_or_create_detail(member)
                detail.is_featured = True
                count += 1
            elif action == "unfeature":
                if member.detail:
                    member.detail.is_featured = False
                count += 1
            elif action == "activate":
                TeamAdminProvider.restore(member)
                count += 1
            elif action == "deactivate":
                TeamAdminProvider.soft_delete(member)
                count += 1
            elif action == "restore":
                TeamAdminProvider.restore(member)
                count += 1
        return count

    @staticmethod
    def parse_social_links_text(text: str) -> list[TeamSocialLinkDTO]:
        items = []
        for line in (text or "").splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split("|", 2)
            if len(parts) >= 2:
                icon = parts[2].strip() if len(parts) == 3 else f"bi-{parts[0].strip()}"
                items.append(TeamSocialLinkDTO(parts[0].strip(), parts[1].strip(), icon))
        return items

    @staticmethod
    def social_links_to_text(links: list[TeamSocialLinkDTO]) -> str:
        lines = []
        for link in links:
            icon = link.icon or f"bi-{link.platform}"
            lines.append(f"{link.platform}|{link.url}|{icon}")
        return "\n".join(lines)
