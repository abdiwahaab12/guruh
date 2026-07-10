"""
Careers Page and job detail pages — CMS blocks and Page Builder sections.

Built from app.data.careers_catalog.
"""

from __future__ import annotations

from typing import Any

from app.data.careers_catalog import (
    CAREERS_FAQ,
    CAREERS_PAGE_CONTENT,
    EMPLOYEE_BENEFITS,
    JOB_APPLICATION_FORM_FIELDS,
    JOBS_CATALOG,
    LIFE_AT_GURUH_GALLERY,
    RECRUITMENT_STEPS,
    WHY_JOIN_US_ITEMS,
)
from app.data.cms_blocks import SEED_TIMESTAMP

_BLOCK_ID_START = 1400
_SECTION_ID_START = 1400
_DETAIL_BLOCK_ID_START = 1600
_DETAIL_SECTION_ID_START = 1600


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
        "og_image": hero_image,
        "items": items or [],
        "extra": extra or {},
        "created_at": SEED_TIMESTAMP,
        "updated_at": SEED_TIMESTAMP,
    }


def _section(
    page_slug: str,
    section_id: int,
    section_key: str,
    section_title: str,
    *,
    block_key: str = "",
    display_order: int = 0,
    layout_type: str = "default",
    background_style: str = "default",
    spacing: str = "default",
    animation: str = "none",
    seo_anchor: str = "",
) -> dict[str, Any]:
    anchor = seo_anchor or section_key.replace("_", "-")
    return {
        "id": section_id,
        "page_slug": page_slug,
        "section_key": section_key,
        "section_title": section_title,
        "block_key": block_key,
        "display_order": display_order,
        "layout_type": layout_type,
        "background_style": background_style,
        "spacing": spacing,
        "animation": animation,
        "is_visible": True,
        "seo_anchor": anchor,
        "is_active": True,
        "extra": {},
        "created_at": SEED_TIMESTAMP,
        "updated_at": SEED_TIMESTAMP,
    }


