"""
Official CMS content blocks — seed data from the approved company profile.

Organized into 18 reusable blocks for the provider layer and future MySQL import.
Templates consume DTOs only — never import this module directly.
"""

from __future__ import annotations

from typing import Any

from app.constants.media import FALLBACK_IMAGES
from app.data.company_profile import COMPANY_PROFILE

_contact_profile = COMPANY_PROFILE["contact"]
_map_profile = _contact_profile.get("map", {})

# Seed timestamp — updated when content is re-imported from the official profile
SEED_TIMESTAMP = "2026-07-08T00:00:00Z"


def _item(
    item_id: int,
    title: str,
    *,
    item_key: str = "",
    subtitle: str = "",
    short_summary: str = "",
    full_content: str = "",
    image: str = "",
    icon: str = "",
    sort_order: int = 0,
    extra: dict | None = None,
) -> dict[str, Any]:
    return {
        "id": item_id,
        "item_key": item_key or f"item-{item_id}",
        "title": title,
        "subtitle": subtitle,
        "short_summary": short_summary,
        "full_content": full_content,
        "image": image,
        "icon": icon,
        "sort_order": sort_order,
        "is_active": True,
        "extra": extra or {},
        "created_at": SEED_TIMESTAMP,
        "updated_at": SEED_TIMESTAMP,
    }


def _block(
    block_id: int,
    block_key: str,
    title: str,
    *,
    subtitle: str = "",
    short_summary: str = "",
    full_content: str = "",
    hero_image: str = "",
    gallery_images: list[str] | None = None,
    display_order: int = 0,
    meta_title: str = "",
    meta_description: str = "",
    og_image: str = "",
    items: list[dict[str, Any]] | None = None,
    extra: dict | None = None,
) -> dict[str, Any]:
    return {
        "id": block_id,
        "block_key": block_key,
        "title": title,
        "subtitle": subtitle,
        "short_summary": short_summary,
        "full_content": full_content,
        "hero_image": hero_image,
        "gallery_images": gallery_images or [],
        "display_order": display_order,
        "is_active": True,
        "meta_title": meta_title or title,
        "meta_description": meta_description or short_summary,
        "og_image": og_image or hero_image,
        "items": items or [],
        "extra": extra or {},
        "created_at": SEED_TIMESTAMP,
        "updated_at": SEED_TIMESTAMP,
    }


