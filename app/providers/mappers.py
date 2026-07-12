"""
Maps SQLAlchemy models to DTOs for template consumption.

Keeps ORM details out of services and templates.
"""

from app.models.catalog import (
    ContactPageContent,
    GalleryImage,
    JobListing,
    Project,
    QuotePageContent,
    Service,
    TeamMember,
    Testimonial,
)
from app.models.cms import AboutSection, CTASection, HeroSlide, Page, Partner, ProcessStep, SectionHeading, Statistic, TrustBadge, WhyChooseUsItem, WhyChooseUsSection, WorkingProcessSection
from app.models.site import CompanyInfo, FooterContent, NavItem, OfficeLocation, SocialLink
from app.schemas.content import (
    AboutSectionDTO,
    CompanyInfoDTO,
    ContactPageDTO,
    CTASectionDTO,
    FooterContentDTO,
    GalleryImageDTO,
    HeroSlideDTO,
    JobListingDTO,
    NavItemDTO,
    OfficeLocationDTO,
    PageMetaDTO,
    PartnerDTO,
    ProjectDTO,
    QuotePageDTO,
    SectionHeadingDTO,
    ServiceDTO,
    SocialLinkDTO,
    StatisticDTO,
    TeamMemberDTO,
    TestimonialDTO,
    WhyChooseUsSectionDTO,
    WorkingProcessSectionDTO,
    FeatureItemDTO,
    ProcessStepDTO,
    TrustBadgeDTO,
)


def company_to_dto(row: CompanyInfo) -> CompanyInfoDTO:
    from app.providers import profile_loader

    seeded = profile_loader.build_company_info_dto()
    return CompanyInfoDTO(
        name=row.name,
        short_name=row.short_name,
        tagline=row.tagline,
        description=row.description,
        phone=row.phone,
        phone_primary=seeded.phone_primary,
        phone_secondary=seeded.phone_secondary,
        phone_tel=profile_loader.phone_to_tel(row.phone.split(" / ")[0] if " / " in row.phone else row.phone),
        email=row.email,
        address=row.address,
        office_hours=row.office_hours,
        head_office_label=seeded.head_office_label,
        postal_address=seeded.postal_address,
        address_area=seeded.address_area,
        address_district=seeded.address_district,
        address_locality=seeded.address_locality,
        address_country=seeded.address_country,
        address_country_code=seeded.address_country_code,
        founded_country=getattr(row, "founded_country", None) or seeded.founded_country,
        founded_country_code=getattr(row, "founded_country_code", None) or seeded.founded_country_code,
        operating_country=getattr(row, "operating_country", None) or seeded.operating_country,
        operating_country_code=getattr(row, "operating_country_code", None) or seeded.operating_country_code,
        headquarters=getattr(row, "headquarters", None) or seeded.headquarters,
        logo_path=row.logo_path or "img/logo.png",
    )


def office_to_dto(row: OfficeLocation) -> OfficeLocationDTO:
    from app.providers.profile_loader import phone_to_tel

    return OfficeLocationDTO(
        id=row.id,
        slug=row.slug,
        name=row.name,
        office_label=row.office_label,
        address=row.address,
        postal_address=row.postal_address or "",
        phone_primary=row.phone_primary,
        phone_secondary=row.phone_secondary or "",
        phone_tel=phone_to_tel(row.phone_primary),
        email=row.email,
        office_hours=row.office_hours or "",
        address_area=row.address_area or "",
        address_locality=row.address_locality or "",
        address_district=row.address_district or "",
        address_country=row.country,
        address_country_code=row.country_code,
        is_headquarters=row.is_headquarters,
        show_on_contact_page=row.show_on_contact_page,
        sort_order=row.sort_order,
        is_active=row.is_active,
    )


def nav_to_dto(row: NavItem) -> NavItemDTO:
    return NavItemDTO(
        id=row.id,
        label=row.label,
        endpoint=row.endpoint,
        sort_order=row.sort_order,
        is_active=row.is_active,
    )


def social_to_dto(row: SocialLink) -> SocialLinkDTO:
    return SocialLinkDTO(
        id=row.id,
        platform=row.platform,
        label=row.label,
        icon=row.icon,
        url=row.url,
        sort_order=row.sort_order,
        is_active=row.is_active,
    )


def footer_to_dto(row: FooterContent, quick_links: list[NavItemDTO], services: list[ServiceDTO]) -> FooterContentDTO:
    return FooterContentDTO(
        copyright_text=row.copyright_text,
        about_text=row.about_text,
        quick_links=quick_links,
        service_links=services,
    )


def page_to_dto(row: Page) -> PageMetaDTO:
    return PageMetaDTO(
        slug=row.slug,
        title=row.title,
        meta_title=row.meta_title,
        meta_description=row.meta_description,
        is_published=row.is_published,
        banner_subtitle=row.banner_subtitle or "",
        banner_image=row.banner_image or "",
    )