def build_careers_page_blocks() -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    bid = _BLOCK_ID_START
    content = CAREERS_PAGE_CONTENT

    intro = content["introduction"]
    blocks.append(
        _block(
            bid,
            "careers_introduction",
            intro["title"],
            subtitle=intro["subtitle"],
            short_summary=intro["short_summary"],
            full_content=intro["full_content"],
            hero_image=intro["hero_image"],
            display_order=bid,
        )
    )
    bid += 1

    why = content["why_join_us"]
    why_items = [
        _item(i + 1, val["title"], short_summary=val["summary"], icon=val["icon"], sort_order=i + 1)
        for i, val in enumerate(WHY_JOIN_US_ITEMS)
    ]
    blocks.append(
        _block(
            bid,
            "careers_why_join",
            why["title"],
            subtitle=why["subtitle"],
            short_summary=why["short_summary"],
            display_order=bid,
            items=why_items,
        )
    )
    bid += 1

    openings = content["job_openings"]
    job_items = [
        _item(
            i + 1,
            job["title"],
            item_key=job["slug"],
            subtitle=job["department"],
            short_summary=job["short_description"],
            full_content=job["description"],
            image=job.get("image", ""),
            sort_order=job.get("sort_order", i + 1),
            extra={
                "job_slug": job["slug"],
                "department": job["department"],
                "location": job["location"],
                "employment_type": job["employment_type"],
                "experience_required": job.get("experience_required", ""),
                "deadline": job.get("deadline", ""),
            },
        )
        for i, job in enumerate(JOBS_CATALOG)
    ]
    blocks.append(
        _block(
            bid,
            "careers_job_openings",
            openings["title"],
            subtitle=openings["subtitle"],
            short_summary=openings["short_summary"],
            display_order=bid,
            items=job_items,
        )
    )
    bid += 1

    process = content["recruitment_process"]
    process_items = [
        _item(
            i + 1,
            step["title"],
            short_summary=step["summary"],
            icon=step["icon"],
            sort_order=i + 1,
            extra={"step_number": i + 1},
        )
        for i, step in enumerate(RECRUITMENT_STEPS)
    ]
    blocks.append(
        _block(
            bid,
            "careers_recruitment",
            process["title"],
            subtitle=process["subtitle"],
            short_summary=process["short_summary"],
            display_order=bid,
            items=process_items,
        )
    )
    bid += 1

    benefits_meta = content["employee_benefits"]
    benefit_items = [
        _item(i + 1, b["title"], short_summary=b["summary"], icon=b["icon"], sort_order=i + 1)
        for i, b in enumerate(EMPLOYEE_BENEFITS)
    ]
    blocks.append(
        _block(
            bid,
            "careers_benefits",
            benefits_meta["title"],
            subtitle=benefits_meta["subtitle"],
            short_summary=benefits_meta["short_summary"],
            display_order=bid,
            items=benefit_items,
        )
    )
    bid += 1

    life = content["life_at_guruh"]
    gallery_images = [g["image"] for g in LIFE_AT_GURUH_GALLERY]
    life_items = [
        _item(
            i + 1,
            g["title"],
            subtitle=g.get("category", ""),
            image=g["image"],
            sort_order=i + 1,
            extra={"gallery_category": g.get("category", "")},
        )
        for i, g in enumerate(LIFE_AT_GURUH_GALLERY)
    ]
    blocks.append(
        _block(
            bid,
            "careers_life_gallery",
            life["title"],
            subtitle=life["subtitle"],
            short_summary=life["short_summary"],
            gallery_images=gallery_images,
            display_order=bid,
            items=life_items,
            extra={"gallery_categories": list({g.get("category", "") for g in LIFE_AT_GURUH_GALLERY})},
        )
    )
    bid += 1

    faq_meta = content["faq"]
    faq_items = [
        _item(
            i + 1,
            faq["question"],
            full_content=faq["answer"],
            short_summary=faq["answer"],
            sort_order=i + 1,
        )
        for i, faq in enumerate(CAREERS_FAQ)
    ]
    blocks.append(
        _block(
            bid,
            "careers_faq",
            faq_meta["title"],
            subtitle=faq_meta["subtitle"],
            short_summary=faq_meta["short_summary"],
            display_order=bid,
            items=faq_items,
        )
    )

    return blocks


def build_careers_page_sections() -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    sid = _SECTION_ID_START
    order = 1
    slug = "careers"

    sections.append(
        _section(slug, sid, "hero_banner", "Hero Banner", display_order=order,
                 layout_type="hero-banner", background_style="brand", spacing="none", animation="fade-in")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "careers_intro", "Careers Introduction",
                 block_key="careers_introduction", display_order=order,
                 layout_type="split-columns", background_style="default", animation="fade-up",
                 seo_anchor="careers-introduction")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "why_join_us", "Why Join Us",
                 block_key="careers_why_join", display_order=order,
                 layout_type="card-grid", background_style="light", animation="stagger",
                 seo_anchor="why-join-us")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "job_openings", "Current Job Openings",
                 block_key="careers_job_openings", display_order=order,
                 layout_type="job-openings", background_style="default", animation="stagger",
                 seo_anchor="job-openings")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "recruitment_process", "Recruitment Process",
                 block_key="careers_recruitment", display_order=order,
                 layout_type="process-steps", background_style="muted", animation="fade-up",
                 seo_anchor="recruitment-process")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "employee_benefits", "Employee Benefits",
                 block_key="careers_benefits", display_order=order,
                 layout_type="card-grid", background_style="default", animation="stagger",
                 seo_anchor="employee-benefits")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "life_at_guruh", "Life at GURUH",
                 block_key="careers_life_gallery", display_order=order,
                 layout_type="project-gallery", background_style="light", animation="fade-up",
                 seo_anchor="life-at-guruh")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "faq", "Frequently Asked Questions",
                 block_key="careers_faq", display_order=order,
                 layout_type="faq-accordion", background_style="default", animation="fade-up",
                 seo_anchor="careers-faq")
    )
    sid += 1
    order += 1

    sections.append(
        _section(slug, sid, "call_to_action", "Call To Action",
                 block_key="call_to_action", display_order=order,
                 layout_type="cta-banner", background_style="brand", spacing="relaxed", animation="fade-up",
                 seo_anchor="apply-now")
    )

    return sections