CMS_CONTENT_BLOCKS: list[dict[str, Any]] = [
    # 1 — Company Overview
    _block(
        1,
        "company_overview",
        "Company Overview",
        subtitle="Who We Are",
        short_summary=(
            "Founded in Kenya in 2008; now operating in Somalia with headquarters in Mogadishu."
        ),
        full_content=(
            "GURUH Construction Company Limited (GCCL) was established in Kenya in 2008 and "
            "incorporated in 2013. Originally a Kenyan construction company specialising in "
            "water works, building works, and civil engineering, the company now operates in "
            "Somalia while retaining its historical portfolio of infrastructure projects "
            "delivered across Kenya. GCCL delivers projects with qualified staff and a "
            "commitment to safety, quality, and client partnership."
        ),
        hero_image=FALLBACK_IMAGES["about"],
        display_order=1,
        meta_description=(
            "Overview of GURUH Construction Company Limited — water, building, and "
            "civil engineering contractor in Kenya."
        ),
    ),
    # 2 — Company Introduction
    _block(
        2,
        "company_introduction",
        "Company Introduction",
        subtitle="Established 2008",
        short_summary=(
            "Registered under CPR/2013/97086 with NCA2 road works and NCA6 building works categories."
        ),
        full_content=(
            "GCCL was established in 2008 and undertakes projects in water works, building "
            "works, and civil engineering works with qualified staff. The company is "
            "registered under Certificate of Incorporation No. CPR/2013/97086 and holds "
            "National Construction Authority registration for road works (Category NCA2) "
            "and building works (Category NCA6)."
        ),
        hero_image=FALLBACK_IMAGES["service"],
        display_order=2,
    ),
    # 3 — Directors' Message
    _block(
        3,
        "directors_message",
        "A Message from the Directors",
        subtitle="Khalif Elmi Guruh & Adam Mariam Warsame",
        short_summary=(
            "Our directors welcome you to GCCL and look forward to building lasting "
            "relationships through one-on-one engagement."
        ),
        full_content=(
            "We appreciate you taking the time to review our company profile. This is a "
            "great opportunity for us to communicate our services to you.\n\n"
            "Since our inception, we have developed a trusted and reliable company by building "
            "lasting relationships with our clients, employees, suppliers, and sub-contractors. "
            "With many years of work under our belt, we continue to learn and build from this "
            "experience.\n\n"
            "We thank all those who have contributed to the development of GCCL over the years, "
            "and we thank you for your interest in our company. We look forward to working with you."
        ),
        hero_image=FALLBACK_IMAGES["about"],
        display_order=3,
        items=[
            _item(1, "Khalif Elmi Guruh", subtitle="Director & Co-Founder", sort_order=1),
            _item(2, "Adam Mariam Warsame", subtitle="Director & Co-Founder", sort_order=2),
        ],
    ),
    # 4 — Company History
    _block(
        4,
        "company_history",
        "Company History",
        subtitle="Our Journey Since 2008",
        short_summary=(
            "Established in Kenya in 2008; incorporated 2013; now operating in Somalia."
        ),
        full_content=(
            "GURUH Construction Company Limited was established in 2008 and incorporated in "
            "Kenya on 22 February 2013 under the Companies Act (Certificate of Incorporation "
            "No. CPR/2013/97086). Founding directors Khalif Elmi Guruh and Adam Mariam Warsame "
            "built the company's reputation delivering civil, building, and water infrastructure "
            "works across multiple Kenyan counties including Nairobi, Mombasa, Kilifi, Turkana, "
            "Taita Taveta, Laikipia, Isiolo, and others. Founded in Kenya and officially "
            "incorporated there, GCCL now operates in Somalia with its headquarters in "
            "Mogadishu while maintaining its historical project portfolio from Kenya."
        ),
        hero_image=FALLBACK_IMAGES["hero_alt"],
        display_order=4,
    ),
    # 5 — Vision
    _block(
        5,
        "vision",
        "Our Vision",
        subtitle="Where We Are Headed",
        short_summary="To become a globally reputed broad based construction solutions provider in East Africa.",
        full_content=(
            "To become a globally reputed broad based construction solutions provider "
            "in East Africa."
        ),
        display_order=5,
    ),
    # 6 — Mission
    _block(
        6,
        "mission",
        "Our Mission",
        subtitle="What Drives Us",
        short_summary=(
            "Proficiency and excellence in engineering and construction management."
        ),
        full_content=(
            "To demonstrate proficiency and excellence in Engineering and Construction "
            "Management of projects resulting in satisfaction to Customers, Stake-Holders "
            "And Associates."
        ),
        display_order=6,
    ),
    # 7 — Core Values
    _block(
        7,
        "core_values",
        "Our Core Values",
        subtitle="What We Stand For",
        short_summary="Professionalism, ethics, and reliability guide every project we deliver.",
        full_content=(
            "Our values define how we engage with clients, communities, and stakeholders "
            "on every construction project."
        ),
        display_order=7,
        items=[
            _item(
                1,
                "Professionalism",
                full_content=(
                    "We seek to abide by all principles and requirements that honour our legal "
                    "environment and mandate in the industry in the investments we accept, "
                    "contracts we engage in, and staff we work with."
                ),
                icon="bi-shield-check",
                sort_order=1,
            ),
            _item(
                2,
                "Ethics",
                full_content=(
                    "We care about our environment and the socio-economic situation of the "
                    "people we serve by the principle of humanity first and profit second."
                ),
                icon="bi-heart-pulse",
                sort_order=2,
            ),
            _item(
                3,
                "Reliability",
                full_content=(
                    "We are a company of integrity who seek to develop trust with all our "
                    "stakeholders."
                ),
                icon="bi-handshake",
                sort_order=3,
            ),
        ],
    ),
    # 8 — HSE Policy
    _block(
        8,
        "hse_policy",
        "Health, Safety & Environmental Policy",
        subtitle="Safety First, Always",
        short_summary="Safety of staff overrides all production targets.",
        full_content=(
            "GCCL believes most injuries, occupational illnesses, as well as safety and "
            "environmental incidents are preventable. GCCL will strive to be a leader in the "
            "field of management of Health, Safety and Environment.\n\n"
            "GCCL is committed to the commitments listed below and holds that the safety of "
            "staff overrides all production targets."
        ),
        display_order=8,
        items=[
            _item(
                i + 1,
                commitment.split(".")[0] if "." in commitment else commitment[:60],
                full_content=commitment,
                icon="bi-check-circle-fill",
                sort_order=i + 1,
            )
            for i, commitment in enumerate(
                [
                    "Conduct all its activities in such a manner as to avoid harm to employees, contractors, and the community.",
                    "Improve continuously its environmental practices and performance.",
                    "Comply with all statutory requirements concerning Health, Safety and Environment.",
                    "Train and validate employees on health and safety practices.",
                    "Audit periodically internal and external work procedures and practices.",
                    "Investigate all accidents including minor ones and near misses, followed by implementation of corrective measures.",
                    "Interact with local communities on operations, likely hazards, and emergency response systems.",
                ]
            )
        ],
    ),
    # 9 — Why Choose GURUH
    _block(
        9,
        "why_choose_guruh",
        "Why Choose GURUH Construction",
        subtitle="Built on Trust & Experience",
        short_summary=(
            "Trusted contractor with qualified staff, official registrations, and a "
            "client-first approach."
        ),
        full_content=(
            "Since inception, GURUH Construction has developed a trusted and reliable "
            "reputation by building lasting relationships with clients, employees, suppliers, "
            "and sub-contractors. The company combines engineering proficiency with practical "
            "site experience across road construction, drainage and culvert works, dam and "
            "water-pan development, and residential estate construction."
        ),
        hero_image=FALLBACK_IMAGES["about"],
        display_order=9,
    ),
    # 10 — Company Strengths
    _block(
        10,
        "company_strengths",
        "Company Strengths",
        subtitle="Our Competitive Advantages",
        short_summary="Registered, experienced, and committed to safety and client partnership.",
        full_content="Key strengths that define GCCL's delivery capability across Kenya.",
        display_order=10,
        items=[
            _item(i + 1, strength, full_content=strength, icon="bi-star-fill", sort_order=i + 1)
            for i, strength in enumerate(
                [
                    "Trusted and reliable delivery built on long-term client and partner relationships.",
                    "Qualified staff with experience across water, building, and civil engineering works.",
                    "Registered NCA2 Road Works and NCA6 Building Works contractor.",
                    "Licensed Qualified Water Resource Contractor for supply, sewerage, dams, and boreholes.",
                    "Strong Health, Safety and Environment commitment with staff-first safety culture.",
                    "Proven portfolio across counties in road works, drainage, dams, and housing estates.",
                    "Direct director engagement and one-on-one client interaction.",
                ]
            )
        ],
    ),
    # 11 — Certifications
    _block(
        11,
        "certifications_registrations",
        "Certifications & Registrations",
        subtitle="Official Credentials",
        short_summary=(
            "Fully registered with NCA, Ministry of Water, and Kenyan company registry."
        ),
        full_content=(
            "GURUH Construction Company Limited holds the following official registrations "
            "and certifications required for civil, building, and water works in Kenya."
        ),
        display_order=11,
        items=[
            _item(
                1,
                "Certificate of Incorporation",
                subtitle="Republic of Kenya",
                short_summary="CPR/2013/97086",
                full_content="Incorporated 22 February 2013.",
                icon="bi-file-earmark-check",
                sort_order=1,
                extra={"reference": "CPR/2013/97086", "category": "Company Registration"},
            ),
            _item(
                2,
                "NCA Road Works Contractor — Category NCA2",
                subtitle="National Construction Authority",
                short_summary="Reg. No. 32627/R/0817",
                full_content="Certificate and annual practising license issued July 2024.",
                icon="bi-signpost-split",
                sort_order=2,
                extra={"reference": "32627/R/0817", "valid_until": "2025-07-31", "category": "Road Works"},
            ),
            _item(
                3,
                "NCA Building Works Contractor — Category NCA6",
                subtitle="National Construction Authority",
                short_summary="Reg. No. 32627/B/0817",
                full_content="Certificate and annual practising license issued July 2024.",
                icon="bi-building",
                sort_order=3,
                extra={"reference": "32627/B/0817", "valid_until": "2025-07-31", "category": "Building Works"},
            ),
            _item(
                4,
                "Qualified Water Resource Contractor Licence",
                subtitle="Ministry of Water, Sanitation and Irrigation",
                short_summary="WD/WC/2669 / MTAC-1893/20",
                full_content=(
                    "Class C — Water supply, sewerage, irrigation & electromechanical (up to "
                    "Kshs. 250M); Class D — Dams 5m high (up to Kshs. 50M); Class C — Borehole "
                    "drilling/equipping (up to Kshs. 5M). Issued October 2020."
                ),
                icon="bi-droplet-fill",
                sort_order=4,
                extra={"reference": "WD/WC/2669 / MTAC-1893/20", "category": "Water Works"},
            ),
            _item(
                5,
                "KRA PIN Registration",
                subtitle="Kenya Revenue Authority",
                short_summary="P051415096L",
                icon="bi-receipt",
                sort_order=5,
                extra={"reference": "P051415096L", "category": "Tax Registration"},
            ),
        ],
    ),
    # 12 — Equipment Overview
    _block(
        12,
        "equipment_overview",
        "Equipment Overview",
        subtitle="Plant & Machinery",
        short_summary=(
            "Heavy plant deployed for civil, road, and water works across project sites."
        ),
        full_content=(
            "GCCL deploys heavy plant and equipment for civil, road, and water works including "
            "bulldozers, motor graders, excavators, road rollers, asphalt pavers, water tankers, "
            "and concrete production support equipment on project sites."
        ),
        hero_image=FALLBACK_IMAGES["project"],
        display_order=12,
        items=[
            _item(
                i + 1,
                eq["name"],
                subtitle=eq["category"],
                full_content=eq["description"],
                icon="bi-gear-wide-connected",
                sort_order=i + 1,
                extra={"category": eq["category"]},
            )
            for i, eq in enumerate(
                [
                    {"name": "Bulldozers", "category": "Earthmoving", "description": "Used for dam, water pan, and road earthworks (including SD22-class units)."},
                    {"name": "Motor Graders", "category": "Road Works", "description": "Road formation, grading, and maintenance on civil projects."},
                    {"name": "Road Rollers / Compactors", "category": "Road Works", "description": "Asphalt and earth compaction for road construction and surfacing."},
                    {"name": "Asphalt Pavers", "category": "Road Works", "description": "Bitumen road paving and surfacing operations."},
                    {"name": "Excavators & Loaders", "category": "Earthmoving", "description": "Excavation, material handling, and site preparation."},
                    {"name": "Water Tankers", "category": "Support Equipment", "description": "Dust suppression and water support on road and civil sites."},
                ]
            )
        ],
    ),
    # 13 — Company Experience
    _block(
        13,
        "company_experience",
        "Company Experience",
        subtitle="Proven Track Record",
        short_summary=(
            "Historical delivery across Kenya; current operations based in Somalia."
        ),
        full_content=(
            "Since 2008, GURUH Construction Company Limited has delivered civil, building, "
            "and water infrastructure projects across Kenya. The company's historical portfolio "
            "includes road construction and maintenance, drainage and culvert works, dam and "
            "water-pan construction, interlocking paving, and residential estate development in "
            "Nairobi, Mombasa, Kilifi, Turkana, Taita Taveta, Laikipia, Isiolo, and other "
            "regions. GCCL now operates in Somalia, delivering current and future projects from "
            "its headquarters in Mogadishu."
        ),
        hero_image=FALLBACK_IMAGES["project"],
        display_order=13,
    ),
    # 14 — Areas of Operation
    _block(
        14,
        "areas_of_operation",
        "Areas of Operation",
        subtitle="Kenya Historical Portfolio · Somalia Current Operations",
        short_summary="Historical project delivery in Kenya; current operations in Somalia.",
        full_content=(
            "GCCL's historical project portfolio spans multiple counties in Kenya. The company "
            "now operates in Somalia with headquarters in Mogadishu. Additional branch offices "
            "can be added through the CMS without changing the website architecture."
        ),
        display_order=14,
        items=[
            _item(i + 1, county, icon="bi-geo-alt-fill", sort_order=i + 1)
            for i, county in enumerate(
                [
                    "Nairobi",
                    "Mombasa",
                    "Kilifi",
                    "Turkana",
                    "Taita Taveta",
                    "Laikipia",
                    "Isiolo",
                    "West Pokot",
                ]
            )
        ],
    ),
    # 15 — Company Statistics
    _block(
        15,
        "company_statistics",
        "Company Statistics",
        subtitle="By the Numbers",
        short_summary="Key metrics that reflect GCCL's experience and capability.",
        full_content="Official company metrics derived from the approved company profile.",
        display_order=15,
        items=[
            _item(
                i + 1,
                stat["label"],
                subtitle=f"{stat['value']}{stat.get('suffix', '')}",
                short_summary=stat["label"],
                icon=stat.get("icon", "bi-bar-chart"),
                sort_order=i + 1,
                extra={"value": stat["value"], "suffix": stat.get("suffix", "")},
            )
            for i, stat in enumerate(
                [
                    {"label": "Years of Experience", "value": "15", "suffix": "+", "icon": "bi-calendar-check"},
                    {"label": "Core Service Areas", "value": "3", "suffix": "", "icon": "bi-grid-fill"},
                    {"label": "Major Projects", "value": "9", "suffix": "+", "icon": "bi-building-check"},
                    {"label": "Counties Served", "value": "8", "suffix": "+", "icon": "bi-geo-alt-fill"},
                ]
            )
        ],
    ),
    # 16 — Leadership Team
    _block(
        16,
        "leadership_team",
        "Leadership Team",
        subtitle="Board of Directors",
        short_summary="Led by founding directors with deep construction industry experience.",
        full_content=(
            "GURUH Construction Company Limited is led by its founding directors who oversee "
            "strategy, operations, and client relationships across all project portfolios."
        ),
        display_order=16,
        items=[
            _item(
                1,
                "Khalif Elmi Guruh",
                subtitle="Director & Co-Founder",
                full_content=(
                    "Co-founder of GURUH Construction Company Limited. Leads company "
                    "strategy, client relationships, and delivery of civil, building, and "
                    "water infrastructure projects across Kenya."
                ),
                icon="bi-person-badge",
                sort_order=1,
            ),
            _item(
                2,
                "Adam Mariam Warsame",
                subtitle="Director & Co-Founder",
                full_content=(
                    "Co-founder of GURUH Construction Company Limited. Supports project "
                    "delivery, contractor operations, and stakeholder engagement across the "
                    "company's construction portfolio."
                ),
                icon="bi-person-badge",
                sort_order=2,
            ),
        ],
    ),
    # 17 — Partners
    _block(
        17,
        "partners",
        "Partners",
        subtitle="Trusted Collaborations",
        short_summary=(
            "GCCL builds lasting relationships with clients, suppliers, and sub-contractors."
        ),
        full_content=(
            "Our staff are the key to our success. GURUH Construction collaborates with "
            "clients, suppliers, sub-contractors, and industry partners to deliver projects "
            "safely, on specification, and to the highest standards. Partner logos and "
            "references are managed through the admin dashboard."
        ),
        display_order=17,
        items=[],
    ),
    # 18 — Call To Action
    _block(
        18,
        "call_to_action",
        "Ready to Start Your Project?",
        subtitle="Speak with our team about your next construction project.",
        short_summary="Contact GCCL for a consultation or project estimate.",
        full_content=(
            "Whether you need road works, building construction, or water infrastructure, "
            "our team is ready to discuss your requirements and provide professional guidance."
        ),
        hero_image=FALLBACK_IMAGES["hero"],
        display_order=18,
        items=[
            _item(
                1,
                "Request a Quote",
                subtitle="Primary action",
                icon="bi-chat-quote",
                sort_order=1,
                extra={"button_url": "/request-quote", "button_style": "accent"},
            ),
            _item(
                2,
                "Contact Us",
                subtitle="Secondary action",
                icon="bi-envelope",
                sort_order=2,
                extra={"button_url": "/contact", "button_style": "outline"},
            ),
        ],
    ),
    # 19 — Company Contact Information (admin-manageable site-wide contact)
    _block(
        19,
        "company_contact_info",
        "Company Contact Information",
        subtitle=_contact_profile.get("head_office_label", "Head Office"),
        short_summary=(
            f"Official contact details for {_contact_profile['company_name']} — "
            f"{_contact_profile['address']}."
        ),
        full_content=(
            f"Reach {_contact_profile['company_name']} at {_contact_profile['email']} or "
            f"{_contact_profile['phone_primary']}. Office hours: "
            f"{_contact_profile['office_hours']}."
        ),
        display_order=19,
        extra={
            "company_name": _contact_profile["company_name"],
            "head_office_label": _contact_profile.get("head_office_label", "Head Office"),
            "address": _contact_profile["address"],
            "postal_address": _contact_profile.get("postal_address", ""),
            "address_area": _contact_profile.get("address_area", ""),
            "address_district": _contact_profile.get("address_district", ""),
            "address_locality": _contact_profile.get("address_locality", ""),
            "address_country": _contact_profile.get("address_country", ""),
            "address_country_code": _contact_profile.get("address_country_code", ""),
            "email": _contact_profile["email"],
            "phone_primary": _contact_profile["phone_primary"],
            "phone_secondary": _contact_profile.get("phone_secondary", ""),
            "office_hours": _contact_profile["office_hours"],
            "map_label": _map_profile.get("label", _contact_profile["address"]),
            "map_latitude": _map_profile.get("latitude"),
            "map_longitude": _map_profile.get("longitude"),
            "map_zoom": _map_profile.get("zoom", 16),
            "map_embed_url": _map_profile.get("embed_url", ""),
            "map_provider": _map_profile.get("map_provider", "google-maps"),
            "map_ready": _map_profile.get("map_ready", False),
        },
    ),
]

