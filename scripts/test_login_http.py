"""Quick HTTP login test against running dev server."""

from __future__ import annotations

import re
import sys
import urllib.parse
import urllib.request
from http.cookiejar import CookieJar

URL = "http://127.0.0.1:5000/admin/login"


def main() -> None:
    jar = CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    page = opener.open(URL, timeout=10).read().decode()
    match = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', page)
    if not match:
        print("FAIL: no CSRF token")
        sys.exit(1)
    data = urllib.parse.urlencode(
        {
            "csrf_token": match.group(1),
            "email": "admin@guruh.com",
            "password": "GuruhAdmin2026!",
            "remember": "y",
            "submit": "Sign In",
        }
    ).encode()
    resp = opener.open(urllib.request.Request(URL, data=data, method="POST"), timeout=15)
    body = resp.read().decode()
    final = resp.geturl()
    print("final_url:", final)
    print("db_error:", "Cannot connect to the database" in body)
    print("invalid:", "Invalid email or password" in body)
    print("success:", "login" not in final)


if __name__ == "__main__":
    main()
