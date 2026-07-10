"""Gallery admin WTForms."""

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

from app.constants.gallery_admin import (
    GALLERY_ALBUMS,
    GALLERY_CATEGORIES,
    GALLERY_COUNTRIES,
    GALLERY_COUNTIES,
    GALLERY_YEARS,
    MEDIA_TYPES,
    VIDEO_PROVIDERS,
)


class GalleryItemForm(FlaskForm):
    gallery_item_id = HiddenField(validators=[Optional()])

    title = StringField("Title", validators=[DataRequired(), Length(max=200)])
    slug = StringField("URL Slug", validators=[Optional(), Length(max=150)])
    category = SelectField(
        "Category",
        choices=[("", "—")] + [(c, c) for c in GALLERY_CATEGORIES],
        validators=[Optional()],
    )
    media_type = SelectField(
        "Media Type",
        choices=MEDIA_TYPES,
        validators=[DataRequired()],
        render_kw={"id": "media_type"},
    )
    album = SelectField(
        "Album",
        choices=[("", "—")] + list(GALLERY_ALBUMS),
        validators=[Optional()],
    )
    caption = TextAreaField("Caption", validators=[Optional()], render_kw={"rows": 3})
    location = StringField("Location", validators=[Optional(), Length(max=150)])
    county = SelectField(
        "County / Region",
        choices=[("", "—")] + [(c, c) for c in GALLERY_COUNTIES],
        validators=[Optional()],
    )
    country = SelectField(
        "Country",
        choices=[(c, c) for c in GALLERY_COUNTRIES],
        validators=[Optional()],
    )
    media_date = StringField("Date", validators=[Optional(), Length(max=50)])
    year = SelectField(
        "Year",
        choices=[("", "—")] + [(y, y) for y in GALLERY_YEARS],
        validators=[Optional()],
    )
    sort_order = IntegerField("Sort Order", validators=[Optional()], default=0)
    is_featured = BooleanField("Featured Media", default=False)
    is_active = BooleanField("Active", default=True)

    image = StringField("Media Path", validators=[DataRequired(), Length(max=255)])
    video_provider = SelectField("Video Provider", choices=VIDEO_PROVIDERS, validators=[Optional()])
    video_id = StringField("Video ID", validators=[Optional(), Length(max=100)])
    embed_url = StringField("Embed URL", validators=[Optional(), Length(max=500)])

    project_id = SelectField("Related Project", coerce=int, validators=[Optional()])
    service_slug = SelectField("Related Service", validators=[Optional()])
    equipment_slug = SelectField("Related Equipment", validators=[Optional()])
    team_member_ids = SelectMultipleField("Related Team Members", coerce=int, validators=[Optional()])

    meta_title = StringField("Meta Title", validators=[Optional(), Length(max=200)])
    meta_description = TextAreaField(
        "Meta Description",
        validators=[Optional(), Length(max=500)],
        render_kw={"rows": 3},
    )
    og_image = StringField("OG Image (Media Path)", validators=[Optional(), Length(max=255)])
    canonical_url = StringField("Canonical URL", validators=[Optional(), Length(max=500)])

    submit = SubmitField("Save Gallery Item")


class GalleryBulkForm(FlaskForm):
    action = SelectField("Bulk Action", validators=[DataRequired()])
    submit = SubmitField("Apply")


class GalleryDeleteForm(FlaskForm):
    submit = SubmitField("Delete Gallery Item")
