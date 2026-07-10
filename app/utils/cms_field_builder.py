"""
Dynamic admin form field definitions derived from ContentBlock DTOs.

Fields are generated from dataclass metadata and runtime values — not hardcoded
per block type.
"""

from __future__ import annotations

import json
from dataclasses import fields, is_dataclass
from typing import Any

from app.constants.website_admin import (
    BLOCK_EDITOR_SKIP,
    FIELD_GROUPS,
    FIELD_HELP,
    FIELD_LABELS,
    ITEM_EDITOR_SKIP,
)
from app.schemas.website_admin import AdminFieldDefinitionDTO


def _humanize(name: str) -> str:
    return FIELD_LABELS.get(name, name.replace("_", " ").title())


def _infer_field_type(name: str, value: Any) -> str:
    lowered = name.lower()
    if lowered in {"file_url"} or lowered.endswith("_file") or lowered.endswith("_document"):
        return "document"
    if lowered in {"hero_image", "og_image", "image", "banner_image"} or lowered.endswith("_image"):
        return "media"
    if name == "gallery_images":
        return "gallery"
    if lowered in {"full_content", "meta_description", "short_summary"} or "content" in lowered:
        if isinstance(value, str) and len(value) > 120:
            return "textarea"
        return "textarea" if name in {"full_content", "meta_description", "short_summary"} else "text"
    if isinstance(value, bool):
        return "checkbox"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return "number"
    if isinstance(value, list):
        return "lines"
    if isinstance(value, dict):
        return "json"
    if isinstance(value, str) and len(value) > 160:
        return "textarea"
    return "text"


def _group_for(name: str) -> str:
    return FIELD_GROUPS.get(name, "extra")


def build_fields_from_dataclass(
    dto: Any,
    *,
    skip: frozenset[str],
    prefix: str = "",
) -> list[AdminFieldDefinitionDTO]:
    if not is_dataclass(dto):
        return []

    result: list[AdminFieldDefinitionDTO] = []
    for field in fields(dto):
        if field.name in skip:
            continue
        value = getattr(dto, field.name)
        if field.name == "extra" and isinstance(value, dict):
            for key in sorted(value.keys()):
                extra_value = value[key]
                result.append(
                    AdminFieldDefinitionDTO(
                        name=f"extra__{key}",
                        label=_humanize(key),
                        field_type=_infer_field_type(key, extra_value),
                        value=extra_value,
                        group="extra",
                        help_text=FIELD_HELP.get(key, ""),
                    )
                )
            continue

        result.append(
            AdminFieldDefinitionDTO(
                name=f"{prefix}{field.name}" if prefix else field.name,
                label=_humanize(field.name),
                field_type=_infer_field_type(field.name, value),
                value=value,
                group=_group_for(field.name),
            )
        )
    return result


def build_block_editor_fields(block_dto: Any) -> list[AdminFieldDefinitionDTO]:
    return build_fields_from_dataclass(block_dto, skip=BLOCK_EDITOR_SKIP)


def build_item_editor_fields(item_dto: Any) -> list[AdminFieldDefinitionDTO]:
    return build_fields_from_dataclass(item_dto, skip=ITEM_EDITOR_SKIP)


def parse_field_value(field: AdminFieldDefinitionDTO, raw: str | None) -> Any:
    if field.field_type == "checkbox":
        return raw in ("1", "true", "on", "yes")
    if field.field_type == "number":
        if not raw:
            return 0
        try:
            return int(raw) if "." not in raw else float(raw)
        except ValueError:
            return 0
    if field.field_type == "lines":
        return [line.strip() for line in (raw or "").splitlines() if line.strip()]
    if field.field_type == "gallery":
        return parse_field_value(
            AdminFieldDefinitionDTO(
                name=field.name,
                label=field.label,
                field_type="lines",
                value=field.value,
                group=field.group,
            ),
            raw,
        )
    if field.field_type == "json":
        if not raw:
            return {}
        try:
            parsed = json.loads(raw)
            return parsed if isinstance(parsed, dict) else {}
        except json.JSONDecodeError:
            return field.value if isinstance(field.value, dict) else {}
    return raw or ""


def apply_form_to_block_dto(block_dto: Any, form_data: dict[str, str]) -> dict[str, Any]:
    """Return dict of standard fields + extra dict from posted form."""
    field_defs = build_block_editor_fields(block_dto)
    payload: dict[str, Any] = {}
    extra: dict[str, Any] = {}

    for field in field_defs:
        raw = form_data.get(field.name, "")
        parsed = parse_field_value(field, raw)
        if field.name.startswith("extra__"):
            extra[field.name.replace("extra__", "", 1)] = parsed
        else:
            payload[field.name] = parsed

    payload["extra"] = extra
    payload["is_active"] = form_data.get("is_active") in ("1", "true", "on", "yes", "y")
    return payload


def apply_form_to_item_dto(item_dto: Any, form_data: dict[str, str]) -> dict[str, Any]:
    field_defs = build_item_editor_fields(item_dto)
    payload: dict[str, Any] = {}
    extra: dict[str, Any] = {}

    for field in field_defs:
        raw = form_data.get(field.name, "")
        parsed = parse_field_value(field, raw)
        if field.name.startswith("extra__"):
            extra[field.name.replace("extra__", "", 1)] = parsed
        else:
            payload[field.name] = parsed

    payload["extra"] = extra
    payload["is_active"] = form_data.get("is_active") in ("1", "true", "on", "yes", "y")
    payload["item_key"] = form_data.get("item_key", "").strip()
    return payload
