"""
Official team catalog and Team & Leadership Page CMS content.

Source: approved GURUH Construction company profile + leadership enrichment.
"""

from __future__ import annotations

from app.constants.media import FALLBACK_IMAGES

TEAM_PAGE_CONTENT: dict = {
    "introduction": {
        "title": "Leadership & Management",
        "subtitle": "Director-Led Delivery",
        "short_summary": (
            "GURUH Construction is led by experienced directors who combine strategic vision "
            "with hands-on project engagement across Kenya."
        ),
        "full_content": (
            "At GURUH Construction Company Limited, leadership means accountability on every "
            "project site. Our directors maintain direct client relationships and ensure that "
            "qualified teams deliver water, building, and civil engineering works to the highest "
            "standards of safety, quality, and professionalism.\n\n"
            "We invest in our people — engineers, supervisors, and skilled workers — and foster "
            "a culture of teamwork, innovation, and continuous improvement."
        ),
        "hero_image": FALLBACK_IMAGES["about"],
    },
    "culture": {
        "title": "Company Culture",
        "subtitle": "How We Work Together",
        "short_summary": "The values that guide every GCCL project and client relationship.",
        "items": [
            {
                "title": "Teamwork",
                "icon": "bi-people-fill",
                "summary": "Cross-functional collaboration between engineers, supervisors, and skilled trades on every site.",
            },
            {
                "title": "Innovation",
                "icon": "bi-lightbulb-fill",
                "summary": "Practical engineering solutions and modern equipment applied to complex civil and water projects.",
            },
            {
                "title": "Safety",
                "icon": "bi-shield-check",
                "summary": "Staff safety overrides production targets — HSE commitment on all project sites.",
            },
            {
                "title": "Professionalism",
                "icon": "bi-award-fill",
                "summary": "NCA-registered delivery, licensed water contracting, and ethical stakeholder engagement.",
            },
            {
                "title": "Client Commitment",
                "icon": "bi-hand-thumbs-up-fill",
                "summary": "One-on-one director engagement and transparent communication from tender to handover.",
            },
        ],
    },
    "expertise": {
        "title": "Our Expertise",
        "subtitle": "People Behind the Projects",
        "short_summary": "Qualified professionals delivering civil, building, and water infrastructure across Kenya.",
        "items": [
            {"label": "Engineers", "value": "12", "suffix": "+", "icon": "bi-person-workspace"},
            {"label": "Technical Staff", "value": "8", "suffix": "+", "icon": "bi-clipboard-data"},
            {"label": "Site Supervisors", "value": "6", "suffix": "+", "icon": "bi-hard-hat"},
            {"label": "Skilled Workers", "value": "45", "suffix": "+", "icon": "bi-tools"},
        ],
    },
    "join_team": {
        "title": "Join Our Team",
        "subtitle": "Build Your Career with GCCL",
        "short_summary": (
            "We welcome qualified engineers, site supervisors, and construction professionals "
            "who share our commitment to excellence."
        ),
        "full_content": (
            "GURUH Construction offers opportunities across civil engineering, water works, "
            "building construction, and site operations. Explore current openings and submit "
            "your application through our careers page."
        ),
    },
    "org_chart": {
        "title": "Organization Structure",
        "subtitle": "How We Are Organized",
        "short_summary": (
            "A clear leadership structure supporting project delivery, safety, and client service. "
            "Interactive org chart integration is prepared for future CMS connection."
        ),
    },
}

