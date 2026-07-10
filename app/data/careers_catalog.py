"""
Careers Page catalog — jobs, culture, benefits, recruitment, FAQ.

Source: GURUH Construction company profile + CMS-ready extensions.
Admin will manage vacancies via MySQL in future.
"""

from app.constants.media import FALLBACK_IMAGES
from app.data.company_profile import COMPANY_PROFILE

CAREERS_PAGE_CONTENT: dict = {
    "introduction": {
        "title": "Build Your Career With GURUH",
        "subtitle": "Join Our Team",
        "short_summary": (
            "GURUH Construction Company Limited offers rewarding careers for skilled "
            "professionals who share our commitment to safety, quality, and excellence."
        ),
        "full_content": (
            "At GURUH Construction, we believe our people are our greatest asset. We foster "
            "a culture of professional growth, teamwork, and continuous learning across "
            "water works, building construction, road works, and civil engineering projects.\n\n"
            "Whether you are an experienced engineer, project manager, or early-career "
            "professional, we provide the platform to develop your skills and contribute to "
            "landmark infrastructure across Somalia and East Africa."
        ),
        "hero_image": FALLBACK_IMAGES["hero_alt"],
    },
    "why_join_us": {
        "title": "Why Join Us",
        "subtitle": "What We Offer",
        "short_summary": "Discover the advantages of building your career with GURUH Construction.",
    },
    "job_openings": {
        "title": "Current Job Openings",
        "subtitle": "Open Positions",
        "short_summary": "Explore our latest vacancies and apply to join the GURUH team.",
    },
    "recruitment_process": {
        "title": "Recruitment Process",
        "subtitle": "How We Hire",
        "short_summary": "Our transparent hiring process ensures the right fit for every role.",
    },
    "employee_benefits": {
        "title": "Employee Benefits",
        "subtitle": "Your Rewards",
        "short_summary": "Competitive packages and support designed for long-term career success.",
    },
    "life_at_guruh": {
        "title": "Life at GURUH",
        "subtitle": "Our Workplace",
        "short_summary": "Experience the culture, teamwork, and project sites that define life at GCCL.",
    },
    "faq": {
        "title": "Frequently Asked Questions",
        "subtitle": "Careers FAQ",
        "short_summary": "Answers to common questions about working at GURUH Construction.",
    },
}

WHY_JOIN_US_ITEMS: list[dict] = [
    {
        "title": "Professional Growth",
        "summary": "Advance your career on diverse civil, building, and water infrastructure projects.",
        "icon": "bi-graph-up-arrow",
    },
    {
        "title": "Safe Working Environment",
        "summary": "HSE-first culture with strict safety protocols on every project site.",
        "icon": "bi-shield-check",
    },
    {
        "title": "Career Development",
        "summary": "Structured pathways from site roles to senior leadership and specialist positions.",
        "icon": "bi-ladder",
    },
    {
        "title": "Competitive Compensation",
        "summary": "Market-aligned salaries and performance-based incentives for qualified professionals.",
        "icon": "bi-cash-coin",
    },
    {
        "title": "Training & Development",
        "summary": "Continuous skills training, certifications, and mentorship from experienced leaders.",
        "icon": "bi-mortarboard",
    },
    {
        "title": "Team Collaboration",
        "summary": "Work alongside engineers, supervisors, and specialists in a supportive team environment.",
        "icon": "bi-people-fill",
    },
]

RECRUITMENT_STEPS: list[dict] = [
    {
        "title": "Application",
        "summary": "Submit your application with CV, cover letter, and supporting documents online.",
        "icon": "bi-file-earmark-person",
    },
    {
        "title": "Review",
        "summary": "Our HR team reviews applications against role requirements and experience.",
        "icon": "bi-search",
    },
    {
        "title": "Interview",
        "summary": "Shortlisted candidates are invited for an initial interview with HR and department heads.",
        "icon": "bi-chat-dots",
    },
    {
        "title": "Technical Assessment",
        "summary": "Role-specific technical evaluation to assess skills, knowledge, and problem-solving.",
        "icon": "bi-clipboard-check",
    },
    {
        "title": "Final Interview",
        "summary": "Senior management interview to confirm fit, expectations, and career alignment.",
        "icon": "bi-person-check",
    },
    {
        "title": "Job Offer",
        "summary": "Successful candidates receive a formal offer with compensation and start date details.",
        "icon": "bi-envelope-check",
    },
]