def hero_to_dto(row: HeroSlide) -> HeroSlideDTO:
    opacity = getattr(row, "overlay_opacity", None)
    if opacity is None:
        opacity = 0.65
    return HeroSlideDTO(
        id=row.id,
        title=row.title,
        subtitle=row.subtitle or "",
        description=row.description or "",
        image=row.image or "",
        cta_text=row.cta_text or "",
        cta_url=row.cta_url or "",
        sort_order=row.sort_order,
        is_active=row.is_active,
        secondary_cta_text=getattr(row, "secondary_cta_text", None) or "",
        secondary_cta_url=getattr(row, "secondary_cta_url", None) or "",
        overlay_opacity=float(opacity),
        text_alignment=getattr(row, "text_alignment", None) or "left",
        background_type=getattr(row, "background_type", None) or "image",
        video_path=getattr(row, "video_path", None) or "",
        video_thumbnail=getattr(row, "video_thumbnail", None) or "",
        autoplay=bool(getattr(row, "autoplay", True)),
        loop=bool(getattr(row, "loop", True)),
        muted=bool(getattr(row, "muted", True)),
        plays_inline=bool(getattr(row, "plays_inline", True)),
    )


def about_to_dto(row: AboutSection) -> AboutSectionDTO:
    return AboutSectionDTO(
        id=row.id,
        heading=row.heading,
        subheading=row.subheading or "",
        content=row.content,
        image=row.image or "",
        highlights=row.highlights or [],
        cta_text=row.cta_text or "",
        cta_url=row.cta_url or "",
    )


def statistic_to_dto(row: Statistic) -> StatisticDTO:
    return StatisticDTO(
        id=row.id,
        label=row.label,
        value=row.value,
        suffix=row.suffix or "",
        icon=row.icon or "",
        sort_order=row.sort_order,
    )


def partner_to_dto(row: Partner) -> PartnerDTO:
    return PartnerDTO(
        id=row.id,
        name=row.name,
        logo=row.logo,
        url=row.url or "",
        sort_order=row.sort_order,
    )


def cta_to_dto(row: CTASection) -> CTASectionDTO:
    return CTASectionDTO(
        heading=row.heading,
        subheading=row.subheading or "",
        button_text=row.button_text,
        button_url=row.button_url,
        secondary_button_text=row.secondary_button_text or "",
        secondary_button_url=row.secondary_button_url or "",
    )


def service_to_dto(row: Service) -> ServiceDTO:
    return ServiceDTO(
        id=row.id,
        title=row.title,
        slug=row.slug,
        short_description=row.short_description,
        description=row.description,
        icon=row.icon or "",
        image=row.image or "",
        sort_order=row.sort_order,
        is_featured=row.is_featured,
        is_active=row.is_active,
    )


def project_to_dto(row: Project, *, full: bool = False) -> ProjectDTO:
    detail = getattr(row, "detail", None)
    completion_year = ""
    if detail and detail.completion_year:
        completion_year = detail.completion_year
    elif row.completion_date and len(row.completion_date) >= 4:
        completion_year = row.completion_date[:4]

    dto = ProjectDTO(
        id=row.id,
        title=row.title,
        slug=row.slug,
        description=row.description,
        location=row.location or "",
        client=row.client or "",
        category=row.category or "",
        cover_image=row.cover_image or "",
        completion_date=row.completion_date or "",
        county=row.county or "",
        country=row.country or "",
        status=row.status or "",
        sort_order=row.sort_order,
        is_featured=row.is_featured,
        is_active=row.is_active,
        completion_year=completion_year,
    )

    if not full:
        return dto

    import json

    from app.models.catalog import GalleryImage, Project

    def _json_list(raw: str | None) -> list:
        if not raw:
            return []
        try:
            data = json.loads(raw)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

    gallery_rows = (
        GalleryImage.query.filter_by(project_id=row.id, is_active=True)
        .order_by(GalleryImage.sort_order)
        .all()
    )
    related_slugs: list[str] = []
    if detail:
        related_ids = [int(x) for x in _json_list(detail.related_project_ids_json) if str(x).isdigit()]
        if related_ids:
            related_slugs = [
                p.slug
                for p in Project.query.filter(Project.id.in_(related_ids), Project.is_active.is_(True)).all()
            ]

    dto.meta_title = detail.meta_title if detail else ""
    dto.meta_description = detail.meta_description if detail else ""
    dto.consultant = detail.consultant if detail else ""
    dto.duration = detail.duration if detail else ""
    dto.overview = (detail.overview if detail and detail.overview else row.description) or row.description
    dto.service_slugs = _json_list(detail.service_slugs_json if detail else "[]")
    dto.scope_of_work = _json_list(detail.scope_of_work_json if detail else "[]")
    dto.challenges = _json_list(detail.challenges_json if detail else "[]")
    dto.solutions = _json_list(detail.solutions_json if detail else "[]")
    dto.equipment_used = _json_list(detail.equipment_json if detail else "[]")
    dto.gallery_images = [g.image for g in gallery_rows]
    dto.related_project_slugs = related_slugs
    if detail:
        dto.meta_title = detail.meta_title or dto.title
        dto.meta_description = detail.meta_description or dto.description
    return dto


