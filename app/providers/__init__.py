"""
Content provider factory — selects data source based on app configuration.
"""

from flask import Flask

from app.providers.base import ContentProvider
from app.providers.database import DatabaseContentProvider
from app.providers.placeholder import PlaceholderContentProvider

_provider: ContentProvider | None = None


def init_content_provider(app: Flask) -> ContentProvider:
    """Initialize and register the content provider for this app instance."""
    global _provider

    if app.config.get("DATABASE_ENABLED"):
        _provider = DatabaseContentProvider()
        app.logger.info("Content provider: DatabaseContentProvider (MySQL)")
    else:
        _provider = PlaceholderContentProvider()
        app.logger.info("Content provider: PlaceholderContentProvider (development)")

    app.extensions["content_provider"] = _provider
    return _provider


def get_content_provider() -> ContentProvider:
    """Return the active content provider. Must call init_content_provider first."""
    if _provider is None:
        raise RuntimeError("Content provider not initialized. Call init_content_provider(app).")
    return _provider
