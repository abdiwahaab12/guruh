"""
WSGI entry point for production deployment (Gunicorn / Passenger).

Namecheap cPanel: prefer passenger_wsgi.py as the startup file.
"""

import os

from app.env_loader import load_project_dotenv
from app import create_app

load_project_dotenv()

config_name = os.environ.get("FLASK_ENV", "production")
if config_name != "production":
    raise RuntimeError("wsgi.py requires FLASK_ENV=production.")

app = create_app("production")
