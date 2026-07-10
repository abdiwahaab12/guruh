"""
LOCAL DEVELOPMENT SERVER ONLY — not used on Namecheap production.

Production entry points:
    passenger_wsgi.py  (cPanel / Passenger)
    wsgi.py            (Gunicorn / WSGI)

Run locally:
    copy .env.development.example .env
    python run.py

Scripts (init_db, seeds, migrations) may import `app` from this module.
"""

import os

from app.env_loader import load_project_dotenv
from app import create_app

load_project_dotenv()

config_name = os.environ.get("FLASK_ENV", "development")
app = create_app(config_name)


if __name__ == "__main__":
    if config_name == "production":
        raise RuntimeError(
            "run.py must not start the dev server in production. "
            "On Namecheap use passenger_wsgi.py with FLASK_ENV=production."
        )
    app.run(
        host="127.0.0.1",
        port=int(os.environ.get("PORT", 5000)),
        debug=app.config.get("DEBUG", True),
    )
