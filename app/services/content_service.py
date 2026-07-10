"""
Business logic layer — routes call services, services call providers.

No HTTP or template logic here. Keeps controllers thin and testable.
"""

from datetime import datetime

from app.providers import get_content_provider
from app.schemas.content import (
    AboutSectionDTO,
    BreadcrumbItemDTO,
    CompanyInfoDTO,
    ContactPageDTO,
    ContentBlockDTO,
    ContentBlockRegistryDTO,
    FooterContentDTO,
    GalleryImageDTO,
    HomePageDTO,
    JobListingDTO,
    NavItemDTO,
    PageMetaDTO,
    PageCompositionDTO,
    PageSectionDTO,
    PageSectionListDTO,
    PageSectionResolvedDTO,
    ProjectDTO,
    QuotePageDTO,
    ServiceDTO,
    SocialLinkDTO,
    TeamMemberDTO,
    TestimonialDTO,
    EquipmentDTO,
)


class SiteService:
    """Site-wide content: company info, navigation, footer, social links."""

    @staticmethod
    def get_company() -> CompanyInfoDTO:
        return get_content_provider().get_company_info()

    @staticmethod
    def get_navigation() -> list[NavItemDTO]:
        from app.constants.public_nav import HEADER_NAV_STRUCTURE

        flat = get_content_provider().get_nav_items(header=True)
        by_endpoint = {item.endpoint: item for item in flat}

        tree: list[NavItemDTO] = []
        for endpoint, child_endpoints in HEADER_NAV_STRUCTURE:
            parent = by_endpoint.get(endpoint)
            if not parent or not parent.is_active:
                continue
            children: list[NavItemDTO] = []
            for child_ep in child_endpoints:
                child = by_endpoint.get(child_ep)
                if child and child.is_active:
                    children.append(
                        NavItemDTO(
                            id=child.id,
                            label=child.label,
                            endpoint=child.endpoint,
                            sort_order=child.sort_order,
                            is_active=child.is_active,
                        )
                    )
            tree.append(
                NavItemDTO(
                    id=parent.id,
                    label=parent.label,
                    endpoint=parent.endpoint,
                    sort_order=parent.sort_order,
                    is_active=parent.is_active,
                    children=children,
                )
            )
        return tree

    @staticmethod
    def get_social_links() -> list[SocialLinkDTO]:
        return get_content_provider().get_social_links()

    @staticmethod
    def get_footer() -> FooterContentDTO:
        footer = get_content_provider().get_footer_content()
        # Replace {year} token in copyright text
        footer.copyright_text = footer.copyright_text.replace(
            "{year}", str(datetime.now().year)
        )
        return footer

    @staticmethod
    def get_global_context() -> dict:
        """Data injected into every template via context processor."""
        from flask import has_request_context, request, url_for

        company = SiteService.get_company()
        footer = SiteService.get_footer()

        canonical_url = ""
        og_image_url = ""
        if has_request_context():
            canonical_url = request.url.split("?")[0].split("#")[0]
            og_image_url = url_for(
                "static", filename=company.logo_path, _external=True
            )

        return {
            "company": company,
            "nav_items": SiteService.get_navigation(),
            "social_links": SiteService.get_social_links(),
            "footer": footer,
            "current_year": datetime.now().year,
            "canonical_url": canonical_url,
            "og_image_url": og_image_url,
        }


class PageService:
    """Page-level metadata, breadcrumbs, and shared page shell."""

    @staticmethod
    def get_meta(slug: str) -> PageMetaDTO | None:
        return get_content_provider().get_page_meta(slug)

    @staticmethod
    def build_breadcrumbs(page: PageMetaDTO | None) -> list[BreadcrumbItemDTO]:
        from flask import has_request_context, request, url_for

        home_url = url_for("main.index", _external=True) if has_request_context() else "/"
        crumbs = [BreadcrumbItemDTO(label="Home", url=home_url, is_current=False)]

        if page and page.slug != "home":
            current_url = (
                request.url.split("?")[0].split("#")[0]
                if has_request_context()
                else f"/{page.slug}"
            )
            crumbs.append(
                BreadcrumbItemDTO(label=page.title, url=current_url, is_current=True)
            )

        return crumbs

    @staticmethod
    def get_cta_for_page(slug: str):
        provider = get_content_provider()
        cta = provider.get_cta_section(slug)
        if cta:
            return cta
        return provider.get_cta_section("global")

    @staticmethod
    def page_shell(slug: str) -> dict:
        """Shared context for every public page template."""
        page = PageService.get_meta(slug)
        return {
            "page": page,
            "breadcrumbs": PageService.build_breadcrumbs(page),
            "cta": PageService.get_cta_for_page(slug),
        }


