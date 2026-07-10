"""
Official GURUH Construction Company Limited profile content.

Extracted from the company profile PDF (website-relevant sections only).
This module is the single source of truth until MySQL + Admin Dashboard are connected.

Source sections used:
  - Cover & contact details
  - Directors' message
  - Vision, Mission & Core Values
  - Health, Safety & Environmental Policy
  - Company introduction
  - Civil, water & building project summaries
  - NCA & water contractor registrations

Ignored: bank statements, audited accounts, legal copies, memorandum, staff CVs,
financial documents, and repetitive photo galleries.
"""

from __future__ import annotations

from typing import Any

COMPANY_PROFILE: dict[str, Any] = {
    "source_document": "GURUH Construction Company Limited — Official Company Profile",
    "last_extracted": "2026-07-08",
    "company_overview": (
        "GURUH Construction Company Limited (GCCL) was established in Kenya in 2008 and "
        "incorporated in 2013. Originally a Kenyan construction company specialising in "
        "water works, building works, and civil engineering, the company now operates in "
        "Somalia while retaining its historical portfolio of infrastructure projects "
        "delivered across Kenya. GCCL delivers projects with qualified staff and a "
        "commitment to safety, quality, and client partnership."
    ),
    "company_introduction": (
        "GCCL was established in 2008 and undertakes projects in water works, building "
        "works, and civil engineering works with qualified staff. The company is "
        "registered under Certificate of Incorporation No. CPR/2013/97086 and holds "
        "National Construction Authority registration for road works (Category NCA2) "
        "and building works (Category NCA6)."
    ),
    "about_the_company": (
        "Since inception, GURUH Construction has developed a trusted and reliable "
        "reputation by building lasting relationships with clients, employees, suppliers, "
        "and sub-contractors. The company combines engineering proficiency with practical "
        "site experience across road construction, drainage and culvert works, dam and "
        "water-pan development, and residential estate construction."
    ),
    "company_history": (
        "GURUH Construction Company Limited was established in 2008 and incorporated in "
        "Kenya on 22 February 2013 under the Companies Act (Certificate of Incorporation "
        "No. CPR/2013/97086). Founding directors Khalif Elmi Guruh and Adam Mariam Warsame "
        "built the company's reputation delivering civil, building, and water infrastructure "
        "works across multiple Kenyan counties including Nairobi, Mombasa, Kilifi, Turkana, "
        "Taita Taveta, Laikipia, Isiolo, and others. Founded in Kenya and officially "
        "incorporated there, GCCL now operates in Somalia with its headquarters in "
        "Mogadishu while maintaining its historical project portfolio from Kenya."
    ),
    "directors_message": {
        "heading": "A Message from the Directors",
        "signatories": ["Khalif Elmi Guruh", "Adam Mariam Warsame"],
        "summary": (
            "The directors thank stakeholders for reviewing the company profile and "
            "welcome the opportunity to introduce GCCL's services. Since inception, the "
            "company has built lasting relationships with clients, employees, suppliers, "
            "and sub-contractors through one-on-one engagement. With many years of "
            "industry experience, GCCL continues to learn, improve, and deliver reliable "
            "construction solutions."
        ),
    },
    "directors": [
        {
            "name": "Khalif Elmi Guruh",
            "role": "Director & Co-Founder",
            "bio": (
                "Co-founder of GURUH Construction Company Limited. Leads company "
                "strategy, client relationships, and delivery of civil, building, and "
                "water infrastructure projects across Kenya."
            ),
        },
        {
            "name": "Adam Mariam Warsame",
            "role": "Director & Co-Founder",
            "bio": (
                "Co-founder of GURUH Construction Company Limited. Supports project "
                "delivery, contractor operations, and stakeholder engagement across the "
                "company's construction portfolio."
            ),
        },
    ],
    "vision": (
        "To become a globally reputed broad based construction solutions provider "
        "in East Africa."
    ),
    "mission": (
        "To demonstrate proficiency and excellence in Engineering and Construction "
        "Management of projects resulting in satisfaction to Customers, Stake-Holders "
        "And Associates."
    ),
    "core_values": [
        {
            "title": "Professionalism",
            "description": (
                "We abide by the principles and requirements that honour our legal "
                "environment and industry mandate in the investments we accept, "
                "contracts we engage in, and staff we work with."
            ),
        },
        {
            "title": "Ethics",
            "description": (
                "We care about our environment and the socio-economic situation of "
                "the people we serve — humanity first, profit second."
            ),
        },
        {
            "title": "Reliability",
            "description": (
                "We are a company of integrity who seek to develop trust with all our "
                "stakeholders."
            ),
        },
    ],
    "hse_policy": {
        "principle": "Safety of staff overrides all the production targets.",
        "summary": (
            "GCCL believes most injuries, occupational illnesses, and safety and "
            "environmental incidents are preventable. The company strives to be a leader "
            "in Health, Safety and Environment management."
        ),
        "commitments": [
            "Conduct all activities to avoid harm to employees, contractors, and the community.",
            "Continuously improve environmental practices and performance.",
            "Comply with all statutory Health, Safety and Environment requirements.",
            "Train and validate employees on health and safety practices.",
            "Periodically audit internal and external work procedures and practices.",
            "Investigate all accidents and near misses, implementing corrective measures.",
            "Engage local communities on operations, hazards, and emergency response.",
        ],
    },
    "company_strengths": [
        "Trusted and reliable delivery built on long-term client and partner relationships.",
        "Qualified staff with experience across water, building, and civil engineering works.",
        "Registered NCA2 Road Works and NCA6 Building Works contractor.",
        "Licensed Qualified Water Resource Contractor for supply, sewerage, dams, and boreholes.",
        "Strong Health, Safety and Environment commitment with staff-first safety culture.",
        "Proven portfolio across counties in road works, drainage, dams, and housing estates.",
        "Direct director engagement and one-on-one client interaction.",
    ],
    "services_offered": [
        {
            "title": "Water Works",
            "slug": "water-works",
            "short_description": "Water supply, dams, boreholes, and irrigation infrastructure.",
            "description": (
                "Design and construction of water pans, earth dams, water supply systems, "
                "borehole drilling and equipping, sewerage, irrigation, and "
                "electromechanical works."
            ),
            "icon": "bi-droplet-fill",
            "is_featured": True,
        },
        {
            "title": "Building Works",
            "slug": "building-works",
            "short_description": "Residential and commercial building construction.",
            "description": (
                "Construction of residential estates, cottages, and commercial buildings "
                "including builders work, electrical, mechanical, and associated civil works."
            ),
            "icon": "bi-building",
            "is_featured": True,
        },
        {
            "title": "Civil Engineering Works",
            "slug": "civil-engineering-works",
            "short_description": "Roads, drainage, culverts, and infrastructure maintenance.",
            "description": (
                "Road construction and upgrading, pipe and box culverts, drainage and soil "
                "erosion protection, routine road maintenance, and paving works."
            ),
            "icon": "bi-signpost-split-fill",
            "is_featured": True,
        },
        {
            "title": "Dam & Earthworks",
            "slug": "dam-earthworks",
            "short_description": "Earth dams, water pans, and associated civil works.",
            "description": (
                "Construction of earth dams and water pans including excavation, embankment "
                "works, and associated access infrastructure."
            ),
            "icon": "bi-layers-fill",
            "is_featured": False,
        },
        {
            "title": "Drainage & Culvert Works",
            "slug": "drainage-culvert-works",
            "short_description": "Pipe culverts, box culverts, and erosion protection.",
            "description": (
                "Construction of standard pipe culverts, box culverts, and improvement of "
                "drainage and soil erosion protection works."
            ),
            "icon": "bi-water",
            "is_featured": False,
        },
        {
            "title": "Road Construction & Maintenance",
            "slug": "road-construction-maintenance",
            "short_description": "Road building, bitumen standards, and emergency maintenance.",
            "description": (
                "Road construction, upgrading to bitumen standards, performance-based routine "
                "maintenance, and emergency road maintenance contracts."
            ),
            "icon": "bi-truck-front-fill",
            "is_featured": True,
        },
    ],
    "major_projects": [
        {
            "title": "Drainage & Culvert Works — Donholm",
            "slug": "drainage-culverts-donholm",
            "description": (
                "Construction of standard pipe culverts, box culverts, and improvement "
                "of drainage and soil erosion protection works in Donholm."
            ),
            "location": "Donholm, Nairobi",
            "client": "",
            "category": "Civil Engineering",
            "completion_date": "",
            "is_featured": True,
        },
        {
            "title": "Road Construction — Donholm",
            "slug": "road-construction-donholm",
            "description": "Road construction works at Donholm including grading and surfacing.",
            "location": "Donholm, Nairobi",
            "client": "",
            "category": "Road Works",
            "completion_date": "",
            "is_featured": True,
        },
        {
            "title": "Isiolo Township Roads Upgrade & Maintenance",
            "slug": "isiolo-township-roads",
            "description": (
                "Upgrading to bitumen standards and performance of routine maintenance "
                "of Isiolo township roads."
            ),
            "location": "Isiolo County",
            "client": "",
            "category": "Road Works",
            "completion_date": "",
            "is_featured": True,
        },
        {
            "title": "JN B4 (Marich Pass) – Kainuk (A1) Emergency Maintenance",
            "slug": "marich-pass-kainuk-road-maintenance",
            "description": (
                "Performance-based contract for emergency maintenance of JN B4 "
                "(Marich Pass) – Kainuk (KWS gate) (A1) Road."
            ),
            "location": "West Pokot / Turkana",
            "client": "",
            "category": "Road Works",
            "completion_date": "",
            "is_featured": True,
        },
        {
            "title": "Water Pan — Turkana County",
            "slug": "water-pan-turkana",
            "description": "Construction of a water pan including earthworks and reservoir development.",
            "location": "Turkana County",
            "client": "",
            "category": "Water Works",
            "completion_date": "",
            "is_featured": False,
        },
        {
            "title": "Mzwanenyi Earth Dam",
            "slug": "mzwanenyi-earth-dam",
            "description": "Construction of Mzwanenyi earth dam including major earthmoving works.",
            "location": "Taita Taveta County",
            "client": "",
            "category": "Water Works",
            "completion_date": "",
            "is_featured": False,
        },
        {
            "title": "Bamburi Amani Estate",
            "slug": "bamburi-amani-estate",
            "description": (
                "Construction of nineteen (19) three-bedroom houses in Bamburi, Mombasa, "
                "including builders, electrical, mechanical, and associated civil works."
            ),
            "location": "Bamburi, Mombasa",
            "client": "",
            "category": "Building Works",
            "completion_date": "",
            "is_featured": True,
        },
        {
            "title": "Oluwa Seun Beach Cottages",
            "slug": "oluwa-seun-beach-cottages",
            "description": (
                "Construction of 1 No. two-bedroom cottage, 1 No. three-bedroom cottage, "
                "3 No. studio cottages, and a swimming pool at Kanamai, Kilifi County."
            ),
            "location": "Kanamai, Kilifi County",
            "client": "",
            "category": "Building Works",
            "completion_date": "",
            "is_featured": True,
        },
        {
            "title": "Kamukunji Dam",
            "slug": "kamukunji-dam",
            "description": (
                "Construction of Kamukunji Dam at Shamanei, Nyahururu, Laikipia County."
            ),
            "location": "Shamanei, Nyahururu, Laikipia County",
            "client": "",
            "category": "Water Works",
            "completion_date": "",
            "is_featured": True,
        },
    ],
    "company_experience": (
        "Since 2008, GURUH Construction Company Limited has delivered civil, building, "
        "and water infrastructure projects across Kenya. The company's historical portfolio "
        "includes road construction and maintenance, drainage and culvert works, dam and "
        "water-pan construction, interlocking paving, and residential estate development in "
        "Nairobi, Mombasa, Kilifi, Turkana, Taita Taveta, Laikipia, Isiolo, and other "
        "regions. GCCL now operates in Somalia, delivering current and future projects from "
        "its headquarters in Mogadishu."
    ),
    "equipment_overview": (
        "GCCL deploys heavy plant and equipment for civil, road, and water works including "
        "bulldozers, motor graders, excavators, road rollers, asphalt pavers, water tankers, "
        "and concrete production support equipment on project sites."
    ),
    "equipment": [
        {
            "name": "Bulldozers",
            "category": "Earthmoving",
            "description": "Used for dam, water pan, and road earthworks (including SD22-class units).",
        },
        {
            "name": "Motor Graders",
            "category": "Road Works",
            "description": "Road formation, grading, and maintenance on civil projects.",
        },
        {
            "name": "Road Rollers / Compactors",
            "category": "Road Works",
            "description": "Asphalt and earth compaction for road construction and surfacing.",
        },
        {
            "name": "Asphalt Pavers",
            "category": "Road Works",
            "description": "Bitumen road paving and surfacing operations.",
        },
        {
            "name": "Excavators & Loaders",
            "category": "Earthmoving",
            "description": "Excavation, material handling, and site preparation.",
        },
        {
            "name": "Water Tankers",
            "category": "Support Equipment",
            "description": "Dust suppression and water support on road and civil sites.",
        },
    ],
    "certifications": [
        {
            "title": "Certificate of Incorporation",
            "issuer": "Republic of Kenya",
            "reference": "CPR/2013/97086",
            "category": "Company Registration",
            "valid_until": "",
            "notes": "Incorporated 22 February 2013.",
        },
        {
            "title": "NCA Road Works Contractor — Category NCA2",
            "issuer": "National Construction Authority",
            "reference": "32627/R/0817",
            "category": "Road Works",
            "valid_until": "2025-07-31",
            "notes": "Certificate and annual practising license issued July 2024.",
        },
        {
            "title": "NCA Building Works Contractor — Category NCA6",
            "issuer": "National Construction Authority",
            "reference": "32627/B/0817",
            "category": "Building Works",
            "valid_until": "2025-07-31",
            "notes": "Certificate and annual practising license issued July 2024.",
        },
        {
            "title": "Qualified Water Resource Contractor Licence",
            "issuer": "Ministry of Water, Sanitation and Irrigation",
            "reference": "WD/WC/2669 / MTAC-1893/20",
            "category": "Water Works",
            "valid_until": "",
            "notes": (
                "Class C — Water supply, sewerage, irrigation & electromechanical (up to "
                "Kshs. 250M); Class D — Dams 5m high (up to Kshs. 50M); Class C — Borehole "
                "drilling/equipping (up to Kshs. 5M). Issued October 2020."
            ),
        },
        {
            "title": "KRA PIN Registration",
            "issuer": "Kenya Revenue Authority",
            "reference": "P051415096L",
            "category": "Tax Registration",
            "valid_until": "",
            "notes": "",
        },
    ],
    "geography": {
        "founded_country": "Kenya",
        "founded_country_code": "KE",
        "operating_country": "Somalia",
        "operating_country_code": "SO",
    },
    "headquarters": {
        "label": "Head Office",
        "summary": "Mogadishu, Taleh, Hodan District, Somalia",
        "locality": "Mogadishu",
        "district": "Hodan District",
        "area": "Taleh",
        "country": "Somalia",
        "country_code": "SO",
    },
    "offices": [
        {
            "id": 1,
            "slug": "mogadishu-head-office",
            "name": "Head Office — Mogadishu",
            "office_label": "Head Office",
            "is_headquarters": True,
            "show_on_contact_page": True,
            "address": "Mogadishu, Taleh, Hodan District, Somalia",
            "postal_address": "",
            "address_area": "Taleh",
            "address_district": "Hodan District",
            "address_locality": "Mogadishu",
            "country": "Somalia",
            "country_code": "SO",
            "email": "guruhconstructionsomalia@gmail.com",
            "phone_primary": "+252 618 409 343",
            "phone_secondary": "",
            "office_hours": "Mon – Sat: 8:00 AM – 6:00 PM",
            "sort_order": 1,
            "is_active": True,
            "map": {
                "label": "Mogadishu, Taleh, Hodan, Somalia",
                "latitude": 2.0469,
                "longitude": 45.3182,
                "zoom": 16,
            },
        },
    ],
    "contact": {
        "company_name": "GURUH Construction Company Limited",
        "short_name": "GURUH Construction",
        "tagline": "Building Excellence Across East Africa",
        "head_office_label": "Head Office",
        "address": "Mogadishu, Taleh, Hodan District, Somalia",
        "postal_address": "",
        "address_area": "Taleh",
        "address_district": "Hodan District",
        "address_locality": "Mogadishu",
        "address_country": "Somalia",
        "address_country_code": "SO",
        "email": "guruhconstructionsomalia@gmail.com",
        "phone_primary": "+252 618 409 343",
        "phone_secondary": "",
        "office_hours": "Mon – Sat: 8:00 AM – 6:00 PM",
        "map": {
            "label": "Mogadishu, Taleh, Hodan, Somalia",
            "latitude": 2.0469,
            "longitude": 45.3182,
            "zoom": 16,
            "embed_url": "",
            "map_provider": "google-maps",
            "map_ready": False,
        },
    },
    "statistics": [
        {"label": "Years of Experience", "value": "15", "suffix": "+", "icon": "bi-calendar-check"},
        {"label": "Core Service Areas", "value": "3", "suffix": "", "icon": "bi-grid-fill"},
        {"label": "Major Project Types", "value": "9", "suffix": "+", "icon": "bi-building-check"},
        {"label": "Historical Counties (Kenya)", "value": "8", "suffix": "+", "icon": "bi-geo-alt-fill"},
        {"label": "Current Operating Country", "value": "Somalia", "suffix": "", "icon": "bi-globe2"},
    ],
}
