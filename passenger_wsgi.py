"""
Passenger WSGI entry point for Namecheap cPanel / shared hosting.

cPanel "Setup Python App" startup file: passenger_wsgi.py
Application entry point: application
"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.env_loader import load_project_dotenv
from app import create_app

load_project_dotenv()

if os.environ.get("FLASK_ENV", "production") != "production":
    raise RuntimeError("passenger_wsgi.py requires FLASK_ENV=production.")

application = create_app("production")
app = application
