"""
Static asset fallback paths — card/content placeholders only.

Hero banners use Media Library uploads (PNG/JPG/WEBP) via pages.banner_image
and hero_slides.image — templates render a brand gradient when no image is set.
"""

FALLBACK_IMAGES = {
    "hero": "",
    "hero_alt": "",
    "about": "img/fallbacks/about.svg",
    "service": "img/fallbacks/service.svg",
    "project": "img/fallbacks/project.svg",
    "partner": "img/fallbacks/partner.svg",
    "default": "img/fallbacks/default.svg",
}
