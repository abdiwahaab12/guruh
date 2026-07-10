# Release Notes — v1.0.0

**Release date:** July 2026  
**Codename:** Enterprise CMS  
**Status:** Production Ready

---

## Overview

GURUH CMS v1.0.0 is the first production release of the enterprise website and content management platform for GURUH Construction Company Limited. It delivers a fully dynamic public website, a comprehensive admin CMS, role-based access control, analytics, and system administration tools.

---

## Public Website

- **12 public routes** including detail pages for projects, equipment, and careers
- Dynamic Page Builder with reusable CMS blocks
- Bootstrap 5 responsive design
- SEO: canonical URLs, Open Graph, Twitter Cards, JSON-LD (Organization, BreadcrumbList, FAQ, JobPosting, etc.)
- Accessibility: skip links, main landmarks, focus-visible states, ARIA on interactive components
- Performance: font preconnect, hero LCP preload, lazy-loaded images via media macro, deferred JS

---

## Admin CMS Modules (Steps 14–27)

| Step | Module |
|------|--------|
| 14 | Admin Dashboard Foundation |
| 15 | Website Settings |
| 16 | Media Library |
| 17 | Projects Management |
| 18 | Services Management |
| 19 | Equipment Management |
| 20 | Team Management |
| 21 | Gallery Management |
| 22 | Careers Management |
| 23 | Website CMS & Page Builder |
| 24 | Messages / Inbox |
| 25 | Users & RBAC |
| 26 | Reports & Analytics |
| 27 | System Administration |

---

## Authentication & Security

- Flask-Login session management with idle timeout (30 min)
- CSRF protection on all admin forms (Flask-WTF)
- Account lockout after failed login attempts
- Password reset flow with expiring tokens
- RBAC with 7 roles and 15 permissions
- Super Admin gate for Users and System modules
- Full audit trail on admin actions

---

## Reports & Analytics (Step 26)

- Overview dashboard with 8 stat cards and 5 charts
- Date filters and CSV/Excel/PDF export
- Audit reports: User, Login, System activity

---

## System Administration (Step 27)

- System health dashboard
- Maintenance mode control
- Database backup create/download/restore
- Health checks (DB, filesystem, uploads, media, app)
- Application, error, and audit log viewer
- Storage metrics and cache management

---

## Technology Stack

- Python 3.11+, Flask 3, SQLAlchemy, Flask-Login, Flask-WTF
- Bootstrap 5.3, Bootstrap Icons, Chart.js (admin reports)
- MySQL 8 (production) / SQLite (dev)
- openpyxl + reportlab (report exports)

---

## Known limitations (v1.0.0)

1. **Maintenance mode** — UI exists; public-site enforcement middleware not yet active (configure at deploy)
2. **Sitemap / robots.txt** — not served at root; configure at web server or add in post-release patch
3. **Placeholder content** — used when `DATABASE_ENABLED=false`; enable MySQL for live CMS data
4. **MySQL restore** — SQL restore executes INSERT statements; full mysqldump restore recommended for large DBs

---

## Upgrade path

Future v1.0.x patches will address known limitations without architectural changes.

---

## Test coverage

16 automated smoke test suites including:
- `test_public.py` — all public pages + SEO markers
- `test_release.py` — master runner (all modules)
- Per-module tests for auth, dashboard, settings, media, catalog, messages, users, reports, system

---

## Credits

Built for GURUH Construction Company Limited — Enterprise CMS Development Program (Steps 1–28).
