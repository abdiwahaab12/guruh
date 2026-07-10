"""Careers admin WTForms."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    HiddenField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, Length, Optional

from app.constants.careers_admin import (
    EMPLOYMENT_TYPES,
    EXPERIENCE_LEVELS,
    JOB_DEPARTMENTS,
    JOB_LOCATIONS,
    JOB_STATUSES,
)


class JobListingForm(FlaskForm):
    job_id = HiddenField(validators=[Optional()])

    title = StringField("Job Title", validators=[DataRequired(), Length(max=200)])
    slug = StringField("URL Slug", validators=[Optional(), Length(max=150)])
    department = SelectField(
        "Department",
        choices=[("", "—")] + [(d, d) for d in JOB_DEPARTMENTS],
        validators=[Optional()],
    )
    location = SelectField(
        "Location",
        choices=[("", "—")] + [(l, l) for l in JOB_LOCATIONS],
        validators=[Optional()],
    )
    employment_type = SelectField(
        "Employment Type",
        choices=[(t, t) for t in EMPLOYMENT_TYPES],
        validators=[DataRequired()],
    )
    status = SelectField("Status", choices=JOB_STATUSES, validators=[DataRequired()])
    short_description = StringField(
        "Short Description",
        validators=[Optional(), Length(max=500)],
    )
    sort_order = IntegerField("Sort Order", validators=[Optional()], default=0)
    is_active = BooleanField("Active Record", default=True)

    description = TextAreaField("Job Description", validators=[DataRequired()], render_kw={"rows": 8})
    requirements = TextAreaField("Requirements Summary", validators=[Optional()], render_kw={"rows": 4})
    experience_required = SelectField(
        "Experience Required",
        choices=[("", "—")] + [(e, e) for e in EXPERIENCE_LEVELS],
        validators=[Optional()],
    )
    image = StringField("Featured Image (Media Path)", validators=[Optional(), Length(max=255)])
    responsibilities = TextAreaField(
        "Responsibilities",
        validators=[Optional()],
        render_kw={"rows": 5},
        description="One item per line",
    )
    qualifications = TextAreaField(
        "Qualifications",
        validators=[Optional()],
        render_kw={"rows": 5},
        description="One item per line",
    )
    skills = TextAreaField(
        "Skills",
        validators=[Optional()],
        render_kw={"rows": 4},
        description="One item per line",
    )
    benefits = TextAreaField(
        "Benefits",
        validators=[Optional()],
        render_kw={"rows": 4},
        description="One item per line",
    )

    deadline = StringField("Application Deadline", validators=[Optional(), Length(max=50)])
    accept_applications = BooleanField("Accept Applications", default=True)
    is_featured = BooleanField("Featured Job", default=False)
    notify_email = StringField(
        "Notification Email",
        validators=[Optional(), Email(), Length(max=120)],
    )
    auto_reply_enabled = BooleanField("Enable Auto Reply", default=False)
    auto_reply_message = TextAreaField(
        "Auto Reply Message",
        validators=[Optional()],
        render_kw={"rows": 4},
    )

    meta_title = StringField("Meta Title", validators=[Optional(), Length(max=200)])
    meta_description = TextAreaField(
        "Meta Description",
        validators=[Optional(), Length(max=500)],
        render_kw={"rows": 3},
    )
    og_image = StringField("OG Image (Media Path)", validators=[Optional(), Length(max=255)])
    canonical_url = StringField("Canonical URL", validators=[Optional(), Length(max=500)])

    submit = SubmitField("Save Job")


class CareersBulkForm(FlaskForm):
    action = SelectField("Bulk Action", validators=[DataRequired()])
    submit = SubmitField("Apply")


class CareersDeleteForm(FlaskForm):
    submit = SubmitField("Delete Job")
