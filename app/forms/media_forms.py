"""Enterprise Media Manager WTForms."""

from __future__ import annotations

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, MultipleFileField
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

from app.constants.media_library import MEDIA_FOLDERS


class MediaUploadForm(FlaskForm):
    folder = SelectField(
        "Folder",
        choices=[(f["slug"], f["label"]) for f in MEDIA_FOLDERS],
        validators=[DataRequired()],
        default="general",
    )
    files = MultipleFileField("Files", validators=[FileRequired(message="Select at least one file.")])
    title = StringField("Default Title", validators=[Optional(), Length(max=200)])
    alt_text = StringField("Default Alt Text", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Upload Files")


class MediaMetadataForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=200)])
    original_filename = StringField("Display Filename", validators=[Optional(), Length(max=255)])
    alt_text = StringField("Alt Text", validators=[Optional(), Length(max=255)])
    caption = StringField("Caption", validators=[Optional(), Length(max=500)])
    description = TextAreaField("Description", validators=[Optional()], render_kw={"rows": 4})
    tags = StringField("Tags", validators=[Optional(), Length(max=500)], description="Comma-separated")
    category = StringField("Category", validators=[Optional(), Length(max=100)])
    seo_title = StringField("SEO Title", validators=[Optional(), Length(max=200)])
    seo_description = StringField("SEO Description", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Save Metadata")


class MediaMoveForm(FlaskForm):
    folder = SelectField(
        "Move to Folder",
        choices=[(f["slug"], f["label"]) for f in MEDIA_FOLDERS],
        validators=[DataRequired()],
    )
    submit = SubmitField("Move File")


class MediaReplaceForm(FlaskForm):
    file = FileField("Replacement File", validators=[FileRequired()])
    submit = SubmitField("Replace File")


class MediaRenameForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=200)])
    original_filename = StringField("Display Filename", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Rename")


class MediaDeleteForm(FlaskForm):
    submit = SubmitField("Delete")


class MediaCopyForm(FlaskForm):
    submit = SubmitField("Create Copy")
