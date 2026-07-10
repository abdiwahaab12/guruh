"""Final QA — public page smoke tests (Step 28)."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from run import app

PUBLIC_ROUTES = (
    "/",
    "/about",
    "/services",
    "/projects",
    "/equipment",
    "/gallery",
    "/team",
    "/careers",
    "/testimonials",
    "/contact",
    "/request-quote",
    "/health",
)

DETAIL_ROUTES = (
    "/projects/isiolo-township-roads",
    "/projects/marich-pass-kainuk-road-maintenance",
    "/equipment/motor-grader-cat-140",
    "/careers/health-safety-officer",
)


def main() -> None:
    client = app.test_client()
    failures = []

    for route in PUBLIC_ROUTES:
        r = client.get(route)
        if r.status_code != 200:
            failures.append(f"{route} -> {r.status_code}")
            continue
        body = r.data.decode(errors="replace")
        if route != "/health" and "<main" not in body and "main-content" not in body:
            failures.append(f"{route} missing main landmark")

    for route in DETAIL_ROUTES:
        r = client.get(route)
        if r.status_code not in (200, 404):
            failures.append(f"{route} -> {r.status_code}")

    # SEO markers on homepage
    home = client.get("/").data.decode(errors="replace")
    for marker in ("og:title", "twitter:card", "canonical", "application/ld+json"):
        if marker not in home:
            failures.append(f"homepage missing SEO marker: {marker}")

    if failures:
        print("PUBLIC PAGE FAILURES:")
        for item in failures:
            print(f"  - {item}")
        raise SystemExit(1)

    print(f"All {len(PUBLIC_ROUTES)} public routes and SEO checks passed.")


if __name__ == "__main__":
    main()
