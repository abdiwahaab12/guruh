"""Enterprise System Administration forms."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class MaintenanceForm(FlaskForm):
    message = TextAreaField(
        "Maintenance Message",
        validators=[DataRequired(), Length(max=2000)],
        render_kw={"rows": 4},
    )
    submit_enable = SubmitField("Enable Maintenance Mode")
    submit_disable = SubmitField("Disable Maintenance Mode")
    submit_message = SubmitField("Save Message")


class BackupRestoreForm(FlaskForm):
    filename = HiddenField("Backup File", validators=[DataRequired()])
    confirm = StringField(
        "Type RESTORE to confirm",
        validators=[DataRequired(), Length(max=20)],
        render_kw={"placeholder": "RESTORE", "autocomplete": "off"},
    )
    submit = SubmitField("Restore Backup")


class LogSearchForm(FlaskForm):
    q = StringField("Search logs", validators=[Optional(), Length(max=120)])
    submit = SubmitField("Search")
