"""Website CMS admin forms."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import BooleanField, HiddenField, IntegerField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class WebsitePageSeoForm(FlaskForm):
    slug = HiddenField()
    title = StringField("Page Title", validators=[DataRequired(), Length(max=200)])
    meta_title = StringField("Meta Title", validators=[Optional(), Length(max=200)])
    meta_description = TextAreaField("Meta Description", validators=[Optional(), Length(max=2000)])
    banner_subtitle = StringField("Banner Subtitle", validators=[Optional(), Length(max=255)])
    banner_image = StringField("Hero Banner Image", validators=[Optional(), Length(max=255)])
    canonical_url = StringField("Canonical URL", validators=[Optional(), Length(max=500)])
    is_published = BooleanField("Published", default=True)
    submit = SubmitField("Save Page")


class WebsiteSectionForm(FlaskForm):
    page_slug = HiddenField()
    section_id = HiddenField()
    section_key = HiddenField()
    section_title = StringField("Section Title", validators=[DataRequired(), Length(max=200)])
    block_key = StringField("Primary Block Key", validators=[Optional(), Length(max=100)])
    display_order = IntegerField("Display Order", default=0)
    layout_type = SelectField("Layout Type", choices=[], validate_choice=False)
    background_style = SelectField("Background Style", choices=[], validate_choice=False)
    spacing = SelectField("Spacing", choices=[], validate_choice=False)
    animation = SelectField("Animation", choices=[], validate_choice=False)
    seo_anchor = StringField("Anchor ID", validators=[Optional(), Length(max=100)])
    is_visible = BooleanField("Visible", default=True)
    is_active = BooleanField("Active", default=True)
    extra_json = TextAreaField("Extra JSON", validators=[Optional()], render_kw={"rows": 4})
    submit = SubmitField("Save Section")
    preview = SubmitField("Preview")


class WebsiteBlockItemForm(FlaskForm):
    item_id = HiddenField()
    block_key = HiddenField()
    item_key = StringField("Item Key", validators=[Optional(), Length(max=100)])
    is_active = BooleanField("Enabled", default=True)
    submit = SubmitField("Save Item")
    preview = SubmitField("Preview")

class WebsiteSectionActionForm(FlaskForm):
    """CSRF-only form for section actions."""

    pass


class WebsiteBlockItemActionForm(FlaskForm):
    """CSRF-only form for block item actions."""

    pass


class WebsiteHeroSlideForm(FlaskForm):
    slide_id = HiddenField()
    title = StringField("Title", validators=[DataRequired(), Length(max=200)])
    subtitle = StringField("Subtitle", validators=[Optional(), Length(max=255)])
    description = TextAreaField("Description", validators=[Optional()])
    image = StringField("Background Image", validators=[Optional(), Length(max=255)])
    cta_text = StringField("Primary Button Text", validators=[Optional(), Length(max=100)])
    cta_url = StringField("Primary Button URL", validators=[Optional(), Length(max=255)])
    secondary_cta_text = StringField("Secondary Button Text", validators=[Optional(), Length(max=100)])
    secondary_cta_url = StringField("Secondary Button URL", validators=[Optional(), Length(max=255)])
    overlay_opacity = StringField("Overlay Opacity (0–1)", validators=[Optional()], default="0.65")
    text_alignment = SelectField(
        "Text Alignment",
        choices=[("left", "Left"), ("center", "Center"), ("right", "Right")],
        default="left",
    )
    sort_order = IntegerField("Display Order", default=0)
    is_active = BooleanField("Active", default=True)
    submit = SubmitField("Save Slide")


class WebsiteHeroSlideActionForm(FlaskForm):
    """CSRF-only form for hero slide reorder/delete/toggle actions."""

    pass
