# Developer Guide

## Project layout

```
app/
├── constants/       # Module tabs, RBAC, settings keys
├── forms/           # Flask-WTF forms
├── models/          # SQLAlchemy models
├── providers/       # Data access layer
├── routes/          # Blueprints (main + admin/*)
├── schemas/         # Dataclass DTOs
├── services/        # Business logic
└── utils/           # Helpers (permissions, export, cache)
templates/
├── admin/           # Admin module templates
├── components/      # Page builder blocks
├── macros/          # Reusable Jinja macros
├── pages/           # Public page templates
└── partials/        # Header, footer, etc.
static/              # CSS, JS, images, uploads
scripts/             # Smoke tests, seeds, migrations
migrations/          # Incremental SQL migrations
docs/                # Documentation
```

## Conventions

### Adding admin functionality (pattern established Steps 14–27)

1. `app/constants/{module}_admin.py` — tabs, actions
2. `app/schemas/{module}_admin.py` — DTOs
3. `app/providers/{module}_admin_provider.py` — queries, audit wrapper
4. `app/services/{module}_admin_service.py` — shell context, actions
5. `app/forms/{module}_forms.py` — WTForms (if needed)
6. `app/routes/admin/{module}.py` — `register_{module}_routes(admin_bp)`
7. `templates/admin/{module}/` — layout + dashboard + tabs
8. `static/css/admin-{module}.css` — module styles
9. Register in `app/routes/admin/__init__.py`
10. Add nav item in `app/constants/admin_nav.py`
11. Add `scripts/test_{module}.py`

### Permissions

```python
from app.utils.permissions import permission_required, super_admin_required

@can_manage_projects
def projects_dashboard(): ...

@super_admin_required
def system_dashboard(): ...
```

Define slugs in `app/constants/rbac.py`.

### Audit logging

```python
AuthProvider.record_audit_event(
    user_id=current_user.id,
    action="module.action",
    resource_type="entity",
    resource_id="123",
    details="Human-readable detail",
    ip_address=request.remote_addr,
)
AuthProvider.commit()
```

### Content provider toggle

- `DATABASE_ENABLED=false` → placeholder data from `app/data/`
- `DATABASE_ENABLED=true` → MySQL via providers

## Testing

```bash
set DATABASE_URL=sqlite:///test_admin.db
python scripts/test_release.py     # all suites
python scripts/test_public.py      # public pages only
```

Tests use Flask test client with CSRF extraction from login forms.

## Code style

- Minimize route logic — delegate to services
- Reuse existing providers rather than duplicating queries
- DTOs for all template context (dataclasses in `schemas/`)
- No business logic in templates
- Bootstrap 5 utility classes; module-specific CSS in `static/css/admin-*.css`

## Local development tips

```bash
FLASK_ENV=development python run.py
```

- Placeholder content works without MySQL
- Admin login: seed with `python scripts/seed_auth.py`
- Test DB: SQLite file avoids MySQL dependency

## Key dependencies

| Package | Purpose |
|---------|---------|
| Flask | Web framework |
| Flask-SQLAlchemy | ORM |
| Flask-Login | Session auth |
| Flask-WTF | Forms + CSRF |
| PyMySQL | MySQL driver |
| openpyxl | Excel export (Reports) |
| reportlab | PDF export (Reports) |

## Extension points

- **New public page**: Route in `main.py` → Service → Template (avoid hardcoding content)
- **New CMS block**: `app/data/cms_blocks.py` + page builder layout template
- **New RBAC permission**: `rbac.py` → seed script → decorator on routes

Do not bypass the Route → Service → Provider pattern.
