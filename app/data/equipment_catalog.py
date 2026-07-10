"""
Official equipment catalog and Equipment Page CMS content.

Source: approved GURUH Construction company profile + fleet enrichment.
"""

from __future__ import annotations

from app.constants.media import FALLBACK_IMAGES

EQUIPMENT_CATEGORIES: list[dict] = [
    {
        "title": "Earth Moving Equipment",
        "slug": "earth-moving",
        "icon": "bi-truck-front-fill",
        "summary": "Bulldozers, excavators, and loaders for earthworks, dams, and site preparation.",
    },
    {
        "title": "Road Construction Equipment",
        "slug": "road-construction",
        "icon": "bi-signpost-split-fill",
        "summary": "Motor graders, rollers, and asphalt pavers for road building and surfacing.",
    },
    {
        "title": "Water Project Equipment",
        "slug": "water-project",
        "icon": "bi-droplet-fill",
        "summary": "Borehole rigs, pumps, and waterworks support plant for dams and supply systems.",
    },
    {
        "title": "Heavy Machinery",
        "slug": "heavy-machinery",
        "icon": "bi-gear-wide-connected",
        "summary": "Cranes, batching plants, and heavy-duty plant for major civil works.",
    },
    {
        "title": "Transport Vehicles",
        "slug": "transport-vehicles",
        "icon": "bi-truck",
        "summary": "Tipper trucks and tankers for material haulage and site logistics.",
    },
    {
        "title": "Support Equipment",
        "slug": "support-equipment",
        "icon": "bi-tools",
        "summary": "Compactors, generators, and auxiliary equipment supporting active sites.",
    },
]

CATEGORY_KEY_MAP: dict[str, str] = {c["title"]: c["slug"] for c in EQUIPMENT_CATEGORIES}


def _specs(*pairs: tuple[str, str]) -> list[dict]:
    return [{"label": label, "value": value} for label, value in pairs]


def _gallery(*groups: tuple[str, list[str]]) -> list[dict]:
    return [{"label": label, "images": imgs} for label, imgs in groups]


EQUIPMENT_PAGE_CONTENT: dict = {
    "overview": {
        "title": "Equipment & Machinery",
        "subtitle": "Modern Plant for Reliable Delivery",
        "short_summary": (
            "GURUH Construction deploys a maintained fleet of heavy plant and support "
            "equipment for civil, road, water, and building projects across Kenya."
        ),
        "full_content": (
            "GCCL invests in modern construction equipment to deliver efficient, safe, and "
            "quality project outcomes. Our fleet includes earthmoving plant, road construction "
            "machinery, water project equipment, transport vehicles, and on-site support assets "
            "— all maintained to strict safety and operational standards.\n\n"
            "Equipment is mobilised based on project scope, terrain, and client requirements, "
            "supported by qualified operators and a preventive maintenance programme."
        ),
        "hero_image": FALLBACK_IMAGES["project"],
    },
    "statistics": {
        "title": "Fleet Statistics",
        "subtitle": "Capability at a Glance",
        "short_summary": "Key metrics reflecting GCCL's equipment capacity and deployment.",
        "items": [
            {"label": "Equipment Types", "value": "12", "suffix": "+", "icon": "bi-truck-front-fill"},
            {"label": "Plant Categories", "value": "6", "suffix": "", "icon": "bi-grid-3x3-gap-fill"},
            {"label": "Counties Deployed", "value": "8", "suffix": "+", "icon": "bi-geo-alt-fill"},
            {"label": "Fleet Availability", "value": "95", "suffix": "%", "icon": "bi-check-circle-fill"},
        ],
    },
    "safety_maintenance": {
        "title": "Safety & Maintenance",
        "subtitle": "Operational Excellence",
        "short_summary": "GCCL maintains equipment to the highest safety and performance standards.",
        "full_content": (
            "Safety of staff overrides all production targets. Every item in the GCCL fleet "
            "undergoes pre-deployment inspection, scheduled servicing, and operator briefing "
            "before mobilisation to site.\n\n"
            "Our maintenance programme includes daily walk-around checks, periodic mechanical "
            "servicing, calibration of compaction and paving plant, and documented handover "
            "procedures. Equipment operators receive HSE training aligned with GCCL's official "
            "Health, Safety and Environmental Policy."
        ),
    },
    "gallery": {
        "title": "Equipment Gallery",
        "subtitle": "Fleet in Action",
        "short_summary": "Browse GCCL plant deployed on road, water, and civil construction sites.",
    },
    "faq": [
        {
            "question": "How does GCCL maintain its construction equipment?",
            "answer": (
                "GCCL follows a preventive maintenance schedule with pre-deployment inspections, "
                "scheduled servicing, and documented operator checks. Critical plant is serviced "
                "by qualified mechanics before and after major mobilisations."
            ),
        },
        {
            "question": "Can GCCL mobilise equipment for projects outside Nairobi?",
            "answer": (
                "Yes. GCCL regularly deploys plant to counties across Kenya including Isiolo, "
                "Turkana, Mombasa, Laikipia, and Taita Taveta based on project requirements."
            ),
        },
        {
            "question": "What types of projects use GCCL road construction equipment?",
            "answer": (
                "Motor graders, rollers, and asphalt pavers support township road upgrades, "
                "bitumen surfacing, and emergency road maintenance contracts such as the "
                "Isiolo township roads and Marich Pass corridor works."
            ),
        },
        {
            "question": "Is equipment included in project quotations?",
            "answer": (
                "Plant and equipment mobilisation is factored into GCCL project estimates based "
                "on scope, duration, and site conditions. Request a quote for project-specific "
                "equipment planning."
            ),
        },
    ],
}

