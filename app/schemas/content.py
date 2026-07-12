"""
Shared dataclasses (DTOs) for passing content from services to templates.

Templates consume these objects — never SQLAlchemy models directly.
This keeps presentation decoupled from the database layer.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class NavItemDTO:
    id: int
    label: str
    endpoint: str
    sort_order: int = 0
    is_active: bool = True
    children: list["NavItemDTO"] = field(default_factory=list)


@dataclass
class SocialLinkDTO:
    id: int
    platform: str
    label: str
    icon: str
    url: str
    sort_order: int = 0
    is_active: bool = True


@dataclass
class CompanyInfoDTO:
    name: str
    short_name: str
    tagline: str
    description: str
    phone: str
    phone_primary: str
    email: str
    address: str
    office_hours: str
    phone_secondary: str = ""
    phone_tel: str = ""
    head_office_label: str = "Head Office"
    postal_address: str = ""
    address_area: str = ""
    address_district: str = ""
    address_locality: str = ""
    address_country: str = ""
    address_country_code: str = ""
    founded_country: str = ""
    founded_country_code: str = ""
    operating_country: str = ""
    operating_country_code: str = ""
    headquarters: str = ""
    logo_path: str = "img/logo.png"


@dataclass
class FooterContentDTO:
    copyright_text: str
    about_text: str
    quick_links: list[NavItemDTO] = field(default_factory=list)
    service_links: list["ServiceDTO"] = field(default_factory=list)


@dataclass
class PageMetaDTO:
    slug: str
    title: str
    meta_title: str
    meta_description: str
    is_published: bool = True
    banner_subtitle: str = ""
    banner_image: str = ""


@dataclass
class BreadcrumbItemDTO:
    label: str
    url: str
    is_current: bool = False


@dataclass
class HeroSlideDTO:
    id: int
    title: str
    subtitle: str
    description: str
    image: str
    cta_text: str
    cta_url: str
    sort_order: int = 0
    is_active: bool = True
    secondary_cta_text: str = ""
    secondary_cta_url: str = ""
    overlay_opacity: float = 0.65
    text_alignment: str = "left"
    background_type: str = "image"
    video_path: str = ""
    video_thumbnail: str = ""
    autoplay: bool = True
    loop: bool = True
    muted: bool = True
    plays_inline: bool = True


@dataclass
class AboutSectionDTO:
    id: int
    heading: str
    subheading: str
    content: str
    image: str
    highlights: list[str] = field(default_factory=list)
    cta_text: str = ""
    cta_url: str = ""


@dataclass
class StatisticDTO:
    id: int
    label: str
    value: str
    suffix: str = ""
    icon: str = ""
    sort_order: int = 0


@dataclass
class PartnerDTO:
    id: int
    name: str
    logo: str
    url: str = ""
    sort_order: int = 0


@dataclass
class ServiceDTO:
    id: int
    title: str
    slug: str
    short_description: str
    description: str
    icon: str
    image: str
    sort_order: int = 0
    is_featured: bool = False
    is_active: bool = True


@dataclass
class ProjectDTO:
    id: int
    title: str
    slug: str
    description: str
    location: str
    client: str
    category: str
    cover_image: str
    completion_date: str = ""
    sort_order: int = 0
    is_featured: bool = False
    is_active: bool = True
    county: str = ""
    country: str = ""
    status: str = ""
    completion_year: str = ""
    service_slugs: list[str] = field(default_factory=list)
    consultant: str = ""
    duration: str = ""
    overview: str = ""
    scope_of_work: list[str] = field(default_factory=list)
    challenges: list[str] = field(default_factory=list)
    solutions: list[str] = field(default_factory=list)
    equipment_used: list[str] = field(default_factory=list)
    gallery_images: list[str] = field(default_factory=list)
    gallery_categories: list[dict] = field(default_factory=list)
    related_project_slugs: list[str] = field(default_factory=list)
    meta_title: str = ""
    meta_description: str = ""
    documents: list[dict] = field(default_factory=list)
    videos: list[dict] = field(default_factory=list)
    testimonial_ids: list[int] = field(default_factory=list)


@dataclass
class GalleryImageDTO:
    """Gallery media item — admin-manageable image record."""

    id: int
    title: str
    image: str
    category: str
    sort_order: int = 0
    is_active: bool = True
    slug: str = ""
    project_slug: str = ""
    project_title: str = ""
    service_slug: str = ""
    service_title: str = ""
    equipment_slug: str = ""
    equipment_title: str = ""
    county: str = ""
    year: str = ""
    location: str = ""
    date: str = ""
    album: str = ""
    caption: str = ""


@dataclass
class GalleryAlbumDTO:
    id: int
    title: str
    slug: str
    description: str
    image: str
    filter_album: str
    icon: str = "bi-images"
    sort_order: int = 0
    is_active: bool = True


@dataclass
class GalleryVideoDTO:
    id: int
    title: str
    provider: str
    description: str = ""
    video_id: str = ""
    embed_url: str = ""
    thumbnail: str = ""
    play_url: str = ""
    is_ready: bool = False
    sort_order: int = 0
    is_active: bool = True


@dataclass
class GalleryDownloadDTO:
    id: int
    title: str
    file_type: str
    description: str
    file_url: str = ""
    is_ready: bool = False
    icon: str = "bi-file-earmark-pdf"
    sort_order: int = 0
    is_active: bool = True


@dataclass
class BeforeAfterItemDTO:
    id: int
    title: str
    before_image: str
    after_image: str
    project_title: str = ""
    location: str = ""
    sort_order: int = 0
    is_active: bool = True


@dataclass
class ProgressGalleryItemDTO:
    id: int
    title: str
    subtitle: str
    image: str
    date: str = ""
    sort_order: int = 0
    is_active: bool = True


@dataclass
class GalleryFilterOptionsDTO:
    projects: list[str] = field(default_factory=list)
    services: list[str] = field(default_factory=list)
    equipment: list[str] = field(default_factory=list)
    categories: list[str] = field(default_factory=list)
    counties: list[str] = field(default_factory=list)
    years: list[str] = field(default_factory=list)
    albums: list[str] = field(default_factory=list)


@dataclass
class TeamMemberDTO:
    id: int
    name: str
    position: str
    bio: str
    photo: str
    email: str = ""
    phone: str = ""
    sort_order: int = 0
    is_active: bool = True
    slug: str = ""
    department: str = ""
    member_type: str = ""
    years_experience: str = ""
    education: str = ""
    experience_summary: str = ""
    social_links: list[dict] = field(default_factory=list)
    is_featured: bool = False


@dataclass
class TestimonialDTO:
    id: int
    client_name: str
    client_title: str
    company: str
    content: str
    photo: str = ""
    rating: int = 5
    sort_order: int = 0
    is_featured: bool = False
    project_slug: str = ""


@dataclass
class JobListingDTO:
    """Job vacancy — admin-manageable careers catalog record."""

    id: int
    title: str
    slug: str
    department: str
    location: str
    employment_type: str
    short_description: str
    description: str
    requirements: str
    experience_required: str = ""
    responsibilities: list[str] = field(default_factory=list)
    qualifications: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    benefits: list[str] = field(default_factory=list)
    deadline: str = ""
    image: str = ""
    meta_title: str = ""
    meta_description: str = ""
    sort_order: int = 0
    is_active: bool = True


@dataclass
class JobApplicationOptionsDTO:
    """Select options for job application form."""

    experience_levels: list[str] = field(default_factory=list)


@dataclass
class CTASectionDTO:
    heading: str
    subheading: str
    button_text: str
    button_url: str
    secondary_button_text: str = ""
    secondary_button_url: str = ""


@dataclass
class FeatureItemDTO:
    """Single feature item (Why Choose Us, values, etc.)."""

    id: int
    title: str
    description: str
    icon: str
    sort_order: int = 0


@dataclass
class WhyChooseUsSectionDTO:
    """Why Choose Us homepage section — admin-manageable."""

    id: int
    heading: str
    subheading: str
    intro: str
    image: str
    items: list[FeatureItemDTO] = field(default_factory=list)


@dataclass
class ProcessStepDTO:
    """Single step in the working process timeline."""

    id: int
    step_number: int
    title: str
    description: str
    icon: str
    sort_order: int = 0


@dataclass
class WorkingProcessSectionDTO:
    """Working process section — admin-manageable."""

    id: int
    heading: str
    subheading: str
    intro: str
    steps: list[ProcessStepDTO] = field(default_factory=list)


@dataclass
class SectionHeadingDTO:
    """Reusable section heading block."""

    heading: str
    subheading: str = ""
    intro: str = ""


@dataclass
class TrustBadgeDTO:
    """Trust badge displayed on hero section."""

    id: int
    label: str
    icon: str
    sort_order: int = 0


@dataclass
class ContactPageDTO:
    heading: str
    subheading: str
    intro: str
    map_embed: str = ""
    form_heading: str = "Send Us a Message"


@dataclass
class QuotePageDTO:
    heading: str
    subheading: str
    intro: str
    form_heading: str = "Request a Project Quote"


@dataclass
class OfficeLocationDTO:
    """Head office or branch — admin-manageable location record."""

    name: str
    address: str
    postal_address: str
    phone_primary: str
    id: int = 0
    slug: str = ""
    office_label: str = "Office"
    phone_secondary: str = ""
    phone_tel: str = ""
    email: str = ""
    office_hours: str = ""
    address_area: str = ""
    address_locality: str = ""
    address_district: str = ""
    address_country: str = ""
    address_country_code: str = ""
    is_headquarters: bool = False
    show_on_contact_page: bool = True
    sort_order: int = 0
    is_active: bool = True


@dataclass
class DepartmentContactDTO:
    """Department contact line — future CMS record."""

    id: int
    name: str
    contact_person: str = ""
    phone: str = ""
    email: str = ""
    description: str = ""
    icon: str = "bi-building"
    sort_order: int = 0
    is_active: bool = True


@dataclass
class EmergencyContactDTO:
    """Emergency / after-hours contact."""

    title: str
    phone: str
    description: str = ""
    availability: str = ""
    icon: str = "bi-exclamation-triangle-fill"
    phone_tel: str = ""


@dataclass
class MapLocationDTO:
    """Map coordinates — prepared for dynamic Google Maps embed."""

    latitude: float
    longitude: float
    zoom: int = 15
    embed_url: str = ""
    map_provider: str = "google-maps"
    map_ready: bool = False
    title: str = ""
    short_summary: str = ""


@dataclass
class FormFieldDTO:
    """Dynamic form field definition — CMS-ready."""

    name: str
    label: str
    field_type: str
    required: bool = False
    placeholder: str = ""
    help_text: str = ""
    options: list[str] = field(default_factory=list)
    options_source: str = ""
    col_class: str = "col-12"
    autocomplete: str = ""
    rows: int = 4
    accept: str = ""
    multiple: bool = False
    disabled: bool = False
    step_key: str = ""


@dataclass
class QuoteFormStepDTO:
    """Multi-step quote wizard step — CMS-ready."""

    key: str
    title: str
    subtitle: str = ""
    description: str = ""
    icon: str = "bi-circle"
    sort_order: int = 0
    step_type: str = "form"


@dataclass
class QuoteFormOptionsDTO:
    """Select options for quote form dropdowns."""

    project_categories: list[str] = field(default_factory=list)
    project_types: list[str] = field(default_factory=list)
    budget_ranges: list[str] = field(default_factory=list)
    currencies: list[str] = field(default_factory=list)
    priorities: list[str] = field(default_factory=list)
    timelines: list[str] = field(default_factory=list)
    contact_methods: list[str] = field(default_factory=list)


@dataclass
class DirectorsMessageDTO:
    heading: str
    signatories: list[str]
    summary: str


@dataclass
class CoreValueDTO:
    title: str
    description: str


@dataclass
class HsePolicyDTO:
    principle: str
    summary: str
    commitments: list[str] = field(default_factory=list)


@dataclass
class CertificationDTO:
    title: str
    issuer: str
    reference: str
    category: str
    valid_until: str = ""
    notes: str = ""


@dataclass
class EquipmentItemDTO:
    name: str
    category: str
    description: str = ""


@dataclass
class EquipmentDTO:
    """Catalog equipment item — admin-manageable fleet record."""

    id: int
    name: str
    slug: str
    category: str
    short_description: str
    description: str
    image: str
    capacity: str = ""
    condition: str = "Operational"
    maintenance_status: str = ""
    category_key: str = ""
    sort_order: int = 0
    is_featured: bool = False
    is_active: bool = True
    usage: str = ""
    specifications: list[dict] = field(default_factory=list)
    gallery_images: list[str] = field(default_factory=list)
    gallery_categories: list[dict] = field(default_factory=list)
    related_project_slugs: list[str] = field(default_factory=list)
    related_service_slugs: list[str] = field(default_factory=list)
    meta_title: str = ""
    meta_description: str = ""


@dataclass
class DirectorDTO:
    name: str
    role: str
    bio: str = ""


@dataclass
class ContentBlockItemDTO:
    """Repeatable item within a CMS content block."""

    id: int
    block_key: str
    item_key: str
    title: str
    subtitle: str = ""
    short_summary: str = ""
    full_content: str = ""
    image: str = ""
    icon: str = ""
    sort_order: int = 0
    is_active: bool = True
    extra: dict = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""


@dataclass
class ContentBlockDTO:
    """
    Reusable CMS content block — composable into any page template.

    Admin dashboard manages these records; templates never hardcode section copy.
    """

    id: int
    block_key: str
    title: str
    subtitle: str = ""
    short_summary: str = ""
    full_content: str = ""
    hero_image: str = ""
    gallery_images: list[str] = field(default_factory=list)
    display_order: int = 0
    is_active: bool = True
    meta_title: str = ""
    meta_description: str = ""
    og_image: str = ""
    extra: dict = field(default_factory=dict)
    items: list[ContentBlockItemDTO] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""


@dataclass
class ContentBlockRegistryDTO:
    """All CMS blocks keyed for page composition."""

    blocks: list[ContentBlockDTO] = field(default_factory=list)

    def get(self, block_key: str) -> Optional[ContentBlockDTO]:
        return next((b for b in self.blocks if b.block_key == block_key), None)

    def active_blocks(self) -> list[ContentBlockDTO]:
        return [b for b in self.blocks if b.is_active]


@dataclass
class PageSectionDTO:
    """
    Page Builder section — placement and presentation config for a page.

    References one or more CMS content blocks via block_key / extra.block_keys.
    """

    id: int
    page_slug: str
    section_key: str
    section_title: str
    block_key: str = ""
    display_order: int = 0
    layout_type: str = "default"
    background_style: str = "default"
    spacing: str = "default"
    animation: str = "none"
    is_visible: bool = True
    seo_anchor: str = ""
    is_active: bool = True
    extra: dict = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""


@dataclass
class PageSectionResolvedDTO(PageSectionDTO):
    """Page section with resolved CMS content block(s) attached."""

    block: Optional[ContentBlockDTO] = None
    blocks: list[ContentBlockDTO] = field(default_factory=list)


@dataclass
class PageSectionListDTO:
    """Ordered sections for a single page."""

    page_slug: str
    sections: list[PageSectionDTO] = field(default_factory=list)

    def active_sections(self) -> list[PageSectionDTO]:
        return [s for s in self.sections if s.is_active]

    def visible_sections(self) -> list[PageSectionDTO]:
        return [s for s in self.sections if s.is_active and s.is_visible]


@dataclass
class PageCompositionDTO:
    """
    Fully resolved page for dynamic frontend rendering.

    Page → Sections → Blocks → Items
    """

    page_slug: str
    sections: list[PageSectionResolvedDTO] = field(default_factory=list)

    def visible_sections(self) -> list[PageSectionResolvedDTO]:
        return [s for s in self.sections if s.is_active and s.is_visible]


@dataclass
class CompanyProfileDTO:
    """Aggregated official company profile — admin-manageable."""

    overview: str
    introduction: str
    about: str
    history: str
    experience: str
    equipment_overview: str
    vision: str
    mission: str
    directors_message: DirectorsMessageDTO
    core_values: list[CoreValueDTO] = field(default_factory=list)
    hse_policy: Optional[HsePolicyDTO] = None
    strengths: list[str] = field(default_factory=list)
    certifications: list[CertificationDTO] = field(default_factory=list)
    equipment: list[EquipmentItemDTO] = field(default_factory=list)
    directors: list[DirectorDTO] = field(default_factory=list)
    source_document: str = ""
    last_extracted: str = ""
    founded_country: str = ""
    founded_country_code: str = ""
    operating_country: str = ""
    operating_country_code: str = ""
    headquarters: str = ""


@dataclass
class HomePageDTO:
    """Aggregated homepage content — each section is admin-manageable."""

    hero_slides: list[HeroSlideDTO] = field(default_factory=list)
    hero_trust_badges: list[TrustBadgeDTO] = field(default_factory=list)
    hero_floating_stats: list[StatisticDTO] = field(default_factory=list)
    about: Optional[AboutSectionDTO] = None
    featured_services: list[ServiceDTO] = field(default_factory=list)
    featured_projects: list[ProjectDTO] = field(default_factory=list)
    why_choose_us: Optional[WhyChooseUsSectionDTO] = None
    statistics: list[StatisticDTO] = field(default_factory=list)
    working_process: Optional[WorkingProcessSectionDTO] = None
    testimonials: list[TestimonialDTO] = field(default_factory=list)
    partners: list[PartnerDTO] = field(default_factory=list)
    cta: Optional[CTASectionDTO] = None
    services_heading: Optional[SectionHeadingDTO] = None
    projects_heading: Optional[SectionHeadingDTO] = None
    testimonials_heading: Optional[SectionHeadingDTO] = None
    partners_heading: Optional[SectionHeadingDTO] = None
