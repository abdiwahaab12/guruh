"""Quote form loader — maps catalog data to DTOs for provider layer."""

from __future__ import annotations

from app.data.quote_catalog import (
    BUDGET_RANGES,
    CONTACT_METHODS,
    CURRENCIES,
    PRIORITIES,
    PROJECT_CATEGORIES,
    PROJECT_TYPES,
    QUOTE_FORM_FIELDS,
    QUOTE_FORM_STEPS,
    TIMELINES,
)
from app.schemas.content import FormFieldDTO, QuoteFormOptionsDTO, QuoteFormStepDTO


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
        step_key=field.get("step_key", ""),
    )


def build_quote_form_fields() -> list[FormFieldDTO]:
    return [_field_dict_to_dto(f) for f in QUOTE_FORM_FIELDS]


def build_quote_form_steps() -> list[QuoteFormStepDTO]:
    return [
        QuoteFormStepDTO(
            key=step["key"],
            title=step["title"],
            subtitle=step.get("subtitle", ""),
            description=step.get("description", ""),
            icon=step.get("icon", "bi-circle"),
            sort_order=step.get("sort_order", 0),
            step_type=step.get("step_type", "form"),
        )
        for step in QUOTE_FORM_STEPS
    ]


def build_quote_form_options() -> QuoteFormOptionsDTO:
    return QuoteFormOptionsDTO(
        project_categories=list(PROJECT_CATEGORIES),
        project_types=list(PROJECT_TYPES),
        budget_ranges=list(BUDGET_RANGES),
        currencies=list(CURRENCIES),
        priorities=list(PRIORITIES),
        timelines=list(TIMELINES),
        contact_methods=list(CONTACT_METHODS),
    )


def build_quote_fields_by_step() -> dict[str, list[FormFieldDTO]]:
    """Group form fields by step key for wizard rendering."""
    grouped: dict[str, list[FormFieldDTO]] = {}
    for field in build_quote_form_fields():
        key = field.step_key or "details"
        grouped.setdefault(key, []).append(field)
    return grouped
