# GURUH Construction — Public Website Production QA Report

**Date:** 8 July 2026  
**Scope:** Full public website review (14 page types, 16+ routes)  
**Status:** All blocking issues fixed — ready for Admin Dashboard phase (pending approval)

---

## Pages Reviewed

| Page | Route | Status |
|------|-------|--------|
| Home | `/` | ✅ Pass |
| About | `/about` | ✅ Pass |
| Services | `/services` | ✅ Pass (service details via in-page anchors `#service-{slug}`) |
| Service Detail | `/services#service-{slug}` | ✅ Pass (embedded sections, no separate URL by design) |
| Projects | `/projects` | ✅ Pass |
| Project Detail | `/projects/{slug}` | ✅ Pass |
| Equipment | `/equipment` | ✅ Pass |
| Equipment Detail | `/equipment/{slug}` | ✅ Pass |
| Team | `/team` | ✅ Pass |
| Careers | `/careers` | ✅ Pass |
| Job Detail | `/careers/{slug}` | ✅ Pass |
| Gallery | `/gallery` | ✅ Pass |
| Contact | `/contact` | ✅ Pass |
| Request Quote | `/request-quote` | ✅ Pass |

**Automated audit:** `python scripts/qa_audit.py` — **16 routes, 0 issues** after fixes.

---

## Issues Found & Resolutions

### 1. SEO — Duplicate BreadcrumbList Schema (Fixed)

**Severity:** High  
**Pages affected:** Contact, Careers, Gallery, Request Quote, Career Detail  

**Issue:** `render_page_seo` emitted a standalone `BreadcrumbList` JSON-LD script while the same pages also included `BreadcrumbList` inside their `@graph` block — duplicate structured data.

**Fix:** Added `breadcrumb_ld` parameter to `render_page_seo` (default `True`). Pages with `@graph` breadcrumbs now pass `breadcrumb_ld=False`.

**Files:** `templates/macros/page_layout.html`, `contact.html`, `careers.html`, `gallery.html`, `request_quote.html`, `career_detail.html`

---

### 2. SEO — Hardcoded Country in Services Schema (Fixed)

**Severity:** Medium  
**Page:** Services  

**Issue:** JSON-LD `areaServed` was hardcoded to `"Kenya"` while company contact/address uses Somalia.

**Fix:** Replaced with `company.address_country` from DTO. Updated `telephone` to `company.phone_primary`.

**Files:** `templates/pages/services.html`

---

### 3. SEO — Inconsistent Telephone in JSON-LD (Fixed)

**Severity:** Low  
**Pages:** Team, Project Detail, Services  

**Issue:** Schema used `company.phone` (display string with optional secondary number) instead of normalized `phone_primary`.

**Fix:** Standardized to `company.phone_primary` in JSON-LD.

**Files:** `templates/pages/team.html`, `project_detail.html`, `services.html`

---

### 4. Security — Forms Missing CSRF Preparation (Fixed)

**Severity:** High  
**Pages:** Contact, Request Quote, Careers (job apply)  

**Issue:** POST forms had no CSRF token placeholder for future Flask-WTF / MySQL integration.

**Fix:** Added to `render_dynamic_form` and `render_multistep_form`:
- Hidden `csrf_token` field with `data-csrf-token`
- `data-csrf-ready="true"` and `data-sanitize-ready="true"` on forms
- `data-upload-ready="true"` on file inputs

**Files:** `templates/macros/forms.html`

---

### 5. Architecture / Data — Services Page Missing Context (Fixed)

**Severity:** Medium  
**Page:** Services  

**Issue:** `render_page_sections()` was called with positional `projects` only; `services` list was not passed to layouts (service-detail sections use `projects` for typical project links — `services` param was omitted for future layout use).

**Fix:** Explicit keyword args: `projects=projects, services=services`.

**Files:** `templates/pages/services.html`

---

### 6. UI Consistency — Page Builder CSS Variables (Fixed)

**Severity:** Low  
**Pages:** Equipment, Team  

**Issue:** `.page-equipment` and `.page-team` were missing from the shared Page Builder CSS custom-property shell (spacing tokens).

