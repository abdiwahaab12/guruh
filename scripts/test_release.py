"""Step 28 — master release smoke test runner."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTS = sorted((ROOT / "scripts").glob("test_*.py"))
TESTS = [t for t in TESTS if t.name != "test_release.py"]

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
except ImportError:
    pass


def main() -> None:
    failed = []
    print("GURUH CMS v1.0.0 — Final QA Test Suite\n" + "=" * 48)
    for script in TESTS:
        name = script.name
        print(f"\n>> {name}")
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=str(ROOT),
            env={**dict(**__import__("os").environ)},
        )
        if result.returncode != 0:
            failed.append(name)
            print(f"   FAILED ({result.returncode})")
        else:
            print("   OK")

    print("\n" + "=" * 48)
    if failed:
        print(f"FAILED: {', '.join(failed)}")
        raise SystemExit(1)
    print(f"PASSED: {len(TESTS)}/{len(TESTS)} test suites")
    print("Release QA complete — ready for v1.0.0 sign-off.")


if __name__ == "__main__":
    main()
