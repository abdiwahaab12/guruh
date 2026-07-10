"""
Request Quote Page catalog — multi-step form, benefits, FAQ, testimonials.

CMS-ready for future admin management of quote requests.
"""

from app.constants.media import FALLBACK_IMAGES

QUOTE_PAGE_CONTENT: dict = {
    "introduction": {
        "title": "Request a Project Quote",
        "subtitle": "Professional Estimation",
        "short_summary": (
            "Tell us about your project and receive a detailed quotation from "
            "our experienced estimation team."
        ),
        "full_content": (
            "GURUH Construction provides competitive quotations for water infrastructure, "
            "building construction, road works, and civil engineering projects "
            "across Somalia.\n\n"
            "Our multi-step quote form captures everything our estimators need to "
            "prepare an accurate proposal — from client details and project scope "
            "to budget, timeline, and supporting documents."
        ),
        "hero_image": FALLBACK_IMAGES["service"],
    },
    "why_request": {
        "title": "Why Request a Quote",
        "subtitle": "Business Benefits",
        "short_summary": (
            "Partner with a registered contractor delivering transparent pricing, "
            "technical expertise, and reliable project delivery."
        ),
        "full_content": (
            "A formal quotation from GURUH Construction gives you clarity on scope, "
            "cost, and programme before committing to construction works."
        ),
    },
    "form": {
        "title": "Multi-Step Quote Request",
        "subtitle": "Quotation Form",
        "short_summary": (
            "Complete all six steps below. Required fields are marked with an asterisk (*). "
            "We typically respond within 2–3 business days."
        ),
        "submit_label": "Submit Quote Request",
        "success_message": "Thank you. Your quote request has been received and will be reviewed by our estimation team.",
        "action_url": "/request-quote",
        "autosave_key": "guruh-quote-draft",
    },
    "faq": {
        "title": "Frequently Asked Questions",
        "subtitle": "Quote Process",
        "short_summary": "Common questions about requesting a construction quotation from GURUH.",
    },
    "testimonials": {
        "title": "What Clients Say",
        "subtitle": "Client Testimonials",
        "short_summary": "Organisations that have worked with GURUH on construction projects across Somalia.",
    },
}

QUOTE_FORM_STEPS: list[dict] = [
    {
        "key": "client_info",
        "title": "Client Information",
        "subtitle": "Step 1 of 6",
        "description": "Tell us who you are and how we can reach you.",
        "icon": "bi-person-vcard",
        "sort_order": 1,
        "step_type": "form",
    },
    {
        "key": "project_info",
        "title": "Project Information",
        "subtitle": "Step 2 of 6",
        "description": "Describe the service, type, location, and expected programme.",
        "icon": "bi-building-gear",
        "sort_order": 2,
        "step_type": "form",
    },
    {
        "key": "budget",
        "title": "Budget & Timeline",
        "subtitle": "Step 3 of 6",
        "description": "Share your estimated budget, currency, priority, and timeline.",
        "icon": "bi-cash-stack",
        "sort_order": 3,
        "step_type": "form",
    },
    {
        "key": "attachments",
        "title": "Attachments",
        "subtitle": "Step 4 of 6",
        "description": "Upload supporting documents — enabled when admin storage is connected.",
        "icon": "bi-paperclip",
        "sort_order": 4,
        "step_type": "form",
    },
    {
        "key": "details",
        "title": "Additional Details",
        "subtitle": "Step 5 of 6",
        "description": "Provide scope description, contact preference, and any extra notes.",
        "icon": "bi-card-text",
        "sort_order": 5,
        "step_type": "form",
    },
    {
        "key": "confirmation",
        "title": "Confirmation",
        "subtitle": "Step 6 of 6",
        "description": "Review your information before submitting your quote request.",
        "icon": "bi-check2-circle",
        "sort_order": 6,
        "step_type": "confirmation",
    },
]

PROJECT_CATEGORIES: list[str] = [
    "Water Works",
    "Building Works",
    "Road Works",
    "Civil Engineering",
    "Mixed / Multi-Discipline",
    "Other",
]

PROJECT_TYPES: list[str] = [
    "New Construction",
    "Renovation / Refurbishment",
    "Extension / Addition",
    "Infrastructure Upgrade",
    "Maintenance / Repair",
    "Other",
]

BUDGET_RANGES: list[str] = [
    "Under USD 50,000",
    "USD 50K – 250K",
    "USD 250K – 1 Million",
    "USD 1M – 5 Million",
    "Over USD 5 Million",
    "Not Sure / To Be Discussed",
]

CURRENCIES: list[str] = [
    "USD",
    "SOS (Somali Shilling)",
    "KES (Kenyan Shilling)",
    "EUR",
    "Other",
]

PRIORITIES: list[str] = [
    "Standard",
    "High Priority",
    "Urgent",
]