**Fix:** Added to the root selector group in `page-builder.css`.

**Files:** `static/css/page-builder.css`

---

### 7. Accessibility — Areas Map Hardcoded Country Label (Fixed)

**Severity:** Low  
**Pages:** About, Projects (areas map section)  

**Issue:** Map placeholder used hardcoded "Kenya" in ARIA label and visible text.

**Fix:** Dynamic label from `company.address_country` via global context processor.

**Files:** `templates/components/page_builder/layouts/areas_map.html`

---

### 8. Production Quality — Dead Template Removed (Fixed)

**Severity:** Low  

**Issue:** `templates/components/catalog/gallery_item.html` was unused after Gallery Page Builder migration (legacy single-page grid).

**Fix:** Removed unused file.

---

## Content Debt (Documented — Not Changed)

These items were **not modified** to avoid unauthorized content redesign. Recommend resolving during Admin Dashboard / CMS content entry:

| Item | Notes |
|------|-------|
| **Kenya vs Somalia in seed CMS data** | Contact block uses Mogadishu, Somalia; company profile PDF seed data (about, projects counties, certifications) still references Kenya/NCA Kenya. Requires business confirmation before bulk CMS update. |
| **Legacy `Arsha/` theme folder** | Original Bootstrap theme assets at repo root — not served by Flask app. Safe to archive/remove in a future cleanup commit. |
| **`/testimonials` route** | Legacy simple page exists but is not in the primary nav Page Builder set. Functional; not part of this QA scope. |
| **Service detail URLs** | Services use in-page anchor sections (`#service-{slug}`), not `/services/{slug}`. By Page Builder design — SEO uses fragment URLs in ItemList schema. |

---

## Review Checklist Summary

### UI Consistency ✅
Shared design system via `main.css`, `sections-shared.css`, `page-builder.css`, and page-specific shells. Bootstrap 5, Inter typography, brand CSS variables, premium cards, consistent hero/CTA patterns.

### Responsive Design ✅
Bootstrap 5 grid, clamp-based section spacing, mobile form/button rules in page CSS, gallery masonry breakpoints, quote stepper grid.

### Accessibility ✅
Skip link, `#main-content` landmark, focus-visible styles, ARIA on filters/forms/lightbox/stepper, semantic headings (single H1 per page via hero banner), form labels and error regions.

### Performance ✅
Lazy loading via `smart_image` macro, hero LCP preload on key pages, deferred JS, SVG fallbacks (no broken images), no duplicate Bootstrap/JS loads.

### SEO ✅
Canonical, Open Graph, Twitter Cards, JSON-LD (WebPage, Organization, BreadcrumbList, page-specific types), meta descriptions, breadcrumb UI + schema.

### Security ✅
Client-side validation, CSRF/upload/sanitize preparation attributes, `safe_href` filter on CMS URLs, no form submission until backend connected.

### Production Quality ✅
Route → Service → Provider → DTO architecture intact. Automated QA script added at `scripts/qa_audit.py`.

---

## Files Changed in QA Pass

- `templates/macros/page_layout.html`
- `templates/macros/forms.html`
- `templates/pages/contact.html`
- `templates/pages/careers.html`
- `templates/pages/career_detail.html`
- `templates/pages/gallery.html`
- `templates/pages/request_quote.html`
- `templates/pages/services.html`
- `templates/pages/team.html`
- `templates/pages/project_detail.html`
- `templates/components/page_builder/layouts/areas_map.html`
- `static/css/page-builder.css`
- `scripts/qa_audit.py` (new)
- `templates/components/catalog/gallery_item.html` (removed)

---

## Verification

```bash
cd C:\Users\cabdi\Downloads\Arsha
.\venv\Scripts\activate
python scripts/qa_audit.py
python run.py
```

All 16 audited public routes return HTTP 200 with canonical, Open Graph, Twitter Cards, JSON-LD, single BreadcrumbList, single H1, and form security markers.

**Recommendation:** Proceed to Admin Dashboard after stakeholder approval of this QA report and content debt items.