ORG_CHART_NODES: list[dict] = [
    {
        "id": "board",
        "title": "Board of Directors",
        "subtitle": "Strategic Leadership",
        "level": 0,
        "parent_id": "",
    },
    {
        "id": "operations",
        "title": "Operations",
        "subtitle": "Project Delivery",
        "level": 1,
        "parent_id": "board",
    },
    {
        "id": "support",
        "title": "Corporate Support",
        "subtitle": "HSE, Finance & Admin",
        "level": 1,
        "parent_id": "board",
    },
    {
        "id": "pm-roads",
        "title": "Road & Civil Projects",
        "subtitle": "Project Management",
        "level": 2,
        "parent_id": "operations",
    },
    {
        "id": "pm-water",
        "title": "Water & Building Projects",
        "subtitle": "Project Management",
        "level": 2,
        "parent_id": "operations",
    },
    {
        "id": "site-teams",
        "title": "Site Engineering Teams",
        "subtitle": "Supervisors & Engineers",
        "level": 2,
        "parent_id": "operations",
    },
    {
        "id": "hse",
        "title": "Health, Safety & Environment",
        "subtitle": "Compliance & Training",
        "level": 2,
        "parent_id": "support",
    },
    {
        "id": "finance",
        "title": "Finance & Administration",
        "subtitle": "Corporate Services",
        "level": 2,
        "parent_id": "support",
    },
]

