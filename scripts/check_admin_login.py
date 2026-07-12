"""Check admin login state and optionally reset password."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import app.models  # noqa: F401
from app.extensions import db
from app.models.auth import User
from run import app


def main() -> None:
    with app.app_context():
        email = app.config["ADMIN_EMAIL"].lower().strip()
        password = app.config["ADMIN_PASSWORD"]
        print(f"Config email: {email}")
        print(f"Config password set: {'yes' if password else 'no'}")

        users = User.query.all()
        print(f"Users in database: {len(users)}")
        for user in users:
            print(
                f"  - {user.email} | active={user.is_active} | locked={user.is_locked} "
                f"| failed_attempts={user.failed_login_attempts}"
            )

        admin = User.query.filter_by(email=email).first()
        if not admin:
            print("No admin user for config email — run: python scripts/seed_auth.py")
            return

        if admin.check_password(password):
            print("Password from .env matches database — login should work.")
        else:
            print("Password from .env does NOT match database.")
            admin.set_password(password)
            admin.failed_login_attempts = 0
            admin.locked_until = None
            admin.is_active = True
            db.session.commit()
            print("Reset password to ADMIN_PASSWORD from .env and cleared lockout.")


if __name__ == "__main__":
    main()
