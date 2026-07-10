# Deployment Guide

## Pre-deployment checklist

- [ ] `FLASK_ENV=production`
- [ ] Strong `SECRET_KEY` set (never commit to git)
- [ ] `ADMIN_PASSWORD` changed from default
- [ ] MySQL configured with `DATABASE_ENABLED=true`
- [ ] SSL/TLS certificate installed (HTTPS)
- [ ] Static files served efficiently (see below)
- [ ] Media upload directory writable
- [ ] Backups scheduled via `/admin/system`
- [ ] Error/application logs monitored
- [ ] `robots.txt` and `sitemap.xml` configured at CDN/web server (recommended)

## Environment variables (production)

```env
FLASK_ENV=production
SECRET_KEY=<generate-with-secrets.token_hex(32)>
DATABASE_ENABLED=true
DATABASE_URL=mysql+pymysql://USER:PASSWORD@HOST/DATABASE
ADMIN_EMAIL=admin@yourdomain.com
ADMIN_PASSWORD=<strong-password>
SESSION_IDLE_TIMEOUT_MINUTES=30
MAX_LOGIN_ATTEMPTS=5
MEDIA_UPLOAD_ROOT=uploads
MEDIA_MAX_FILE_SIZE=20971520
```

## Gunicorn (Linux / VPS)

```bash
pip install gunicorn
export FLASK_ENV=production
gunicorn -w 4 -b 127.0.0.1:8000 --timeout 120 wsgi:app
```

Recommended systemd unit:

```ini
[Unit]
Description=GURUH CMS
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/guruh-cms
EnvironmentFile=/var/www/guruh-cms/.env
ExecStart=/var/www/guruh-cms/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

## Nginx reverse proxy

```nginx
server {
    listen 443 ssl http2;
    server_name www.guruh.com;

    ssl_certificate     /etc/ssl/certs/guruh.crt;
    ssl_certificate_key /etc/ssl/private/guruh.key;

    location /static/ {
        alias /var/www/guruh-cms/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable gzip/brotli compression in Nginx for CSS, JS, and HTML.

## Passenger (cPanel / shared hosting)

1. Upload project to `~/guruh-cms`
2. Create Python app in cPanel pointing to project root
3. Set startup file to `wsgi.py` (or copy/symlink as `passenger_wsgi.py`)
4. Set `FLASK_ENV=production` in cPanel environment variables
5. Run `pip install -r requirements.txt` in virtualenv
6. Run `python init_db.py` and `python scripts/seed_auth.py` via SSH

## Static and media files

| Path | Purpose |
|------|---------|
| `static/` | CSS, JS, images, compiled assets |
| `static/uploads/` | User-uploaded media (configurable via `MEDIA_UPLOAD_ROOT`) |
| `instance/` | Cache, backups, logs (not in git) |

Ensure `instance/` and `static/uploads/` are writable by the web server user.

## SSL

- Terminate TLS at Nginx/Apache or load balancer
- Set secure cookies automatically when `FLASK_ENV=production` (`SESSION_COOKIE_SECURE=true`)
- Force HTTPS redirect at web server level

## Logging

Application logs are written to `instance/logs/` when actions occur via System Administration.

Configure web server access/error logs separately. Monitor:
- `instance/logs/application.log`
- `instance/logs/error.log`
- Admin → System → Logs

## Backups

1. **Automated**: Schedule cron to call admin backup or mysqldump
2. **Manual**: Admin → System → Backup → Create Backup
3. Store backups off-server (S3, NAS)
4. Test restore in staging before relying on backups

## Health monitoring

- `GET /health` → `200 OK` (load balancer probe)
- Admin → System → Health Check (full diagnostics)

## Post-deploy smoke test

```bash
curl -I https://www.guruh.com/health
python scripts/test_public.py   # against staging URL if configured
```

Sign in to admin and verify Dashboard, Messages, Reports, System modules load.
