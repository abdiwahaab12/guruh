"""Admin authentication WTForms — CSRF protected."""

from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class LoginForm(FlaskForm):
    email = EmailField(
        "Email Address",
        validators=[DataRequired(message="Email is required."), Email(message="Enter a valid email.")],
        render_kw={"autocomplete": "email", "placeholder": "you@company.com"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(message="Password is required.")],
        render_kw={"autocomplete": "current-password"},
    )
    remember = BooleanField("Remember me", validators=[Optional()])
    submit = SubmitField("Sign In")


class ForgotPasswordForm(FlaskForm):
    email = EmailField(
        "Email Address",
        validators=[DataRequired(message="Email is required."), Email(message="Enter a valid email.")],
        render_kw={"autocomplete": "email", "placeholder": "you@company.com"},
    )
    submit = SubmitField("Send Reset Link")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "New Password",
        validators=[
            DataRequired(message="Password is required."),
            Length(min=8, message="Password must be at least 8 characters."),
        ],
        render_kw={"autocomplete": "new-password"},
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(message="Please confirm your password."),
            EqualTo("password", message="Passwords must match."),
        ],
        render_kw={"autocomplete": "new-password"},
    )
    submit = SubmitField("Reset Password")
