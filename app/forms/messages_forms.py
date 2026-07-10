"""Messages / Inbox admin forms."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class MessagesBulkForm(FlaskForm):
    action = SelectField("Action", choices=[], validate_choice=False)
    submit = SubmitField("Apply to Selected")


class MessageReplyForm(FlaskForm):
    reply_subject = StringField("Reply Subject", validators=[Optional(), Length(max=200)])
    reply_body = TextAreaField("Reply Message", validators=[DataRequired(), Length(max=10000)], render_kw={"rows": 8})
    admin_notes = TextAreaField("Internal Notes", validators=[Optional(), Length(max=5000)], render_kw={"rows": 3})
    submit = SubmitField("Save Reply")


class MessageActionForm(FlaskForm):
    """CSRF-only form for single-message actions."""

    pass