TIMELINES: list[str] = [
    "Flexible",
    "1–3 Months",
    "3–6 Months",
    "6–12 Months",
    "12+ Months",
]

CONTACT_METHODS: list[str] = [
    "Email",
    "Phone Call",
    "WhatsApp",
    "In-Person Meeting",
]

WHY_REQUEST_QUOTE_ITEMS: list[dict] = [
    {
        "title": "Transparent Pricing",
        "summary": "Detailed breakdowns with no hidden costs — scope, materials, labour, and programme clearly defined.",
        "icon": "bi-receipt-cutoff",
    },
    {
        "title": "Expert Estimation Team",
        "summary": "Qualified quantity surveyors and engineers review every request against current market rates.",
        "icon": "bi-calculator",
    },
    {
        "title": "Fast Turnaround",
        "summary": "Most quotations delivered within 2–3 business days for standard civil and building projects.",
        "icon": "bi-lightning-charge",
    },
    {
        "title": "Registered Contractor",
        "summary": "NCA-registered with proven delivery on roads, water, buildings, and infrastructure across Somalia.",
        "icon": "bi-patch-check",
    },
    {
        "title": "Tailored Proposals",
        "summary": "Every quote is customised to your site conditions, specifications, and procurement requirements.",
        "icon": "bi-sliders",
    },
    {
        "title": "Dedicated Follow-Up",
        "summary": "Assigned staff contact for clarifications, revisions, and pre-contract discussions.",
        "icon": "bi-headset",
    },
]

QUOTE_FAQ: list[dict] = [
    {
        "question": "How long does it take to receive a quotation?",
        "answer": (
            "Standard quote requests are reviewed within 2–3 business days. Complex or "
            "multi-discipline projects may require a site visit and can take up to one week."
        ),
    },
    {
        "question": "What information should I include in my request?",
        "answer": (
            "Provide as much detail as possible: project location, scope description, "
            "expected dates, budget range, and any BOQ or drawings you have available."
        ),
    },
    {
        "question": "Is the quote request free and without obligation?",
        "answer": (
            "Yes. Requesting a quotation is completely free and does not commit you to "
            "awarding the contract to GURUH Construction."
        ),
    },
    {
        "question": "Can I attach documents to my quote request?",
        "answer": (
            "File upload for BOQ, drawings, PDFs, and images will be enabled when the "
            "admin media library is connected. You may email documents separately in the meantime."
        ),
    },
    {
        "question": "Which areas does GURUH Construction serve?",
        "answer": (
            "We deliver projects across Somalia including Banadir, Lower Shabelle, "
            "Middle Shabelle, and other regions subject to site assessment."
        ),
    },
    {
        "question": "Will someone contact me after I submit?",
        "answer": (
            "Yes. A member of our estimation or business development team will contact "
            "you via your preferred method to discuss requirements and next steps."
        ),
    },
]

QUOTE_TESTIMONIALS: list[dict] = [
    {
        "name": "Mohamed Ibrahim",
        "role": "Director, Public Infrastructure Client",
        "quote": (
            "GURUH provided a detailed quotation within 48 hours. Their pricing was "
            "competitive and the proposal clearly addressed our road rehabilitation scope."
        ),
        "rating": 5,
    },
    {
        "name": "Amina Hassan",
        "role": "Project Coordinator, Water Authority",
        "quote": (
            "The quote process was professional and transparent. Every line item was "
            "explained and revisions were handled promptly."
        ),
        "rating": 5,
    },
    {
        "name": "Abdi Warsame",
        "role": "Commercial Developer",
        "quote": (
            "We received a comprehensive building works quotation that helped us secure "
            "project financing. Highly recommended for commercial projects."
        ),
        "rating": 5,
    },
    {
        "name": "Fatima Ali",
        "role": "NGO Programme Manager",
        "quote": (
            "GURUH's estimation team understood our community water kiosk programme "
            "and delivered a tailored quote aligned with donor requirements."
        ),
        "rating": 5,
    },
]

