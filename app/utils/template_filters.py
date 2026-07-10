"""
Template filters for safe rendering of CMS-managed content.
"""

from flask import url_for


def safe_href(value: str) -> str:
    """
    Sanitize URLs from the database before use in href attributes.
    Allows relative internal paths only — blocks javascript/data protocol injection.
    """
    if not value or not isinstance(value, str):
        return url_for("main.index")

    cleaned = value.strip()

    lowered = cleaned.lower()
    if lowered.startswith(("javascript:", "data:", "vbscript:")):
        return url_for("main.index")

    if cleaned.startswith("//"):
        return url_for("main.index")

    if cleaned.startswith("/"):
        return cleaned

    # Allow same-site relative paths stored without leading slash
    if cleaned and not cleaned.startswith(("http://", "https://", "mailto:", "tel:")):
        return f"/{cleaned.lstrip('/')}"

    # External URLs — permitted for partner links; use with rel="noopener" in template
    if cleaned.startswith(("http://", "https://", "mailto:", "tel:")):
        return cleaned

    return url_for("main.index")


def register_template_filters(app) -> None:
    """Register Jinja2 filters on the Flask app."""
    app.jinja_env.filters["safe_href"] = safe_href
