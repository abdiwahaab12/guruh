"""
Canonical CMS content block keys.

Used by models, providers, admin dashboard, and page templates.
"""

from typing import Final

# Ordered registry — display_order follows this list by default
CONTENT_BLOCK_KEYS: Final[tuple[str, ...]] = (
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
)

CONTENT_BLOCK_LABELS: Final[dict[str, str]] = {
    "company_overview": "Company Overview",
    "company_introduction": "Company Introduction",
    "directors_message": "Directors' Message",
    "company_history": "Company History",
    "vision": "Vision",
    "mission": "Mission",
    "core_values": "Core Values",
    "hse_policy": "Health, Safety & Environmental Policy",
    "why_choose_guruh": "Why Choose GURUH",
    "company_strengths": "Company Strengths",
    "certifications_registrations": "Certifications & Registrations",
    "equipment_overview": "Equipment Overview",
    "company_experience": "Company Experience",
    "areas_of_operation": "Areas of Operation",
    "company_statistics": "Company Statistics",
    "leadership_team": "Leadership Team",
    "partners": "Partners",
    "call_to_action": "Call To Action",
}

# CMS blocks whose contact fields must mirror CompanyInfo for the public site
CONTACT_SYNC_BLOCK_KEYS: Final[frozenset[str]] = frozenset(
    {
        "company_contact_info",
        "contact_office_info",
    }
)

# Blocks that use nested items (lists managed in admin)
ITEMIZED_BLOCK_KEYS: Final[frozenset[str]] = frozenset(
    {
        "core_values",
        "hse_policy",
        "company_strengths",
        "certifications_registrations",
        "equipment_overview",
        "areas_of_operation",
        "company_statistics",
        "leadership_team",
        "partners",
        "call_to_action",
    }
)
