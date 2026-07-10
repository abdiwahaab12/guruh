"""
Content provider interface.

Implementations:
  - PlaceholderContentProvider  → development without MySQL
  - DatabaseContentProvider     → production with MySQL

Services call get_content_provider() — never import a provider directly.
"""

from abc import ABC, abstractmethod
from typing import Optional

from app.schemas.content import (
    AboutSectionDTO,
    BeforeAfterItemDTO,
    CompanyInfoDTO,
    CompanyProfileDTO,
    ContactPageDTO,
    ContentBlockDTO,
    ContentBlockRegistryDTO,
    CTASectionDTO,
    DepartmentContactDTO,
    EmergencyContactDTO,
    FooterContentDTO,
    FormFieldDTO,
    GalleryImageDTO,
    GalleryAlbumDTO,
    GalleryDownloadDTO,
    GalleryFilterOptionsDTO,
    GalleryVideoDTO,
    HeroSlideDTO,
    HomePageDTO,
    JobListingDTO,
    MapLocationDTO,
    JobApplicationOptionsDTO,
    NavItemDTO,
    OfficeLocationDTO,
    PageMetaDTO,
    PageSectionListDTO,
    PartnerDTO,
    ProgressGalleryItemDTO,
    ProjectDTO,
    ProcessStepDTO,
    QuoteFormOptionsDTO,
    QuoteFormStepDTO,
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


class ContentProvider(ABC):
    """Abstract data source — swap implementations without changing services."""

    # --- Site-wide (header, footer, settings) ---

    @abstractmethod
    def get_company_info(self) -> CompanyInfoDTO: ...

    @abstractmethod
    def get_nav_items(self, *, header: bool = True) -> list[NavItemDTO]: ...

    @abstractmethod
    def get_social_links(self) -> list[SocialLinkDTO]: ...

    @abstractmethod
    def get_footer_content(self) -> FooterContentDTO: ...

    # --- Page metadata ---

    @abstractmethod
    def get_page_meta(self, slug: str) -> Optional[PageMetaDTO]: ...

    # --- Homepage sections ---

    @abstractmethod
    def get_homepage(self) -> HomePageDTO: ...

    # --- Catalog pages ---

    @abstractmethod
    def get_about_section(self, page_slug: str = "about") -> Optional[AboutSectionDTO]: ...

    @abstractmethod
    def get_services(self, *, featured_only: bool = False) -> list[ServiceDTO]: ...

    @abstractmethod
    def get_service_by_slug(self, slug: str) -> Optional[ServiceDTO]: ...

    @abstractmethod
    def get_projects(self, *, featured_only: bool = False) -> list[ProjectDTO]: ...

    @abstractmethod
    def get_project_by_slug(self, slug: str) -> Optional[ProjectDTO]: ...

    @abstractmethod
    def get_equipment(self, *, featured_only: bool = False) -> list[EquipmentDTO]: ...

    @abstractmethod
    def get_equipment_by_slug(self, slug: str) -> Optional[EquipmentDTO]: ...

    @abstractmethod
    def get_gallery_images(self) -> list[GalleryImageDTO]: ...

    @abstractmethod
    def get_gallery_albums(self) -> list[GalleryAlbumDTO]: ...

    @abstractmethod
    def get_gallery_videos(self) -> list[GalleryVideoDTO]: ...

    @abstractmethod
    def get_gallery_downloads(self) -> list[GalleryDownloadDTO]: ...

    @abstractmethod
    def get_before_after_gallery(self) -> list[BeforeAfterItemDTO]: ...

    @abstractmethod
    def get_progress_gallery(self) -> list[ProgressGalleryItemDTO]: ...

    @abstractmethod
    def get_awards_gallery(self) -> list[GalleryImageDTO]: ...

    @abstractmethod
    def get_gallery_filter_options(self) -> GalleryFilterOptionsDTO: ...

    @abstractmethod
    def get_team_members(self) -> list[TeamMemberDTO]: ...

    @abstractmethod
    def get_testimonials(self, *, featured_only: bool = False) -> list[TestimonialDTO]: ...

    @abstractmethod
    def get_job_listings(self) -> list[JobListingDTO]: ...

    @abstractmethod
    def get_job_by_slug(self, slug: str) -> Optional[JobListingDTO]: ...

    @abstractmethod
    def get_job_application_fields(self) -> list[FormFieldDTO]: ...

    @abstractmethod
    def get_job_application_options(self) -> JobApplicationOptionsDTO: ...

    @abstractmethod
    def get_contact_page(self) -> ContactPageDTO: ...

    @abstractmethod
    def get_quote_page(self) -> QuotePageDTO: ...

    @abstractmethod
    def get_office_location(self) -> OfficeLocationDTO: ...

    @abstractmethod
    def get_office_locations(self) -> list[OfficeLocationDTO]: ...

    @abstractmethod
    def get_contact_offices(self) -> list[OfficeLocationDTO]: ...

    @abstractmethod
    def get_department_contacts(self) -> list[DepartmentContactDTO]: ...

    @abstractmethod
    def get_emergency_contact(self) -> EmergencyContactDTO: ...

    @abstractmethod
    def get_map_location(self) -> MapLocationDTO: ...

    @abstractmethod
    def get_contact_form_fields(self) -> list[FormFieldDTO]: ...

    @abstractmethod
    def get_quote_form_fields(self) -> list[FormFieldDTO]: ...

    @abstractmethod
    def get_quote_form_options(self) -> QuoteFormOptionsDTO: ...

    @abstractmethod
    def get_quote_form_steps(self) -> list[QuoteFormStepDTO]: ...

    @abstractmethod
    def get_cta_section(self, page_slug: str = "home") -> Optional[CTASectionDTO]: ...

    @abstractmethod
    def get_statistics(self) -> list[StatisticDTO]: ...

    @abstractmethod
    def get_partners(self) -> list[PartnerDTO]: ...

    @abstractmethod
    def get_why_choose_us(self, page_slug: str = "home") -> Optional[WhyChooseUsSectionDTO]: ...

    @abstractmethod
    def get_working_process(self, page_slug: str = "home") -> Optional[WorkingProcessSectionDTO]: ...

    @abstractmethod
    def get_section_heading(self, section_key: str, page_slug: str = "home") -> Optional[SectionHeadingDTO]: ...

    @abstractmethod
    def get_company_profile(self) -> CompanyProfileDTO: ...

    # --- Reusable CMS content blocks ---

    @abstractmethod
    def get_content_blocks(self, *, active_only: bool = True) -> ContentBlockRegistryDTO: ...

    @abstractmethod
    def get_content_block(self, block_key: str) -> Optional[ContentBlockDTO]: ...

    # --- Page Builder (Page → Sections → Blocks) ---

    @abstractmethod
    def get_page_sections(
        self, page_slug: str, *, active_only: bool = True
    ) -> PageSectionListDTO: ...
