"""
Public header navigation structure — Step 23.2.

Labels come from CMS nav_items (or placeholder defaults) matched by endpoint.
This module defines hierarchy only (which items nest under Services).
"""

from __future__ import annotations

# Top-level header order; tuple = (endpoint, child_endpoints)
HEADER_NAV_STRUCTURE: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("main.index", ()),
    ("main.about", ()),
    ("main.services", ("main.projects", "main.gallery", "main.team")),
    ("main.careers", ()),
    ("main.contact", ()),
)

# Endpoints grouped under dropdowns — excluded from flat top-level display
NESTED_NAV_ENDPOINTS: frozenset[str] = frozenset(
    child for _, children in HEADER_NAV_STRUCTURE for child in children
)

MAX_HERO_SLIDES = 5
