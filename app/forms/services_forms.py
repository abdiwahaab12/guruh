"""Services admin WTForms."""

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

from app.constants.services_admin import SERVICE_ICONS


class ServiceForm(FlaskForm):
    service_id = HiddenField(validators=[Optional()])

    title = StringField("Service Title", validators=[DataRequired(), Length(max=200)])
    slug = StringField("URL Slug", validators=[Optional(), Length(max=150)])
    short_description = StringField(
        "Short Description",
        validators=[DataRequired(), Length(max=500)],
    )
    description = TextAreaField("Description", validators=[DataRequired()], render_kw={"rows": 6})
    icon = SelectField(
        "Icon",
        choices=[(i, i) for i in SERVICE_ICONS],
        validators=[Optional()],
    )
    sort_order = IntegerField("Sort Order", validators=[Optional()], default=0)
    is_featured = BooleanField("Featured Service", default=False)
    is_active = BooleanField("Active", default=True)

    scope_of_work = TextAreaField(
        "Scope of Work",
        validators=[Optional()],
        render_kw={"rows": 5},
        description="One item per line",
    )
    benefits = TextAreaField(
        "Benefits",
        validators=[Optional()],
        render_kw={"rows": 5},
        description="One item per line",
    )
    equipment = TextAreaField(
        "Related Equipment",
        validators=[Optional()],
        render_kw={"rows": 4},
        description="One item per line",
    )
    team_member_ids = SelectMultipleField("Team Members", coerce=int, validators=[Optional()])

    image = StringField("Featured Image (Media Path)", validators=[Optional(), Length(max=255)])

    related_project_ids = SelectMultipleField("Related Projects", coerce=int, validators=[Optional()])
    related_service_slugs = SelectMultipleField("Related Services", coerce=str, validators=[Optional()])

    meta_title = StringField("Meta Title", validators=[Optional(), Length(max=200)])
    meta_description = TextAreaField(
        "Meta Description",
        validators=[Optional(), Length(max=500)],
        render_kw={"rows": 3},
    )
    og_image = StringField("OG Image (Media Path)", validators=[Optional(), Length(max=255)])
    canonical_url = StringField("Canonical URL", validators=[Optional(), Length(max=500)])

    submit = SubmitField("Save Service")


class ServiceBulkForm(FlaskForm):
    action = SelectField("Bulk Action", validators=[DataRequired()])
    submit = SubmitField("Apply")


class ServiceDeleteForm(FlaskForm):
    submit = SubmitField("Delete Service")
