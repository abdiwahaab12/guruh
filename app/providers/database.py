"""
MySQL content provider — loads all website content from the database.

Used when DATABASE_ENABLED=true. Falls back to PlaceholderContentProvider
if the database is unreachable or tables are empty (during initial setup).
"""

import logging
from dataclasses import replace

from flask import current_app

from app.constants.settings_keys import (
    KEY_MAPS_DEFAULT_LAT,
    KEY_MAPS_DEFAULT_LNG,
    KEY_MAPS_DEFAULT_ZOOM,
    KEY_MAPS_EMBED_URL,
    KEY_MAPS_PROVIDER,
)
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
from app.models.cms import (
    AboutSection,
    CTASection,
    HeroSlide,
    Page,
    Partner,
    ProcessStep,
    SectionHeading,
    Statistic,
    TrustBadge,
    WhyChooseUsItem,
    WhyChooseUsSection,
    WorkingProcessSection,
)
from app.models.site import CompanyInfo, FooterContent, NavItem, OfficeLocation, SiteSetting, SocialLink
from app.providers.base import ContentProvider
from app.providers import mappers
from app.providers.placeholder import PlaceholderContentProvider
from app.schemas.content import (
    AboutSectionDTO,
    CompanyInfoDTO,
    CompanyProfileDTO,
    ContactPageDTO,
    ContentBlockDTO,
    ContentBlockRegistryDTO,
    CTASectionDTO,
    DepartmentContactDTO,
    EmergencyContactDTO,
    FooterContentDTO,
    GalleryFilterOptionsDTO,
    GalleryImageDTO,
    HomePageDTO,
    JobListingDTO,
    MapLocationDTO,
    NavItemDTO,
    OfficeLocationDTO,
    PageMetaDTO,
    PageSectionListDTO,
    PartnerDTO,
    ProjectDTO,
    QuotePageDTO,
    ServiceDTO,
    SocialLinkDTO,
    StatisticDTO,
    TeamMemberDTO,
    TestimonialDTO,
)

logger = logging.getLogger(__name__)


