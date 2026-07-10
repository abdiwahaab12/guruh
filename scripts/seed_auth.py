"""
Seed RBAC roles, permissions, and default super admin user.

Run after database tables are created:
    python init_db.py
    python scripts/seed_auth.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.extensions import db
from app.models.auth import Permission, Role, RolePermission, User

import app.models  # noqa: F401 — register all models before run import
from run import app
from app.constants.rbac import (
    ALL_PERMISSIONS,
    PERMISSION_LABELS,
    ROLE_DEFINITIONS,
    ROLE_PERMISSIONS,
    ROLE_SUPER_ADMIN,
)


def seed_permissions() -> dict[str, Permission]:
    """Create or update permission records."""
    by_slug: dict[str, Permission] = {}
    for slug in ALL_PERMISSIONS:
        permission = Permission.query.filter_by(slug=slug).first()
        if not permission:
            permission = Permission(
                slug=slug,
                name=PERMISSION_LABELS.get(slug, slug.replace("_", " ").title()),
                description=f"Allows {PERMISSION_LABELS.get(slug, slug).lower()}.",
            )
            db.session.add(permission)
        else:
            permission.name = PERMISSION_LABELS.get(slug, permission.name)
            permission.is_active = True
        by_slug[slug] = permission
    db.session.flush()
    return by_slug


def seed_roles(permissions_by_slug: dict[str, Permission]) -> dict[str, Role]:
    """Create or update role records and role-permission mappings."""
    by_slug: dict[str, Role] = {}
    for role_def in ROLE_DEFINITIONS:
        role = Role.query.filter_by(slug=role_def["slug"]).first()
        if not role:
            role = Role(
                slug=role_def["slug"],
                name=role_def["name"],
                description=role_def["description"],
            )
            db.session.add(role)
        else:
            role.name = role_def["name"]
            role.description = role_def["description"]
            role.is_active = True
        by_slug[role_def["slug"]] = role

    db.session.flush()

    for role_slug, permission_slugs in ROLE_PERMISSIONS.items():
        role = by_slug[role_slug]
        existing = {rp.permission.slug for rp in role.role_permissions}
        for perm_slug in permission_slugs:
            if perm_slug in existing:
                continue
            permission = permissions_by_slug.get(perm_slug)
            if permission:
                db.session.add(RolePermission(role_id=role.id, permission_id=permission.id))

    db.session.flush()
    return by_slug


def seed_super_admin(roles_by_slug: dict[str, Role]) -> User | None:
    """Create default super admin if no users exist."""
    admin_email = app.config["ADMIN_EMAIL"].lower().strip()
    existing = User.query.filter_by(email=admin_email).first()
    if existing:
        print(f"Super admin already exists: {admin_email}")
        return existing

    super_admin_role = roles_by_slug.get(ROLE_SUPER_ADMIN)
    if not super_admin_role:
        print("Super Admin role not found — aborting user seed.")
        return None

    user = User(
        email=admin_email,
        first_name=app.config["ADMIN_FIRST_NAME"],
        last_name=app.config["ADMIN_LAST_NAME"],
        role_id=super_admin_role.id,
        is_active=True,
    )
    user.set_password(app.config["ADMIN_PASSWORD"])
    db.session.add(user)
    db.session.flush()
    print(f"Created super admin: {admin_email}")
    return user


def seed_auth() -> None:
    with app.app_context():
        permissions = seed_permissions()
        roles = seed_roles(permissions)
        seed_super_admin(roles)
        db.session.commit()
        print("Auth seed completed: roles, permissions, role mappings, and super admin.")


if __name__ == "__main__":
    seed_auth()