TEAM_CATALOG: list[dict] = [
    {
        "name": "Khalif Elmi Guruh",
        "slug": "khalif-elmi-guruh",
        "position": "Director & Co-Founder",
        "member_type": "director",
        "department": "Board of Directors",
        "bio": (
            "Co-founder of GURUH Construction Company Limited. Leads company strategy, client "
            "relationships, and delivery of civil, building, and water infrastructure projects "
            "across Kenya."
        ),
        "experience_summary": (
            "15+ years in construction management and client engagement across East Africa."
        ),
        "education": "Construction & Business Management",
        "years_experience": "15+",
        "email": "guruhconstructionsomalia@gmail.com",
        "photo": "",
        "social_links": [{"platform": "linkedin", "url": "https://linkedin.com/", "icon": "bi-linkedin"}],
        "is_featured": True,
        "sort_order": 1,
    },
    {
        "name": "Adam Mariam Warsame",
        "slug": "adam-mariam-warsame",
        "position": "Director & Co-Founder",
        "member_type": "director",
        "department": "Board of Directors",
        "bio": (
            "Co-founder of GURUH Construction Company Limited. Supports project delivery, "
            "contractor operations, and stakeholder engagement across the company's construction "
            "portfolio."
        ),
        "experience_summary": (
            "Extensive experience in contractor operations, procurement, and project coordination."
        ),
        "education": "Civil Engineering & Project Management",
        "years_experience": "15+",
        "photo": "",
        "social_links": [{"platform": "linkedin", "url": "https://linkedin.com/", "icon": "bi-linkedin"}],
        "is_featured": True,
        "sort_order": 2,
    },
    {
        "name": "Eng. Hassan Mohamed",
        "slug": "hassan-mohamed",
        "position": "Chief Operations Manager",
        "member_type": "executive",
        "department": "Operations",
        "bio": (
            "Oversees day-to-day project delivery across road, water, and building contracts. "
            "Coordinates site teams, plant mobilisation, and client reporting."
        ),
        "experience_summary": "12+ years managing multi-county civil and road infrastructure projects.",
        "education": "BSc Civil Engineering",
        "years_experience": "12+",
        "photo": "",
        "social_links": [],
        "is_featured": True,
        "sort_order": 3,
    },
    {
        "name": "Grace Wanjiku",
        "slug": "grace-wanjiku",
        "position": "Project Manager — Road Works",
        "member_type": "executive",
        "department": "Road & Civil Projects",
        "bio": (
            "Leads road construction and maintenance contracts including township upgrades and "
            "emergency corridor maintenance programmes."
        ),
        "experience_summary": "Managed Isiolo township roads and national highway maintenance contracts.",
        "education": "BSc Civil Engineering, PMP",
        "years_experience": "10+",
        "photo": "",
        "social_links": [],
        "is_featured": False,
        "sort_order": 4,
    },
    {
        "name": "Abdi Noor",
        "slug": "abdi-noor",
        "position": "Project Manager — Water Works",
        "member_type": "executive",
        "department": "Water & Building Projects",
        "bio": (
            "Directs dam, water pan, and water supply projects under GCCL's licensed water "
            "resource contractor scope."
        ),
        "experience_summary": "Delivered earth dam and water pan projects in Turkana, Laikipia, and Taita Taveta.",
        "education": "BSc Water Engineering",
        "years_experience": "9+",
        "photo": "",
        "social_links": [],
        "is_featured": False,
        "sort_order": 5,
    },
    {
        "name": "Peter Omondi",
        "slug": "peter-omondi",
        "position": "Health, Safety & Environment Manager",
        "member_type": "executive",
        "department": "Health, Safety & Environment",
        "bio": (
            "Implements GCCL's HSE policy across all active sites — training, audits, incident "
            "investigation, and community liaison."
        ),
        "experience_summary": "HSE leadership on road, water, and building project sites nationwide.",
        "education": "Diploma Occupational Health & Safety",
        "years_experience": "8+",
        "photo": "",
        "social_links": [],
        "is_featured": False,
        "sort_order": 6,
    },
    {
        "name": "Fatuma Ali",
        "slug": "fatuma-ali",
        "position": "Finance & Administration Manager",
        "member_type": "executive",
        "department": "Finance & Administration",
        "bio": (
            "Manages corporate finance, procurement support, and administrative services for "
            "GCCL project and head office operations."
        ),
        "experience_summary": "Financial and contract administration for NCA-registered construction contracts.",
        "education": "BCom Finance & Accounting",
        "years_experience": "7+",
        "photo": "",
        "social_links": [],
        "is_featured": False,
        "sort_order": 7,
    },
    {
        "name": "James Mutua",
        "slug": "james-mutua",
        "position": "Senior Site Engineer",
        "member_type": "staff",
        "department": "Site Engineering",
        "bio": "Site engineering and quality control on road and civil infrastructure projects.",
        "years_experience": "8",
        "photo": "",
        "sort_order": 8,
    },
    {
        "name": "Mary Njeri",
        "slug": "mary-njeri",
        "position": "Civil Engineer",
        "member_type": "staff",
        "department": "Engineering",
        "bio": "Structural and civil design support for building and drainage works.",
        "years_experience": "6",
        "photo": "",
        "sort_order": 9,
    },
    {
        "name": "Ibrahim Yusuf",
        "slug": "ibrahim-yusuf",
        "position": "Quantity Surveyor",
        "member_type": "staff",
        "department": "Commercial",
        "bio": "Cost planning, BOQ preparation, and contract measurement for GCCL projects.",
        "years_experience": "5",
        "photo": "",
        "sort_order": 10,
    },
    {
        "name": "David Kiprop",
        "slug": "david-kiprop",
        "position": "Plant & Equipment Supervisor",
        "member_type": "staff",
        "department": "Equipment",
        "bio": "Fleet mobilisation, operator coordination, and plant maintenance on project sites.",
        "years_experience": "7",
        "photo": "",
        "sort_order": 11,
    },
    {
        "name": "Amina Hassan",
        "slug": "amina-hassan",
        "position": "Safety Officer",
        "member_type": "staff",
        "department": "Health, Safety & Environment",
        "bio": "Daily site safety inspections, toolbox talks, and incident reporting.",
        "years_experience": "4",
        "photo": "",
        "sort_order": 12,
    },
    {
        "name": "John Kamau",
        "slug": "john-kamau",
        "position": "Site Supervisor",
        "member_type": "staff",
        "department": "Site Operations",
        "bio": "On-site supervision of skilled workers and subcontractor coordination.",
        "years_experience": "9",
        "photo": "",
        "sort_order": 13,
    },
    {
        "name": "Lucy Wambui",
        "slug": "lucy-wambui",
        "position": "Administrative Officer",
        "member_type": "staff",
        "department": "Administration",
        "bio": "Office administration, document control, and project correspondence support.",
        "years_experience": "3",
        "photo": "",
        "sort_order": 14,
    },
]

TEAM_BY_TYPE: dict[str, list[dict]] = {
    "director": [m for m in TEAM_CATALOG if m["member_type"] == "director"],
    "executive": [m for m in TEAM_CATALOG if m["member_type"] == "executive"],
    "staff": [m for m in TEAM_CATALOG if m["member_type"] == "staff"],
}