QUOTE_FORM_FIELDS: list[dict] = [
    # Step 1 — Client Information
    {
        "name": "full_name",
        "label": "Full Name",
        "field_type": "text",
        "required": True,
        "placeholder": "Your full name",
        "autocomplete": "name",
        "col_class": "col-md-6",
        "step_key": "client_info",
    },
    {
        "name": "company",
        "label": "Company Name",
        "field_type": "text",
        "required": True,
        "placeholder": "Company or organisation name",
        "autocomplete": "organization",
        "col_class": "col-md-6",
        "step_key": "client_info",
    },
    {
        "name": "email",
        "label": "Email Address",
        "field_type": "email",
        "required": True,
        "placeholder": "you@company.com",
        "autocomplete": "email",
        "col_class": "col-md-6",
        "step_key": "client_info",
    },
    {
        "name": "phone",
        "label": "Phone Number",
        "field_type": "tel",
        "required": True,
        "placeholder": "+252 XXX XXX XXX",
        "autocomplete": "tel",
        "col_class": "col-md-6",
        "step_key": "client_info",
    },
    # Step 2 — Project Information
    {
        "name": "service_type",
        "label": "Service Required",
        "field_type": "select",
        "required": True,
        "placeholder": "Select service",
        "options_source": "services",
        "col_class": "col-md-6",
        "step_key": "project_info",
    },
    {
        "name": "project_type",
        "label": "Project Type",
        "field_type": "select",
        "required": True,
        "placeholder": "Select project type",
        "options_source": "project_types",
        "col_class": "col-md-6",
        "step_key": "project_info",
    },
    {
        "name": "project_category",
        "label": "Project Category",
        "field_type": "select",
        "required": True,
        "placeholder": "Select category",
        "options_source": "project_categories",
        "col_class": "col-md-6",
        "step_key": "project_info",
    },
    {
        "name": "project_location",
        "label": "Project Location",
        "field_type": "text",
        "required": True,
        "placeholder": "County, district, or site address",
        "col_class": "col-md-6",
        "step_key": "project_info",
    },
    {
        "name": "expected_start_date",
        "label": "Expected Start Date",
        "field_type": "date",
        "required": False,
        "col_class": "col-md-6",
        "step_key": "project_info",
    },
    {
        "name": "expected_completion",
        "label": "Expected Completion Date",
        "field_type": "date",
        "required": False,
        "col_class": "col-md-6",
        "step_key": "project_info",
    },
    # Step 3 — Budget
    {
        "name": "estimated_budget",
        "label": "Estimated Budget",
        "field_type": "select",
        "required": True,
        "placeholder": "Select budget range",
        "options_source": "budget_ranges",
        "col_class": "col-md-6",
        "step_key": "budget",
    },
    {
        "name": "currency",
        "label": "Currency",
        "field_type": "select",
        "required": True,
        "placeholder": "Select currency",
        "options_source": "currencies",
        "col_class": "col-md-6",
        "step_key": "budget",
    },
    {
        "name": "priority",
        "label": "Priority",
        "field_type": "select",
        "required": True,
        "placeholder": "Select priority",
        "options_source": "priorities",
        "col_class": "col-md-6",
        "step_key": "budget",
    },
    {
        "name": "timeline",
        "label": "Timeline",
        "field_type": "select",
        "required": True,
        "placeholder": "Select timeline",
        "options_source": "timelines",
        "col_class": "col-md-6",
        "step_key": "budget",
    },
    # Step 4 — Attachments (disabled until admin upload)
    {
        "name": "boq_file",
        "label": "BOQ Documents",
        "field_type": "file",
        "required": False,
        "disabled": True,
        "help_text": "Bill of Quantities — upload enabled in future release.",
        "accept": ".pdf,.xls,.xlsx,.csv",
        "col_class": "col-md-6",
        "step_key": "attachments",
    },
    {
        "name": "drawings_file",
        "label": "Drawings & Plans",
        "field_type": "file",
        "required": False,
        "disabled": True,
        "help_text": "Architectural and engineering drawings — upload enabled in future release.",
        "accept": ".pdf,.dwg,.dxf",
        "col_class": "col-md-6",
        "step_key": "attachments",
    },
    {
        "name": "pdf_file",
        "label": "PDF Documents",
        "field_type": "file",
        "required": False,
        "disabled": True,
        "help_text": "Specifications, reports, and other PDFs — upload enabled in future release.",
        "accept": ".pdf",
        "col_class": "col-md-6",
        "step_key": "attachments",
    },
    {
        "name": "images_file",
        "label": "Site Images",
        "field_type": "file",
        "required": False,
        "disabled": True,
        "help_text": "Photos of site conditions — upload enabled in future release.",
        "accept": ".jpg,.jpeg,.png,.webp",
        "multiple": True,
        "col_class": "col-md-6",
        "step_key": "attachments",
    },
    # Step 5 — Additional Details
    {
        "name": "project_description",
        "label": "Project Description",
        "field_type": "textarea",
        "required": True,
        "placeholder": "Describe scope, deliverables, site conditions, and special requirements…",
        "rows": 6,
        "col_class": "col-12",
        "step_key": "details",
    },
    {
        "name": "preferred_contact_method",
        "label": "Preferred Contact Method",
        "field_type": "select",
        "required": True,
        "placeholder": "How should we reach you?",
        "options_source": "contact_methods",
        "col_class": "col-md-6",
        "step_key": "details",
    },
    {
        "name": "additional_notes",
        "label": "Additional Notes",
        "field_type": "textarea",
        "required": False,
        "placeholder": "Any other information for our estimation team…",
        "rows": 3,
        "col_class": "col-12",
        "step_key": "details",
    },
]