EQUIPMENT_CATALOG: list[dict] = [
    {
        "name": "Bulldozers",
        "slug": "bulldozers",
        "category": "Earth Moving Equipment",
        "short_description": "Heavy earthmoving for dams, water pans, and road formation.",
        "description": (
            "SD22-class bulldozers used for bulk earthworks, dam basin stripping, and road "
            "formation on civil and water resource projects."
        ),
        "capacity": "SD22-class / ~220 HP",
        "condition": "Operational",
        "maintenance_status": "Quarterly service; pre-mobilisation inspection required",
        "image": FALLBACK_IMAGES["project"],
        "gallery_images": [FALLBACK_IMAGES["project"], FALLBACK_IMAGES["service"]],
        "gallery_categories": _gallery(("Earthworks", [FALLBACK_IMAGES["project"]])),
        "specifications": _specs(
            ("Class", "SD22-track type"),
            ("Application", "Dam & road earthworks"),
            ("Blade Capacity", "Heavy-duty semi-U"),
        ),
        "usage": "Dam construction, water pan development, bulk cut-and-fill, and access road formation.",
        "related_project_slugs": ["kamukunji-dam", "mzwanenyi-earth-dam", "water-pan-turkana"],
        "related_service_slugs": ["earth-works", "water-works"],
        "is_featured": True,
        "meta_title": "Bulldozers — GCCL Fleet",
        "meta_description": "SD22-class bulldozers for dam, water pan, and road earthworks by GURUH Construction.",
    },
    {
        "name": "Excavators & Loaders",
        "slug": "excavators-loaders",
        "category": "Earth Moving Equipment",
        "short_description": "Excavation, trenching, and material handling on civil sites.",
        "description": (
            "Hydraulic excavators and wheel loaders for excavation, trenching, loading, and "
            "general material handling across building and civil projects."
        ),
        "capacity": "20–30 Ton excavator class",
        "condition": "Operational",
        "maintenance_status": "Monthly hydraulic inspection; greasing schedule enforced",
        "image": FALLBACK_IMAGES["project"],
        "gallery_images": [FALLBACK_IMAGES["project"]],
        "gallery_categories": _gallery(("Site Operations", [FALLBACK_IMAGES["project"]])),
        "specifications": _specs(
            ("Excavator Class", "20–30 Ton"),
            ("Loader Type", "Wheel loader"),
            ("Attachments", "Buckets, breakers (project-specific)"),
        ),
        "usage": "Foundation excavation, culvert trenching, material loading, and site preparation.",
        "related_project_slugs": ["drainage-culverts-donholm", "bamburi-amani-estate"],
        "related_service_slugs": ["civil-engineering", "building-works", "earth-works"],
        "is_featured": True,
        "meta_title": "Excavators & Loaders",
        "meta_description": "Hydraulic excavators and wheel loaders in the GCCL construction fleet.",
    },
    {
        "name": "Motor Graders",
        "slug": "motor-graders",
        "category": "Road Construction Equipment",
        "short_description": "Precision grading for road formation and maintenance.",
        "description": (
            "Motor graders for road formation, subgrade trimming, gravel spreading, and "
            "maintenance grading on township and highway corridor projects."
        ),
        "capacity": "140–180 HP grader class",
        "condition": "Operational",
        "maintenance_status": "Blade and circle drive inspected before road mobilisation",
        "image": FALLBACK_IMAGES["project"],
        "gallery_images": [FALLBACK_IMAGES["project"]],
        "gallery_categories": _gallery(("Road Grading", [FALLBACK_IMAGES["project"]])),
        "specifications": _specs(
            ("Power Class", "140–180 HP"),
            ("Primary Use", "Road formation & maintenance"),
            ("Moldboard", "Heavy-duty adjustable"),
        ),
        "usage": "Road formation, shoulder grading, and emergency maintenance corridor works.",
        "related_project_slugs": ["isiolo-township-roads", "marich-pass-kainuk-road-maintenance"],
        "related_service_slugs": ["road-construction", "road-maintenance"],
        "is_featured": True,
        "meta_title": "Motor Graders",
        "meta_description": "Motor graders for road formation and maintenance by GURUH Construction.",
    },
    {
        "name": "Road Rollers / Compactors",
        "slug": "road-rollers-compactors",
        "category": "Road Construction Equipment",
        "short_description": "Asphalt and earth compaction for road surfacing.",
        "description": (
            "Vibratory rollers and compactors for subgrade, base course, and asphalt compaction "
            "on road construction and upgrading projects."
        ),
        "capacity": "10–12 Ton vibratory roller",
        "condition": "Operational",
        "maintenance_status": "Vibration system tested before asphalt works",
        "image": FALLBACK_IMAGES["project"],
        "gallery_images": [FALLBACK_IMAGES["project"]],
        "gallery_categories": _gallery(("Compaction", [FALLBACK_IMAGES["project"]])),
        "specifications": _specs(
            ("Roller Type", "Vibratory smooth drum"),
            ("Compaction", "Subgrade & asphalt layers"),
            ("Drum Width", "Standard highway class"),
        ),
        "usage": "Subgrade compaction, asphalt layer compaction, and dam embankment works.",
        "related_project_slugs": ["isiolo-township-roads", "kamukunji-dam"],
        "related_service_slugs": ["road-construction", "earth-works"],
        "is_featured": True,
        "meta_title": "Road Rollers & Compactors",
        "meta_description": "Road rollers and compactors for GCCL road and earthworks projects.",
    },
    {
        "name": "Asphalt Pavers",
        "slug": "asphalt-pavers",
        "category": "Road Construction Equipment",
        "short_description": "Bitumen paving and surfacing operations.",
        "description": (
            "Asphalt pavers for bitumen surfacing and township road upgrading to engineered "
            "standards on county and national road contracts."
        ),
        "capacity": "Standard highway paver class",
        "condition": "Operational",
        "maintenance_status": "Screed calibration before each paving shift",
        "image": FALLBACK_IMAGES["project"],
        "gallery_images": [FALLBACK_IMAGES["project"], FALLBACK_IMAGES["service"]],
        "gallery_categories": _gallery(("Paving", [FALLBACK_IMAGES["project"]])),
        "specifications": _specs(
            ("Paver Type", "Tracked asphalt paver"),
            ("Application", "Bitumen surfacing"),
            ("Screed", "Adjustable width"),
        ),
        "usage": "Township road upgrading, bitumen surfacing, and patch paving operations.",
        "related_project_slugs": ["isiolo-township-roads"],
        "related_service_slugs": ["road-construction"],
        "is_featured": True,
        "meta_title": "Asphalt Pavers",
        "meta_description": "Asphalt pavers for bitumen road surfacing by GURUH Construction.",
    },
    {
        "name": "Borehole Drilling Rig",
        "slug": "borehole-drilling-rig",
        "category": "Water Project Equipment",
        "short_description": "Borehole drilling and equipping for water supply projects.",
        "description": (
            "Drilling rig for borehole development and equipping under GCCL's licensed "
            "water resource contractor scope."
        ),
        "capacity": "Class C borehole drilling (up to Kshs. 5M)",
        "condition": "Operational",
        "maintenance_status": "Rig inspection and tooling check before each drilling mobilisation",
        "image": FALLBACK_IMAGES["service"],
        "gallery_images": [FALLBACK_IMAGES["service"]],
        "gallery_categories": _gallery(("Drilling", [FALLBACK_IMAGES["service"]])),
        "specifications": _specs(
            ("Licence Class", "WD/WC/2669 — Class C"),
            ("Application", "Borehole drilling & equipping"),
            ("Depth Capacity", "Project-specific"),
        ),
        "usage": "Community boreholes, water supply equipping, and rural water access projects.",
        "related_project_slugs": ["water-pan-turkana", "kamukunji-dam"],
        "related_service_slugs": ["water-works"],
        "is_featured": False,
        "meta_title": "Borehole Drilling Rig",
        "meta_description": "Licensed borehole drilling rig operated by GURUH Construction.",
    },
    {
        "name": "Water Pumps & Generators",
        "slug": "water-pumps-generators",
        "category": "Water Project Equipment",
        "short_description": "Pumping and power support for waterworks and dewatering.",
        "description": (
            "Portable pumps and generator sets supporting water supply testing, dewatering, "
            "and electromechanical water works on site."
        ),
        "capacity": "Multi-stage pumps / 50–150 kVA generators",
        "condition": "Operational",
        "maintenance_status": "Electrical safety check before waterworks deployment",
        "image": FALLBACK_IMAGES["service"],
        "gallery_images": [FALLBACK_IMAGES["service"]],
        "gallery_categories": _gallery(("Waterworks Support", [FALLBACK_IMAGES["service"]])),
        "specifications": _specs(
            ("Pump Types", "Centrifugal & dewatering"),
            ("Generator Range", "50–150 kVA"),
            ("Application", "Water testing & site power"),
        ),
        "usage": "Dam commissioning, dewatering excavations, and temporary site power supply.",
        "related_project_slugs": ["kamukunji-dam", "mzwanenyi-earth-dam"],
        "related_service_slugs": ["water-works"],
        "is_featured": False,
        "meta_title": "Water Pumps & Generators",
        "meta_description": "Water pumps and generators supporting GCCL water infrastructure projects.",
    },
    {
        "name": "Mobile Cranes",
        "slug": "mobile-cranes",
        "category": "Heavy Machinery",
        "short_description": "Lifting operations for building and civil structures.",
        "description": (
            "Mobile cranes for lifting precast elements, plant components, and structural "
            "materials on building and infrastructure sites."
        ),
        "capacity": "25–50 Ton mobile crane class",
        "condition": "Operational",
        "maintenance_status": "Certified lift plan required; annual thorough examination",
        "image": FALLBACK_IMAGES["about"],
        "gallery_images": [FALLBACK_IMAGES["about"]],
        "gallery_categories": _gallery(("Lifting Operations", [FALLBACK_IMAGES["about"]])),
        "specifications": _specs(
            ("Capacity", "25–50 Ton class"),
            ("Type", "Mobile hydraulic crane"),
            ("Certification", "Lifting plan & operator licence"),
        ),
        "usage": "Building structural lifts, culvert placement, and heavy component installation.",
        "related_project_slugs": ["bamburi-amani-estate", "drainage-culverts-donholm"],
        "related_service_slugs": ["building-works", "civil-engineering"],
        "is_featured": False,
        "meta_title": "Mobile Cranes",
        "meta_description": "Mobile cranes for building and civil lifting operations by GCCL.",
    },
    {
        "name": "Concrete Batching Plant",
        "slug": "concrete-batching-plant",
        "category": "Heavy Machinery",
        "short_description": "On-site concrete production for building and civil works.",
        "description": (
            "Portable batching plant supporting estate development and structural concrete "
            "production with quality-controlled mix designs."
        ),
        "capacity": "30–60 m³/hour batch output",
        "condition": "Operational",
        "maintenance_status": "Mixer drum and scale calibration verified per project",
        "image": FALLBACK_IMAGES["about"],
        "gallery_images": [FALLBACK_IMAGES["about"], FALLBACK_IMAGES["project"]],
        "gallery_categories": _gallery(("Concrete Production", [FALLBACK_IMAGES["about"]])),
        "specifications": _specs(
            ("Output", "30–60 m³/hour"),
            ("Type", "Portable batching plant"),
            ("Quality Control", "Mix design & slump testing"),
        ),
        "usage": "Estate construction, culvert casting, and structural concrete on building sites.",
        "related_project_slugs": ["bamburi-amani-estate", "oluwa-seun-beach-cottages"],
        "related_service_slugs": ["building-works", "civil-engineering"],
        "is_featured": True,
        "meta_title": "Concrete Batching Plant",
        "meta_description": "Portable concrete batching plant supporting GCCL building projects.",
    },
    {
        "name": "Tipper Trucks",
        "slug": "tipper-trucks",
        "category": "Transport Vehicles",
        "short_description": "Material haulage for earthworks and road construction.",
        "description": (
            "Tipper trucks for hauling aggregates, spoil, and construction materials between "
            "borrow pits, sites, and disposal areas."
        ),
        "capacity": "10–20 Ton payload",
        "condition": "Operational",
        "maintenance_status": "Roadworthiness inspection before long-distance haulage",
        "image": FALLBACK_IMAGES["project"],
        "gallery_images": [FALLBACK_IMAGES["project"]],
        "gallery_categories": _gallery(("Haulage", [FALLBACK_IMAGES["project"]])),
        "specifications": _specs(
            ("Payload", "10–20 Ton"),
            ("Fleet Use", "Aggregate & spoil haulage"),
            ("Configuration", "6×4 tipper"),
        ),
        "usage": "Earthworks haulage, aggregate delivery, and road construction logistics.",
        "related_project_slugs": ["road-construction-donholm", "isiolo-township-roads"],
        "related_service_slugs": ["road-construction", "earth-works"],
        "is_featured": False,
        "meta_title": "Tipper Trucks",
        "meta_description": "Tipper trucks for construction material haulage by GURUH Construction.",
    },
    {
        "name": "Water Tankers",
        "slug": "water-tankers",
        "category": "Transport Vehicles",
        "short_description": "Dust suppression and water support on road and civil sites.",
        "description": (
            "Water bowser tankers for dust suppression, compaction moisture, and general "
            "water support during road and earthworks operations."
        ),
        "capacity": "10,000–20,000 L capacity",
        "condition": "Operational",
        "maintenance_status": "Tank integrity and pump check before site deployment",
        "image": FALLBACK_IMAGES["service"],
        "gallery_images": [FALLBACK_IMAGES["service"]],
        "gallery_categories": _gallery(("Water Support", [FALLBACK_IMAGES["service"]])),
        "specifications": _specs(
            ("Capacity", "10,000–20,000 Litres"),
            ("Application", "Dust suppression & compaction"),
            ("Spray System", "Rear & side spray bars"),
        ),
        "usage": "Road dust control, compaction watering, and arid site moisture support.",
        "related_project_slugs": ["marich-pass-kainuk-road-maintenance", "isiolo-township-roads"],
        "related_service_slugs": ["road-maintenance", "road-construction"],
        "is_featured": True,
        "meta_title": "Water Tankers",
        "meta_description": "Water tankers for dust suppression and site water support by GCCL.",
    },
    {
        "name": "Plate Compactors & Generators",
        "slug": "plate-compactors-generators",
        "category": "Support Equipment",
        "short_description": "Compaction and power support for confined site areas.",
        "description": (
            "Plate compactors and portable generators for trench compaction, paving edges, "
            "and auxiliary power on urban and confined civil works."
        ),
        "capacity": "Heavy-duty plate / 10–30 kVA generators",
        "condition": "Operational",
        "maintenance_status": "Weekly operator check; fuel and exhaust inspection",
        "image": FALLBACK_IMAGES["project"],
        "gallery_images": [FALLBACK_IMAGES["project"]],
        "gallery_categories": _gallery(("Support Plant", [FALLBACK_IMAGES["project"]])),
        "specifications": _specs(
            ("Plate Compactor", "Heavy-duty reversible"),
            ("Generator Range", "10–30 kVA"),
            ("Use Case", "Trenches & confined areas"),
        ),
        "usage": "Trench backfill compaction, footpath works, and temporary site power.",
        "related_project_slugs": ["drainage-culverts-donholm"],
        "related_service_slugs": ["civil-engineering", "drainage-culvert-works"],
        "is_featured": False,
        "meta_title": "Plate Compactors & Generators",
        "meta_description": "Support equipment for compaction and site power by GURUH Construction.",
    },
]

for _eq in EQUIPMENT_CATALOG:
    _eq["category_key"] = CATEGORY_KEY_MAP.get(_eq["category"], "")

EQUIPMENT_BY_SLUG: dict[str, dict] = {e["slug"]: e for e in EQUIPMENT_CATALOG}

# Combined gallery images for listing page gallery section
FLEET_GALLERY_IMAGES: list[str] = list(
    dict.fromkeys(
        img
        for eq in EQUIPMENT_CATALOG
        for img in eq.get("gallery_images", [])
    )
)
