"""Projects admin WTForms."""

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

from app.constants.projects_admin import (
    PROJECT_CATEGORIES,
    PROJECT_CLIENTS,
    PROJECT_COUNTIES,
    PROJECT_COUNTRIES,
    PROJECT_STATUSES,
    PROJECT_YEARS,
)


class ProjectForm(FlaskForm):
    project_id = HiddenField(validators=[Optional()])

    title = StringField("Project Title", validators=[DataRequired(), Length(max=200)])
    slug = StringField("URL Slug", validators=[Optional(), Length(max=150)])
    description = TextAreaField("Description", validators=[DataRequired()], render_kw={"rows": 5})
    overview = TextAreaField("Overview", validators=[Optional()], render_kw={"rows": 4})
    consultant = StringField("Consultant", validators=[Optional(), Length(max=150)])
    duration = StringField("Duration", validators=[Optional(), Length(max=100)])
    completion_date = StringField("Completion Date", validators=[Optional(), Length(max=50)])
    completion_year = SelectField("Year", choices=[("", "—")] + [(y, y) for y in PROJECT_YEARS], validators=[Optional()])
    sort_order = IntegerField("Sort Order", validators=[Optional()], default=0)
    is_featured = BooleanField("Featured Project", default=False)
    is_active = BooleanField("Active", default=True)

    location = StringField("Location", validators=[Optional(), Length(max=150)])
    country = SelectField("Country", choices=[(c, c) for c in PROJECT_COUNTRIES], validators=[DataRequired()])
    county = SelectField(
        "County / Region",
        choices=[("", "—")] + [(c, c) for c in PROJECT_COUNTIES + ["Banaadir", "Hodan District"]],
        validators=[Optional()],
    )
    status = SelectField("Status", choices=[("", "—")] + [(s, s) for s in PROJECT_STATUSES], validators=[Optional()])
    client = SelectField(
        "Client",
        choices=[("", "—")] + [(c, c) for c in PROJECT_CLIENTS],
        validators=[Optional()],
    )
    category = SelectField(
        "Category",
        choices=[("", "—")] + [(c, c) for c in PROJECT_CATEGORIES],
        validators=[Optional()],
    )

    service_slugs = SelectMultipleField("Services", coerce=str, validators=[Optional()])
    equipment = TextAreaField("Equipment Used", validators=[Optional()], render_kw={"rows": 4}, description="One item per line")
    team_member_ids = SelectMultipleField("Team Members", coerce=int, validators=[Optional()])

    meta_title = StringField("Meta Title", validators=[Optional(), Length(max=200)])
    meta_description = TextAreaField("Meta Description", validators=[Optional(), Length(max=500)], render_kw={"rows": 3})
    og_image = StringField("OG Image (Media Path)", validators=[Optional(), Length(max=255)])
    canonical_url = StringField("Canonical URL", validators=[Optional(), Length(max=500)])

    cover_image = StringField("Featured Image (Media Path)", validators=[Optional(), Length(max=255)])

    timeline = TextAreaField(
        "Timeline",
        validators=[Optional()],
        render_kw={"rows": 5},
        description="One milestone per line: YYYY-MM|Title|Description",
    )
    challenges = TextAreaField("Challenges", validators=[Optional()], render_kw={"rows": 4}, description="One per line")
    solutions = TextAreaField("Solutions", validators=[Optional()], render_kw={"rows": 4}, description="One per line")
    scope_of_work = TextAreaField("Scope of Work", validators=[Optional()], render_kw={"rows": 4}, description="One per line")

    related_project_ids = SelectMultipleField("Related Projects", coerce=int, validators=[Optional()])
    related_service_slugs = SelectMultipleField("Related Services", coerce=str, validators=[Optional()])

    submit = SubmitField("Save Project")


class ProjectBulkForm(FlaskForm):
    action = SelectField("Bulk Action", validators=[DataRequired()])
    submit = SubmitField("Apply")


class ProjectDeleteForm(FlaskForm):
    submit = SubmitField("Delete Project")