def _slug_key(slug: str) -> str:
    return slug.replace("-", "_")


def build_job_detail_blocks(job: dict[str, Any], block_id_start: int) -> list[dict[str, Any]]:
    sk = _slug_key(job["slug"])
    bid = block_id_start
    blocks: list[dict[str, Any]] = []

    blocks.append(
        _block(
            bid,
            f"job_{sk}_overview",
            job["title"],
            subtitle=f"{job['department']} · {job['employment_type']}",
            short_summary=job["short_description"],
            full_content=job["description"],
            hero_image=job.get("image", ""),
            meta_title=job.get("meta_title", job["title"]),
            meta_description=job.get("meta_description", job["short_description"]),
            extra={
                "job_slug": job["slug"],
                "department": job["department"],
                "location": job["location"],
                "employment_type": job["employment_type"],
                "experience_required": job.get("experience_required", ""),
                "deadline": job.get("deadline", ""),
                "responsibilities": job.get("responsibilities", []),
                "qualifications": job.get("qualifications", []),
                "skills": job.get("skills", []),
                "benefits": job.get("benefits", []),
            },
        )
    )
    bid += 1

    blocks.append(
        _block(
            bid,
            f"job_{sk}_apply",
            "Apply for This Position",
            subtitle="Job Application",
            short_summary="Complete the form below to submit your application. We review all submissions carefully.",
            display_order=bid,
            extra={
                "form_id": f"job-apply-{job['slug']}",
                "action_url": f"/careers/{job['slug']}",
                "submit_label": "Submit Application",
                "success_message": "Thank you. Your application has been received and will be reviewed by our HR team.",
                "fields": JOB_APPLICATION_FORM_FIELDS,
                "prefill_position": job["title"],
                "prefill_position_slug": job["slug"],
            },
        )
    )

    return blocks


def build_job_detail_sections(job: dict[str, Any], section_id_start: int) -> list[dict[str, Any]]:
    sk = _slug_key(job["slug"])
    page_slug = f"career-{job['slug']}"
    sid = section_id_start
    order = 1
    sections: list[dict[str, Any]] = []

    sections.append(
        _section(page_slug, sid, "hero_banner", "Hero Banner", display_order=order,
                 layout_type="hero-banner", background_style="brand", spacing="none", animation="fade-in")
    )
    sid += 1
    order += 1

    sections.append(
        _section(page_slug, sid, "job_overview", job["title"],
                 block_key=f"job_{sk}_overview", display_order=order,
                 layout_type="job-detail-overview", background_style="default", animation="fade-up",
                 seo_anchor="job-description")
    )
    sid += 1
    order += 1

    sections.append(
        _section(page_slug, sid, "job_apply", "Apply Now",
                 block_key=f"job_{sk}_apply", display_order=order,
                 layout_type="job-apply-form", background_style="light", animation="fade-up",
                 seo_anchor="apply-form")
    )

    return sections


def build_all_job_detail_data() -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    all_blocks: list[dict[str, Any]] = []
    sections_by_slug: dict[str, list[dict[str, Any]]] = {}
    block_id = _DETAIL_BLOCK_ID_START
    section_id = _DETAIL_SECTION_ID_START

    for job in JOBS_CATALOG:
        job_blocks = build_job_detail_blocks(job, block_id)
        all_blocks.extend(job_blocks)
        block_id += len(job_blocks)

        job_sections = build_job_detail_sections(job, section_id)
        sections_by_slug[f"career-{job['slug']}"] = job_sections
        section_id += len(job_sections)

    return all_blocks, sections_by_slug


CAREERS_PAGE_BLOCKS: list[dict[str, Any]] = build_careers_page_blocks()
CAREERS_PAGE_SECTIONS: list[dict[str, Any]] = build_careers_page_sections()
CAREER_DETAIL_BLOCKS, CAREER_DETAIL_SECTIONS_BY_SLUG = build_all_job_detail_data()
