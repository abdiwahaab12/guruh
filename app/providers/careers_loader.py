"""Maps careers catalog data to DTOs for providers and services."""

from app.data.careers_catalog import (
    EXPERIENCE_LEVELS,
    JOB_APPLICATION_FORM_FIELDS,
    JOBS_CATALOG,
)
from app.schemas.content import FormFieldDTO, JobApplicationOptionsDTO, JobListingDTO


def build_jobs() -> list[JobListingDTO]:
    return [_catalog_to_dto(job, i) for i, job in enumerate(JOBS_CATALOG)]


def build_job_by_slug(slug: str) -> JobListingDTO | None:
    for i, job in enumerate(JOBS_CATALOG):
        if job["slug"] == slug:
            return _catalog_to_dto(job, i)
    return None


def _catalog_to_dto(job: dict, index: int) -> JobListingDTO:
    return JobListingDTO(
        id=index + 1,
        title=job["title"],
        slug=job["slug"],
        department=job["department"],
        location=job["location"],
        employment_type=job["employment_type"],
        short_description=job.get("short_description", job["description"][:200]),
        description=job["description"],
        requirements=job.get("requirements", ""),
        experience_required=job.get("experience_required", ""),
        responsibilities=list(job.get("responsibilities", [])),
        qualifications=list(job.get("qualifications", [])),
        skills=list(job.get("skills", [])),
        benefits=list(job.get("benefits", [])),
        deadline=job.get("deadline", ""),
        image=job.get("image", ""),
        meta_title=job.get("meta_title", job["title"]),
        meta_description=job.get("meta_description", job.get("short_description", "")),
        sort_order=job.get("sort_order", index + 1),
        is_active=job.get("is_active", True),
    )


def _field_dict_to_dto(field: dict) -> FormFieldDTO:
    return FormFieldDTO(
        name=field["name"],
        label=field["label"],
        field_type=field["field_type"],
        required=field.get("required", False),
        placeholder=field.get("placeholder", ""),
        help_text=field.get("help_text", ""),
        options=list(field.get("options", [])),
        options_source=field.get("options_source", ""),
        col_class=field.get("col_class", "col-12"),
        autocomplete=field.get("autocomplete", ""),
        rows=field.get("rows", 4),
        accept=field.get("accept", ""),
        multiple=field.get("multiple", False),
        disabled=field.get("disabled", False),
    )


def build_job_application_fields() -> list[FormFieldDTO]:
    return [_field_dict_to_dto(f) for f in JOB_APPLICATION_FORM_FIELDS]


def build_job_application_options() -> JobApplicationOptionsDTO:
    return JobApplicationOptionsDTO(experience_levels=list(EXPERIENCE_LEVELS))
