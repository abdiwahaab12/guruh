"""
Contact Page catalog — office, departments, map, form config.

Office and map data are sourced from app.data.company_profile.contact.
Admin will manage these records via MySQL in future.
"""

from app.constants.media import FALLBACK_IMAGES
from app.data.company_profile import COMPANY_PROFILE

_contact = COMPANY_PROFILE["contact"]
_map = _contact.get("map", {})
_head_office = _contact.get("head_office_label", "Head Office")
_locality = _contact.get("address_locality", "")


def _dept_phone(use_secondary: bool = False) -> str:
    if use_secondary and _contact.get("phone_secondary"):
        return _contact["phone_secondary"]
    return _contact["phone_primary"]


CONTACT_PAGE_CONTENT: dict = {
    "introduction": {
        "title": "Get in Touch",
        "subtitle": "We're Here to Help",
        "short_summary": (
            "Reach out to GURUH Construction for project inquiries, partnerships, "
            "tender submissions, or general support."
        ),
        "full_content": (
            "Whether you are planning a water works project, building development, "
            "road construction, or civil engineering works, our team is ready to "
            "discuss your requirements and provide professional guidance.\n\n"
            f"Visit our {_head_office.lower()} in {_locality}, call us directly, or complete the form "
            "below and we will respond within one business day."
        ),
        "hero_image": FALLBACK_IMAGES["about"],
    },
    "office": {
        "name": f"{_head_office} — {_locality}",
        "address": _contact["address"],
        "postal_address": _contact.get("postal_address", ""),
        "phone_primary": _contact["phone_primary"],
        "phone_secondary": _contact.get("phone_secondary", ""),
        "email": _contact["email"],
        "office_hours": _contact["office_hours"],
        "address_locality": _locality,
        "address_district": _contact.get("address_district", ""),
        "address_country": _contact.get("address_country", ""),
        "address_country_code": _contact.get("address_country_code", ""),
    },
    "map": {
        "title": "Find Us",
        "subtitle": f"Visit Our {_head_office}",
        "short_summary": _map.get("label", _contact["address"]),
        "latitude": _map.get("latitude", 0.0),
        "longitude": _map.get("longitude", 0.0),
        "zoom": _map.get("zoom", 16),
        "embed_url": _map.get("embed_url", ""),
        "map_provider": _map.get("map_provider", "google-maps"),
        "map_ready": _map.get("map_ready", False),
    },
    "form": {
        "title": "Send Us a Message",
        "subtitle": "Contact Form",
        "short_summary": "Complete the form and our team will respond within one business day.",
        "submit_label": "Send Message",
        "success_message": "Thank you. Your message has been received and will be reviewed shortly.",
        "action_url": "/contact",
    },
    "departments": {
        "title": "Department Contacts",
        "subtitle": "Direct Lines",
        "short_summary": "Reach the right team for faster assistance.",
    },
    "emergency": {
        "title": "Emergency Contact",
        "subtitle": "24/7 Site Support",
        "phone": _contact["phone_primary"],
        "description": (
            "For urgent site emergencies, safety incidents, or after-hours project "
            "support, contact our on-call team immediately."
        ),
        "availability": "Available 24 hours for active project sites",
        "icon": "bi-exclamation-triangle-fill",
    },
    "social": {
        "title": "Connect With Us",
        "subtitle": "Follow GURUH Construction",
        "short_summary": "Stay updated on projects, milestones, and company news.",
    },
}

DEPARTMENT_CONTACTS: list[dict] = [
    {
        "id": "general-office",
        "name": "General Office",
        "contact_person": "Reception",
        "phone": _dept_phone(),
        "email": _contact["email"],
        "description": "General inquiries, appointments, and visitor coordination.",
        "icon": "bi-building",
        "sort_order": 1,
    },
    {
        "id": "projects",
        "name": "Projects Department",
        "contact_person": "Projects Manager",
        "phone": _dept_phone(),
        "email": _contact["email"],
        "description": "Project planning, site coordination, and delivery updates.",
        "icon": "bi-kanban",
        "sort_order": 2,
    },
    {
        "id": "tender",
        "name": "Tender Department",
        "contact_person": "Tender Officer",
        "phone": _dept_phone(use_secondary=True),
        "email": _contact["email"],
        "description": "Tender submissions, prequalification, and procurement documents.",
        "icon": "bi-file-earmark-text",
        "sort_order": 3,
    },
    {
        "id": "finance",
        "name": "Finance",
        "contact_person": "Finance Manager",
        "phone": _dept_phone(use_secondary=True),
        "email": _contact["email"],
        "description": "Invoices, payments, and financial correspondence.",
        "icon": "bi-cash-stack",
        "sort_order": 4,
    },
    {
        "id": "customer-support",
        "name": "Customer Support",
        "contact_person": "Client Relations",
        "phone": _dept_phone(),
        "email": _contact["email"],
        "description": "Client feedback, warranty requests, and post-project support.",
        "icon": "bi-headset",
        "sort_order": 5,
    },
]

CONTACT_FORM_FIELDS: list[dict] = [
    {
        "name": "full_name",
        "label": "Full Name",
        "field_type": "text",
        "required": True,
        "placeholder": "Your full name",
        "autocomplete": "name",
        "col_class": "col-md-6",
    },
    {
        "name": "company_name",
        "label": "Company Name",
        "field_type": "text",
        "required": False,
        "placeholder": "Organisation (optional)",
        "autocomplete": "organization",
        "col_class": "col-md-6",
    },
    {
        "name": "email",
        "label": "Email Address",
        "field_type": "email",
        "required": True,
        "placeholder": "you@company.com",
        "autocomplete": "email",
        "col_class": "col-md-6",
    },
    {
        "name": "phone",
        "label": "Phone Number",
        "field_type": "tel",
        "required": True,
        "placeholder": "+252 XXX XXX XXX",
        "autocomplete": "tel",
        "col_class": "col-md-6",
    },
    {
        "name": "subject",
        "label": "Subject",
        "field_type": "text",
        "required": True,
        "placeholder": "Brief subject line",
        "col_class": "col-12",
    },
    {
        "name": "service_required",
        "label": "Service Required",
        "field_type": "select",
        "required": True,
        "placeholder": "Select a service",
        "options_source": "services",
        "col_class": "col-12",
    },
    {
        "name": "message",
        "label": "Message",
        "field_type": "textarea",
        "required": True,
        "placeholder": "Describe your inquiry or project requirements…",
        "rows": 5,
        "col_class": "col-12",
    },
]