class DatabaseContentProvider(ContentProvider):
    """Reads content from MySQL via SQLAlchemy models."""

    def __init__(self):
        self._fallback = PlaceholderContentProvider()

    def _use_fallback(self, method_name: str, exc: Exception | None = None) -> bool:
        if exc:
            logger.warning("DatabaseContentProvider.%s failed: %s — using placeholder.", method_name, exc)
        return True

    def get_company_info(self) -> CompanyInfoDTO:
        try:
            row = CompanyInfo.query.filter_by(is_active=True).first()
            if row:
                return mappers.company_to_dto(row)
        except Exception as exc:
            self._use_fallback("get_company_info", exc)
        return self._fallback.get_company_info()

    def get_nav_items(self, *, header: bool = True) -> list[NavItemDTO]:
        try:
            query = NavItem.query.filter_by(is_active=True)
            if header:
                query = query.filter_by(show_in_header=True)
            else:
                query = query.filter_by(show_in_footer=True)
            rows = query.order_by(NavItem.sort_order).all()
            if rows:
                return [mappers.nav_to_dto(r) for r in rows]
        except Exception as exc:
            self._use_fallback("get_nav_items", exc)
        return self._fallback.get_nav_items(header=header)

    def get_social_links(self) -> list[SocialLinkDTO]:
        try:
            rows = SocialLink.query.filter_by(is_active=True).order_by(SocialLink.sort_order).all()
            if rows:
                return [mappers.social_to_dto(r) for r in rows]
        except Exception as exc:
            self._use_fallback("get_social_links", exc)
        return self._fallback.get_social_links()

    def get_footer_content(self) -> FooterContentDTO:
        try:
            row = FooterContent.query.filter_by(is_active=True).first()
            if row:
                return mappers.footer_to_dto(
                    row,
                    self.get_nav_items(header=False),
                    self.get_services(featured_only=True),
                )
        except Exception as exc:
            self._use_fallback("get_footer_content", exc)
        return self._fallback.get_footer_content()

    def get_page_meta(self, slug: str) -> PageMetaDTO | None:
        try:
            row = Page.query.filter_by(slug=slug, is_published=True).first()
            if row:
                dto = mappers.page_to_dto(row)
                return self._enrich_page_banner(slug, dto)
        except Exception as exc:
            self._use_fallback("get_page_meta", exc)
        dto = self._fallback.get_page_meta(slug)
        if dto:
            return self._enrich_page_banner(slug, dto)
        return dto

    def _enrich_page_banner(self, slug: str, dto: PageMetaDTO) -> PageMetaDTO:
        if dto.banner_image and not dto.banner_image.startswith("img/fallbacks/"):
            return dto

        resolved = ""
        try:
            from app.providers.website_admin_provider import WebsiteAdminProvider

            resolved = WebsiteAdminProvider.resolve_page_banner_image(slug)
        except Exception:
            pass

        if not resolved:
            from app.constants.website_admin import PAGE_INTRO_BLOCK_KEYS

            block_key = PAGE_INTRO_BLOCK_KEYS.get(slug)
            if block_key:
                block = self.get_content_block(block_key)
                if block and block.hero_image and not block.hero_image.startswith("img/fallbacks/"):
                    resolved = block.hero_image

        if not resolved and slug == "about":
            about = self.get_about_section("about")
            if about and about.image and not about.image.startswith("img/fallbacks/"):
                resolved = about.image

        if resolved:
            return replace(dto, banner_image=resolved)
        return dto

    def get_homepage(self) -> HomePageDTO:
        return HomePageDTO(
            hero_slides=self._query_hero_slides(),
            hero_trust_badges=self._query_trust_badges(),
            hero_floating_stats=self.get_statistics()[:3],
            about=self.get_about_section("home"),
            featured_services=self.get_services(featured_only=True),
            featured_projects=self.get_projects(featured_only=True),
            why_choose_us=self.get_why_choose_us("home"),
            statistics=self.get_statistics(),
            working_process=self.get_working_process("home"),
            testimonials=self.get_testimonials(featured_only=True),
            partners=self.get_partners(),
            cta=self.get_cta_section("home"),
            services_heading=self.get_section_heading("services"),
            projects_heading=self.get_section_heading("projects"),
            testimonials_heading=self.get_section_heading("testimonials"),
            partners_heading=self.get_section_heading("partners"),
        )

    def _query_hero_slides(self) -> list:
        try:
            rows = HeroSlide.query.filter_by(is_active=True).order_by(HeroSlide.sort_order).all()
            if rows:
                return [mappers.hero_to_dto(r) for r in rows]
        except Exception as exc:
            self._use_fallback("_query_hero_slides", exc)
        return self._fallback._hero_slides()

    def _query_trust_badges(self) -> list:
        try:
            rows = (
                TrustBadge.query.filter_by(page_slug="home", is_active=True)
                .order_by(TrustBadge.sort_order)
                .all()
            )
            if rows:
                return [mappers.trust_badge_to_dto(r) for r in rows]
        except Exception as exc:
            self._use_fallback("_query_trust_badges", exc)
        return self._fallback._hero_trust_badges()

    def get_about_section(self, page_slug: str = "about") -> AboutSectionDTO | None:
        from app.providers.website_admin_provider import WebsiteAdminProvider

        try:
            lookup_slug = "home" if page_slug == "home" else page_slug
            row = AboutSection.query.filter_by(page_slug=lookup_slug, is_active=True).first()
            resolved_image = WebsiteAdminProvider.resolve_about_image()

            if row:
                dto = mappers.about_to_dto(row)
                if dto.image and not dto.image.startswith("img/fallbacks/"):
                    return dto
                if resolved_image:
                    return AboutSectionDTO(
                        id=dto.id,
                        heading=dto.heading,
                        subheading=dto.subheading,
                        content=dto.content,
                        image=resolved_image,
                        highlights=dto.highlights,
                        cta_text=dto.cta_text,
                        cta_url=dto.cta_url,
                    )
                return dto

            fallback = self._fallback.get_about_section(page_slug)
            if not fallback:
                return None
            if resolved_image:
                return AboutSectionDTO(
                    id=fallback.id,
                    heading=fallback.heading,
                    subheading=fallback.subheading,
                    content=fallback.content,
                    image=resolved_image,
                    highlights=fallback.highlights,
                    cta_text=fallback.cta_text,
                    cta_url=fallback.cta_url,
                )
            return fallback
        except Exception as exc:
            self._use_fallback("get_about_section", exc)
        return self._fallback.get_about_section(page_slug)

    def get_statistics(self) -> list[StatisticDTO]:
        try:
            rows = Statistic.query.filter_by(is_active=True).order_by(Statistic.sort_order).all()
            if rows:
                return [mappers.statistic_to_dto(r) for r in rows]
        except Exception as exc:
            self._use_fallback("get_statistics", exc)
        return self._fallback.get_statistics()

    def get_partners(self) -> list[PartnerDTO]:
        try:
            rows = Partner.query.filter_by(is_active=True).order_by(Partner.sort_order).all()
            if rows:
                return [mappers.partner_to_dto(r) for r in rows]
            from app.providers.website_admin_provider import WebsiteAdminProvider

            block = WebsiteAdminProvider.get_block_dto("partners", include_inactive_items=False)
            if block and block.items:
                return [
                    PartnerDTO(
                        id=item.id,
                        name=item.title,
                        logo=item.image,
                        url=(item.extra or {}).get("url", ""),
                        sort_order=item.sort_order,
                    )
                    for item in block.items
                    if item.is_active and item.image
                ]
        except Exception as exc:
            self._use_fallback("get_partners", exc)
        return self._fallback.get_partners()

    def get_cta_section(self, page_slug: str = "home") -> CTASectionDTO | None:
        try:
            row = CTASection.query.filter_by(page_slug=page_slug, is_active=True).first()
            if row:
                return mappers.cta_to_dto(row)
            if page_slug not in ("home", "global"):
                global_row = CTASection.query.filter_by(page_slug="global", is_active=True).first()
                if global_row:
                    return mappers.cta_to_dto(global_row)
        except Exception as exc:
            self._use_fallback("get_cta_section", exc)
        return self._fallback.get_cta_section(page_slug)

    def get_services(self, *, featured_only: bool = False) -> list[ServiceDTO]:
        try:
            query = Service.query.filter_by(is_active=True)
            if featured_only:
                query = query.filter_by(is_featured=True)
            rows = query.order_by(Service.sort_order).all()
            if rows:
                return [mappers.service_to_dto(r) for r in rows]
        except Exception as exc:
            self._use_fallback("get_services", exc)
        return self._fallback.get_services(featured_only=featured_only)

    def get_service_by_slug(self, slug: str) -> ServiceDTO | None:
        try:
            row = Service.query.filter_by(slug=slug, is_active=True).first()
            if row:
                return mappers.service_to_dto(row)
        except Exception as exc:
            self._use_fallback("get_service_by_slug", exc)
        return self._fallback.get_service_by_slug(slug)

    def get_projects(self, *, featured_only: bool = False) -> list[ProjectDTO]:
        try:
            query = Project.query.filter_by(is_active=True)
            if featured_only:
                query = query.filter_by(is_featured=True)
            rows = query.order_by(Project.sort_order).all()
            if rows:
                return [mappers.project_to_dto(r) for r in rows]
        except Exception as exc:
            self._use_fallback("get_projects", exc)
        return self._fallback.get_projects(featured_only=featured_only)

    def get_project_by_slug(self, slug: str) -> ProjectDTO | None:
        try:
            from sqlalchemy.orm import joinedload

            row = (
                Project.query.options(joinedload(Project.detail))
                .filter_by(slug=slug, is_active=True)
                .first()
            )
            if row:
                return mappers.project_to_dto(row, full=True)
        except Exception as exc:
            self._use_fallback("get_project_by_slug", exc)
        return self._fallback.get_project_by_slug(slug)

    def get_equipment(self, *, featured_only: bool = False) -> list:
        try:
            from app.providers.equipment_provider import load_equipment

            db_rows = load_equipment(featured_only=featured_only)
            catalog_rows = self._fallback.get_equipment(featured_only=featured_only)
            if not db_rows:
                return catalog_rows

            db_by_slug = {row.slug: row for row in db_rows}
            merged = []
            seen: set[str] = set()
            for item in catalog_rows:
                if item.slug in db_by_slug:
                    merged.append(db_by_slug[item.slug])
                    seen.add(item.slug)
                else:
                    merged.append(item)
            for item in db_rows:
                if item.slug not in seen:
                    merged.append(item)
            merged.sort(key=lambda row: (row.sort_order, row.name))
            return merged
        except Exception as exc:
            self._use_fallback("get_equipment", exc)
        return self._fallback.get_equipment(featured_only=featured_only)

    def get_equipment_by_slug(self, slug: str):
        try:
            from app.providers.equipment_provider import load_equipment_by_slug

            item = load_equipment_by_slug(slug)
            if item:
                return item
        except Exception as exc:
            self._use_fallback("get_equipment_by_slug", exc)
        return self._fallback.get_equipment_by_slug(slug)

    def get_gallery_images(self) -> list[GalleryImageDTO]:
        try:
            from app.providers.gallery_provider import load_gallery_images

            return load_gallery_images()
        except Exception as exc:
            self._use_fallback("get_gallery_images", exc)
        return self._fallback.get_gallery_images()

    def get_gallery_albums(self):
        try:
            from app.providers.gallery_provider import load_gallery_albums, load_gallery_images

            images = load_gallery_images()
            if images:
                return load_gallery_albums(images)
            return []
        except Exception as exc:
            self._use_fallback("get_gallery_albums", exc)
        return self._fallback.get_gallery_albums()

    def get_gallery_videos(self):
        try:
            from app.providers.gallery_provider import load_gallery_videos

            videos = load_gallery_videos()
            if videos:
                return videos
            return []
        except Exception as exc:
            self._use_fallback("get_gallery_videos", exc)
        return self._fallback.get_gallery_videos()

    def get_gallery_downloads(self):
        return self._fallback.get_gallery_downloads()

    def get_before_after_gallery(self):
        try:
            from app.providers.gallery_provider import load_before_after_items

            return load_before_after_items()
        except Exception as exc:
            self._use_fallback("get_before_after_gallery", exc)
        return self._fallback.get_before_after_gallery()

    def get_progress_gallery(self):
        try:
            from app.providers.gallery_provider import load_progress_items

            return load_progress_items()
        except Exception as exc:
            self._use_fallback("get_progress_gallery", exc)
        return self._fallback.get_progress_gallery()

    def get_awards_gallery(self):
        try:
            from app.providers.gallery_provider import load_awards_items

            return load_awards_items()
        except Exception as exc:
            self._use_fallback("get_awards_gallery", exc)
        return self._fallback.get_awards_gallery()

    def get_gallery_filter_options(self):
        try:
            from app.providers.gallery_provider import load_gallery_filter_options, load_gallery_images

            images = load_gallery_images()
            if images:
                return load_gallery_filter_options(images)
            return GalleryFilterOptionsDTO()
        except Exception as exc:
            self._use_fallback("get_gallery_filter_options", exc)
        return self._fallback.get_gallery_filter_options()

    def get_team_members(self) -> list[TeamMemberDTO]:
        try:
            rows = TeamMember.query.filter_by(is_active=True).order_by(TeamMember.sort_order).all()
            if rows:
                return [mappers.team_to_dto(r) for r in rows]
        except Exception as exc:
            self._use_fallback("get_team_members", exc)
        return self._fallback.get_team_members()

    def get_testimonials(self, *, featured_only: bool = False) -> list[TestimonialDTO]:
        try:
            query = Testimonial.query.filter_by(is_active=True)
            if featured_only:
                query = query.filter_by(is_featured=True)
            rows = query.order_by(Testimonial.sort_order).all()
            if rows:
                return [mappers.testimonial_to_dto(r) for r in rows]
        except Exception as exc:
            self._use_fallback("get_testimonials", exc)
        return self._fallback.get_testimonials(featured_only=featured_only)

    def get_job_listings(self) -> list[JobListingDTO]:
        try:
            rows = JobListing.query.filter_by(is_active=True).order_by(JobListing.sort_order).all()
            if rows:
                return [mappers.job_to_dto(r) for r in rows]
        except Exception as exc:
            self._use_fallback("get_job_listings", exc)
        return self._fallback.get_job_listings()

    def get_job_by_slug(self, slug: str) -> JobListingDTO | None:
        try:
            row = JobListing.query.filter_by(slug=slug, is_active=True).first()
            if row:
                return mappers.job_to_dto(row)
        except Exception as exc:
            self._use_fallback("get_job_by_slug", exc)
        return self._fallback.get_job_by_slug(slug)

    def get_job_application_fields(self):
        return self._fallback.get_job_application_fields()

    def get_job_application_options(self):
        return self._fallback.get_job_application_options()

    def get_contact_page(self) -> ContactPageDTO:
        try:
            row = ContactPageContent.query.filter_by(is_active=True).first()
            if row:
                return mappers.contact_page_to_dto(row)
        except Exception as exc:
            self._use_fallback("get_contact_page", exc)
        return self._fallback.get_contact_page()

    def get_quote_page(self) -> QuotePageDTO:
        try:
            row = QuotePageContent.query.filter_by(is_active=True).first()
            if row:
                return mappers.quote_page_to_dto(row)
        except Exception as exc:
            self._use_fallback("get_quote_page", exc)
        return self._fallback.get_quote_page()

    def _db_only(self) -> bool:
        return bool(current_app.config.get("DATABASE_ENABLED"))

    def _load_active_offices(self) -> list[OfficeLocation]:
        return (
            OfficeLocation.query.filter_by(is_active=True)
            .order_by(OfficeLocation.sort_order, OfficeLocation.name)
            .all()
        )

    @staticmethod
    def _head_office_row(offices: list[OfficeLocation]) -> OfficeLocation | None:
        for office in offices:
            if office.is_headquarters:
                return office
        return offices[0] if offices else None

    @staticmethod
    def _office_from_company(row: CompanyInfo) -> OfficeLocationDTO:
        from app.providers.profile_loader import phone_to_tel

        phone_primary = row.phone.split(" / ")[0] if " / " in row.phone else row.phone
        return OfficeLocationDTO(
            id=0,
            slug="head-office",
            name=row.name,
            office_label="Head Office",
            address=row.address,
            postal_address="",
            phone_primary=phone_primary,
            phone_tel=phone_to_tel(phone_primary),
            email=row.email,
            office_hours=row.office_hours,
            address_country=row.operating_country,
            address_country_code=row.operating_country_code,
            is_headquarters=True,
            show_on_contact_page=True,
        )

    def _maps_settings(self) -> dict[str, str]:
        rows = SiteSetting.query.filter(
            SiteSetting.key.in_(
                (
                    KEY_MAPS_DEFAULT_LAT,
                    KEY_MAPS_DEFAULT_LNG,
                    KEY_MAPS_DEFAULT_ZOOM,
                    KEY_MAPS_EMBED_URL,
                    KEY_MAPS_PROVIDER,
                )
            )
        ).all()
        return {row.key: row.value for row in rows}

    def get_office_locations(self) -> list[OfficeLocationDTO]:
        try:
            rows = self._load_active_offices()
            if rows:
                return [mappers.office_to_dto(row) for row in rows]
            company = CompanyInfo.query.filter_by(is_active=True).first()
            if company:
                return [self._office_from_company(company)]
            return []
        except Exception as exc:
            self._use_fallback("get_office_locations", exc)
            if self._db_only():
                return []
            return self._fallback.get_office_locations()

    def get_contact_offices(self) -> list[OfficeLocationDTO]:
        try:
            rows = [
                row for row in self._load_active_offices() if row.show_on_contact_page
            ]
            if rows:
                return [mappers.office_to_dto(row) for row in rows]
            company = CompanyInfo.query.filter_by(is_active=True).first()
            if company:
                office = self._office_from_company(company)
                if office.show_on_contact_page:
                    return [office]
            return []
        except Exception as exc:
            self._use_fallback("get_contact_offices", exc)
            if self._db_only():
                return []
            return self._fallback.get_contact_offices()

    def get_office_location(self) -> OfficeLocationDTO:
        try:
            offices = self.get_office_locations()
            for office in offices:
                if office.is_headquarters:
                    return office
            if offices:
                return offices[0]
            company = CompanyInfo.query.filter_by(is_active=True).first()
            if company:
                return self._office_from_company(company)
            if self._db_only():
                raise RuntimeError("No office or company contact data in database.")
            return self._fallback.get_office_location()
        except Exception as exc:
            self._use_fallback("get_office_location", exc)
            if self._db_only():
                company = CompanyInfo.query.filter_by(is_active=True).first()
                if company:
                    return self._office_from_company(company)
                raise
            return self._fallback.get_office_location()

    def get_department_contacts(self) -> list[DepartmentContactDTO]:
        try:
            from app.models.content_blocks import ContentBlock, ContentBlockItem

            row = ContentBlock.query.filter_by(
                block_key="contact_departments", is_active=True
            ).first()
            if not row:
                return []
            items = (
                row.items.filter_by(is_active=True)
                .order_by(ContentBlockItem.sort_order)
                .all()
            )
            departments: list[DepartmentContactDTO] = []
            for item in items:
                extra = dict(item.extra or {})
                departments.append(
                    DepartmentContactDTO(
                        id=item.id,
                        name=item.title,
                        contact_person=extra.get("contact_person", item.subtitle or ""),
                        phone=extra.get("phone", ""),
                        email=extra.get("email", ""),
                        description=item.short_summary or "",
                        icon=item.icon or "bi-building",
                        sort_order=item.sort_order,
                    )
                )
            return departments
        except Exception as exc:
            self._use_fallback("get_department_contacts", exc)
            if self._db_only():
                return []
            return self._fallback.get_department_contacts()

    def get_emergency_contact(self) -> EmergencyContactDTO:
        try:
            from app.models.content_blocks import ContentBlock
            from app.providers.profile_loader import phone_to_tel

            row = ContentBlock.query.filter_by(
                block_key="contact_emergency", is_active=True
            ).first()
            if row:
                extra = dict(row.extra or {})
                phone = extra.get("phone", "")
                return EmergencyContactDTO(
                    title=row.title,
                    phone=phone,
                    description=row.short_summary or "",
                    availability=extra.get("availability", ""),
                    icon=extra.get("icon", "bi-exclamation-triangle-fill"),
                    phone_tel=extra.get("phone_tel", "") or phone_to_tel(phone),
                )

            hq = self._head_office_row(self._load_active_offices())
            if hq:
                return EmergencyContactDTO(
                    title="Emergency Contact",
                    phone=hq.phone_primary,
                    description="",
                    availability=hq.office_hours or "",
                    phone_tel=phone_to_tel(hq.phone_primary),
                )

            company = CompanyInfo.query.filter_by(is_active=True).first()
            if company:
                phone_primary = (
                    company.phone.split(" / ")[0]
                    if " / " in company.phone
                    else company.phone
                )
                return EmergencyContactDTO(
                    title="Emergency Contact",
                    phone=phone_primary,
                    description="",
                    availability=company.office_hours,
                    phone_tel=phone_to_tel(phone_primary),
                )

            return EmergencyContactDTO(title="Emergency Contact", phone="")
        except Exception as exc:
            self._use_fallback("get_emergency_contact", exc)
            if self._db_only():
                return EmergencyContactDTO(title="Emergency Contact", phone="")
            return self._fallback.get_emergency_contact()

    def get_map_location(self) -> MapLocationDTO:
        try:
            settings = self._maps_settings()
            offices = self._load_active_offices()
            hq = self._head_office_row(offices)

            lat: float | None = None
            lng: float | None = None
            zoom = 16
            title = ""
            short_summary = ""

            if hq and hq.map_latitude is not None and hq.map_longitude is not None:
                lat = float(hq.map_latitude)
                lng = float(hq.map_longitude)
                zoom = hq.map_zoom or 16
                title = hq.name
                short_summary = hq.address
            else:
                lat_raw = settings.get(KEY_MAPS_DEFAULT_LAT, "")
                lng_raw = settings.get(KEY_MAPS_DEFAULT_LNG, "")
                if lat_raw and lng_raw:
                    lat = float(lat_raw)
                    lng = float(lng_raw)
                zoom_raw = settings.get(KEY_MAPS_DEFAULT_ZOOM, "16")
                zoom = int(zoom_raw) if str(zoom_raw).isdigit() else 16
                if hq:
                    title = hq.name
                    short_summary = hq.address
                else:
                    company = CompanyInfo.query.filter_by(is_active=True).first()
                    if company:
                        title = company.name
                        short_summary = company.address

            embed_url = settings.get(KEY_MAPS_EMBED_URL, "")
            map_provider = settings.get(KEY_MAPS_PROVIDER, "google-maps") or "google-maps"
            map_ready = bool(embed_url) or (lat is not None and lng is not None)

            return MapLocationDTO(
                latitude=lat if lat is not None else 0.0,
                longitude=lng if lng is not None else 0.0,
                zoom=zoom,
                embed_url=embed_url,
                map_provider=map_provider,
                map_ready=map_ready,
                title=title,
                short_summary=short_summary,
            )
        except Exception as exc:
            self._use_fallback("get_map_location", exc)
            if self._db_only():
                return MapLocationDTO(latitude=0.0, longitude=0.0)
            return self._fallback.get_map_location()

    def get_contact_form_fields(self):
        return self._fallback.get_contact_form_fields()

    def get_quote_form_fields(self):
        return self._fallback.get_quote_form_fields()

    def get_quote_form_options(self):
        return self._fallback.get_quote_form_options()

    def get_quote_form_steps(self):
        return self._fallback.get_quote_form_steps()

    def get_why_choose_us(self, page_slug: str = "home"):
        try:
            from app.models.cms import WhyChooseUsItem, WhyChooseUsSection

            section = WhyChooseUsSection.query.filter_by(page_slug=page_slug, is_active=True).first()
            if section:
                items = WhyChooseUsItem.query.filter_by(is_active=True).order_by(WhyChooseUsItem.sort_order).all()
                return mappers.why_choose_us_to_dto(section, items)
        except Exception as exc:
            self._use_fallback("get_why_choose_us", exc)
        return self._fallback.get_why_choose_us(page_slug)

    def get_working_process(self, page_slug: str = "home"):
        try:
            from app.models.cms import ProcessStep, WorkingProcessSection

            section = WorkingProcessSection.query.filter_by(page_slug=page_slug, is_active=True).first()
            if section:
                steps = ProcessStep.query.filter_by(page_slug=page_slug, is_active=True).order_by(ProcessStep.sort_order).all()
                return mappers.working_process_to_dto(section, steps)
        except Exception as exc:
            self._use_fallback("get_working_process", exc)
        return self._fallback.get_working_process(page_slug)

    def get_section_heading(self, section_key: str, page_slug: str = "home"):
        try:
            from app.models.cms import SectionHeading

            row = SectionHeading.query.filter_by(
                page_slug=page_slug, section_key=section_key, is_active=True
            ).first()
            if row:
                return mappers.section_heading_to_dto(row)
        except Exception as exc:
            self._use_fallback("get_section_heading", exc)
        return self._fallback.get_section_heading(section_key, page_slug)

    def get_company_profile(self) -> CompanyProfileDTO:
        try:
            from app.providers import profile_loader

            return profile_loader.build_company_profile_dto()
        except Exception as exc:
            self._use_fallback("get_company_profile", exc)
        return self._fallback.get_company_profile()

    @staticmethod
    def _enrich_overview_block(dto: ContentBlockDTO) -> ContentBlockDTO:
        """Use page banner / media library when overview blocks still have SVG placeholders."""
        from app.constants.website_admin import PAGE_INTRO_BLOCK_KEYS
        from app.providers.website_admin_provider import WebsiteAdminProvider

        page_slug = next(
            (slug for slug, key in PAGE_INTRO_BLOCK_KEYS.items() if key == dto.block_key),
            None,
        )
        if not page_slug:
            return dto
        if dto.hero_image and not dto.hero_image.startswith("img/fallbacks/"):
            return dto
        resolved = WebsiteAdminProvider.resolve_page_overview_image(page_slug)
        if not resolved:
            return dto
        return ContentBlockDTO(
            id=dto.id,
            block_key=dto.block_key,
            title=dto.title,
            subtitle=dto.subtitle,
            short_summary=dto.short_summary,
            full_content=dto.full_content,
            hero_image=resolved,
            gallery_images=dto.gallery_images,
            display_order=dto.display_order,
            is_active=dto.is_active,
            meta_title=dto.meta_title,
            meta_description=dto.meta_description,
            og_image=dto.og_image,
            items=dto.items,
            extra=dto.extra,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )

    def get_content_blocks(self, *, active_only: bool = True) -> ContentBlockRegistryDTO:
        try:
            from app.models.content_blocks import ContentBlock
            from app.providers import block_loader

            query = ContentBlock.query.order_by(ContentBlock.display_order)
            if active_only:
                query = query.filter_by(is_active=True)
            rows = query.all()
            if rows:
                return ContentBlockRegistryDTO(
                    blocks=[
                        self._enrich_overview_block(block_loader.block_from_model(row))
                        for row in rows
                    ]
                )
        except Exception as exc:
            self._use_fallback("get_content_blocks", exc)
        return self._fallback.get_content_blocks(active_only=active_only)

    def get_content_block(self, block_key: str) -> ContentBlockDTO | None:
        try:
            from app.models.content_blocks import ContentBlock
            from app.providers import block_loader

            row = ContentBlock.query.filter_by(block_key=block_key, is_active=True).first()
            if row:
                return self._enrich_overview_block(block_loader.block_from_model(row))
        except Exception as exc:
            self._use_fallback("get_content_block", exc)
        return self._fallback.get_content_block(block_key)

    def get_page_sections(
        self, page_slug: str, *, active_only: bool = True
    ) -> PageSectionListDTO:
        try:
            from app.models.page_sections import PageSection
            from app.providers import page_loader

            query = PageSection.query.filter_by(page_slug=page_slug).order_by(
                PageSection.display_order
            )
            if active_only:
                query = query.filter_by(is_active=True)
            rows = query.all()
            if rows:
                sections = [page_loader.section_from_model(row) for row in rows]
                return PageSectionListDTO(page_slug=page_slug, sections=sections)
        except Exception as exc:
            self._use_fallback("get_page_sections", exc)
        return self._fallback.get_page_sections(page_slug, active_only=active_only)
