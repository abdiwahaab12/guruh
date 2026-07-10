"""Maps team catalog data to TeamMemberDTO for providers and services."""

from app.data.team_catalog import TEAM_CATALOG
from app.schemas.content import TeamMemberDTO


def build_team_members() -> list[TeamMemberDTO]:
    return [_catalog_to_dto(m, i) for i, m in enumerate(TEAM_CATALOG)]


def build_team_by_type(member_type: str) -> list[TeamMemberDTO]:
    return [dto for dto in build_team_members() if dto.member_type == member_type and dto.is_active]


def _catalog_to_dto(member: dict, index: int) -> TeamMemberDTO:
    return TeamMemberDTO(
        id=index + 1,
        name=member["name"],
        slug=member.get("slug", ""),
        position=member["position"],
        bio=member.get("bio", ""),
        photo=member.get("photo", ""),
        email=member.get("email", ""),
        phone=member.get("phone", ""),
        department=member.get("department", ""),
        member_type=member.get("member_type", ""),
        years_experience=str(member.get("years_experience", "")),
        education=member.get("education", ""),
        experience_summary=member.get("experience_summary", ""),
        social_links=list(member.get("social_links", [])),
        sort_order=member.get("sort_order", index + 1),
        is_featured=member.get("is_featured", False),
        is_active=member.get("is_active", True),
    )
