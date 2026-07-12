"""
Import official portfolio projects from PROJECTS_CATALOG into MySQL.

Run after init_db.py and seed_auth.py:
    python scripts/seed_projects.py

Safe to re-run — updates existing projects matched by slug.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import app.models  # noqa: F401 — register models before app import
from app.data.projects_catalog import CATEGORY_TO_SERVICE_SLUG, PROJECTS_CATALOG
from app.extensions import db
from app.models.catalog import Project
from app.providers.projects_admin_provider import ProjectsAdminProvider
from app.schemas.projects_admin import ProjectAdminDTO
from run import app


def _catalog_to_dto(entry: dict, sort_order: int, project_id: int | None = None) -> ProjectAdminDTO:
    category = entry.get("category", "")
    service_slugs = list(entry.get("service_slugs", []))
    if not service_slugs and category in CATEGORY_TO_SERVICE_SLUG:
        service_slugs = [CATEGORY_TO_SERVICE_SLUG[category]]

    gallery_paths = list(entry.get("gallery_images", []))
    if not gallery_paths and entry.get("cover_image"):
        gallery_paths = [entry["cover_image"]]

    return ProjectAdminDTO(
        id=project_id,
        title=entry["title"],
        slug=entry["slug"],
        description=entry.get("description", ""),
        location=entry.get("location", ""),
        country=entry.get("country", "Kenya"),
        county=entry.get("county", ""),
        status=entry.get("status", "Completed"),
        client=entry.get("client", ""),
        category=category,
        cover_image=entry.get("cover_image", ""),
        completion_date=entry.get("completion_date", ""),
        completion_year=entry.get("completion_year", ""),
        sort_order=sort_order,
        is_featured=bool(entry.get("is_featured", False)),
        is_active=True,
        meta_title=entry.get("meta_title", entry["title"]),
        meta_description=entry.get("meta_description", entry.get("description", "")),
        overview=entry.get("overview", ""),
        consultant=entry.get("consultant", ""),
        duration=entry.get("duration", ""),
        challenges=list(entry.get("challenges", [])),
        solutions=list(entry.get("solutions", [])),
        scope_of_work=list(entry.get("scope_of_work", [])),
        service_slugs=service_slugs,
        equipment=list(entry.get("equipment_used", [])),
        gallery_paths=gallery_paths,
        related_service_slugs=service_slugs,
    )


def seed_projects() -> None:
    created = 0
    updated = 0
    slug_to_id: dict[str, int] = {}

    with app.app_context():
        for index, entry in enumerate(PROJECTS_CATALOG, start=1):
            existing = Project.query.filter_by(slug=entry["slug"]).first()
            dto = _catalog_to_dto(entry, sort_order=index, project_id=existing.id if existing else None)
            project = ProjectsAdminProvider.save_from_dto(dto)
            slug_to_id[project.slug] = project.id
            if existing:
                updated += 1
            else:
                created += 1

        for entry in PROJECTS_CATALOG:
            related_slugs = list(entry.get("related_project_slugs", []))
            if not related_slugs:
                continue
            project = Project.query.filter_by(slug=entry["slug"]).first()
            if not project or not project.detail:
                continue
            related_ids = [slug_to_id[s] for s in related_slugs if s in slug_to_id]
            import json

            project.detail.related_project_ids_json = json.dumps(related_ids)

        db.session.commit()
        total = Project.query.count()
        featured = Project.query.filter_by(is_active=True, is_featured=True).count()
        print(f"Projects seed complete: {created} created, {updated} updated.")
        print(f"Database now has {total} projects ({featured} featured).")


if __name__ == "__main__":
    seed_projects()