EMPLOYEE_BENEFITS: list[dict] = [
    {
        "title": "Health & Safety Coverage",
        "summary": "Comprehensive workplace safety programmes and health support for all staff.",
        "icon": "bi-heart-pulse",
    },
    {
        "title": "Paid Leave",
        "summary": "Annual leave, public holidays, and compassionate leave in line with company policy.",
        "icon": "bi-calendar2-check",
    },
    {
        "title": "Professional Certifications",
        "summary": "Support for NCA, HSE, and industry certifications relevant to your role.",
        "icon": "bi-award",
    },
    {
        "title": "Performance Bonuses",
        "summary": "Merit-based bonuses tied to project delivery, safety, and quality outcomes.",
        "icon": "bi-trophy",
    },
    {
        "title": "Site Allowances",
        "summary": "Competitive site allowances for field-based engineering and supervisory roles.",
        "icon": "bi-geo-alt",
    },
    {
        "title": "Career Progression",
        "summary": "Clear promotion pathways from graduate engineer to senior management.",
        "icon": "bi-bar-chart-steps",
    },
]

LIFE_AT_GURUH_GALLERY: list[dict] = [
    {"title": "Site Supervision", "image": FALLBACK_IMAGES["project"], "category": "Projects"},
    {"title": "Team Briefing", "image": FALLBACK_IMAGES["about"], "category": "Team"},
    {"title": "Equipment Operations", "image": FALLBACK_IMAGES["service"], "category": "Equipment"},
    {"title": "Engineering Works", "image": FALLBACK_IMAGES["hero_alt"], "category": "Engineering"},
    {"title": "Safety Briefing", "image": FALLBACK_IMAGES["project"], "category": "HSE"},
    {"title": "Project Milestone", "image": FALLBACK_IMAGES["about"], "category": "Projects"},
]

CAREERS_FAQ: list[dict] = [
    {
        "question": "How do I apply for a position?",
        "answer": (
            "Browse our current openings, select a role, and complete the application form on "
            "the job detail page. Upload your CV and cover letter when file upload is enabled."
        ),
    },
    {
        "question": "What is the typical recruitment timeline?",
        "answer": (
            "Our process usually takes 2–4 weeks from application to offer, depending on the "
            "role and number of applicants. We keep candidates informed at each stage."
        ),
    },
    {
        "question": "Do you hire fresh graduates?",
        "answer": (
            "Yes. We offer graduate and entry-level opportunities for civil engineering, "
            "quantity surveying, and site supervision roles with structured mentorship."
        ),
    },
    {
        "question": "Are positions based in Mogadishu only?",
        "answer": (
            "Our head office is in Mogadishu, but project sites span multiple locations across "
            "Somalia. Some roles require travel or relocation to project sites."
        ),
    },
    {
        "question": "What documents should I prepare?",
        "answer": (
            "Prepare an updated CV, cover letter, academic certificates, professional "
            "certifications, and references. File upload will be enabled in a future release."
        ),
    },
]