def gallery_to_dto(row: GalleryImage) -> GalleryImageDTO:
    return GalleryImageDTO(
        id=row.id,
        title=row.title,
        image=row.image,
        category=row.category or "",
        sort_order=row.sort_order,
    )


def team_to_dto(row: TeamMember) -> TeamMemberDTO:
    return TeamMemberDTO(
        id=row.id,
        name=row.name,
        position=row.position,
        bio=row.bio or "",
        photo=row.photo or "",
        email=row.email or "",
        phone=row.phone or "",
        sort_order=row.sort_order,
        is_active=row.is_active,
    )


def testimonial_to_dto(row: Testimonial) -> TestimonialDTO:
    return TestimonialDTO(
        id=row.id,
        client_name=row.client_name,
        client_title=row.client_title or "",
        company=row.company or "",
        content=row.content,
        photo=row.photo or "",
        rating=row.rating or 5,
        sort_order=row.sort_order,
        is_featured=row.is_featured,
    )


def job_to_dto(row: JobListing) -> JobListingDTO:
    from app.providers import careers_loader

    seeded = careers_loader.build_job_by_slug(row.slug)
    return JobListingDTO(
        id=row.id,
        title=row.title,
        slug=row.slug,
        department=row.department or (seeded.department if seeded else ""),
        location=row.location or (seeded.location if seeded else ""),
        employment_type=row.employment_type or (seeded.employment_type if seeded else ""),
        short_description=seeded.short_description if seeded else "",
        description=row.description,
        requirements=row.requirements or (seeded.requirements if seeded else ""),
        experience_required=seeded.experience_required if seeded else "",
        responsibilities=list(seeded.responsibilities) if seeded else [],
        qualifications=list(seeded.qualifications) if seeded else [],
        skills=list(seeded.skills) if seeded else [],
        benefits=list(seeded.benefits) if seeded else [],
        deadline=row.deadline or (seeded.deadline if seeded else ""),
        image=seeded.image if seeded else "",
        meta_title=seeded.meta_title if seeded else row.title,
        meta_description=seeded.meta_description if seeded else "",
        sort_order=row.sort_order,
        is_active=row.is_active,
    )


def contact_page_to_dto(row: ContactPageContent) -> ContactPageDTO:
    return ContactPageDTO(
        heading=row.heading,
        subheading=row.subheading or "",
        intro=row.intro or "",
        map_embed=row.map_embed or "",
        form_heading=row.form_heading,
    )


def quote_page_to_dto(row: QuotePageContent) -> QuotePageDTO:
    return QuotePageDTO(
        heading=row.heading,
        subheading=row.subheading or "",
        intro=row.intro or "",
        form_heading=row.form_heading,
    )


def why_choose_us_to_dto(section: WhyChooseUsSection, items: list) -> WhyChooseUsSectionDTO:
    return WhyChooseUsSectionDTO(
        id=section.id,
        heading=section.heading,
        subheading=section.subheading or "",
        intro=section.intro or "",
        image=section.image or "",
        items=[
            FeatureItemDTO(
                id=item.id,
                title=item.title,
                description=item.description,
                icon=item.icon or "",
                sort_order=item.sort_order,
            )
            for item in items
        ],
    )


def working_process_to_dto(section: WorkingProcessSection, steps: list) -> WorkingProcessSectionDTO:
    return WorkingProcessSectionDTO(
        id=section.id,
        heading=section.heading,
        subheading=section.subheading or "",
        intro=section.intro or "",
        steps=[
            ProcessStepDTO(
                id=step.id,
                step_number=step.step_number,
                title=step.title,
                description=step.description,
                icon=step.icon or "",
                sort_order=step.sort_order,
            )
            for step in steps
        ],
    )


def section_heading_to_dto(row: SectionHeading) -> SectionHeadingDTO:
    return SectionHeadingDTO(
        heading=row.heading,
        subheading=row.subheading or "",
        intro=row.intro or "",
    )


def trust_badge_to_dto(row: TrustBadge) -> TrustBadgeDTO:
    return TrustBadgeDTO(
        id=row.id,
        label=row.label,
        icon=row.icon or "",
        sort_order=row.sort_order,
    )
