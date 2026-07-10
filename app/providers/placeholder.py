"""
Placeholder content provider — structured sample data for development.

Mirrors the exact shape returned by DatabaseContentProvider so templates
and services work identically before MySQL is connected.
Replace by setting DATABASE_ENABLED=true in .env.
"""

from app.constants.media import FALLBACK_IMAGES
from app.data.company_profile import COMPANY_PROFILE
from app.providers import block_loader, careers_loader, contact_loader, equipment_loader, gallery_loader, page_loader, profile_loader, team_loader
from app.providers.base import ContentProvider
from app.schemas.content import (
    AboutSectionDTO,
    BeforeAfterItemDTO,
    CompanyInfoDTO,
    ContactPageDTO,
    ContentBlockDTO,
    ContentBlockRegistryDTO,
    CTASectionDTO,
    CompanyProfileDTO,
    FeatureItemDTO,
    FooterContentDTO,
    GalleryImageDTO,
    GalleryAlbumDTO,
    GalleryDownloadDTO,
    GalleryFilterOptionsDTO,
    GalleryVideoDTO,
    HeroSlideDTO,
    HomePageDTO,
    JobListingDTO,
    NavItemDTO,
    PageMetaDTO,
    PageSectionListDTO,
    PartnerDTO,
    ProcessStepDTO,
    ProgressGalleryItemDTO,
    ProjectDTO,
    QuotePageDTO,
    SectionHeadingDTO,
    ServiceDTO,
    EquipmentDTO,
    SocialLinkDTO,
    StatisticDTO,
    TeamMemberDTO,
    TestimonialDTO,
    TrustBadgeDTO,
    WhyChooseUsSectionDTO,
    WorkingProcessSectionDTO,
)


