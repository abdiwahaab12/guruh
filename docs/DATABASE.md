# Database Guide

## Overview

GURUH CMS uses **SQLAlchemy** with **Flask-SQLAlchemy**. Schema is defined in `app/models/`.

Production target: **MySQL 8.0+** (`utf8mb4`). Development/QA: **SQLite**.

## Initial setup

```bash
python init_db.py          # db.create_all() — all models
python scripts/seed_auth.py   # roles, permissions, super admin
```

## Connection string

```
mysql+pymysql://USER:PASSWORD@HOST:3306/DATABASE
```

Set in `.env` as `DATABASE_URL`. Enable with `DATABASE_ENABLED=true`.

Engine options (in `app/config.py`):
- `pool_pre_ping=True` — reconnect stale connections
- `pool_recycle=300` — recycle connections every 5 minutes

## Core tables

### Authentication & RBAC
| Table | Model | Purpose |
|-------|-------|---------|
| `users` | `User` | Admin accounts |
| `roles` | `Role` | Role definitions |
| `permissions` | `Permission` | Permission slugs |
| `role_permissions` | association | Role ↔ Permission |
| `user_sessions` | `UserSession` | Active sessions |
| `login_history` | `LoginHistory` | Login attempts |
| `audit_logs` | `AuditLog` | Admin action audit trail |
| `password_resets` | `PasswordReset` | Reset tokens |

### Site & CMS
| Table | Model | Purpose |
|-------|-------|---------|
| `site_settings` | `SiteSetting` | Key-value settings |
| `company_info` | `CompanyInfo` | Company profile |
| `office_locations` | `OfficeLocation` | Office addresses |
| `pages` | `Page` | CMS pages |
| `page_sections` | `PageSection` | Page sections |
| `content_blocks` | `ContentBlock` | Block instances |

### Catalog
| Table | Model | Purpose |
|-------|-------|---------|
| `projects` / `project_details` | `Project` | Portfolio |
| `services` / `service_details` | `Service` | Services |
| `equipment` | `Equipment` | Equipment fleet |
| `gallery_images` / `gallery_details` | `GalleryImage` | Gallery |
| `team_members` / `team_details` | `TeamMember` | Team |
| `job_listings` / `job_listing_details` | `JobListing` | Careers |

### Messages
| Table | Model | Purpose |
|-------|-------|---------|
| `contact_submissions` | `ContactSubmission` | Contact form |
| `quote_requests` | `QuoteRequest` | Quote form |
| `job_applications` | `JobApplication` | Job applications |

### Media
| Table | Model | Purpose |
|-------|-------|---------|
| `media_assets` | `MediaAsset` | Central media library |

## Migrations

Incremental migration scripts in `migrations/`:

| Script | Description |
|--------|-------------|
| `001_pre_admin_schema.py` | Base schema |
| `002_media_assets.py` | Media library |
| `003_project_details.py` | Project extended fields |
| `004_service_details.py` | Service extended fields |
| `005_equipment.py` | Equipment module |
| `006_team_details.py` | Team extended fields |
| `007_gallery_details.py` | Gallery albums/types |
| `008_job_listing_details.py` | Career listing status |
| `009_messages_inbox.py` | Message detail tables |

Run manually when upgrading existing databases:

```bash
python migrations/00N_script.py
```

New installs can use `init_db.py` alone.

## Seeding

| Script | Purpose |
|--------|---------|
| `scripts/seed_auth.py` | Roles, permissions, super admin user |

Content seeding is done via admin UI or future import tools.

## Backups

- **SQLite**: file copy of `.db` file
- **MySQL**: `mysqldump` (preferred) or SQLAlchemy export via System Admin
- Backups stored in `instance/backups/`

Restore via Admin → System → Backup (Super Admin only).

## Performance notes

- Indexes on foreign keys and frequently filtered columns (`slug`, `is_active`, `created_at`)
- Use pagination in admin list views (default 20 per page)
- Media file sizes tracked in `media_assets.file_size`
- Connection pooling enabled for MySQL

## Security

- All admin writes go through SQLAlchemy ORM (parameterized queries)
- No raw user input in SQL except controlled health-check `SELECT 1`
- Passwords hashed with werkzeug/security (via auth provider)
