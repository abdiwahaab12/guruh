"""
Role-Based Access Control — roles, permissions, and seed mappings.

Used by auth models, seed script, and permission decorators.
"""

from typing import Final

# ---------------------------------------------------------------------------
# Permission slugs (used in decorators and RBAC checks)
# ---------------------------------------------------------------------------

PERMISSION_MANAGE_PAGES: Final[str] = "manage_pages"
PERMISSION_MANAGE_SERVICES: Final[str] = "manage_services"
PERMISSION_MANAGE_PROJECTS: Final[str] = "manage_projects"
PERMISSION_MANAGE_GALLERY: Final[str] = "manage_gallery"
PERMISSION_MANAGE_EQUIPMENT: Final[str] = "manage_equipment"
PERMISSION_MANAGE_TEAM: Final[str] = "manage_team"
PERMISSION_MANAGE_CAREERS: Final[str] = "manage_careers"
PERMISSION_MANAGE_JOB_APPLICATIONS: Final[str] = "manage_job_applications"
PERMISSION_MANAGE_USERS: Final[str] = "manage_users"
PERMISSION_MANAGE_SETTINGS: Final[str] = "manage_settings"
PERMISSION_MANAGE_QUOTES: Final[str] = "manage_quotes"
PERMISSION_MANAGE_CONTACTS: Final[str] = "manage_contacts"
PERMISSION_MANAGE_MEDIA: Final[str] = "manage_media"
PERMISSION_VIEW_DASHBOARD: Final[str] = "view_dashboard"
PERMISSION_VIEW_REPORTS: Final[str] = "view_reports"

ALL_PERMISSIONS: Final[tuple[str, ...]] = (
    PERMISSION_MANAGE_PAGES,
    PERMISSION_MANAGE_SERVICES,
    PERMISSION_MANAGE_PROJECTS,
    PERMISSION_MANAGE_GALLERY,
    PERMISSION_MANAGE_EQUIPMENT,
    PERMISSION_MANAGE_TEAM,
    PERMISSION_MANAGE_CAREERS,
    PERMISSION_MANAGE_JOB_APPLICATIONS,
    PERMISSION_MANAGE_USERS,
    PERMISSION_MANAGE_SETTINGS,
    PERMISSION_MANAGE_QUOTES,
    PERMISSION_MANAGE_CONTACTS,
    PERMISSION_MANAGE_MEDIA,
    PERMISSION_VIEW_DASHBOARD,
    PERMISSION_VIEW_REPORTS,
)

PERMISSION_LABELS: Final[dict[str, str]] = {
    PERMISSION_MANAGE_PAGES: "Manage Pages",
    PERMISSION_MANAGE_SERVICES: "Manage Services",
    PERMISSION_MANAGE_PROJECTS: "Manage Projects",
    PERMISSION_MANAGE_GALLERY: "Manage Gallery",
    PERMISSION_MANAGE_EQUIPMENT: "Manage Equipment",
    PERMISSION_MANAGE_TEAM: "Manage Team",
    PERMISSION_MANAGE_CAREERS: "Manage Careers",
    PERMISSION_MANAGE_JOB_APPLICATIONS: "Manage Job Applications",
    PERMISSION_MANAGE_USERS: "Manage Users",
    PERMISSION_MANAGE_SETTINGS: "Manage Settings",
    PERMISSION_MANAGE_QUOTES: "Manage Quote Requests",
    PERMISSION_MANAGE_CONTACTS: "Manage Contact Submissions",
    PERMISSION_MANAGE_MEDIA: "Manage Media & Documents",
    PERMISSION_VIEW_DASHBOARD: "View Dashboard",
    PERMISSION_VIEW_REPORTS: "View Reports & Analytics",
}

# ---------------------------------------------------------------------------
# Role slugs
# ---------------------------------------------------------------------------