class HomeService:
    """Homepage section aggregation."""

    @staticmethod
    def get_page_context() -> dict:
        provider = get_content_provider()
        home: HomePageDTO = provider.get_homepage()
        return {
            **PageService.page_shell("home"),
            "home": home,
        }


class ContentBlockService:
    """Reusable CMS content blocks — composable page sections."""

    @staticmethod
    def get_registry(*, active_only: bool = True) -> ContentBlockRegistryDTO:
        return get_content_provider().get_content_blocks(active_only=active_only)

    @staticmethod
    def get_block(block_key: str) -> ContentBlockDTO | None:
        return get_content_provider().get_content_block(block_key)

    @staticmethod
    def get_blocks_for_page(block_keys: list[str]) -> list[ContentBlockDTO]:
        """Return ordered blocks for a page composition (skips missing/inactive keys)."""
        registry = ContentBlockService.get_registry(active_only=True)
        blocks: list[ContentBlockDTO] = []
        for key in block_keys:
            block = registry.get(key)
            if block:
                blocks.append(block)
        return blocks


class PageBuilderService:
    """
    Page Builder — composes pages from ordered sections and CMS blocks.

    Page → Page Sections → Content Blocks → Content Block Items
    """

    @staticmethod
    def get_sections(page_slug: str, *, active_only: bool = True) -> PageSectionListDTO:
        return get_content_provider().get_page_sections(page_slug, active_only=active_only)

    @staticmethod
    def _resolve_block_keys(section: PageSectionDTO) -> list[str]:
        keys: list[str] = []
        if section.block_key:
            keys.append(section.block_key)
        for key in section.extra.get("block_keys", []):
            if key and key not in keys:
                keys.append(key)
        return keys

    @staticmethod
    def resolve_section(
        section: PageSectionDTO,
        registry: ContentBlockRegistryDTO,
    ) -> PageSectionResolvedDTO:
        blocks: list[ContentBlockDTO] = []
        for key in PageBuilderService._resolve_block_keys(section):
            block = registry.get(key)
            if block and block.is_active:
                blocks.append(block)

        return PageSectionResolvedDTO(
            id=section.id,
            page_slug=section.page_slug,
            section_key=section.section_key,
            section_title=section.section_title,
            block_key=section.block_key,
            display_order=section.display_order,
            layout_type=section.layout_type,
            background_style=section.background_style,
            spacing=section.spacing,
            animation=section.animation,
            is_visible=section.is_visible,
            seo_anchor=section.seo_anchor,
            is_active=section.is_active,
            extra=section.extra,
            created_at=section.created_at,
            updated_at=section.updated_at,
            block=blocks[0] if blocks else None,
            blocks=blocks,
        )

    @staticmethod
    def get_composition(
        page_slug: str,
        *,
        active_only: bool = True,
        include_hidden: bool = True,
    ) -> PageCompositionDTO:
        """
        Build a fully resolved page for dynamic frontend rendering.

        When include_hidden=False, sections with is_visible=False are omitted.
        """
        section_list = PageBuilderService.get_sections(page_slug, active_only=active_only)
        registry = ContentBlockService.get_registry(active_only=True)

        sections: list[PageSectionResolvedDTO] = []
        for section in section_list.sections:
            if not include_hidden and not section.is_visible:
                continue
            sections.append(PageBuilderService.resolve_section(section, registry))

        return PageCompositionDTO(page_slug=page_slug, sections=sections)


class AboutService:
    @staticmethod
    def get_page_context() -> dict:
        provider = get_content_provider()
        page_composition = PageBuilderService.get_composition("about")
        about_blocks = ContentBlockService.get_blocks_for_page(
            [
                "company_overview",
                "company_introduction",
                "directors_message",
                "company_history",
                "vision",
                "mission",
                "core_values",
                "hse_policy",
                "why_choose_guruh",
                "company_strengths",
                "certifications_registrations",
                "equipment_overview",
                "company_experience",
                "areas_of_operation",
                "company_statistics",
                "leadership_team",
                "partners",
                "call_to_action",
            ]
        )
        return {
            **PageService.page_shell("about"),
            "about": provider.get_about_section("about"),
            "profile": provider.get_company_profile(),
            "cms_blocks": ContentBlockRegistryDTO(blocks=about_blocks),
            "page_composition": page_composition,
        }

    @staticmethod
    def get_company_profile():
        """Official company profile DTO — ready for About page templates."""
        return get_content_provider().get_company_profile()


