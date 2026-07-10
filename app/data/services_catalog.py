"""
Official services catalog and Services Page CMS content.

Source: approved GURUH Construction company profile.
Used by CMS blocks, page sections, and profile_loader.
"""

from app.constants.media import FALLBACK_IMAGES

SERVICES_CATALOG: list[dict] = [
    {
        "title": "Water Works",
        "slug": "water-works",
        "short_description": "Water supply, dams, boreholes, and irrigation infrastructure.",
        "description": (
            "GURUH Construction delivers licensed water resource works including water pans, "
            "earth dams, water supply systems, borehole drilling and equipping, sewerage, "
            "irrigation, and electromechanical installations across Kenya."
        ),
        "icon": "bi-droplet-fill",
        "image": FALLBACK_IMAGES["service"],
        "is_featured": True,
        "scope_of_work": [
            "Water pan and earth dam construction",
            "Water supply and distribution systems",
            "Borehole drilling and equipping",
            "Sewerage and irrigation infrastructure",
            "Electromechanical water works",
        ],
        "benefits": [
            "Licensed Qualified Water Resource Contractor (WD/WC/2669)",
            "Experienced teams for rural and urban water projects",
            "Compliance with Ministry of Water standards",
            "Integrated civil and electromechanical delivery",
        ],
        "typical_project_slugs": ["water-pan-turkana", "mzwanenyi-earth-dam", "kamukunji-dam"],
        "related_equipment": ["Bulldozers", "Excavators & Loaders", "Water Tankers"],
        "gallery_images": [FALLBACK_IMAGES["service"], FALLBACK_IMAGES["project"]],
        "project_categories": ["Water Works"],
    },
    {
        "title": "Building Works",
        "slug": "building-works",
        "short_description": "Residential and commercial building construction.",
        "description": (
            "GCCL constructs residential estates, cottages, and commercial buildings with "
            "builders work, electrical, mechanical, and associated civil works delivered "
            "to specification and safety standards."
        ),
        "icon": "bi-building",
        "image": FALLBACK_IMAGES["about"],
        "is_featured": True,
        "scope_of_work": [
            "Residential estate development",
            "Commercial and institutional buildings",
            "Builders, electrical, and mechanical works",
            "Associated civil and finishing works",
            "Interlocking paving and hard landscaping",
        ],
        "benefits": [
            "NCA6 registered building works contractor",
            "Turnkey delivery from foundation to handover",
            "Quality materials and skilled trades",
            "Director-led client engagement",
        ],
        "typical_project_slugs": ["bamburi-amani-estate", "oluwa-seun-beach-cottages"],
        "related_equipment": ["Excavators & Loaders", "Concrete production support"],
        "gallery_images": [FALLBACK_IMAGES["about"], FALLBACK_IMAGES["project"]],
        "project_categories": ["Building Works"],
    },
    {
        "title": "Civil Engineering",
        "slug": "civil-engineering",
        "short_description": "Infrastructure, drainage, culverts, and civil structures.",
        "description": (
            "Our civil engineering division delivers drainage systems, culverts, erosion "
            "protection, paving, and general infrastructure works for public and private clients."
        ),
        "icon": "bi-signpost-split-fill",
        "image": FALLBACK_IMAGES["project"],
        "is_featured": True,
        "scope_of_work": [
            "Drainage and soil erosion protection",
            "Pipe and box culvert construction",
            "Interlocking paving and hardstanding",
            "General civil infrastructure",
            "Site preparation and earthworks support",
        ],
        "benefits": [
            "Registered NCA2 road and civil contractor",
            "Proven delivery in urban and county projects",
            "Integrated planning and site execution",
            "Strong HSE and quality culture",
        ],
        "typical_project_slugs": ["drainage-culverts-donholm"],
        "related_equipment": ["Excavators & Loaders", "Road Rollers / Compactors"],
        "gallery_images": [FALLBACK_IMAGES["project"]],
        "project_categories": ["Civil Engineering"],
    },
    {
        "title": "Road Construction",
        "slug": "road-construction",
        "short_description": "Road building, grading, and bitumen surfacing.",
        "description": (
            "GCCL executes road construction and upgrading to bitumen standards including "
            "formation, grading, surfacing, and associated drainage for township and "
            "highway projects."
        ),
        "icon": "bi-sign-turn-right-fill",
        "image": FALLBACK_IMAGES["project"],
        "is_featured": True,
        "scope_of_work": [
            "Road formation and grading",
            "Asphalt and bitumen surfacing",
            "Urban and rural road construction",
            "Associated drainage integration",
            "Traffic management during construction",
        ],
        "benefits": [
            "NCA2 road works registration",
            "Modern plant including graders and pavers",
            "Experienced road construction crews",
            "On-time delivery on county contracts",
        ],
        "typical_project_slugs": ["road-construction-donholm", "isiolo-township-roads"],
        "related_equipment": ["Motor Graders", "Asphalt Pavers", "Road Rollers / Compactors"],
        "gallery_images": [FALLBACK_IMAGES["project"]],
        "project_categories": ["Road Works"],
    },
    {
        "title": "Road Maintenance",
        "slug": "road-maintenance",
        "short_description": "Routine, performance-based, and emergency road maintenance.",
        "description": (
            "We provide performance-based routine maintenance and emergency road maintenance "
            "contracts, keeping critical transport links operational across Kenya."
        ),
        "icon": "bi-truck-front-fill",
        "image": FALLBACK_IMAGES["project"],
        "is_featured": True,
        "scope_of_work": [
            "Performance-based routine maintenance",
            "Emergency road maintenance contracts",
            "Pothole patching and shoulder repairs",
            "Drainage clearance along road corridors",
            "Grading and re-gravelling works",
        ],
        "benefits": [
            "Rapid mobilisation for emergency works",
            "Documented QA and reporting processes",
            "Fleet of graders, rollers, and support plant",
            "Proven A1 highway maintenance experience",
        ],
        "typical_project_slugs": ["marich-pass-kainuk-road-maintenance", "isiolo-township-roads"],
        "related_equipment": ["Motor Graders", "Road Rollers / Compactors", "Water Tankers"],
        "gallery_images": [FALLBACK_IMAGES["project"]],
        "project_categories": ["Road Works"],
    },
    {
        "title": "Drainage & Culvert Works",
        "slug": "drainage-culvert-works",
        "short_description": "Pipe culverts, box culverts, and erosion protection.",
        "description": (
            "Specialist construction of standard pipe culverts, box culverts, and drainage "
            "improvements that protect roads, estates, and communities from flooding and "
            "soil erosion."
        ),
        "icon": "bi-water",
        "image": FALLBACK_IMAGES["service"],
        "is_featured": False,
        "scope_of_work": [
            "Standard pipe culvert installation",
            "Reinforced box culvert construction",
            "Drainage channel improvement",
            "Soil erosion protection works",
            "Stormwater management structures",
        ],
        "benefits": [
            "Engineered solutions for urban drainage",
            "Quality materials and workmanship",
            "Minimal disruption to existing traffic",
            "Long-term durability and safety",
        ],
        "typical_project_slugs": ["drainage-culverts-donholm"],
        "related_equipment": ["Excavators & Loaders", "Concrete production support"],
        "gallery_images": [FALLBACK_IMAGES["project"]],
        "project_categories": ["Civil Engineering"],
    },
    {
        "title": "Dam Construction",
        "slug": "dam-construction",
        "short_description": "Earth dams, water pans, and reservoir development.",
        "description": (
            "Construction of earth dams and water pans including excavation, embankment works, "
            "spillways, and associated access infrastructure for water resource projects."
        ),
        "icon": "bi-layers-fill",
        "image": FALLBACK_IMAGES["project"],
        "is_featured": False,
        "scope_of_work": [
            "Earth dam embankment construction",
            "Water pan excavation and lining",
            "Spillway and outlet works",
            "Access road construction to sites",
            "Quality compaction and testing",
        ],
        "benefits": [
            "Class D dam construction licence capability",
            "Heavy earthmoving fleet on site",
            "Experienced dam construction teams",
            "Community and environmental sensitivity",
        ],
        "typical_project_slugs": ["water-pan-turkana", "mzwanenyi-earth-dam", "kamukunji-dam"],
        "related_equipment": ["Bulldozers", "Excavators & Loaders", "Road Rollers / Compactors"],
        "gallery_images": [FALLBACK_IMAGES["service"], FALLBACK_IMAGES["project"]],
        "project_categories": ["Water Works"],
    },
    {
        "title": "Earth Works",
        "slug": "earth-works",
        "short_description": "Excavation, embankments, and site preparation.",
        "description": (
            "Comprehensive earthworks including excavation, cut-and-fill, embankment "
            "construction, and site preparation for roads, dams, building platforms, and "
            "infrastructure projects."
        ),
        "icon": "bi-mountain",
        "image": FALLBACK_IMAGES["project"],
        "is_featured": False,
        "scope_of_work": [
            "Bulk excavation and filling",
            "Embankment and platform construction",
            "Site clearing and grubbing",
            "Cut slope stabilisation",
            "Material haulage and placement",
        ],
        "benefits": [
            "Modern bulldozers and excavators",
            "Efficient production rates",
            "Skilled operators and supervisors",
            "Integrated with civil and road teams",
        ],
        "typical_project_slugs": ["water-pan-turkana", "road-construction-donholm"],
        "related_equipment": ["Bulldozers", "Excavators & Loaders", "Motor Graders"],
        "gallery_images": [FALLBACK_IMAGES["project"]],
        "project_categories": ["Civil Engineering", "Road Works", "Water Works"],
    },
]

