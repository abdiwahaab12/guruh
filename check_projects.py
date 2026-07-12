from app import create_app
from app.models.catalog import Project

app = create_app("development")

with app.app_context():
    print("Projects:", Project.query.count())
    for p in Project.query.all():
        print("-", p.title)