class ServicesService:
    @staticmethod
    def get_page_context() -> dict:
        provider = get_content_provider()
        return {
            **PageService.page_shell("services"),
            "services": provider.get_services(),
            "projects": provider.get_projects(),
            "page_composition": PageBuilderService.get_composition("services"),
        }


class ProjectsService:
    @staticmethod
    def get_page_context() -> dict:
        provider = get_content_provider()
        return {
            **PageService.page_shell("projects"),
            "projects": provider.get_projects(),
            "services": provider.get_services(),
            "page_composition": PageBuilderService.get_composition("projects"),
        }

    @staticmethod
    def get_detail_context(slug: str) -> dict | None:
        from flask import has_request_context, request, url_for

        provider = get_content_provider()
        project = provider.get_project_by_slug(slug)
        if not project or not project.is_active:
            return None

        page_slug = f"project-{slug}"
        page = PageMetaDTO(
            slug=page_slug,
            title=project.title,
            meta_title=project.meta_title or project.title,
            meta_description=project.meta_description or project.description,
            is_published=True,
            banner_subtitle=f"{project.category} · {project.location}",
            banner_image=project.cover_image,
        )

        home_url = url_for("main.index", _external=True) if has_request_context() else "/"
        projects_url = url_for("main.projects", _external=True) if has_request_context() else "/projects"
        current_url = (
            request.url.split("?")[0].split("#")[0]
            if has_request_context()
            else f"/projects/{slug}"
        )

        breadcrumbs = [
            BreadcrumbItemDTO(label="Home", url=home_url, is_current=False),
            BreadcrumbItemDTO(label="Projects", url=projects_url, is_current=False),
            BreadcrumbItemDTO(label=project.title, url=current_url, is_current=True),
        ]

        from app.providers.project_detail_loader import build_composition_for_project

        composition = build_composition_for_project(project)

        return {
            "page": page,
            "project": project,
            "projects": provider.get_projects(),
            "services": provider.get_services(),
            "breadcrumbs": breadcrumbs,
            "cta": PageService.get_cta_for_page("projects"),
            "page_composition": composition,
        }


class EquipmentService:
    @staticmethod
    def get_page_context() -> dict:
        provider = get_content_provider()
        return {
            **PageService.page_shell("equipment"),
            "equipment": provider.get_equipment(),
            "projects": provider.get_projects(),
            "services": provider.get_services(),
            "page_composition": PageBuilderService.get_composition("equipment"),
        }

    @staticmethod
    def get_detail_context(slug: str) -> dict | None:
        from flask import has_request_context, request, url_for

        provider = get_content_provider()
        item = provider.get_equipment_by_slug(slug)
        if not item or not item.is_active:
            return None

        page_slug = f"equipment-{slug}"
        page = PageMetaDTO(
            slug=page_slug,
            title=item.name,
            meta_title=item.meta_title or item.name,
            meta_description=item.meta_description or item.short_description,
            is_published=True,
            banner_subtitle=f"{item.category} · {item.capacity}",
            banner_image=item.image,
        )

        home_url = url_for("main.index", _external=True) if has_request_context() else "/"
        equipment_url = url_for("main.equipment", _external=True) if has_request_context() else "/equipment"
        current_url = (
            request.url.split("?")[0].split("#")[0]
            if has_request_context()
            else f"/equipment/{slug}"
        )

        breadcrumbs = [
            BreadcrumbItemDTO(label="Home", url=home_url, is_current=False),
            BreadcrumbItemDTO(label="Equipment", url=equipment_url, is_current=False),
            BreadcrumbItemDTO(label=item.name, url=current_url, is_current=True),
        ]

        return {
            "page": page,
            "equipment_item": item,
            "equipment": provider.get_equipment(),
            "projects": provider.get_projects(),
            "services": provider.get_services(),
            "breadcrumbs": breadcrumbs,
            "cta": PageService.get_cta_for_page("equipment"),
            "page_composition": PageBuilderService.get_composition(page_slug),
        }


class TeamService:
    @staticmethod
    def get_page_context() -> dict:
        provider = get_content_provider()
        team = provider.get_team_members()
        return {
            **PageService.page_shell("team"),
            "team": team,
            "directors": [m for m in team if m.member_type == "director" and m.is_active],
            "executives": [m for m in team if m.member_type == "executive" and m.is_active],
            "staff": [m for m in team if m.member_type == "staff" and m.is_active],
            "page_composition": PageBuilderService.get_composition("team"),
        }


