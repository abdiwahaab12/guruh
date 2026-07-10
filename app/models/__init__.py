"""
SQLAlchemy models — import all models here for migrations and db.create_all().
"""

from app.models.base import BaseModel
from app.models.catalog import (
    ContactPageContent,
    ContactSubmission,
    GalleryImage,
    JobListing,
    Project,
    QuotePageContent,
    QuoteRequest,
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
from app.models.content_blocks import ContentBlock, ContentBlockItem
from app.models.page_sections import PageSection
from app.models.site import (
    CompanyInfo,
    FooterContent,
    NavItem,
    OfficeLocation,
    SiteSetting,
    SocialLink,
)
from app.models.auth import (
    AuditLog,
    LoginHistory,
    PasswordReset,
    Permission,
    Role,
    RolePermission,
    User,
    UserSession,
)
from app.models.media import MediaAsset
from app.models.project_detail import ProjectDetail
from app.models.service_detail import ServiceDetail
from app.models.equipment import Equipment, EquipmentDetail
from app.models.team_detail import TeamDetail
from app.models.gallery_detail import GalleryDetail
from app.models.job_listing_detail import JobListingDetail
from app.models.contact_submission_detail import ContactSubmissionDetail
from app.models.quote_request_detail import QuoteRequestDetail
from app.models.job_application import JobApplication

__all__ = [
    "BaseModel",
    "NavItem",
    "SocialLink",
    "CompanyInfo",
    "OfficeLocation",
    "FooterContent",
    "SiteSetting",
    "Page",
    "HeroSlide",
    "AboutSection",
    "ContentBlock",
    "ContentBlockItem",
    "PageSection",
    "Statistic",
    "Partner",
    "CTASection",
    "WhyChooseUsSection",
    "WhyChooseUsItem",
    "WorkingProcessSection",
    "ProcessStep",
    "SectionHeading",
    "TrustBadge",
    "Service",
    "Project",
    "GalleryImage",
    "TeamMember",
    "Testimonial",
    "JobListing",
    "ContactPageContent",
    "QuotePageContent",
    "ContactSubmission",
    "QuoteRequest",
    "Role",
    "Permission",
    "RolePermission",
    "User",
    "UserSession",
    "PasswordReset",
    "LoginHistory",
    "AuditLog",
    "MediaAsset",
    "ProjectDetail",
    "ServiceDetail",
    "Equipment",
    "EquipmentDetail",
    "TeamDetail",
    "GalleryDetail",
    "JobListingDetail",
    "ContactSubmissionDetail",
    "QuoteRequestDetail",
    "JobApplication",
]