JOBS_CATALOG: list[dict] = [
    {
        "title": "Site Engineer",
        "slug": "site-engineer",
        "department": "Engineering",
        "location": "Mogadishu, Somalia",
        "employment_type": "Full-time",
        "experience_required": "3+ years",
        "short_description": (
            "Manage on-site construction activities, supervise subcontractors, and ensure "
            "quality and safety compliance on civil engineering projects."
        ),
        "description": (
            "GURUH Construction is seeking an experienced Site Engineer to oversee daily "
            "construction operations on water works, building, and road projects. You will "
            "coordinate site teams, monitor progress against schedules, and ensure works "
            "comply with specifications, drawings, and safety standards."
        ),
        "responsibilities": [
            "Supervise daily site activities and coordinate subcontractors",
            "Monitor work progress, quality, and compliance with specifications",
            "Prepare site reports, progress updates, and as-built documentation",
            "Enforce HSE policies and conduct toolbox talks",
            "Liaise with project managers, consultants, and client representatives",
        ],
        "qualifications": [
            "BSc in Civil Engineering or equivalent",
            "Minimum 3 years site experience on construction projects",
            "Strong knowledge of construction methods and materials",
            "Valid professional registration preferred",
        ],
        "skills": [
            "Site supervision and team leadership",
            "AutoCAD / drawing interpretation",
            "MS Project or scheduling tools",
            "Health, safety, and environmental awareness",
            "Report writing and communication",
        ],
        "benefits": [
            "Competitive salary with site allowances",
            "Career progression to senior engineer roles",
            "HSE training and certification support",
            "Exposure to major infrastructure projects",
        ],
        "requirements": "BSc Civil Engineering, 3+ years site experience, HSE awareness.",
        "deadline": "2026-09-15",
        "image": FALLBACK_IMAGES["project"],
        "meta_title": "Site Engineer Vacancy",
        "meta_description": "Apply for Site Engineer at GURUH Construction — Mogadishu, Somalia.",
        "sort_order": 1,
    },
    {
        "title": "Project Manager",
        "slug": "project-manager",
        "department": "Management",
        "location": "Mogadishu, Somalia",
        "employment_type": "Full-time",
        "experience_required": "5+ years",
        "short_description": (
            "Lead and coordinate construction projects from planning through handover, "
            "managing budgets, schedules, and stakeholder relationships."
        ),
        "description": (
            "We are looking for a Project Manager to lead medium to large-scale construction "
            "projects for GURUH Construction. You will manage project teams, control budgets "
            "and timelines, and deliver projects to client satisfaction while maintaining "
            "GCCL quality and safety standards."
        ),
        "responsibilities": [
            "Lead project planning, execution, and close-out phases",
            "Manage project budgets, schedules, and resource allocation",
            "Coordinate engineers, supervisors, subcontractors, and suppliers",
            "Report to directors and clients on progress, risks, and milestones",
            "Ensure contractual, quality, and HSE compliance throughout delivery",
        ],
        "qualifications": [
            "BSc in Civil Engineering, Construction Management, or related field",
            "Minimum 5 years project management experience in construction",
            "PMP or equivalent certification preferred",
            "Proven track record delivering infrastructure projects",
        ],
        "skills": [
            "Project planning and control",
            "Contract and procurement management",
            "Leadership and stakeholder management",
            "Risk management and problem-solving",
            "Financial and cost control",
        ],
        "benefits": [
            "Senior leadership exposure and career growth",
            "Performance-based bonuses",
            "Professional development and certification support",
            "Lead high-profile GCCL projects",
        ],
        "requirements": "BSc + 5 years PM experience, PMP preferred, strong leadership skills.",
        "deadline": "2026-09-30",
        "image": FALLBACK_IMAGES["hero_alt"],
        "meta_title": "Project Manager Vacancy",
        "meta_description": "Apply for Project Manager at GURUH Construction — Mogadishu, Somalia.",
        "sort_order": 2,
    },
    {
        "title": "Quantity Surveyor",
        "slug": "quantity-surveyor",
        "department": "Commercial",
        "location": "Mogadishu, Somalia",
        "employment_type": "Full-time",
        "experience_required": "4+ years",
        "short_description": (
            "Prepare BOQs, cost estimates, valuations, and commercial reports for "
            "construction projects across GCCL's portfolio."
        ),
        "description": (
            "GURUH Construction seeks a Quantity Surveyor to support our commercial team "
            "with cost planning, tender preparation, contract administration, and final "
            "account processes on water works, building, and civil engineering projects."
        ),
        "responsibilities": [
            "Prepare BOQs, cost plans, and tender documents",
            "Evaluate subcontractor and supplier quotations",
            "Manage interim valuations, variations, and final accounts",
            "Support procurement and contract administration",
            "Provide commercial advice to project teams and management",
        ],
        "qualifications": [
            "BSc in Quantity Surveying or Construction Economics",
            "Minimum 4 years QS experience in construction",
            "Membership of professional QS body preferred",
            "Strong analytical and numerical skills",
        ],
        "skills": [
            "BOQ preparation and cost estimation",
            "Contract types and commercial management",
            "Excel and estimating software proficiency",
            "Tender analysis and reporting",
            "Attention to detail and accuracy",
        ],
        "benefits": [
            "Commercial leadership pathway",
            "Involvement in major tenders and contracts",
            "Professional body membership support",
            "Collaborative project team environment",
        ],
        "requirements": "BSc Quantity Surveying, 4+ years experience, tender/commercial skills.",
        "deadline": "2026-09-20",
        "image": FALLBACK_IMAGES["service"],
        "meta_title": "Quantity Surveyor Vacancy",
        "meta_description": "Apply for Quantity Surveyor at GURUH Construction — Mogadishu, Somalia.",
        "sort_order": 3,
    },
    {
        "title": "Civil Engineer",
        "slug": "civil-engineer",
        "department": "Engineering",
        "location": "Mogadishu, Somalia",
        "employment_type": "Full-time",
        "experience_required": "2+ years",
        "short_description": (
            "Support design review, site engineering, and technical documentation for "
            "civil infrastructure projects."
        ),
        "description": (
            "Join our engineering team as a Civil Engineer contributing to the design, "
            "planning, and execution of roads, drainage, water works, and building projects "
            "across Somalia."
        ),
        "responsibilities": [
            "Review designs, drawings, and technical specifications",
            "Support site engineers with technical queries and solutions",
            "Prepare engineering calculations and method statements",
            "Assist with quality assurance and material testing coordination",
            "Participate in design meetings and project planning sessions",
        ],
        "qualifications": [
            "BSc in Civil Engineering",
            "Minimum 2 years relevant experience",
            "Graduate engineers with strong academic record welcome",
        ],
        "skills": [
            "Structural and civil design fundamentals",
            "AutoCAD and technical drawing review",
            "Technical report writing",
            "Site engineering support",
            "Team collaboration",
        ],
        "benefits": [
            "Graduate-to-professional development programme",
            "Mentorship from senior engineers",
            "Diverse project exposure",
            "Professional registration support",
        ],
        "requirements": "BSc Civil Engineering, 2+ years experience or strong graduate profile.",
        "deadline": "2026-10-01",
        "image": FALLBACK_IMAGES["about"],
        "meta_title": "Civil Engineer Vacancy",
        "meta_description": "Apply for Civil Engineer at GURUH Construction — Mogadishu, Somalia.",
        "sort_order": 4,
    },
    {
        "title": "Health & Safety Officer",
        "slug": "health-safety-officer",
        "department": "HSE",
        "location": "Mogadishu, Somalia",
        "employment_type": "Full-time",
        "experience_required": "3+ years",
        "short_description": (
            "Implement and monitor HSE policies across GCCL project sites, ensuring "
            "compliance with company and regulatory standards."
        ),
        "description": (
            "GURUH Construction is hiring a Health & Safety Officer to lead HSE implementation "
            "on construction sites. You will conduct inspections, training, incident "
            "investigations, and support our zero-harm culture."
        ),
        "responsibilities": [
            "Implement GCCL HSE policies and procedures on site",
            "Conduct safety inspections, audits, and toolbox talks",
            "Investigate incidents and prepare corrective action reports",
            "Maintain HSE records, permits, and compliance documentation",
            "Train site personnel on safety procedures and PPE requirements",
        ],
        "qualifications": [
            "Diploma or degree in Occupational Health & Safety or related field",
            "Minimum 3 years HSE experience in construction",
            "NEBOSH, IOSH, or equivalent certification preferred",
        ],
        "skills": [
            "HSE legislation and best practices",
            "Risk assessment and method statements",
            "Incident investigation and reporting",
            "Training and communication",
            "Site inspection and audit",
        ],
        "benefits": [
            "Lead HSE across major projects",
            "Certification and training support",
            "Safety leadership career path",
            "Impact on company-wide safety culture",
        ],
        "requirements": "HSE qualification, 3+ years construction HSE experience, NEBOSH preferred.",
        "deadline": "2026-09-25",
        "image": FALLBACK_IMAGES["project"],
        "meta_title": "Health & Safety Officer Vacancy",
        "meta_description": "Apply for HSE Officer at GURUH Construction — Mogadishu, Somalia.",
        "sort_order": 5,
    },
]

