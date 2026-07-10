"""
Official projects catalog and Projects Page CMS content.

Source: approved GURUH Construction company profile + portfolio enrichment.
Used by CMS blocks, page sections, profile_loader, and project detail pages.
"""

from __future__ import annotations

from app.constants.media import FALLBACK_IMAGES

CATEGORY_TO_SERVICE_SLUG: dict[str, str] = {
    "Water Works": "water-works",
    "Building Works": "building-works",
    "Road Works": "road-construction",
    "Civil Engineering": "civil-engineering",
}

PROJECT_STATUSES: list[str] = ["Completed", "Ongoing", "Maintenance"]

PROJECT_COUNTIES: list[str] = [
    "Nairobi",
    "Mombasa",
    "Kilifi",
    "Turkana",
    "Taita Taveta",
    "Laikipia",
    "Isiolo",
    "West Pokot",
]

PROJECT_COUNTRIES: list[str] = ["Kenya", "Somalia"]

PROJECT_REGIONS_SOMALIA: list[str] = ["Banaadir", "Hodan District"]

PROJECT_CLIENTS: list[str] = [
    "Nairobi City County",
    "Isiolo County Government",
    "Kenya National Highways Authority",
    "Turkana County Government",
    "Taita Taveta County Government",
    "Private Developer",
    "Ministry of Water & Irrigation",
    "Laikipia County Government",
    "Mogadishu Municipal Partner",
    "Private Sector Client — Somalia",
]