ROLE_SUPER_ADMIN: Final[str] = "super_admin"
ROLE_ADMINISTRATOR: Final[str] = "administrator"
ROLE_CONTENT_MANAGER: Final[str] = "content_manager"
ROLE_HR_MANAGER: Final[str] = "hr_manager"
ROLE_PROJECT_MANAGER: Final[str] = "project_manager"
ROLE_MEDIA_MANAGER: Final[str] = "media_manager"
ROLE_VIEWER: Final[str] = "viewer"

ROLE_DEFINITIONS: Final[list[dict[str, str]]] = [
    {
        "slug": ROLE_SUPER_ADMIN,
        "name": "Super Admin",
        "description": "Full system access including all CMS modules and user management.",
    },
    {
        "slug": ROLE_ADMINISTRATOR,
        "name": "Administrator",
        "description": "Manage website content, users, and system settings.",
    },
    {
        "slug": ROLE_CONTENT_MANAGER,
        "name": "Content Manager",
        "description": "Manage pages, services, projects, gallery, and equipment.",
    },
    {
        "slug": ROLE_HR_MANAGER,
        "name": "HR Manager",
        "description": "Manage careers, job applications, and team members.",
    },
    {
        "slug": ROLE_PROJECT_MANAGER,
        "name": "Project Manager",
        "description": "Manage projects and equipment records.",
    },
    {
        "slug": ROLE_MEDIA_MANAGER,
        "name": "Media Manager",
        "description": "Manage images, videos, and downloadable documents.",
    },
    {
        "slug": ROLE_VIEWER,
        "name": "Viewer",
        "description": "Read-only access to the admin dashboard.",
    },
]

# Role → permission slugs (Super Admin gets all permissions via code bypass)
ROLE_PERMISSIONS: Final[dict[str, tuple[str, ...]]] = {
    ROLE_SUPER_ADMIN: ALL_PERMISSIONS,
    ROLE_ADMINISTRATOR: (
        PERMISSION_MANAGE_PAGES,
        PERMISSION_MANAGE_SERVICES,
        PERMISSION_MANAGE_PROJECTS,
        PERMISSION_MANAGE_GALLERY,
        PERMISSION_MANAGE_EQUIPMENT,
        PERMISSION_MANAGE_TEAM,
        PERMISSION_MANAGE_CAREERS,
        PERMISSION_MANAGE_JOB_APPLICATIONS,
        PERMISSION_MANAGE_USERS,
        PERMISSION_MANAGE_SETTINGS,
        PERMISSION_MANAGE_QUOTES,
        PERMISSION_MANAGE_CONTACTS,
        PERMISSION_MANAGE_MEDIA,
        PERMISSION_VIEW_DASHBOARD,
        PERMISSION_VIEW_REPORTS,
    ),
    ROLE_CONTENT_MANAGER: (
        PERMISSION_MANAGE_PAGES,
        PERMISSION_MANAGE_SERVICES,
        PERMISSION_MANAGE_PROJECTS,
        PERMISSION_MANAGE_GALLERY,
        PERMISSION_MANAGE_EQUIPMENT,
        PERMISSION_VIEW_DASHBOARD,
        PERMISSION_VIEW_REPORTS,
    ),
    ROLE_HR_MANAGER: (
        PERMISSION_MANAGE_CAREERS,
        PERMISSION_MANAGE_JOB_APPLICATIONS,
        PERMISSION_MANAGE_TEAM,
        PERMISSION_VIEW_DASHBOARD,
        PERMISSION_VIEW_REPORTS,
    ),
    ROLE_PROJECT_MANAGER: (
        PERMISSION_MANAGE_PROJECTS,
        PERMISSION_MANAGE_EQUIPMENT,
        PERMISSION_VIEW_DASHBOARD,
        PERMISSION_VIEW_REPORTS,
    ),
    ROLE_MEDIA_MANAGER: (
        PERMISSION_MANAGE_GALLERY,
        PERMISSION_MANAGE_MEDIA,
        PERMISSION_VIEW_DASHBOARD,
        PERMISSION_VIEW_REPORTS,
    ),
    ROLE_VIEWER: (PERMISSION_VIEW_DASHBOARD, PERMISSION_VIEW_REPORTS),
}
