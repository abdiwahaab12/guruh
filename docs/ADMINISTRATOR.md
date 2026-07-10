# Administrator Guide

Guide for site managers using the GURUH CMS admin panel.

## Signing in

1. Go to `/admin/login`
2. Enter email and password
3. Sessions expire after **30 minutes** of inactivity (configurable)

If locked out after failed attempts, wait 15 minutes or contact a Super Admin.

## Roles and permissions

| Role | Typical access |
|------|----------------|
| Super Admin | Everything including Users, System |
| Administrator | All content, settings, reports |
| Content Manager | Pages, services, projects, gallery, equipment |
| HR Manager | Careers, team, job applications |
| Project Manager | Projects, equipment |
| Media Manager | Gallery, media library |
| Viewer | Read-only dashboard and reports |

Your sidebar shows only modules you can access.

## Content workflow

### Website pages
**Content → Pages** (`/admin/website`)
- Edit page metadata, sections, and CMS blocks
- Preview before publishing
- Manage SEO per page

### Catalog modules
Each module follows the same pattern:
1. **Dashboard** — stats and recent items
2. **List** — search, filter, bulk actions
3. **Create/Edit** — form with media picker and SEO fields

Modules: Projects, Services, Equipment, Gallery, Team, Careers

### Media library
**Media** (`/admin/media`)
- Upload images, videos, documents
- Organize by folder and type
- Reuse assets across all modules

## Messages inbox

**Messages** (`/admin/messages`)
- **Contact Messages** — general enquiries
- **Quote Requests** — project quote form submissions
- **Job Applications** — career applications

Mark as read, add notes, change status, export if needed.

## Website settings

**Settings** (`/admin/settings`)
- Company info, contact, offices
- SEO defaults, social links
- Email (SMTP), maps, theme, analytics
- Maintenance mode (also manageable under **System**)

## Reports

**Reports** (`/admin/reports`) — requires `view_reports` permission
- Overview statistics and charts
- Date filters: Today, Week, Month, Year, Custom
- Export CSV, Excel, PDF
- Audit report tabs

## Users & RBAC (Super Admin only)

**Users & RBAC** (`/admin/users`)
- Create/edit users, assign roles
- Manage role permissions
- View sessions, login history, audit logs

## System administration (Super Admin only)

**System** (`/admin/system`)
- **Dashboard** — health overview
- **Maintenance** — enable/disable public site maintenance
- **Backup** — create, download, restore database backups
- **Health Check** — database, filesystem, uploads, media, app
- **Logs** — application, error, audit logs
- **Storage** — disk and database usage
- **Cache** — clear or rebuild file cache

> **Important**: Backup restore overwrites data. Type `RESTORE` to confirm.

## Best practices

1. Change default admin password immediately
2. Use strong passwords (minimum 8 characters)
3. Assign least-privilege roles
4. Create backups before major content changes
5. Review Messages and Reports weekly
6. Keep media files optimized before upload

## Support

For technical issues, contact your development team with:
- Steps to reproduce
- Screenshot of error
- User role and module affected