PROJECT_YEARS: list[str] = ["2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]

PROJECTS_PAGE_CONTENT: dict = {
    "overview": {
        "title": "Construction Portfolio",
        "subtitle": "Kenya Heritage · Somalia Operations",
        "short_summary": (
            "Explore historical infrastructure delivered across Kenya and current projects "
            "underway in Somalia."
        ),
        "full_content": (
            "GURUH Construction Company Limited was founded in Kenya and built a proven "
            "portfolio of civil, building, road, and water infrastructure projects across "
            "multiple Kenyan counties since 2008. The company now operates in Somalia, "
            "delivering current and future projects from its headquarters in Mogadishu.\n\n"
            "Historical Kenya projects remain part of our portfolio. Current and future "
            "projects are categorized under Somalia."
        ),
        "hero_image": FALLBACK_IMAGES["project"],
    },
    "statistics": {
        "title": "Project Statistics",
        "subtitle": "Portfolio at a Glance",
        "short_summary": "Key metrics from GCCL's Kenya historical portfolio and Somalia operations.",
        "items": [
            {"label": "Kenya Historical Projects", "value": "9", "suffix": "+", "icon": "bi-building-check"},
            {"label": "Somalia Active Projects", "value": "3", "suffix": "+", "icon": "bi-globe2"},
            {"label": "Project Categories", "value": "4", "suffix": "", "icon": "bi-grid-3x3-gap-fill"},
            {"label": "Years of Delivery", "value": "15", "suffix": "+", "icon": "bi-calendar-check"},
        ],
    },
    "areas_map": {
        "title": "Areas of Operation",
        "subtitle": "Kenya Historical Portfolio · Somalia Current Operations",
        "short_summary": (
            "GCCL's historical project delivery spans multiple Kenyan counties. Current "
            "operations are based in Somalia with headquarters in Mogadishu."
        ),
        "full_content": (
            "Select a region to explore operational experience. Kenya counties reflect "
            "historical projects completed since 2008. Somalia regions reflect current "
            "and future project delivery."
        ),
    },
    "testimonials": {
        "title": "Client Testimonials",
        "subtitle": "Trusted Project Delivery",
        "short_summary": "What clients and partners say about working with GURUH Construction.",
    },
    "portfolio": {
        "title": "Our Project Portfolio",
        "subtitle": "Featured Work",
        "short_summary": "Filter by category, county, status, year, client, or service type.",
        "full_content": "Use the filters below to explore GCCL projects by sector, location, and delivery status.",
    },
}

PROJECT_TESTIMONIALS: list[dict] = [
    {
        "id": 1,
        "client_name": "Eng. Peter Kamau",
        "client_title": "County Engineer",
        "company": "Isiolo County Government",
        "content": (
            "GURUH Construction delivered the Isiolo township roads upgrade with professional "
            "site management and adherence to bitumen standards. Their team maintained clear "
            "communication throughout the contract period."
        ),
        "project_slug": "isiolo-township-roads",
        "rating": 5,
        "is_featured": True,
    },
    {
        "id": 2,
        "client_name": "Sarah Mwangi",
        "client_title": "Project Director",
        "company": "Private Developer",
        "content": (
            "The Bamburi Amani Estate was delivered to specification with quality finishes "
            "across all nineteen units. GCCL coordinated builders, electrical, and mechanical "
            "works efficiently on a challenging coastal site."
        ),
        "project_slug": "bamburi-amani-estate",
        "rating": 5,
        "is_featured": True,
    },
    {
        "id": 3,
        "client_name": "Hassan Abdi",
        "client_title": "Water Engineer",
        "company": "Laikipia County Government",
        "content": (
            "Kamukunji Dam construction required careful earthworks and reservoir development. "
            "GURUH demonstrated strong capability in dam construction and community water "
            "infrastructure delivery."
        ),
        "project_slug": "kamukunji-dam",
        "rating": 5,
        "is_featured": True,
    },
    {
        "id": 4,
        "client_name": "James Ochieng",
        "client_title": "Infrastructure Manager",
        "company": "Nairobi City County",
        "content": (
            "Drainage and culvert works at Donholm improved stormwater management and erosion "
            "protection. The GCCL team executed pipe and box culvert installation with minimal "
            "disruption to residents."
        ),
        "project_slug": "drainage-culverts-donholm",
        "rating": 5,
        "is_featured": True,
    },
]


def _multi_gallery(*groups: tuple[str, list[str]]) -> list[dict]:
    return [{"label": label, "images": imgs} for label, imgs in groups]


PROJECTS_CATALOG: list[dict] = [
    {
        "title": "Drainage & Culvert Works — Donholm",
        "slug": "drainage-culverts-donholm",
        "description": (
            "Construction of standard pipe culverts, box culverts, and improvement "
            "of drainage and soil erosion protection works in Donholm."
        ),
        "location": "Donholm, Nairobi",
        "county": "Nairobi",
        "client": "Nairobi City County",
        "consultant": "County consulting engineer",
        "category": "Civil Engineering",
        "status": "Completed",
        "completion_date": "2021",
        "completion_year": "2021",
        "duration": "8 months",
        "cover_image": FALLBACK_IMAGES["project"],
        "is_featured": True,
        "overview": (
            "This civil engineering project improved drainage infrastructure and erosion "
            "protection across the Donholm area in Nairobi. GCCL constructed standard pipe "
            "culverts and box culverts to manage stormwater flow and protect adjacent "
            "roadways and residential properties."
        ),
        "scope_of_work": [
            "Standard pipe culvert construction",
            "Box culvert installation",
            "Drainage channel improvement",
            "Soil erosion protection works",
            "Site reinstatement and finishing",
        ],
        "challenges": [
            "Working within a densely populated urban corridor",
            "Managing stormwater during active construction",
            "Coordinating with existing utility services",
        ],
        "solutions": [
            "Phased construction with traffic and resident management plans",
            "Temporary drainage diversion during culvert installation",
            "Daily HSE briefings and community liaison on site",
        ],
        "equipment_used": ["Excavators & Loaders", "Concrete production support"],
        "gallery_images": [FALLBACK_IMAGES["project"], FALLBACK_IMAGES["service"]],
        "gallery_categories": _multi_gallery(
            ("Site Overview", [FALLBACK_IMAGES["project"]]),
            ("Culvert Works", [FALLBACK_IMAGES["service"], FALLBACK_IMAGES["project"]]),
        ),
        "related_project_slugs": ["road-construction-donholm"],
        "meta_title": "Drainage & Culvert Works — Donholm",
        "meta_description": (
            "GCCL drainage and culvert works at Donholm, Nairobi — pipe culverts, box culverts, "
            "and erosion protection delivered for Nairobi City County."
        ),
    },
    {
        "title": "Road Construction — Donholm",
        "slug": "road-construction-donholm",
        "description": "Road construction works at Donholm including grading and surfacing.",
        "location": "Donholm, Nairobi",
        "county": "Nairobi",
        "client": "Nairobi City County",
        "consultant": "County consulting engineer",
        "category": "Road Works",
        "status": "Completed",
        "completion_date": "2020",
        "completion_year": "2020",
        "duration": "10 months",
        "cover_image": FALLBACK_IMAGES["project"],
        "is_featured": True,
        "overview": (
            "GCCL executed road construction at Donholm including earthworks, grading, and "
            "surfacing to improve local access and connectivity within the Nairobi metropolitan area."
        ),
        "scope_of_work": [
            "Site clearance and earthworks",
            "Road formation and grading",
            "Surfacing and compaction",
            "Drainage integration",
            "Road furniture and finishing",
        ],
        "challenges": [
            "Limited working width in urban sections",
            "Material haulage coordination in residential areas",
        ],
        "solutions": [
            "Night-shift haulage where approved by county authorities",
            "Compact equipment deployment for constrained sections",
        ],
        "equipment_used": ["Motor Graders", "Road Rollers / Compactors", "Excavators & Loaders"],
        "gallery_images": [FALLBACK_IMAGES["project"]],
        "gallery_categories": _multi_gallery(
            ("Road Construction", [FALLBACK_IMAGES["project"]]),
        ),
        "related_project_slugs": ["drainage-culverts-donholm"],
        "meta_title": "Road Construction — Donholm",
        "meta_description": "Road construction and surfacing at Donholm, Nairobi by GURUH Construction.",
    },
    {
        "title": "Isiolo Township Roads Upgrade & Maintenance",
        "slug": "isiolo-township-roads",
        "description": (
            "Upgrading to bitumen standards and performance of routine maintenance "
            "of Isiolo township roads."
        ),
        "location": "Isiolo County",
        "county": "Isiolo",
        "client": "Isiolo County Government",
        "consultant": "County roads department",
        "category": "Road Works",
        "status": "Completed",
        "completion_date": "2022",
        "completion_year": "2022",
        "duration": "18 months",
        "cover_image": FALLBACK_IMAGES["project"],
        "is_featured": True,
        "overview": (
            "A major township roads contract covering upgrading to bitumen standards and "
            "performance-based routine maintenance across Isiolo. GCCL deployed road plant "
            "and experienced crews for paving, compaction, and ongoing maintenance."
        ),
        "scope_of_work": [
            "Road upgrading to bitumen standards",
            "Asphalt paving and surfacing",
            "Performance-based routine maintenance",
            "Drainage and shoulder works",
            "Quality assurance and reporting",
        ],
        "challenges": [
            "Remote logistics and material supply to Isiolo",
            "Maintaining traffic flow during upgrading works",
        ],
        "solutions": [
            "Dedicated material staging and plant maintenance on site",
            "Section-by-section traffic management with county police liaison",
        ],
        "equipment_used": ["Asphalt Pavers", "Road Rollers / Compactors", "Motor Graders", "Water Tankers"],
        "gallery_images": [FALLBACK_IMAGES["project"], FALLBACK_IMAGES["service"]],
        "gallery_categories": _multi_gallery(
            ("Township Roads", [FALLBACK_IMAGES["project"]]),
            ("Paving Operations", [FALLBACK_IMAGES["service"]]),
        ),
        "related_project_slugs": ["marich-pass-kainuk-road-maintenance"],
        "meta_title": "Isiolo Township Roads Upgrade",
        "meta_description": (
            "Isiolo township roads upgrade and maintenance — bitumen standards delivery by "
            "GURUH Construction for Isiolo County Government."
        ),
    },
    {
        "title": "JN B4 (Marich Pass) – Kainuk (A1) Emergency Maintenance",
        "slug": "marich-pass-kainuk-road-maintenance",
        "description": (
            "Performance-based contract for emergency maintenance of JN B4 "
            "(Marich Pass) – Kainuk (KWS gate) (A1) Road."
        ),
        "location": "West Pokot / Turkana",
        "county": "West Pokot",
        "client": "Kenya National Highways Authority",
        "consultant": "KeNHA supervising engineer",
        "category": "Road Works",
        "status": "Maintenance",
        "completion_date": "2024",
        "completion_year": "2024",
        "duration": "Performance contract",
        "cover_image": FALLBACK_IMAGES["project"],
        "is_featured": True,
        "overview": (
            "Emergency maintenance of the strategic JN B4 (Marich Pass) – Kainuk (A1) corridor "
            "under a performance-based contract. GCCL maintains road rideability, drainage, and "
            "emergency repairs on this critical national link."
        ),
        "scope_of_work": [
            "Emergency pothole and pavement repairs",
            "Drainage clearance and erosion control",
            "Grading and re-gravelling",
            "Performance reporting to KeNHA",
            "Rapid response to road failures",
        ],
        "challenges": [
            "Harsh terrain and long transport distances",
            "Weather-related road deterioration",
        ],
        "solutions": [
            "Mobile maintenance crews with on-route plant deployment",
            "Pre-positioned materials at strategic points along the corridor",
        ],
        "equipment_used": ["Motor Graders", "Road Rollers / Compactors", "Water Tankers", "Excavators & Loaders"],
        "gallery_images": [FALLBACK_IMAGES["project"]],
        "gallery_categories": _multi_gallery(
            ("Road Maintenance", [FALLBACK_IMAGES["project"]]),
        ),
        "related_project_slugs": ["isiolo-township-roads"],
        "meta_title": "Marich Pass – Kainuk Road Maintenance",
        "meta_description": (
            "Emergency road maintenance on JN B4 Marich Pass – Kainuk (A1) by GURUH Construction."
        ),
    },
    {
        "title": "Water Pan — Turkana County",
        "slug": "water-pan-turkana",
        "description": "Construction of a water pan including earthworks and reservoir development.",
        "location": "Turkana County",
        "county": "Turkana",
        "client": "Turkana County Government",
        "consultant": "County water department",
        "category": "Water Works",
        "status": "Completed",
        "completion_date": "2019",
        "completion_year": "2019",
        "duration": "6 months",
        "cover_image": FALLBACK_IMAGES["service"],
        "is_featured": False,
        "overview": (
            "Construction of a community water pan in Turkana County including excavation, "
            "embankment works, and reservoir development to improve water security for "
            "pastoral communities."
        ),
        "scope_of_work": [
            "Site survey and setting out",
            "Excavation and embankment construction",
            "Spillway and inlet works",
            "Compaction and quality testing",
            "Community handover support",
        ],
        "challenges": [
            "Arid conditions and limited water for compaction",
            "Remote site access and logistics",
        ],
        "solutions": [
            "Water tanker support for compaction operations",
            "Advance material and plant mobilisation planning",
        ],
        "equipment_used": ["Bulldozers", "Excavators & Loaders", "Water Tankers"],
        "gallery_images": [FALLBACK_IMAGES["service"], FALLBACK_IMAGES["project"]],
        "gallery_categories": _multi_gallery(
            ("Earthworks", [FALLBACK_IMAGES["service"]]),
            ("Completed Pan", [FALLBACK_IMAGES["project"]]),
        ),
        "related_project_slugs": ["mzwanenyi-earth-dam", "kamukunji-dam"],
        "meta_title": "Water Pan — Turkana County",
        "meta_description": "Water pan construction in Turkana County by GURUH Construction.",
    },
    {
        "title": "Mzwanenyi Earth Dam",
        "slug": "mzwanenyi-earth-dam",
        "description": "Construction of Mzwanenyi earth dam including major earthmoving works.",
        "location": "Taita Taveta County",
        "county": "Taita Taveta",
        "client": "Taita Taveta County Government",
        "consultant": "County water engineer",
        "category": "Water Works",
        "status": "Completed",
        "completion_date": "2020",
        "completion_year": "2020",
        "duration": "12 months",
        "cover_image": FALLBACK_IMAGES["service"],
        "is_featured": False,
        "overview": (
            "Major earth dam construction at Mzwanenyi involving large-scale earthmoving, "
            "embankment compaction, and spillway works for community water storage."
        ),
        "scope_of_work": [
            "Dam basin excavation",
            "Embankment construction and compaction",
            "Spillway and outlet works",
            "Access road to dam site",
            "Quality control and as-built documentation",
        ],
        "challenges": [
            "Large volume earthworks in variable geology",
            "Seasonal rainfall during construction",
        ],
        "solutions": [
            "Phased embankment lifts with moisture conditioning",
            "Weather monitoring and adjusted work programmes",
        ],
        "equipment_used": ["Bulldozers", "Excavators & Loaders", "Road Rollers / Compactors"],
        "gallery_images": [FALLBACK_IMAGES["service"]],
        "gallery_categories": _multi_gallery(
            ("Dam Construction", [FALLBACK_IMAGES["service"]]),
        ),
        "related_project_slugs": ["kamukunji-dam", "water-pan-turkana"],
        "meta_title": "Mzwanenyi Earth Dam",
        "meta_description": "Mzwanenyi earth dam construction in Taita Taveta County by GCCL.",
    },
    {
        "title": "Bamburi Amani Estate",
        "slug": "bamburi-amani-estate",
        "description": (
            "Construction of nineteen (19) three-bedroom houses in Bamburi, Mombasa, "
            "including builders, electrical, mechanical, and associated civil works."
        ),
        "location": "Bamburi, Mombasa",
        "county": "Mombasa",
        "client": "Private Developer",
        "consultant": "Project architect",
        "category": "Building Works",
        "status": "Completed",
        "completion_date": "2023",
        "completion_year": "2023",
        "duration": "24 months",
        "cover_image": FALLBACK_IMAGES["about"],
        "is_featured": True,
        "overview": (
            "Turnkey delivery of nineteen three-bedroom residential units at Bamburi Amani Estate "
            "in Mombasa — including structural works, MEP installations, and associated civil "
            "infrastructure for a modern coastal housing development."
        ),
        "scope_of_work": [
            "Foundation and structural works for 19 units",
            "Builders, electrical, and mechanical installations",
            "Roofing, finishes, and external works",
            "Estate roads and drainage",
            "Handover and defect liability period",
        ],
        "challenges": [
            "Coastal climate effects on curing and finishes",
            "Coordinating multiple trades across 19 units",
        ],
        "solutions": [
            "Protected curing regimes and moisture-controlled storage",
            "Master programme with trade sequencing and weekly coordination meetings",
        ],
        "equipment_used": ["Excavators & Loaders", "Concrete production support"],
        "gallery_images": [FALLBACK_IMAGES["about"], FALLBACK_IMAGES["project"]],
        "gallery_categories": _multi_gallery(
            ("Estate Overview", [FALLBACK_IMAGES["about"]]),
            ("Construction Progress", [FALLBACK_IMAGES["project"]]),
        ),
        "related_project_slugs": ["oluwa-seun-beach-cottages"],
        "meta_title": "Bamburi Amani Estate",
        "meta_description": (
            "19 three-bedroom houses at Bamburi Amani Estate, Mombasa — building works by GCCL."
        ),
    },
    {
        "title": "Oluwa Seun Beach Cottages",
        "slug": "oluwa-seun-beach-cottages",
        "description": (
            "Construction of 1 No. two-bedroom cottage, 1 No. three-bedroom cottage, "
            "3 No. studio cottages, and a swimming pool at Kanamai, Kilifi County."
        ),
        "location": "Kanamai, Kilifi County",
        "county": "Kilifi",
        "client": "Private Developer",
        "consultant": "Resort design consultant",
        "category": "Building Works",
        "status": "Completed",
        "completion_date": "2022",
        "completion_year": "2022",
        "duration": "14 months",
        "cover_image": FALLBACK_IMAGES["about"],
        "is_featured": True,
        "overview": (
            "Boutique coastal resort construction at Kanamai featuring multiple cottage typologies "
            "and a swimming pool — delivered with attention to coastal aesthetics, MEP integration, "
            "and hospitality-quality finishes."
        ),
        "scope_of_work": [
            "Two-bedroom and three-bedroom cottage construction",
            "Three studio cottage units",
            "Swimming pool construction",
            "Landscaping and external works",
            "MEP and finishing works",
        ],
        "challenges": [
            "Beachfront site constraints and environmental sensitivity",
            "Pool waterproofing in coastal conditions",
        ],
        "solutions": [
            "Environmental management plan with controlled working zones",
            "Specialist pool waterproofing specification and inspection hold points",
        ],
        "equipment_used": ["Excavators & Loaders", "Concrete production support"],
        "gallery_images": [FALLBACK_IMAGES["about"]],
        "gallery_categories": _multi_gallery(
            ("Resort Construction", [FALLBACK_IMAGES["about"]]),
        ),
        "related_project_slugs": ["bamburi-amani-estate"],
        "meta_title": "Oluwa Seun Beach Cottages",
        "meta_description": (
            "Beach cottages and swimming pool at Kanamai, Kilifi — building works by GCCL."
        ),
    },
    {
        "title": "Kamukunji Dam",
        "slug": "kamukunji-dam",
        "description": (
            "Construction of Kamukunji Dam at Shamanei, Nyahururu, Laikipia County."
        ),
        "location": "Shamanei, Nyahururu, Laikipia County",
        "county": "Laikipia",
        "client": "Laikipia County Government",
        "consultant": "Ministry of Water supervising team",
        "category": "Water Works",
        "status": "Completed",
        "completion_date": "2021",
        "completion_year": "2021",
        "duration": "14 months",
        "cover_image": FALLBACK_IMAGES["service"],
        "is_featured": True,
        "overview": (
            "Kamukunji Dam at Shamanei, Nyahururu — a significant earth dam project delivering "
            "community water storage for Laikipia County. GCCL executed embankment construction, "
            "spillway works, and associated civil infrastructure."
        ),
        "scope_of_work": [
            "Dam basin and embankment earthworks",
            "Spillway and outlet structure construction",
            "Compaction and geotechnical compliance",
            "Access and site infrastructure",
            "Commissioning and handover documentation",
        ],
        "challenges": [
            "Highland terrain access and material sourcing",
            "Community engagement around water resource use",
        ],
        "solutions": [
            "Improved access track construction prior to main works",
            "Regular stakeholder meetings with county and community representatives",
        ],
        "equipment_used": ["Bulldozers", "Excavators & Loaders", "Road Rollers / Compactors"],
        "gallery_images": [FALLBACK_IMAGES["service"], FALLBACK_IMAGES["project"]],
        "gallery_categories": _multi_gallery(
            ("Dam Site", [FALLBACK_IMAGES["service"]]),
            ("Embankment Works", [FALLBACK_IMAGES["project"]]),
        ),
        "related_project_slugs": ["mzwanenyi-earth-dam", "water-pan-turkana"],
        "meta_title": "Kamukunji Dam",
        "meta_description": (
            "Kamukunji Dam construction at Shamanei, Nyahururu, Laikipia County by GCCL."
        ),
    },
    {
        "title": "Hodan District Road Rehabilitation — Mogadishu",
        "slug": "hodan-road-rehabilitation-mogadishu",
        "description": (
            "Road rehabilitation and drainage improvement works in Hodan District, Mogadishu."
        ),
        "location": "Hodan District, Mogadishu",
        "county": "Banaadir",
        "country": "Somalia",
        "client": "Mogadishu Municipal Partner",
        "consultant": "Municipal engineering team",
        "category": "Road Works",
        "status": "Ongoing",
        "completion_date": "",
        "completion_year": "2026",
        "duration": "12 months",
        "cover_image": FALLBACK_IMAGES["project"],
        "is_featured": True,
        "overview": (
            "GCCL is delivering road rehabilitation and associated drainage improvements "
            "in Hodan District, Mogadishu — part of the company's current operations in Somalia."
        ),
        "scope_of_work": [
            "Road formation and resurfacing",
            "Drainage channel improvement",
            "Site safety and traffic management",
        ],
        "challenges": ["Urban corridor access and coordination with local stakeholders"],
        "solutions": ["Phased works with community liaison and daily HSE briefings"],
        "equipment_used": ["Motor Graders", "Road Rollers / Compactors", "Excavators & Loaders"],
        "gallery_images": [FALLBACK_IMAGES["project"]],
        "gallery_categories": _multi_gallery(("Road Works", [FALLBACK_IMAGES["project"]])),
        "related_project_slugs": ["taleh-water-supply-mogadishu"],
        "meta_title": "Hodan District Road Rehabilitation — Mogadishu",
        "meta_description": "Road rehabilitation in Hodan District, Mogadishu by GURUH Construction.",
    },
    {
        "title": "Taleh Water Supply Infrastructure — Mogadishu",
        "slug": "taleh-water-supply-mogadishu",
        "description": (
            "Water supply infrastructure development in Taleh, Hodan District, Mogadishu."
        ),
        "location": "Taleh, Hodan District, Mogadishu",
        "county": "Hodan District",
        "country": "Somalia",
        "client": "Private Sector Client — Somalia",
        "consultant": "Independent water engineer",
        "category": "Water Works",
        "status": "Ongoing",
        "completion_date": "",
        "completion_year": "2026",
        "duration": "10 months",
        "cover_image": FALLBACK_IMAGES["service"],
        "is_featured": True,
        "overview": (
            "Water supply infrastructure works in Taleh supporting GCCL's current Somalia "
            "operations from the Mogadishu headquarters."
        ),
        "scope_of_work": [
            "Distribution line installation",
            "Storage and control infrastructure",
            "Site civil works and commissioning support",
        ],
        "challenges": ["Coordinating supply routes within an active urban district"],
        "solutions": ["Staged installation with verified hold points and quality checks"],
        "equipment_used": ["Excavators & Loaders", "Water Tankers"],
        "gallery_images": [FALLBACK_IMAGES["service"]],
        "gallery_categories": _multi_gallery(("Water Infrastructure", [FALLBACK_IMAGES["service"]])),
        "related_project_slugs": ["hodan-road-rehabilitation-mogadishu"],
        "meta_title": "Taleh Water Supply Infrastructure — Mogadishu",
        "meta_description": "Water supply infrastructure in Taleh, Mogadishu by GURUH Construction.",
    },
    {
        "title": "Commercial Building Works — Mogadishu",
        "slug": "commercial-building-mogadishu",
        "description": (
            "Commercial building construction works in Mogadishu for a private sector client."
        ),
        "location": "Mogadishu",
        "county": "Banaadir",
        "country": "Somalia",
        "client": "Private Sector Client — Somalia",
        "consultant": "Project architect",
        "category": "Building Works",
        "status": "Ongoing",
        "completion_date": "",
        "completion_year": "2026",
        "duration": "14 months",
        "cover_image": FALLBACK_IMAGES["about"],
        "is_featured": False,
        "overview": (
            "Current building works project in Mogadishu reflecting GCCL's expanded "
            "operations in Somalia."
        ),
        "scope_of_work": [
            "Structural and builders works",
            "Mechanical and electrical coordination",
            "Site finishing and handover preparation",
        ],
        "challenges": ["Material logistics and multi-trade coordination on a compact site"],
        "solutions": ["Integrated programme with weekly trade coordination meetings"],
        "equipment_used": ["Concrete production support", "Excavators & Loaders"],
        "gallery_images": [FALLBACK_IMAGES["about"]],
        "gallery_categories": _multi_gallery(("Building Works", [FALLBACK_IMAGES["about"]])),
        "related_project_slugs": ["hodan-road-rehabilitation-mogadishu"],
        "meta_title": "Commercial Building Works — Mogadishu",
        "meta_description": "Commercial building construction in Mogadishu by GURUH Construction.",
    },
]

for _proj in PROJECTS_CATALOG:
    _proj.setdefault("country", "Kenya")
    cat = _proj.get("category", "")
    service_slug = CATEGORY_TO_SERVICE_SLUG.get(cat, "")
    _proj["service_slugs"] = [service_slug] if service_slug else []

PROJECTS_BY_SLUG: dict[str, dict] = {p["slug"]: p for p in PROJECTS_CATALOG}
