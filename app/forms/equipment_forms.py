"""Equipment admin WTForms."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    HiddenField,
    IntegerField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, Optional

from app.constants.equipment_admin import CONDITION_OPTIONS, EQUIPMENT_CATEGORY_TITLES


class EquipmentForm(FlaskForm):
    equipment_id = HiddenField(validators=[Optional()])

    name = StringField("Equipment Name", validators=[DataRequired(), Length(max=200)])
    slug = StringField("URL Slug", validators=[Optional(), Length(max=150)])
    category = SelectField(
        "Category",
        choices=[(c, c) for c in EQUIPMENT_CATEGORY_TITLES],
        validators=[DataRequired()],
    )
    short_description = StringField(
        "Short Description",
        validators=[DataRequired(), Length(max=500)],
    )
    description = TextAreaField("Description", validators=[DataRequired()], render_kw={"rows": 6})
    sort_order = IntegerField("Sort Order", validators=[Optional()], default=0)
    is_featured = BooleanField("Featured Equipment", default=False)
    is_active = BooleanField("Active", default=True)

    capacity = StringField("Capacity", validators=[Optional(), Length(max=150)])
    condition = SelectField(
        "Condition",
        choices=[(c, c) for c in CONDITION_OPTIONS],
        validators=[Optional()],
    )
    maintenance_status = StringField("Maintenance Status", validators=[Optional(), Length(max=255)])
    usage = TextAreaField("Typical Usage", validators=[Optional()], render_kw={"rows": 4})
    specifications = TextAreaField(
        "Technical Specifications",
        validators=[Optional()],
        render_kw={"rows": 5},
        description="One spec per line: Label|Value",
    )

    image = StringField("Featured Image (Media Path)", validators=[Optional(), Length(max=255)])

    related_project_ids = SelectMultipleField("Related Projects", coerce=int, validators=[Optional()])
    related_service_slugs = SelectMultipleField("Related Services", coerce=str, validators=[Optional()])
    team_member_ids = SelectMultipleField("Team Members", coerce=int, validators=[Optional()])

    meta_title = StringField("Meta Title", validators=[Optional(), Length(max=200)])
    meta_description = TextAreaField(
        "Meta Description",
        validators=[Optional(), Length(max=500)],
        render_kw={"rows": 3},
    )
    og_image = StringField("OG Image (Media Path)", validators=[Optional(), Length(max=255)])
    canonical_url = StringField("Canonical URL", validators=[Optional(), Length(max=500)])

    submit = SubmitField("Save Equipment")


class EquipmentBulkForm(FlaskForm):
    action = SelectField("Bulk Action", validators=[DataRequired()])
    submit = SubmitField("Apply")


class EquipmentDeleteForm(FlaskForm):
    submit = SubmitField("Delete Equipment")
