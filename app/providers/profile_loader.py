"""
Maps official company profile data to DTOs for providers and services.

Reads from app.data.company_profile until MySQL records are seeded.
"""

from app.constants.media import FALLBACK_IMAGES
from app.data.company_profile import COMPANY_PROFILE
from app.data.projects_catalog import PROJECTS_CATALOG
from app.data.services_catalog import SERVICES_CATALOG
from app.schemas.content import (
    AboutSectionDTO,
    CertificationDTO,
    CompanyInfoDTO,
    CompanyProfileDTO,
    CoreValueDTO,
    DirectorDTO,
    DirectorsMessageDTO,
    EquipmentItemDTO,
    HsePolicyDTO,
    ProjectDTO,
    ServiceDTO,
    StatisticDTO,
    TeamMemberDTO,
)


def build_company_profile_dto() -> CompanyProfileDTO:
    """Return the full official company profile as a DTO."""
    msg = COMPANY_PROFILE["directors_message"]
    hse = COMPANY_PROFILE["hse_policy"]
    geo = COMPANY_PROFILE.get("geography", {})
    hq = COMPANY_PROFILE.get("headquarters", {})

    return CompanyProfileDTO(
        overview=COMPANY_PROFILE["company_overview"],
        introduction=COMPANY_PROFILE["company_introduction"],
        about=COMPANY_PROFILE["about_the_company"],
        history=COMPANY_PROFILE["company_history"],
        experience=COMPANY_PROFILE["company_experience"],
        equipment_overview=COMPANY_PROFILE["equipment_overview"],
        vision=COMPANY_PROFILE["vision"],
        mission=COMPANY_PROFILE["mission"],
        founded_country=geo.get("founded_country", ""),
        founded_country_code=geo.get("founded_country_code", ""),
        operating_country=geo.get("operating_country", ""),
        operating_country_code=geo.get("operating_country_code", ""),
        headquarters=hq.get("summary", ""),
        directors_message=DirectorsMessageDTO(
            heading=msg["heading"],
            signatories=list(msg["signatories"]),
            summary=msg["summary"],
        ),
        core_values=[
            CoreValueDTO(title=v["title"], description=v["description"])
            for v in COMPANY_PROFILE["core_values"]
        ],
        hse_policy=HsePolicyDTO(
            principle=hse["principle"],
            summary=hse["summary"],
            commitments=list(hse["commitments"]),
        ),
        strengths=list(COMPANY_PROFILE["company_strengths"]),
        certifications=[
            CertificationDTO(
                title=c["title"],
                issuer=c["issuer"],
                reference=c["reference"],
                category=c["category"],
                valid_until=c.get("valid_until", ""),
                notes=c.get("notes", ""),
            )
            for c in COMPANY_PROFILE["certifications"]
        ],
        equipment=[
            EquipmentItemDTO(
                name=e["name"],
                category=e["category"],
                description=e.get("description", ""),
            )
            for e in COMPANY_PROFILE["equipment"]
        ],
        directors=[
            DirectorDTO(name=d["name"], role=d["role"], bio=d.get("bio", ""))
            for d in COMPANY_PROFILE["directors"]
        ],
        source_document=COMPANY_PROFILE.get("source_document", ""),
        last_extracted=COMPANY_PROFILE.get("last_extracted", ""),
    )


def phone_to_tel(phone: str) -> str:
    """Normalize a display phone number for tel: hyperlinks."""
    return "".join(ch for ch in phone if ch.isdigit() or ch == "+")


def build_company_info_dto() -> CompanyInfoDTO:
    contact = COMPANY_PROFILE["contact"]
    geo = COMPANY_PROFILE.get("geography", {})
    hq = COMPANY_PROFILE.get("headquarters", {})
    phone_primary = contact["phone_primary"]
    phone_secondary = contact.get("phone_secondary", "")
    phone_display = (
        f"{phone_primary} / {phone_secondary}" if phone_secondary else phone_primary
    )
    postal_address = contact.get("postal_address", "")
    address = contact["address"]
    full_address = f"{address}. {postal_address}" if postal_address else address
    operating_country = geo.get("operating_country", contact.get("address_country", ""))
    operating_country_code = geo.get(
        "operating_country_code", contact.get("address_country_code", "")
    )

    return CompanyInfoDTO(
        name=contact["company_name"],
        short_name=contact["short_name"],
        tagline=contact["tagline"],
        description=COMPANY_PROFILE["company_overview"],
        phone=phone_display,
        phone_primary=phone_primary,
        phone_secondary=phone_secondary,
        phone_tel=phone_to_tel(phone_primary),
        email=contact["email"],
        address=full_address,
        head_office_label=contact.get("head_office_label", hq.get("label", "Head Office")),
        postal_address=postal_address,
        address_area=contact.get("address_area", hq.get("area", "")),
        address_district=contact.get("address_district", hq.get("district", "")),
        address_locality=contact.get("address_locality", hq.get("locality", "")),
        address_country=operating_country,
        address_country_code=operating_country_code,
        founded_country=geo.get("founded_country", ""),
        founded_country_code=geo.get("founded_country_code", ""),
        operating_country=operating_country,
        operating_country_code=operating_country_code,
        headquarters=hq.get("summary", full_address),
        office_hours=contact["office_hours"],
        logo_path="img/logo.png",
    )


