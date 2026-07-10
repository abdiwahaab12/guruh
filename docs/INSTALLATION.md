# Installation Guide

## Requirements

- Python 3.11+
- pip
- MySQL 8.0+ (production) or SQLite (development)
- Git

## 1. Clone and virtual environment

```bash
git clone <repository-url> guruh-cms
cd guruh-cms
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate     # Linux/macOS
pip install -r requirements.txt
```

## 2. Environment configuration

```bash
copy .env.example .env       # Windows
# cp .env.example .env         # Linux/macOS
```

Edit `.env`:

| Variable | Development | Production |
|----------|-------------|------------|
| `FLASK_ENV` | `development` | `production` |
| `SECRET_KEY` | any string | **strong random 32+ chars** |
| `DATABASE_ENABLED` | `false` (placeholder data) | `true` |
| `DATABASE_URL` | SQLite or MySQL URI | MySQL URI |
| `ADMIN_EMAIL` / `ADMIN_PASSWORD` | defaults | **change immediately** |

## 3. Database setup

### SQLite (development / QA)

```bash
set DATABASE_URL=sqlite:///guruh_dev.db
python init_db.py
python scripts/seed_auth.py
```

### MySQL (production)

```sql
CREATE DATABASE guruh_construction CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'guruh'@'localhost' IDENTIFIED BY 'strong-password';
GRANT ALL PRIVILEGES ON guruh_construction.* TO 'guruh'@'localhost';
FLUSH PRIVILEGES;
```

```bash
set DATABASE_URL=mysql+pymysql://guruh:strong-password@localhost/guruh_construction
set DATABASE_ENABLED=true
python init_db.py
python scripts/seed_auth.py
```

Apply incremental migrations if upgrading:

```bash
python migrations/002_media_assets.py
# … through 009_messages_inbox.py
```

## 4. Run development server

```bash
python run.py
```

- Public site: http://127.0.0.1:5000
- Admin: http://127.0.0.1:5000/admin
- Health check: http://127.0.0.1:5000/health

## 5. Verify installation

```bash
python scripts/test_public.py
python scripts/test_auth.py
python scripts/test_release.py
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `SECRET_KEY required in production` | Set `SECRET_KEY` in `.env` when `FLASK_ENV=production` |
| MySQL connection refused | Check `DATABASE_URL`, firewall, MySQL service |
| Admin 403 | Ensure user role has required permissions; super admin for Users/System |
| CSRF errors on forms | Ensure cookies enabled; session not expired |
