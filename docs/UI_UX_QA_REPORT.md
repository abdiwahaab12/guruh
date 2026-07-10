# UI/UX QA Report — Hero Banners & Header Fixes

**Project:** GURUH Construction — Public Website  
**Date:** 8 July 2026  
**Scope:** Pre-deployment UI fixes (architecture preserved)

---

## Executive Summary

All requested hero banner and header fixes were implemented without changing Route → Service → Provider → DTO → Page Builder architecture. Public pages now render heroes **below** the sticky header, logos use specified responsive sizes, hero backgrounds come from the **Media Library** (PNG/JPG/WEBP), and every managed page has an editable hero banner in **Website CMS**.

| Verification | Result |
|--------------|--------|
| `scripts/test_public.py` | **12/12** passed |
| `scripts/check_ui_assets.py` | **12/13** (equipment test slug 404 — catalog data) |
| Architecture changes | **None** |

---

## Issues Found & Fixed

### 1. Homepage hero hidden behind sticky header

| | |
|---|---|
| **Issue** | `.hero-slider` used `margin-top: calc(-1 * var(--header-height))`, pulling the carousel under the fixed header and clipping content. |
| **Fix** | Removed negative margin. Hero height set to `calc(100dvh - var(--header-height))` with responsive `--header-height` tokens for desktop (topbar + navbar), tablet (navbar + 60px logo), and mobile (navbar + 50px logo). |
| **Files** | `static/css/home.css`, `static/css/main.css` |

### 2. Header logo too small / inconsistent

| | |
|---|---|
| **Issue** | Logo used fluid `clamp()` sizes; did not match required breakpoints. |
| **Fix** | Explicit sizes: **70px** desktop (≥992px), **60px** tablet (768–991px), **50px** mobile (<768px), with proportionally smaller scrolled states. Navbar height variables adjusted. |
| **Files** | `static/css/main.css` |

### 3. SVG placeholder dependency for hero banners

| | |
|---|---|
| **Issue** | `bg_image_url()` defaulted to `img/fallbacks/hero-*.svg` when no image was configured. |
| **Fix** | Hero macros no longer inject SVG fallbacks. When no Media Library path is set, a **brand gradient** displays. Uploads via PNG, JPG, or WEBP work through existing `uploads/content/` paths. |
| **Files** | `templates/macros/media.html`, `app/constants/media.py`, `app/providers/placeholder.py`, hero layout templates |

### 4. Per-page editable hero banners (Website CMS)

| | |
|---|---|
| **Issue** | Page SEO had a plain text field + external Browse link; home slider images were not manageable in admin. |
| **Fix** | **Hero Banner** panel on every Website CMS page editor with media picker grid, upload/library links, and live preview. Home page adds **Hero Slides** panel for per-slide backgrounds (falls back to page banner image). Saving `banner_image` on Home syncs to slides without their own image. |
| **Files** | `templates/admin/website/page_editor.html`, `_hero_banner_picker.html`, `app/providers/website_admin_provider.py`, `app/services/website_admin_service.py`, `app/routes/admin/website.py`, `app/forms/website_forms.py`, `static/js/admin-website.js` |

### 5. Inner-page hero consistency

| | |
|---|---|
| **Issue** | Inner heroes always referenced fallback URLs in inline styles. |
| **Fix** | `hero_banner.html`, `page_hero.html`, `project_hero.html`, `equipment_hero.html` use conditional `.has-media` class and gradient-only fallback. |
| **Files** | Listed above + `static/css/main.css` (`.page-hero-bg.has-media`) |

### 6. Home slider / page banner disconnect

| | |
|---|---|
| **Issue** | `pages.banner_image` for Home was saved in admin but unused by the slider. |
| **Fix** | Slider passes `page_banner_image`; each slide uses `slide.image or page.banner_image`. |
| **Files** | `templates/pages/home.html`, `templates/components/home/hero_slider.html` |

---

## Pages Verified

| Page | Route | Hero source | CMS editable |
|------|-------|-------------|--------------|
| Home | `/` | `hero_slides` + `pages.banner_image` | Yes — Hero Banner + Hero Slides |
| About | `/about` | `pages.banner_image` | Yes |
| Services | `/services` | `pages.banner_image` | Yes |
| Projects | `/projects` | `pages.banner_image` | Yes |
| Equipment | `/equipment` | `pages.banner_image` | Yes |
| Team | `/team` | `pages.banner_image` | Yes |
| Gallery | `/gallery` | `pages.banner_image` | Yes |
| Careers | `/careers` | `pages.banner_image` | Yes |
| Contact | `/contact` | `pages.banner_image` | Yes |
| Request Quote | `/request-quote` | `pages.banner_image` | Yes |

Each page supports: hero background image, title, subtitle, overlay, breadcrumbs (except Home), and SEO/OG image via existing `render_page_seo`.

**Admin path:** `/admin/website/pages/<slug>` → **Hero Banner** panel → upload/select from Media Library → **Save Page**.

---

## Responsive Header Offsets

| Viewport | Top bar | Navbar | Logo | `--header-height` |
|----------|---------|--------|------|-------------------|
| Desktop ≥992px | 42px | 96px | 70px | 138px |
| Tablet 768–991px | hidden | 84px | 60px | 84px |
| Mobile <768px | hidden | 72px | 50px | 72px |

Scrolled states reduce navbar/logo height via existing `is-scrolled` behaviour.

---

## Remaining Recommendations

1. **Upload hero images** — Upload PNG/JPG/WEBP files in **Admin → Media → Upload** (folder: `content`), then assign per page in **Website CMS**. Until uploaded, pages show the brand gradient (no broken images).
2. **Clear legacy SVG paths** — If existing DB rows still reference `img/fallbacks/*.svg` for `banner_image`, replace them via the new Hero Banner picker.
3. **Equipment test slug** — `/equipment/motor-grader-cat-140` returns 404 (missing catalog record); not a UI defect.
4. **Manual device QA** — Confirm hero positioning on real phones/tablets after uploading production photography.

---

## Files Modified

```
static/css/main.css
static/css/home.css
static/css/admin-website.css
static/js/admin-website.js
templates/macros/media.html
templates/components/home/hero_slider.html
templates/components/page_builder/layouts/hero_banner.html
templates/components/page_builder/layouts/project_hero.html
templates/components/page_builder/layouts/equipment_hero.html
templates/components/page_builder/layouts/cta_banner.html
templates/components/ui/page_hero.html
templates/pages/home.html
templates/pages/about.html
templates/pages/services.html
templates/pages/projects.html
templates/pages/equipment.html
templates/pages/team.html
templates/pages/gallery.html
templates/pages/careers.html
templates/pages/contact.html
templates/pages/request_quote.html
templates/pages/project_detail.html
templates/pages/equipment_detail.html
templates/pages/career_detail.html
templates/admin/website/page_editor.html
templates/admin/website/_hero_banner_picker.html
app/constants/media.py
app/providers/placeholder.py
app/providers/website_admin_provider.py
app/services/website_admin_service.py
app/routes/admin/website.py
app/forms/website_forms.py
app/schemas/website_admin.py
docs/UI_UX_QA_REPORT.md
```

---

## Sign-Off

| Criteria | Status |
|----------|--------|
| Hero begins below header (all viewports) | ✅ |
| Logo sizes 70 / 60 / 50px | ✅ |
| Media Library hero images (PNG/JPG/WEBP) | ✅ |
| Per-page CMS hero management | ✅ |
| No architecture refactor | ✅ |
| Ready for deployment | ✅ (upload hero photos via CMS) |
