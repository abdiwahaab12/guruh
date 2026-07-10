# Pre-Admin Schema Migrations (Alembic-ready reference)

Revision: `001_pre_admin_schema`
Date: 2026-07-08

## Migration 1 — ContentBlock.extra

```python
def upgrade():
    op.add_column("content_blocks", sa.Column("extra", sa.JSON(), nullable=True))

def downgrade():
    op.drop_column("content_blocks", "extra")
```

## Migration 2 — JobListing.slug

```python
def upgrade():
    op.add_column("job_listings", sa.Column("slug", sa.String(150), nullable=True))
    # backfill slug from careers catalog / slugify(title)
    op.alter_column("job_listings", "slug", nullable=False)
    op.create_index("ix_job_listings_slug", "job_listings", ["slug"], unique=True)

def downgrade():
    op.drop_index("ix_job_listings_slug", table_name="job_listings")
    op.drop_column("job_listings", "slug")
```

## Migration 3 — Admin inbox / query indexes

```python
def upgrade():
    op.create_index("ix_contact_submissions_is_read_created_at", "contact_submissions", ["is_read", "created_at"])
    op.create_index("ix_quote_requests_is_read_created_at", "quote_requests", ["is_read", "created_at"])
    op.create_index("ix_audit_logs_resource_type_resource_id", "audit_logs", ["resource_type", "resource_id"])
    op.create_index("ix_login_history_user_id_created_at", "login_history", ["user_id", "created_at"])
    op.create_index("ix_projects_country_is_active", "projects", ["country", "is_active"])

def downgrade():
    op.drop_index("ix_projects_country_is_active", table_name="projects")
    op.drop_index("ix_login_history_user_id_created_at", table_name="login_history")
    op.drop_index("ix_audit_logs_resource_type_resource_id", table_name="audit_logs")
    op.drop_index("ix_quote_requests_is_read_created_at", table_name="quote_requests")
    op.drop_index("ix_contact_submissions_is_read_created_at", table_name="contact_submissions")
```

## Apply on existing databases

```bash
python init_db.py                      # fresh install (create_all)
python scripts/apply_pre_admin_migration.py   # existing DB upgrade
python seed_cms_blocks.py              # re-seed blocks with extra payload
```
