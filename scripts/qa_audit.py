"""Production QA audit — run: python scripts/qa_audit.py"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import create_app  # noqa: E402


def audit() -> list[str]:
    app = create_app()
    client = app.test_client()
    issues: list[str] = []

    with app.app_context():
        from app.providers import get_content_provider

        provider = get_content_provider()
        routes: list[tuple[str, str]] = [
            ("/", "Home"),
            ("/about", "About"),
            ("/services", "Services"),
            ("/projects", "Projects"),
            ("/equipment", "Equipment"),
            ("/team", "Team"),
            ("/careers", "Careers"),
            ("/gallery", "Gallery"),
            ("/contact", "Contact"),
            ("/request-quote", "Request Quote"),
        ]
        for proj in provider.get_projects()[:2]:
            routes.append((f"/projects/{proj.slug}", f"Project {proj.slug}"))
        for eq in provider.get_equipment()[:2]:
            routes.append((f"/equipment/{eq.slug}", f"Equipment {eq.slug}"))
        for job in provider.get_job_listings()[:2]:
            routes.append((f"/careers/{job.slug}", f"Job {job.slug}"))

        for path, name in routes:
            r = client.get(path)
            html = r.data.decode("utf-8", errors="replace")
            if r.status_code != 200:
                issues.append(f"[HTTP {r.status_code}] {name} ({path})")
                continue
            if 'rel="canonical"' not in html:
                issues.append(f"[SEO] Missing canonical: {name}")
            if "og:title" not in html:
                issues.append(f"[SEO] Missing Open Graph: {name}")
            if "twitter:card" not in html:
                issues.append(f"[SEO] Missing Twitter card: {name}")
            if "application/ld+json" not in html:
                issues.append(f"[SEO] Missing JSON-LD: {name}")
            if 'id="main-content"' not in html:
                issues.append(f"[A11Y] Missing main landmark: {name}")
            bc_count = html.count("BreadcrumbList")
            if bc_count > 1:
                issues.append(f"[SEO] Duplicate BreadcrumbList ({bc_count}x): {name}")
            elif bc_count == 0 and path != "/":
                issues.append(f"[SEO] Missing BreadcrumbList: {name}")
            h1_count = len(re.findall(r"<h1[^>]*>", html, re.I))
            if h1_count == 0:
                issues.append(f"[SEO] No H1: {name}")
            elif h1_count > 1:
                issues.append(f"[SEO] Multiple H1 ({h1_count}): {name}")
            if path in ("/contact", "/request-quote"):
                if 'method="post"' in html.lower() and "csrf" not in html.lower():
                    issues.append(f"[SECURITY] Form missing CSRF prep: {name}")

        print(f"Audited {len(routes)} public routes")
        if issues:
            print(f"\nFound {len(issues)} issues:\n")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("No automated issues found.")
        return issues


if __name__ == "__main__":
    audit()