class CareersService:
    @staticmethod
    def get_page_context() -> dict:
        provider = get_content_provider()
        return {
            **PageService.page_shell("careers"),
            "jobs": provider.get_job_listings(),
            "job_application_fields": provider.get_job_application_fields(),
            "job_application_options": provider.get_job_application_options(),
            "page_composition": PageBuilderService.get_composition("careers"),
        }

    @staticmethod
    def get_detail_context(slug: str) -> dict | None:
        from flask import has_request_context, request, url_for

        provider = get_content_provider()
        job = provider.get_job_by_slug(slug)
        if not job or not job.is_active:
            return None

        page_slug = f"career-{slug}"
        page = PageMetaDTO(
            slug=page_slug,
            title=job.title,
            meta_title=job.meta_title or job.title,
            meta_description=job.meta_description or job.short_description,
            is_published=True,
            banner_subtitle=f"{job.department} · {job.location}",
            banner_image=job.image,
        )

        home_url = url_for("main.index", _external=True) if has_request_context() else "/"
        careers_url = url_for("main.careers", _external=True) if has_request_context() else "/careers"
        current_url = (
            request.url.split("?")[0].split("#")[0]
            if has_request_context()
            else f"/careers/{slug}"
        )

        breadcrumbs = [
            BreadcrumbItemDTO(label="Home", url=home_url, is_current=False),
            BreadcrumbItemDTO(label="Careers", url=careers_url, is_current=False),
            BreadcrumbItemDTO(label=job.title, url=current_url, is_current=True),
        ]

        return {
            "page": page,
            "job": job,
            "jobs": provider.get_job_listings(),
            "job_application_fields": provider.get_job_application_fields(),
            "job_application_options": provider.get_job_application_options(),
            "breadcrumbs": breadcrumbs,
            "cta": PageService.get_cta_for_page("careers"),
            "page_composition": PageBuilderService.get_composition(page_slug),
        }


class GalleryService:
    @staticmethod
    def get_page_context() -> dict:
        provider = get_content_provider()
        gallery_images = provider.get_gallery_images()
        return {
            **PageService.page_shell("gallery"),
            "gallery": gallery_images,
            "gallery_images": gallery_images,
            "gallery_albums": provider.get_gallery_albums(),
            "gallery_videos": provider.get_gallery_videos(),
            "gallery_downloads": provider.get_gallery_downloads(),
            "before_after_items": provider.get_before_after_gallery(),
            "progress_items": provider.get_progress_gallery(),
            "awards_items": provider.get_awards_gallery(),
            "gallery_filter_options": provider.get_gallery_filter_options(),
            "page_composition": PageBuilderService.get_composition("gallery"),
        }


class CatalogService:
    """Services, projects, gallery, team, testimonials, careers."""

    @staticmethod
    def get_services_page() -> dict:
        return ServicesService.get_page_context()

    @staticmethod
    def get_projects_page() -> dict:
        return ProjectsService.get_page_context()

    @staticmethod
    def get_equipment_page() -> dict:
        return EquipmentService.get_page_context()

    @staticmethod
    def get_gallery_page() -> dict:
        return GalleryService.get_page_context()

    @staticmethod
    def get_team_page() -> dict:
        return TeamService.get_page_context()

    @staticmethod
    def get_testimonials_page() -> dict:
        provider = get_content_provider()
        return {
            **PageService.page_shell("testimonials"),
            "testimonials": provider.get_testimonials(),
        }

    @staticmethod
    def get_careers_page() -> dict:
        return CareersService.get_page_context()


class ContactService:
    @staticmethod
    def get_contact_page() -> dict:
        provider = get_content_provider()
        return {
            **PageService.page_shell("contact"),
            "contact": provider.get_contact_page(),
            "office": provider.get_office_location(),
            "offices": provider.get_contact_offices(),
            "departments": provider.get_department_contacts(),
            "emergency": provider.get_emergency_contact(),
            "map_location": provider.get_map_location(),
            "contact_form_fields": provider.get_contact_form_fields(),
            "services": provider.get_services(),
            "social_links": provider.get_social_links(),
            "page_composition": PageBuilderService.get_composition("contact"),
        }

    @staticmethod
    def get_quote_page() -> dict:
        provider = get_content_provider()
        return {
            **PageService.page_shell("request-quote"),
            "quote": provider.get_quote_page(),
            "quote_form_fields": provider.get_quote_form_fields(),
            "quote_form_steps": provider.get_quote_form_steps(),
            "quote_form_options": provider.get_quote_form_options(),
            "services": provider.get_services(),
            "page_composition": PageBuilderService.get_composition("request-quote"),
        }
