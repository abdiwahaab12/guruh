"""Team admin WTForms."""

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

from app.constants.team_admin import MEMBER_TYPES, TEAM_DEPARTMENTS


class TeamMemberForm(FlaskForm):
    team_member_id = HiddenField(validators=[Optional()])

    name = StringField("Full Name", validators=[DataRequired(), Length(max=150)])
    slug = StringField("URL Slug", validators=[Optional(), Length(max=150)])
    position = StringField("Position", validators=[DataRequired(), Length(max=150)])
    department = SelectField(
        "Department",
        choices=[("", "—")] + [(d, d) for d in TEAM_DEPARTMENTS],
        validators=[Optional()],
    )
    member_type = SelectField(
        "Member Type",
        choices=MEMBER_TYPES,
        validators=[DataRequired()],
    )
    email = StringField("Email", validators=[Optional(), Length(max=120)])
    phone = StringField("Phone", validators=[Optional(), Length(max=50)])
    sort_order = IntegerField("Sort Order", validators=[Optional()], default=0)
    is_featured = BooleanField("Featured Member", default=False)
    is_active = BooleanField("Active", default=True)

    years_experience = StringField("Years of Experience", validators=[Optional(), Length(max=50)])
    education = StringField("Education", validators=[Optional(), Length(max=255)])
    experience_summary = TextAreaField(
        "Experience Summary",
        validators=[Optional()],
        render_kw={"rows": 4},
    )
    related_project_ids = SelectMultipleField("Related Projects", coerce=int, validators=[Optional()])
    related_service_slugs = SelectMultipleField("Related Services", coerce=str, validators=[Optional()])
    related_equipment_ids = SelectMultipleField("Related Equipment", coerce=int, validators=[Optional()])

    bio = TextAreaField("Biography", validators=[Optional()], render_kw={"rows": 8})

    photo = StringField("Profile Photo (Media Path)", validators=[Optional(), Length(max=255)])

    social_links = TextAreaField(
        "Social Links",
        validators=[Optional()],
        render_kw={"rows": 4},
        description="One link per line: platform|url|icon (icon optional)",
    )

    meta_title = StringField("Meta Title", validators=[Optional(), Length(max=200)])
    meta_description = TextAreaField(
        "Meta Description",
        validators=[Optional(), Length(max=500)],
        render_kw={"rows": 3},
    )
    og_image = StringField("OG Image (Media Path)", validators=[Optional(), Length(max=255)])
    canonical_url = StringField("Canonical URL", validators=[Optional(), Length(max=500)])

    submit = SubmitField("Save Team Member")


class TeamBulkForm(FlaskForm):
    action = SelectField("Bulk Action", validators=[DataRequired()])
    submit = SubmitField("Apply")


class TeamDeleteForm(FlaskForm):
    submit = SubmitField("Delete Team Member")
