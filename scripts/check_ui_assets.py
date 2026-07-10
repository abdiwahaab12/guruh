"""UI QA — verify public pages render and static assets exist."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from run import app  # noqa: E402

ROUTES = (
    "/",
    "/about",
    "/services",
    "/projects",
    "/equipment",
    "/gallery",
    "/team",
    "/careers",
    "/contact",
    "/request-quote",
    "/projects/isiolo-township-roads",
    "/equipment/motor-grader-cat-140",
    "/careers/health-safety-officer",
)


def main() -> None:
    client = app.test_client()
    issues: list[str] = []

    for route in ROUTES:
        resp = client.get(route)
        if resp.status_code != 200:
            issues.append(f"{route}: HTTP {resp.status_code}")
            continue

        body = resp.data.decode(errors="replace")

        for path in re.findall(r"/static/([^\"'?#]+)", body):
            static_path = ROOT / "static" / path.strip()
            if not static_path.is_file():
                issues.append(f"{route}: missing static/{path.strip()}")

        if "<h1" not in body.lower():
            issues.append(f"{route}: missing H1")

        for marker in ("site-header", "site-footer", "main-content"):
            if marker not in body:
                issues.append(f"{route}: missing {marker}")

    if issues:
        print("UI ASSET CHECK FAILURES:")
        for item in issues:
            print(f"  - {item}")
        raise SystemExit(1)

    print(f"UI asset check passed for {len(ROUTES)} routes.")


if __name__ == "__main__":
    main()
