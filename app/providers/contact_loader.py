"""Maps contact and quote catalog data to DTOs for providers and services."""

from app.data.company_profile import COMPANY_PROFILE
from app.data.contact_catalog import (
    CONTACT_FORM_FIELDS,
    CONTACT_PAGE_CONTENT,
    DEPARTMENT_CONTACTS,
)
from app.data.quote_catalog import QUOTE_FORM_FIELDS
from app.providers import quote_loader
from app.providers.profile_loader import phone_to_tel
from app.schemas.content import (
    DepartmentContactDTO,
    EmergencyContactDTO,
    FormFieldDTO,
    MapLocationDTO,
    OfficeLocationDTO,
    QuoteFormOptionsDTO,
    QuoteFormStepDTO,
)


def _office_dict_to_dto(office: dict, index: int = 0) -> OfficeLocationDTO:
    """Map a catalog office record to OfficeLocationDTO."""
    phone_primary = office.get("phone_primary", "")
    return OfficeLocationDTO(
        id=office.get("id", index + 1),
        slug=office.get("slug", f"office-{index + 1}"),
        name=office.get("name", office.get("office_label", "Office")),
        office_label=office.get("office_label", "Office"),
        address=office["address"],
        postal_address=office.get("postal_address", ""),
        phone_primary=phone_primary,
        phone_secondary=office.get("phone_secondary", ""),
        phone_tel=phone_to_tel(phone_primary),
        email=office.get("email", ""),
        office_hours=office.get("office_hours", ""),
        address_area=office.get("address_area", ""),
        address_locality=office.get("address_locality", ""),
        address_district=office.get("address_district", ""),
        address_country=office.get("country", office.get("address_country", "")),
        address_country_code=office.get("country_code", office.get("address_country_code", "")),
        is_headquarters=office.get("is_headquarters", False),
        show_on_contact_page=office.get("show_on_contact_page", True),
        sort_order=office.get("sort_order", index + 1),
        is_active=office.get("is_active", True),
    )


def build_office_locations() -> list[OfficeLocationDTO]:
    """All active company offices — headquarters and future branches."""
    offices = COMPANY_PROFILE.get("offices") or []
    if offices:
        return [
            _office_dict_to_dto(office, index)
            for index, office in enumerate(offices)
            if office.get("is_active", True)
        ]

    office = CONTACT_PAGE_CONTENT["office"]
    return [
        OfficeLocationDTO(
            name=office["name"],
            address=office["address"],
            postal_address=office["postal_address"],
            phone_primary=office["phone_primary"],
            phone_secondary=office.get("phone_secondary", ""),
            phone_tel=phone_to_tel(office["phone_primary"]),
            email=office["email"],
            office_hours=office["office_hours"],
            address_locality=office.get("address_locality", ""),
            address_district=office.get("address_district", ""),
            address_country=office.get("address_country", ""),
            address_country_code=office.get("address_country_code", ""),
            is_headquarters=True,
            show_on_contact_page=True,
        )
    ]


def build_contact_offices() -> list[OfficeLocationDTO]:
    """Offices displayed on the public contact page (current operating locations)."""
    return [
        office
        for office in build_office_locations()
        if office.show_on_contact_page and office.is_active
    ]


def build_office_location() -> OfficeLocationDTO:
    """Primary office — headquarters when configured, else legacy contact block."""
    offices = build_office_locations()
    for office in offices:
        if office.is_headquarters:
            return office
    return offices[0]


def build_department_contacts() -> list[DepartmentContactDTO]:
    return [
        DepartmentContactDTO(
            id=i + 1,
            name=dept["name"],
            contact_person=dept.get("contact_person", ""),
            phone=dept.get("phone", ""),
            email=dept.get("email", ""),
            description=dept.get("description", ""),
            icon=dept.get("icon", "bi-building"),
            sort_order=dept.get("sort_order", i + 1),
        )
        for i, dept in enumerate(DEPARTMENT_CONTACTS)
    ]


def build_emergency_contact() -> EmergencyContactDTO:
    emergency = CONTACT_PAGE_CONTENT["emergency"]
    return EmergencyContactDTO(
        title=emergency["title"],
        phone=emergency["phone"],
        description=emergency["description"],
        availability=emergency["availability"],
        icon=emergency.get("icon", "bi-exclamation-triangle-fill"),
        phone_tel=phone_to_tel(emergency["phone"]),
    )


def build_map_location() -> MapLocationDTO:
    map_data = CONTACT_PAGE_CONTENT["map"]
    return MapLocationDTO(
        latitude=map_data["latitude"],
        longitude=map_data["longitude"],
        zoom=map_data["zoom"],
        embed_url=map_data["embed_url"],
        map_provider=map_data["map_provider"],
        map_ready=map_data["map_ready"],
        title=map_data["title"],
        short_summary=map_data["short_summary"],
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
        step_key=field.get("step_key", ""),
    )


def build_contact_form_fields() -> list[FormFieldDTO]:
    return [_field_dict_to_dto(f) for f in CONTACT_FORM_FIELDS]


def build_quote_form_fields() -> list[FormFieldDTO]:
    return quote_loader.build_quote_form_fields()


def build_quote_form_steps() -> list[QuoteFormStepDTO]:
    return quote_loader.build_quote_form_steps()


def build_quote_form_options() -> QuoteFormOptionsDTO:
    return quote_loader.build_quote_form_options()


def build_company_contact_block_extra() -> dict:
    """CMS block payload for admin-managed company contact information."""
    contact = COMPANY_PROFILE["contact"]
    geo = COMPANY_PROFILE.get("geography", {})
    hq = COMPANY_PROFILE.get("headquarters", {})
    map_data = contact.get("map", {})
    primary_office = build_office_location()
    return {
        "company_name": contact["company_name"],
        "head_office_label": contact.get("head_office_label", hq.get("label", "Head Office")),
        "founded_country": geo.get("founded_country", ""),
        "founded_country_code": geo.get("founded_country_code", ""),
        "operating_country": geo.get("operating_country", contact.get("address_country", "")),
        "operating_country_code": geo.get(
            "operating_country_code", contact.get("address_country_code", "")
        ),
        "headquarters": hq.get("summary", primary_office.address),
        "address": primary_office.address,
        "postal_address": primary_office.postal_address,
        "address_area": primary_office.address_area,
        "address_district": primary_office.address_district,
        "address_locality": primary_office.address_locality,
        "address_country": primary_office.address_country,
        "address_country_code": primary_office.address_country_code,
        "email": primary_office.email,
        "phone_primary": primary_office.phone_primary,
        "phone_secondary": primary_office.phone_secondary,
        "phone_tel": primary_office.phone_tel or phone_to_tel(primary_office.phone_primary),
        "office_hours": primary_office.office_hours,
        "map_label": map_data.get("label", primary_office.address),
        "map_latitude": map_data.get("latitude"),
        "map_longitude": map_data.get("longitude"),
        "map_zoom": map_data.get("zoom", 16),
        "map_embed_url": map_data.get("embed_url", ""),
        "map_provider": map_data.get("map_provider", "google-maps"),
        "map_ready": map_data.get("map_ready", False),
    }