# MySQL Pre-Deployment Verification Report

**Date:** 8 July 2026  
**Database:** `guruh_construction` on MariaDB 10.4.32 (127.0.0.1)  
**Verdict:** ✅ **PASSED — MySQL production-ready**

---

## Root Cause of Reported Error

```
sqlite3.OperationalError: no such column: projects.country
```

| Finding | Detail |
|---------|--------|
| **Cause** | Application was connected to a **stale SQLite database** (`test_admin.db`) via shell `DATABASE_URL`, not MySQL |
| **Schema gap** | Old SQLite DBs created before `country`/`county` columns were added to the `Project` model |
| **Fix applied** | `.env` configured for MySQL; `migrate_projects_country()` added to pre-admin migration; `load_dotenv(override=True)` in `run.py` / `wsgi.py` |

---

## 1. SQLite References Found

| Location | Status | Action |
|----------|--------|--------|
| Shell `DATABASE_URL=sqlite:///.../test_admin.db` | ⚠️ Was overriding `.env` | Fixed: `.env` now takes precedence via `override=True` |
| `app/config.py` TestingConfig | ✅ Kept | SQLite only for automated testing (`:memory:`) |
| `app/utils/system_backup.py` | ✅ Kept | Backup utility supports both engines |
| `migrations/*.py` SQLITE_CREATE | ✅ Kept | Dual-dialect migration definitions |
| Documentation examples | ℹ️ Informational | Refer to MySQL for production |

**Runtime configuration after fix:**

```
DATABASE_ENABLED=true
DATABASE_URL=mysql+pymysql://root:@127.0.0.1/guruh_construction?charset=utf8mb4
Content provider: DatabaseContentProvider (MySQL)
```

---

## 2. MySQL Connection Status

| Check | Result |
|-------|--------|
| Server | MariaDB 10.4.32 via TCP/IP |
| Database | `guruh_construction` (utf8mb4_unicode_ci) |
| SQLAlchemy dialect | `mysql` |
| `SELECT 1` | ✅ OK |
| `DATABASE_ENABLED=true` | ✅ Switches to `DatabaseContentProvider` |

---

## 3. Tables Created (50/50)

All SQLAlchemy model tables verified present:

`about_sections`, `audit_logs`, `company_info`, `contact_*`, `content_blocks`, `content_block_items`, `cta_sections`, `equipment`, `equipment_details`, `footer_content`, `gallery_*`, `hero_slides`, `job_*`, `login_history`, `media_assets`, `nav_items`, `office_locations`, `page_sections`, `pages`, `partners`, `password_resets`, `permissions`, `process_steps`, `project_details`, `projects`, `quote_*`, `role_permissions`, `roles`, `section_headings`, `service_details`, `services`, `site_settings`, `social_links`, `statistics`, `team_*`, `testimonials`, `trust_badges`, `user_sessions`, `users`, `why_choose_us_*`, `working_process_sections`

**Critical schema check:** `projects.country` ✅ · `projects.county` ✅

---

## 4. Migrations Applied

| Migration | Status |
|-----------|--------|
| `init_db.py` (create_all) | ✅ Applied |
| `apply_pre_admin_migration.py` | ✅ Applied (includes new `country`/`county` columns) |
| `002_media_assets` | ✅ Applied |
| `003_project_details` | ✅ Applied |
| `004_service_details` | ✅ Applied |
| `005_equipment` | ✅ Applied |
| `006_team_details` | ✅ Applied |
| `007_gallery_details` | ✅ Applied |
| `008_job_listing_details` | ✅ Applied |
| `009_messages_inbox` | ✅ Applied |

**Setup command:** `python scripts/setup_mysql.py`  
**Apply migrations only:** `python scripts/apply_all_migrations.py`

---

## 5. Seed Data Imported

| Data | Count |
|------|-------|
| Roles | 7 |
| Permissions | 15 |
| Super admin user | 1 (`admin@guruh.com`) |
| Company info | 1 |
| Site settings | 42 keys |
| CMS content blocks | 224 |
| Page sections | 96 |

Catalog tables (projects, services, equipment, etc.) are **empty by design** — content is managed via admin UI. Public pages use placeholder fallback until catalog data is entered in admin.

---

## 6. Public Pages (MySQL)

| Route | Status |
|-------|--------|
| `/` | 200 ✅ |
| `/about` | 200 ✅ |
| `/services` | 200 ✅ |
| `/projects` | 200 ✅ |
| `/equipment` | 200 ✅ |
| `/gallery` | 200 ✅ |
| `/team` | 200 ✅ |
| `/careers` | 200 ✅ |
| `/testimonials` | 200 ✅ |
| `/contact` | 200 ✅ |
| `/request-quote` | 200 ✅ |
| `/health` | 200 ✅ |

---

## 7. Admin Modules & Tests

**16/16 test suites PASSED** against MySQL:

`test_auth`, `test_careers`, `test_dashboard`, `test_equipment`, `test_gallery`, `test_media`, `test_messages`, `test_projects`, `test_public`, `test_reports`, `test_services`, `test_settings`, `test_system`, `test_team`, `test_users`, `test_website`

---

## 8. Fixes Applied (Minimum Safe Changes)

| File | Change |
|------|--------|
| `.env` | Created with MySQL production config |
| `.env.example` | Updated defaults to MySQL + `DATABASE_ENABLED=true` |
| `scripts/apply_pre_admin_migration.py` | Added `migrate_projects_country()` for legacy schemas |
| `scripts/apply_all_migrations.py` | **New** — runs all migrations in order |
| `scripts/setup_mysql.py` | **New** — create DB + init + migrate + seed |
| `scripts/verify_mysql.py` | **New** — full verification report |
| `run.py` / `wsgi.py` | `load_dotenv(override=True)` — `.env` wins over stale shell vars |
| `scripts/test_release.py` | Loads `.env`; no longer defaults to SQLite |

**No architecture changes. No UI changes. No model changes.**

---

## 9. Remaining Deployment Blockers

| Priority | Item | Owner |
|----------|------|-------|
| **P0** | Change `SECRET_KEY` and `ADMIN_PASSWORD` in `.env` | DevOps |
| **P0** | Set MySQL root password on production server (currently empty on local XAMPP) | DevOps |
| **P1** | Populate catalog content via admin (projects, services, etc.) | Content team |
| **P1** | Unset stale `DATABASE_URL` in deployment shell/CI if set to SQLite | DevOps |
| **P2** | Add `robots.txt` / `sitemap.xml` at web server | DevOps |

---

## 10. How to Reproduce Verification

```bash
# One-time MySQL setup
python scripts/setup_mysql.py

# Full verification (schema + pages + 16 test suites)
python scripts/verify_mysql.py

# Start application (uses .env MySQL config)
python run.py
```

Admin login: `admin@guruh.com` / password from `.env`

---

*End of MySQL Pre-Deployment Verification Report*