def build_services() -> list[ServiceDTO]:
    return [
        ServiceDTO(
            id=i + 1,
            title=s["title"],
            slug=s["slug"],
            short_description=s["short_description"],
            description=s["description"],
            icon=s["icon"],
            image=s.get("image", FALLBACK_IMAGES["service"]),
            sort_order=i + 1,
            is_featured=s.get("is_featured", False),
        )
        for i, s in enumerate(SERVICES_CATALOG)
    ]


def _catalog_to_project_dto(p: dict, index: int) -> ProjectDTO:
    category_fallback = {
        "Water Works": FALLBACK_IMAGES["service"],
        "Building Works": FALLBACK_IMAGES["about"],
        "Road Works": FALLBACK_IMAGES["project"],
        "Civil Engineering": FALLBACK_IMAGES["project"],
    }
    cover = p.get("cover_image") or category_fallback.get(p["category"], FALLBACK_IMAGES["project"])
    return ProjectDTO(
        id=index + 1,
        title=p["title"],
        slug=p["slug"],
        description=p["description"],
        location=p["location"],
        client=p.get("client", ""),
        category=p["category"],
        cover_image=cover,
        completion_date=p.get("completion_date", ""),
        sort_order=index + 1,
        is_featured=p.get("is_featured", False),
        county=p.get("county", ""),
        country=p.get("country", ""),
        status=p.get("status", ""),
        completion_year=p.get("completion_year", ""),
        service_slugs=list(p.get("service_slugs", [])),
        consultant=p.get("consultant", ""),
        duration=p.get("duration", ""),
        overview=p.get("overview", ""),
        scope_of_work=list(p.get("scope_of_work", [])),
        challenges=list(p.get("challenges", [])),
        solutions=list(p.get("solutions", [])),
        equipment_used=list(p.get("equipment_used", [])),
        gallery_images=list(p.get("gallery_images", [])),
        gallery_categories=list(p.get("gallery_categories", [])),
        related_project_slugs=list(p.get("related_project_slugs", [])),
        meta_title=p.get("meta_title", p["title"]),
        meta_description=p.get("meta_description", p["description"]),
    )


def build_projects() -> list[ProjectDTO]:
    return [_catalog_to_project_dto(p, i) for i, p in enumerate(PROJECTS_CATALOG)]


def build_project_by_slug(slug: str) -> ProjectDTO | None:
    for i, p in enumerate(PROJECTS_CATALOG):
        if p["slug"] == slug:
            return _catalog_to_project_dto(p, i)
    return None


def build_directors_as_team() -> list[TeamMemberDTO]:
    return [
        TeamMemberDTO(
            id=i + 1,
            name=d["name"],
            position=d["role"],
            bio=d.get("bio", ""),
            photo="",
            email=COMPANY_PROFILE["contact"]["email"] if i == 0 else "",
            sort_order=i + 1,
        )
        for i, d in enumerate(COMPANY_PROFILE["directors"])
    ]


def build_statistics() -> list[StatisticDTO]:
    return [
        StatisticDTO(
            id=i + 1,
            label=s["label"],
            value=s["value"],
            suffix=s.get("suffix", ""),
            icon=s.get("icon", ""),
            sort_order=i + 1,
        )
        for i, s in enumerate(COMPANY_PROFILE["statistics"])
    ]


def build_about_section(page_slug: str) -> AboutSectionDTO | None:
    if page_slug == "home":
        return AboutSectionDTO(
            id=1,
            heading="About GURUH Construction",
            subheading="Who We Are",
            content=COMPANY_PROFILE["company_introduction"],
            image=FALLBACK_IMAGES["about"],
            highlights=COMPANY_PROFILE["company_strengths"][:4],
            cta_text="Learn More",
            cta_url="/about",
        )
    if page_slug == "about":
        return AboutSectionDTO(
            id=2,
            heading="Our Story",
            subheading="Building With Purpose Since 2008",
            content=COMPANY_PROFILE["company_history"],
            image=FALLBACK_IMAGES["about"],
            highlights=[
                "Established 2008",
                "Incorporated 2013",
                "NCA2 Road Works Contractor",
                "Qualified Water Resource Contractor",
            ],
            cta_text="Contact Us",
            cta_url="/contact",
        )
    return None