from app.data.services_page import SERVICES_PAGE_BLOCKS
from app.data.projects_page import PROJECTS_PAGE_BLOCKS, PROJECT_DETAIL_BLOCKS
from app.data.equipment_page import EQUIPMENT_PAGE_BLOCKS, EQUIPMENT_DETAIL_BLOCKS
from app.data.team_page import TEAM_PAGE_BLOCKS
from app.data.contact_page import CONTACT_PAGE_BLOCKS
from app.data.quote_page import QUOTE_PAGE_BLOCKS
from app.data.careers_page import CAREERS_PAGE_BLOCKS, CAREER_DETAIL_BLOCKS
from app.data.gallery_page import GALLERY_PAGE_BLOCKS

CMS_CONTENT_BLOCKS.extend(SERVICES_PAGE_BLOCKS)
CMS_CONTENT_BLOCKS.extend(PROJECTS_PAGE_BLOCKS)
CMS_CONTENT_BLOCKS.extend(PROJECT_DETAIL_BLOCKS)
CMS_CONTENT_BLOCKS.extend(EQUIPMENT_PAGE_BLOCKS)
CMS_CONTENT_BLOCKS.extend(EQUIPMENT_DETAIL_BLOCKS)
CMS_CONTENT_BLOCKS.extend(TEAM_PAGE_BLOCKS)
CMS_CONTENT_BLOCKS.extend(CONTACT_PAGE_BLOCKS)
CMS_CONTENT_BLOCKS.extend(QUOTE_PAGE_BLOCKS)
CMS_CONTENT_BLOCKS.extend(CAREERS_PAGE_BLOCKS)
CMS_CONTENT_BLOCKS.extend(CAREER_DETAIL_BLOCKS)
CMS_CONTENT_BLOCKS.extend(GALLERY_PAGE_BLOCKS)

CMS_BLOCKS_BY_KEY: dict[str, dict[str, Any]] = {b["block_key"]: b for b in CMS_CONTENT_BLOCKS}