JOB_APPLICATION_FORM_FIELDS: list[dict] = [
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
        "name": "email",
        "label": "Email Address",
        "field_type": "email",
        "required": True,
        "placeholder": "you@email.com",
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
        "name": "position",
        "label": "Position Applying For",
        "field_type": "select",
        "required": True,
        "placeholder": "Select a position",
        "options_source": "jobs",
        "col_class": "col-md-6",
    },
    {
        "name": "years_experience",
        "label": "Years of Experience",
        "field_type": "select",
        "required": True,
        "placeholder": "Select experience",
        "options_source": "experience_levels",
        "col_class": "col-md-6",
    },
    {
        "name": "education",
        "label": "Highest Education",
        "field_type": "text",
        "required": True,
        "placeholder": "e.g. BSc Civil Engineering",
        "col_class": "col-md-6",
    },
    {
        "name": "cover_letter",
        "label": "Cover Letter",
        "field_type": "textarea",
        "required": True,
        "placeholder": "Tell us why you are a great fit for this role…",
        "rows": 6,
        "col_class": "col-12",
    },
    {
        "name": "resume",
        "label": "Resume / CV Upload",
        "field_type": "file",
        "required": False,
        "disabled": True,
        "help_text": "Upload your CV — file upload will be enabled in a future release.",
        "accept": ".pdf,.doc,.docx",
        "col_class": "col-md-6",
    },
    {
        "name": "certificates",
        "label": "Certificates Upload",
        "field_type": "file",
        "required": False,
        "disabled": True,
        "help_text": "Upload certificates — file upload will be enabled in a future release.",
        "accept": ".pdf,.jpg,.jpeg,.png",
        "multiple": True,
        "col_class": "col-md-6",
    },
]

EXPERIENCE_LEVELS: list[str] = [
    "Less than 1 year",
    "1–2 years",
    "3–5 years",
    "5–10 years",
    "10+ years",
]
