"""Users & RBAC admin forms."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import BooleanField, HiddenField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError


class UserForm(FlaskForm):
    user_id = HiddenField()
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    first_name = StringField("First Name", validators=[DataRequired(), Length(max=100)])
    last_name = StringField("Last Name", validators=[Optional(), Length(max=100)])
    role_id = SelectField("Role", coerce=int, validators=[DataRequired()])
    is_active = BooleanField("Active", default=True)
    password = PasswordField("Password", validators=[Optional(), Length(min=8, max=128)])
    new_password = PasswordField("New Password", validators=[Optional(), Length(min=8, max=128)])
    submit = SubmitField("Save User")

    def validate_password(self, field):
        if not self.user_id.data and not field.data:
            raise ValidationError("Password is required for new users.")


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField("New Password", validators=[DataRequired(), Length(min=8, max=128)])
    submit = SubmitField("Reset Password")


class UsersBulkForm(FlaskForm):
    action = SelectField("Action", choices=[], validate_choice=False)
    submit = SubmitField("Apply to Selected")


class RolePermissionsForm(FlaskForm):
    submit = SubmitField("Save Permissions")


class SessionActionForm(FlaskForm):
    pass
