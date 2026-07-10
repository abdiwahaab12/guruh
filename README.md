# GURUH Construction CMS — v1.0.0

Enterprise website and content management system for **GURUH Construction Company Limited**.

Built with **Flask 3**, **Bootstrap 5**, **SQLAlchemy**, and **MySQL** (SQLite supported for development/testing).

## Features

### Public Website
- Dynamic pages: Home, About, Services, Projects, Equipment, Gallery, Team, Careers, Testimonials, Contact, Request Quote
- Page Builder with reusable CMS blocks
- SEO: canonical URLs, Open Graph, Twitter Cards, JSON-LD structured data
- Accessible layout with skip links, ARIA landmarks, keyboard focus states

### Admin CMS (28 modules)
| Module | Route | Access |
|--------|-------|--------|
| Dashboard | `/admin` | Authenticated |
| Website CMS | `/admin/website` | `manage_pages` |
| Projects | `/admin/projects` | `manage_projects` |
| Services | `/admin/services` | `manage_services` |
| Equipment | `/admin/equipment` | `manage_equipment` |
| Gallery | `/admin/gallery` | `manage_gallery` |
| Team | `/admin/team` | `manage_team` |
| Careers | `/admin/careers` | `manage_careers` |
| Messages | `/admin/messages` | Contacts / Quotes / Applications |
| Media | `/admin/media` | `manage_media` |
| Settings | `/admin/settings` | `manage_settings` |
| Users & RBAC | `/admin/users` | Super Admin |
| Reports | `/admin/reports` | `view_reports` |
| System | `/admin/system` | Super Admin |

## Architecture

```
Request → Route → Service → Provider → Model / DTO → Template
```

- **Routes** — thin HTTP controllers (`app/routes/`)
- **Services** — business logic (`app/services/`)
- **Providers** — data access (`app/providers/`)
- **Schemas** — DTOs (`app/schemas/`)
- **Models** — SQLAlchemy (`app/models/`)
- **Templates** — Jinja2 (`templates/`)

## Quick Start

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env
python init_db.py
python scripts/seed_auth.py
python run.py
```

Visit **http://127.0.0.1:5000** · Admin: **http://127.0.0.1:5000/admin**

Default super admin (change in production): `admin@guruh.com` / see `.env`

## Documentation

| Guide | Description |
|-------|-------------|
| [Installation](docs/INSTALLATION.md) | Local setup, dependencies, database |
| [Deployment](docs/DEPLOYMENT.md) | Production, Gunicorn, Passenger, SSL |
| [Administrator](docs/ADMINISTRATOR.md) | CMS usage for site managers |
| [Developer](docs/DEVELOPER.md) | Code structure, conventions, testing |
| [Database](docs/DATABASE.md) | Schema, migrations, seeding |
| [Release Notes v1.0.0](docs/RELEASE_NOTES_v1.0.0.md) | What's included in this release |
| [Production Report](docs/PRODUCTION_REPORT.md) | Final QA audit (Step 28) |

## Testing

```bash
# Full release QA suite
set DATABASE_URL=sqlite:///test_admin.db
python scripts/test_release.py

# Individual suites
python scripts/test_public.py
python scripts/test_auth.py
```

## Production Deployment (Namecheap / GitHub)

**cPanel Python app startup file:** `passenger_wsgi.py` (application callable: `application`)

```bash
# On the server after git clone / deploy:
cp .env.production .env
# Edit .env — set SECRET_KEY, DB_PASSWORD, ADMIN_PASSWORD (never commit .env)

python init_db.py
python scripts/seed_auth.py
```

**Required production environment:**

```env
FLASK_ENV=production
SECRET_KEY=<strong-random-key>
DATABASE_ENABLED=true
DATABASE_URL=mysql+pymysql://USER:PASSWORD@localhost/DATABASE?charset=utf8mb4
```

Or use `DB_HOST`, `DB_USER`, `DB_NAME`, `DB_PASSWORD` (recommended when password contains `@`).

See [Deployment Guide](docs/DEPLOYMENT.md) for the full Namecheap checklist.

## License

Proprietary — GURUH Construction Company Limited.