SERVICES_PAGE_CONTENT: dict = {
    "overview": {
        "title": "Services Overview",
        "subtitle": "What We Deliver",
        "short_summary": (
            "GCCL provides water works, building works, and civil engineering services "
            "backed by official NCA and water contractor registrations."
        ),
        "full_content": (
            "GURUH Construction Company Limited delivers a comprehensive range of construction "
            "services across Kenya. From water infrastructure and building projects to road "
            "construction, maintenance, and specialist civil works, our qualified teams combine "
            "engineering proficiency with practical site experience.\n\n"
            "Every service is delivered with a commitment to safety, quality, and client "
            "partnership — supported by modern equipment and director-led project engagement."
        ),
        "hero_image": FALLBACK_IMAGES["service"],
    },
    "working_process": [
        {
            "title": "Consultation",
            "description": "We assess your requirements, site conditions, and project goals through detailed consultation.",
            "icon": "bi-chat-dots",
        },
        {
            "title": "Planning",
            "description": "Our team develops scope, methodology, programme, and resource plans aligned to your budget.",
            "icon": "bi-clipboard-check",
        },
        {
            "title": "Engineering",
            "description": "Technical design, specifications, and engineering solutions are prepared for approval.",
            "icon": "bi-rulers",
        },
        {
            "title": "Execution",
            "description": "Skilled crews and modern plant execute works with rigorous site management and HSE compliance.",
            "icon": "bi-hammer",
        },
        {
            "title": "Quality Control",
            "description": "Inspection, testing, and documentation at every milestone ensure works meet specification.",
            "icon": "bi-patch-check",
        },
        {
            "title": "Project Delivery",
            "description": "Final handover, as-built documentation, and client sign-off complete every engagement.",
            "icon": "bi-key",
        },
    ],
    "industries": [
        {"title": "Residential", "icon": "bi-house-door", "summary": "Estates, cottages, and housing developments."},
        {"title": "Commercial", "icon": "bi-shop", "summary": "Commercial buildings and mixed-use projects."},
        {"title": "Government", "icon": "bi-bank", "summary": "Public infrastructure and county contracts."},
        {"title": "Infrastructure", "icon": "bi-signpost-split", "summary": "Roads, drainage, and civil structures."},
        {"title": "Water Resources", "icon": "bi-droplet", "summary": "Dams, water pans, and supply systems."},
        {"title": "Industrial", "icon": "bi-gear-wide-connected", "summary": "Industrial civils and site works."},
    ],
    "why_choose": [
        {"title": "Quality", "icon": "bi-award", "summary": "Works delivered to specification with documented QA processes."},
        {"title": "Safety", "icon": "bi-shield-check", "summary": "Staff-first HSE culture on every project site."},
        {"title": "Modern Equipment", "icon": "bi-truck", "summary": "Heavy plant and support fleet for efficient delivery."},
        {"title": "Experienced Engineers", "icon": "bi-person-workspace", "summary": "Qualified staff across water, building, and civil disciplines."},
        {"title": "On-Time Delivery", "icon": "bi-clock-history", "summary": "Programme-driven execution with accountable milestones."},
        {"title": "Competitive Pricing", "icon": "bi-currency-exchange", "summary": "Transparent estimates and value-focused proposals."},
    ],
    "faq": [
        {
            "question": "What types of construction projects does GCCL undertake?",
            "answer": (
                "GCCL delivers water works, building works, civil engineering, road construction "
                "and maintenance, drainage and culvert works, dam construction, and earthworks "
                "across Kenya."
            ),
        },
        {
            "question": "Is GURUH Construction a registered contractor?",
            "answer": (
                "Yes. GCCL holds NCA2 Road Works and NCA6 Building Works registrations, plus a "
                "Qualified Water Resource Contractor licence (WD/WC/2669) from the Ministry of "
                "Water, Sanitation and Irrigation."
            ),
        },
        {
            "question": "Which counties do you operate in?",
            "answer": (
                "We have delivered projects in Nairobi, Mombasa, Kilifi, Turkana, Taita Taveta, "
                "Laikipia, Isiolo, West Pokot, and other regions across Kenya."
            ),
        },
        {
            "question": "How do I request a project quote?",
            "answer": (
                "Submit a request through our online quote form or contact our office directly. "
                "Our team will review your scope and respond with a professional proposal."
            ),
        },
        {
            "question": "Do you provide road maintenance contracts?",
            "answer": (
                "Yes. GCCL performs performance-based routine maintenance and emergency road "
                "maintenance, including contracts on major highway corridors."
            ),
        },
        {
            "question": "What equipment does GCCL deploy on site?",
            "answer": (
                "Our fleet includes bulldozers, motor graders, excavators, road rollers, asphalt "
                "pavers, and water tankers — deployed based on project requirements."
            ),
        },
    ],
    "featured_projects_intro": {
        "title": "Featured Projects",
        "subtitle": "Proven Delivery",
        "short_summary": "Explore selected projects across our core service areas.",
        "full_content": "Filter by service area to view relevant project experience from the GCCL portfolio.",
    },
    "project_filters": [
        {"item_key": "all", "title": "All Projects", "extra": {"filter_key": "all"}},
        {"item_key": "water-works", "title": "Water Works", "extra": {"filter_key": "water-works"}},
        {"item_key": "building-works", "title": "Building Works", "extra": {"filter_key": "building-works"}},
        {"item_key": "civil-engineering", "title": "Civil Engineering", "extra": {"filter_key": "civil-engineering"}},
        {"item_key": "road-works", "title": "Road Works", "extra": {"filter_key": "road-works"}},
    ],
}

# Legacy key used by profile_loader — simplified list for catalog DTOs
SERVICES_OFFERED_LEGACY = [
    {
        "title": s["title"],
        "slug": s["slug"],
        "short_description": s["short_description"],
        "description": s["description"],
        "icon": s["icon"],
        "is_featured": s.get("is_featured", False),
    }
    for s in SERVICES_CATALOG
]

PROJECT_CATEGORY_TO_FILTER: dict[str, str] = {
    "Water Works": "water-works",
    "Building Works": "building-works",
    "Civil Engineering": "civil-engineering",
    "Road Works": "road-works",
}