class PlaceholderContentProvider(ContentProvider):
    """Returns realistic placeholder data matching future database records."""

    # ------------------------------------------------------------------
    # Site-wide
    # ------------------------------------------------------------------

    def get_company_info(self) -> CompanyInfoDTO:
        return profile_loader.build_company_info_dto()

    def get_nav_items(self, *, header: bool = True) -> list[NavItemDTO]:
        items = [
            NavItemDTO(1, "Home", "main.index", 1),
            NavItemDTO(2, "About", "main.about", 2),
            NavItemDTO(3, "Services", "main.services", 3),
            NavItemDTO(4, "Projects", "main.projects", 4),
            NavItemDTO(5, "Gallery", "main.gallery", 5),
            NavItemDTO(6, "Team", "main.team", 6),
            NavItemDTO(7, "Careers", "main.careers", 7),
            NavItemDTO(8, "Contact", "main.contact", 8),
        ]
        if header:
            return [i for i in items if i.is_active]
        # Footer: flat list without nested-only duplication logic
        return [i for i in items if i.is_active]

    def get_social_links(self) -> list[SocialLinkDTO]:
        return [
            SocialLinkDTO(1, "facebook", "Facebook", "bi-facebook", "https://facebook.com/", 1),
            SocialLinkDTO(2, "twitter", "Twitter", "bi-twitter-x", "https://twitter.com/", 2),
            SocialLinkDTO(3, "instagram", "Instagram", "bi-instagram", "https://instagram.com/", 3),
            SocialLinkDTO(4, "linkedin", "LinkedIn", "bi-linkedin", "https://linkedin.com/", 4),
        ]

    def get_footer_content(self) -> FooterContentDTO:
        company = self.get_company_info()
        return FooterContentDTO(
            copyright_text=f"© {{year}} {company.name}. All rights reserved.",
            about_text=company.description,
            quick_links=self.get_nav_items(),
            service_links=self.get_services(featured_only=True),
        )

    # ------------------------------------------------------------------
    # Page metadata
    # ------------------------------------------------------------------

    def get_page_meta(self, slug: str) -> PageMetaDTO | None:
        pages = {
            "home": self._page_meta(
                "home", "Home", "Home",
                "GURUH Construction — professional construction services.",
                banner_subtitle="Water · Building · Civil Engineering Works",
            ),
            "about": self._page_meta(
                "about", "About Us", "About Us",
                "Learn about GURUH Construction — our story, mission, and values.",
            ),
            "services": self._page_meta(
                "services", "Services", "Our Services",
                "Water works, building works, civil engineering, road construction, and infrastructure services across Kenya.",
                banner_subtitle="Professional Construction Services Across Kenya",
            ),
            "projects": self._page_meta(
                "projects", "Projects", "Our Projects",
                "Explore GURUH Construction's portfolio of civil, building, road, and water infrastructure projects across Kenya.",
                banner_subtitle="International Construction Portfolio — Delivering Excellence Since 2008",
            ),
            "equipment": self._page_meta(
                "equipment", "Equipment", "Equipment & Machinery",
                "Explore GURUH Construction's fleet of heavy plant, road machinery, and support equipment for civil and water projects across Kenya.",
                banner_subtitle="Modern Plant & Machinery — Safe, Maintained, Project-Ready",
            ),
            "gallery": self._page_meta(
                "gallery", "Gallery", "Gallery & Media Center",
                "Browse GURUH Construction's project photography, equipment fleet, corporate events, and downloadable company media.",
                banner_subtitle="Projects, Progress & Corporate Media — Documented with Excellence",
            ),
            "team": self._page_meta(
                "team", "Team", "Team & Leadership",
                "Meet the directors, executives, and professionals leading GURUH Construction's delivery across Kenya.",
                banner_subtitle="Leadership, Expertise & Commitment — Building Excellence Together",
            ),
            "careers": self._page_meta(
                "careers", "Careers", "Careers at GURUH Construction",
                "Join GURUH Construction — explore open positions and build your career in construction.",
            ),
            "testimonials": self._page_meta(
                "testimonials", "Testimonials", "Client Testimonials",
                "Read what our clients say about working with GURUH Construction.",
            ),
            "contact": self._page_meta(
                "contact", "Contact", "Contact Us",
                "Get in touch with GURUH Construction for inquiries and support.",
            ),
            "request-quote": self._page_meta(
                "request-quote", "Request Quote", "Request a Quote",
                "Request a free project estimate from our expert team.",
            ),
        }
        return pages.get(slug)

    @staticmethod
    def _page_meta(
        slug: str,
        title: str,
        meta_title: str,
        meta_description: str,
        *,
        banner_subtitle: str = "",
        banner_image: str = "",
    ) -> PageMetaDTO:
        return PageMetaDTO(
            slug=slug,
            title=title,
            meta_title=meta_title,
            meta_description=meta_description,
            is_published=True,
            banner_subtitle=banner_subtitle or meta_description,
            banner_image=banner_image,
        )

    # ------------------------------------------------------------------
    # Homepage
    # ------------------------------------------------------------------

    def get_homepage(self) -> HomePageDTO:
        stats = self.get_statistics()
        return HomePageDTO(
            hero_slides=self._hero_slides(),
            hero_trust_badges=self._hero_trust_badges(),
            hero_floating_stats=stats[:3],
            about=self.get_about_section("home"),
            featured_services=self.get_services(featured_only=True),
            featured_projects=self.get_projects(featured_only=True),
            why_choose_us=self.get_why_choose_us("home"),
            statistics=stats,
            working_process=self.get_working_process("home"),
            testimonials=self.get_testimonials(featured_only=True),
            partners=self.get_partners(),
            cta=self.get_cta_section("home"),
            services_heading=self.get_section_heading("services"),
            projects_heading=self.get_section_heading("projects"),
            testimonials_heading=self.get_section_heading("testimonials"),
            partners_heading=self.get_section_heading("partners"),
        )

    def _hero_trust_badges(self) -> list[TrustBadgeDTO]:
        return [
            TrustBadgeDTO(1, "NCA2 Road Works", "bi-signpost-split", 1),
            TrustBadgeDTO(2, "NCA6 Building Works", "bi-building", 2),
            TrustBadgeDTO(3, "Water Contractor Licensed", "bi-droplet-fill", 3),
            TrustBadgeDTO(4, "Safety First", "bi-shield-check", 4),
        ]

    def _hero_slides(self) -> list[HeroSlideDTO]:
        contact = profile_loader.build_company_info_dto()
        return [
            HeroSlideDTO(
                id=1,
                title="GURUH Construction Company Limited",
                subtitle="Water · Building · Civil Engineering Works",
                description=COMPANY_PROFILE["company_introduction"],
                image="",
                cta_text="Our Projects",
                cta_url="/projects",
                secondary_cta_text="Contact Us",
                secondary_cta_url="/contact",
                overlay_opacity=0.65,
                sort_order=1,
            ),
            HeroSlideDTO(
                id=2,
                title="Building Excellence Across East Africa",
                subtitle=contact.tagline,
                description=COMPANY_PROFILE["company_overview"],
                image="",
                cta_text="Request a Quote",
                cta_url="/request-quote",
                secondary_cta_text="Our Services",
                secondary_cta_url="/services",
                overlay_opacity=0.65,
                sort_order=2,
            ),
            HeroSlideDTO(
                id=3,
                title="Trusted Infrastructure Delivery Since 2008",
                subtitle="NCA Registered · Safety First · Quality Assured",
                description="Delivering roads, buildings, water works, and civil engineering projects across Kenya and the region.",
                image="",
                cta_text="View Equipment",
                cta_url="/equipment",
                secondary_cta_text="Meet Our Team",
                secondary_cta_url="/team",
                overlay_opacity=0.65,
                sort_order=3,
            ),
        ]

    # ------------------------------------------------------------------
    # Sections & catalog
    # ------------------------------------------------------------------

    def get_company_profile(self) -> CompanyProfileDTO:
        return profile_loader.build_company_profile_dto()

    def get_content_blocks(self, *, active_only: bool = True) -> ContentBlockRegistryDTO:
        registry = block_loader.build_block_registry_from_seed()
        if active_only:
            return ContentBlockRegistryDTO(blocks=registry.active_blocks())
        return registry

    def get_content_block(self, block_key: str) -> ContentBlockDTO | None:
        return block_loader.get_seed_block(block_key)

    def get_page_sections(
        self, page_slug: str, *, active_only: bool = True
    ) -> PageSectionListDTO:
        section_list = page_loader.build_section_list_from_seed(page_slug)
        if active_only:
            return PageSectionListDTO(
                page_slug=page_slug,
                sections=section_list.active_sections(),
            )
        return section_list

    def get_about_section(self, page_slug: str = "about") -> AboutSectionDTO | None:
        return profile_loader.build_about_section(page_slug)

    def get_statistics(self) -> list[StatisticDTO]:
        return profile_loader.build_statistics()

    def get_partners(self) -> list[PartnerDTO]:
        return [
            PartnerDTO(1, "BuildCorp International", "img/fallbacks/partner.svg", "", 1),
            PartnerDTO(2, "Urban Developers", "img/fallbacks/partner.svg", "", 2),
            PartnerDTO(3, "InfraTech Group", "img/fallbacks/partner.svg", "", 3),
        ]

    def get_cta_section(self, page_slug: str = "home") -> CTASectionDTO | None:
        ctas = {
            "home": CTASectionDTO(
                heading="Ready to Start Your Project?",
                subheading="Contact us today for a free consultation and project estimate.",
                button_text="Request a Quote",
                button_url="/request-quote",
                secondary_button_text="Contact Us",
                secondary_button_url="/contact",
            ),
            "global": CTASectionDTO(
                heading="Let's Build Something Great Together",
                subheading="Speak with our team about your next construction project.",
                button_text="Request a Quote",
                button_url="/request-quote",
                secondary_button_text="Contact Us",
                secondary_button_url="/contact",
            ),
        }
        return ctas.get(page_slug) or ctas.get("global")

    def get_why_choose_us(self, page_slug: str = "home") -> WhyChooseUsSectionDTO | None:
        if page_slug != "home":
            return None
        profile = profile_loader.build_company_profile_dto()
        icons = ["bi-shield-check", "bi-heart-pulse", "bi-handshake"]
        return WhyChooseUsSectionDTO(
            id=1,
            heading="Why Choose GURUH Construction",
            subheading="Our Core Values",
            intro=profile.about,
            image=FALLBACK_IMAGES["about"],
            items=[
                FeatureItemDTO(i + 1, v.title, v.description, icons[i % len(icons)], i + 1)
                for i, v in enumerate(profile.core_values)
            ],
        )

    def get_working_process(self, page_slug: str = "home") -> WorkingProcessSectionDTO | None:
        if page_slug != "home":
            return None
        return WorkingProcessSectionDTO(
            id=1,
            heading="Our Working Process",
            subheading="How We Build",
            intro="A streamlined, transparent approach from initial consultation to project handover.",
            steps=[
                ProcessStepDTO(1, 1, "Consultation", "We listen to your vision, assess requirements, and provide expert guidance.", "bi-chat-dots", 1),
                ProcessStepDTO(2, 2, "Planning & Design", "Detailed planning, architectural design, and comprehensive project scoping.", "bi-rulers", 2),
                ProcessStepDTO(3, 3, "Construction", "Expert execution with rigorous quality checks at every milestone.", "bi-hammer", 3),
                ProcessStepDTO(4, 4, "Handover", "Final inspection, documentation, and seamless project delivery.", "bi-key", 4),
            ],
        )

    def get_section_heading(self, section_key: str, page_slug: str = "home") -> SectionHeadingDTO | None:
        headings = {
            "services": SectionHeadingDTO("Our Services", "What We Offer", "Comprehensive construction solutions tailored to your needs."),
            "projects": SectionHeadingDTO("Featured Projects", "Our Portfolio", "Explore our recent work delivering excellence across sectors."),
            "testimonials": SectionHeadingDTO("Client Testimonials", "What Clients Say", "Trusted by businesses and homeowners across the region."),
            "partners": SectionHeadingDTO("Our Partners", "Trusted By", "Collaborating with industry leaders to deliver outstanding results."),
        }
        return headings.get(section_key)

    def get_services(self, *, featured_only: bool = False) -> list[ServiceDTO]:
        services = profile_loader.build_services()
        if featured_only:
            return [s for s in services if s.is_featured]
        return services

    def get_service_by_slug(self, slug: str) -> ServiceDTO | None:
        return next((s for s in self.get_services() if s.slug == slug), None)

    def get_projects(self, *, featured_only: bool = False) -> list[ProjectDTO]:
        projects = profile_loader.build_projects()
        if featured_only:
            return [p for p in projects if p.is_featured]
        return projects

    def get_project_by_slug(self, slug: str) -> ProjectDTO | None:
        return profile_loader.build_project_by_slug(slug)

    def get_equipment(self, *, featured_only: bool = False) -> list[EquipmentDTO]:
        items = equipment_loader.build_equipment()
        if featured_only:
            return [e for e in items if e.is_featured]
        return items

    def get_equipment_by_slug(self, slug: str) -> EquipmentDTO | None:
        return equipment_loader.build_equipment_by_slug(slug)

    def get_gallery_images(self) -> list[GalleryImageDTO]:
        return gallery_loader.build_gallery_images()

    def get_gallery_albums(self) -> list[GalleryAlbumDTO]:
        return gallery_loader.build_gallery_albums()

    def get_gallery_videos(self) -> list[GalleryVideoDTO]:
        return gallery_loader.build_gallery_videos()

    def get_gallery_downloads(self) -> list[GalleryDownloadDTO]:
        return gallery_loader.build_gallery_downloads()

    def get_before_after_gallery(self) -> list[BeforeAfterItemDTO]:
        return gallery_loader.build_before_after_items()

    def get_progress_gallery(self) -> list[ProgressGalleryItemDTO]:
        return gallery_loader.build_progress_gallery_items()

    def get_awards_gallery(self) -> list[GalleryImageDTO]:
        return gallery_loader.build_awards_gallery_items()

    def get_gallery_filter_options(self) -> GalleryFilterOptionsDTO:
        return gallery_loader.build_gallery_filter_options()

    def get_team_members(self) -> list[TeamMemberDTO]:
        return team_loader.build_team_members()

    def get_testimonials(self, *, featured_only: bool = False) -> list[TestimonialDTO]:
        items = [
            TestimonialDTO(1, "Mohamed Ibrahim", "Director", "ABC Corporation", "GURUH delivered our project on time and exceeded expectations.", "", 5, 1, True),
            TestimonialDTO(2, "Amina Mohamed", "Homeowner", "", "Professional team and excellent craftsmanship on our home renovation.", "", 5, 2, True),
        ]
        if featured_only:
            return [t for t in items if t.is_featured]
        return items

    def get_job_listings(self) -> list[JobListingDTO]:
        return careers_loader.build_jobs()

    def get_job_by_slug(self, slug: str) -> JobListingDTO | None:
        return careers_loader.build_job_by_slug(slug)

    def get_job_application_fields(self):
        return careers_loader.build_job_application_fields()

    def get_job_application_options(self):
        return careers_loader.build_job_application_options()

    def get_contact_page(self) -> ContactPageDTO:
        return ContactPageDTO(
            heading="Contact Us",
            subheading="We'd Love to Hear From You",
            intro="Reach out for inquiries, partnerships, or project discussions.",
            map_embed="",
            form_heading="Send Us a Message",
        )

    def get_quote_page(self) -> QuotePageDTO:
        return QuotePageDTO(
            heading="Request a Quote",
            subheading="Tell Us About Your Project",
            intro="Fill out the form below and our team will get back to you with a detailed estimate.",
            form_heading="Project Quote Request",
        )

    def get_office_location(self):
        return contact_loader.build_office_location()

    def get_office_locations(self):
        return contact_loader.build_office_locations()

    def get_contact_offices(self):
        return contact_loader.build_contact_offices()

    def get_department_contacts(self):
        return contact_loader.build_department_contacts()

    def get_emergency_contact(self):
        return contact_loader.build_emergency_contact()

    def get_map_location(self):
        return contact_loader.build_map_location()

    def get_contact_form_fields(self):
        return contact_loader.build_contact_form_fields()

    def get_quote_form_fields(self):
        return contact_loader.build_quote_form_fields()

    def get_quote_form_options(self):
        return contact_loader.build_quote_form_options()

    def get_quote_form_steps(self):
        return contact_loader.build_quote_form_steps()
