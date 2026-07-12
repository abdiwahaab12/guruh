"""Hero background video upload and rendering tests."""

from __future__ import annotations

import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import app.models  # noqa: F401
from run import app
from app.utils.hero_video import validate_hero_video_file
from werkzeug.datastructures import FileStorage


def extract_csrf(html: str) -> str:
    match = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', html)
    if not match:
        raise AssertionError("CSRF token missing")
    return match.group(1)


def _login(client) -> None:
    token = extract_csrf(client.get("/admin/login").data.decode())
    r = client.post(
        "/admin/login",
        data={
            "csrf_token": token,
            "email": "admin@guruh.com",
            "password": "GuruhAdmin2026!",
            "remember": "y",
            "submit": "Sign In",
        },
        follow_redirects=True,
    )
    assert r.status_code == 200, "Admin login failed"


def _file(name: str, data: bytes, mime: str) -> FileStorage:
    return FileStorage(stream=io.BytesIO(data), filename=name, content_type=mime)


MINIMAL_MP4 = (
    b"\x00\x00\x00\x20ftypmp42\x00\x00\x00\x00mp42isom"
    b"\x00\x00\x00\x08free\x00\x00\x00\x00"
)
MINIMAL_WEBM = b"\x1a\x45\xdf\xa3" + b"\x00" * 32


def test_validation() -> None:
    failures: list[str] = []

    with app.app_context():
        ok, _ = validate_hero_video_file(_file("clip.mp4", MINIMAL_MP4, "video/mp4"))
        if not ok:
            failures.append("MP4 should be accepted")

        ok, _ = validate_hero_video_file(_file("clip.webm", MINIMAL_WEBM, "video/webm"))
        if not ok:
            failures.append("WEBM should be accepted")

        ok, msg = validate_hero_video_file(_file("clip.avi", b"RIFF", "video/x-msvideo"))
        if ok or "AVI" not in msg:
            failures.append(f"AVI should be rejected: {msg}")

        ok, msg = validate_hero_video_file(_file("clip.mov", b"moov", "video/quicktime"))
        if ok or "MOV" not in msg:
            failures.append(f"MOV should be rejected: {msg}")

        huge = _file("big.mp4", MINIMAL_MP4, "video/mp4")

        class HugeStream(io.BytesIO):
            def tell(self):
                return 101 * 1024 * 1024

        huge.stream = HugeStream(MINIMAL_MP4)
        ok, msg = validate_hero_video_file(huge)
        if ok or "maximum size" not in msg.lower():
            failures.append(f"100MB+ file should be rejected: {msg}")

        max_size = app.config.get("MEDIA_MAX_FILE_SIZE", 0)
        if max_size != 100 * 1024 * 1024:
            failures.append(f"MEDIA_MAX_FILE_SIZE expected 100MB, got {max_size}")

        max_content = app.config.get("MAX_CONTENT_LENGTH", 0)
        if max_content != 100 * 1024 * 1024:
            failures.append(f"MAX_CONTENT_LENGTH expected 100MB, got {max_content}")

    if failures:
        raise AssertionError("; ".join(failures))
    print("Hero video validation tests passed.")


def test_admin_and_rendering() -> None:
    failures: list[str] = []
    client = app.test_client()

    with app.app_context():
        from app.extensions import db
        from sqlalchemy import text

        try:
            db.session.execute(text("SELECT 1")).scalar()
        except Exception as exc:
            print(f"Skipping admin/rendering tests — database unavailable: {exc}")
            return

        _login(client)

        r = client.get("/admin/website/pages/home/hero-slides/1/edit")
        if r.status_code != 200:
            failures.append(f"hero slide edit returned {r.status_code}")
        body = r.data.decode("utf-8", errors="replace")
        if "Background Type" not in body:
            failures.append("admin form missing Background Type")
        if "heroBgVideoPanel" not in body:
            failures.append("admin form missing video panel")

        token = extract_csrf(body)
        r = client.post(
            "/admin/website/pages/home/hero-slides/1/edit",
            data={
                "csrf_token": token,
                "slide_id": "1",
                "title": "Test Hero Image Mode",
                "background_type": "image",
                "image": "",
                "overlay_opacity": "0.65",
                "text_alignment": "left",
                "sort_order": "1",
                "is_active": "y",
                "submit": "Save Slide",
            },
            follow_redirects=False,
        )
        if r.status_code not in (302, 200):
            failures.append(f"image mode save returned {r.status_code}")

        token = extract_csrf(
            client.get("/admin/website/pages/home/hero-slides/1/edit").data.decode()
        )
        r = client.post(
            "/admin/website/pages/home/hero-slides/1/edit",
            data={
                "csrf_token": token,
                "slide_id": "1",
                "title": "Test Hero Video Mode",
                "background_type": "video",
                "image": "",
                "autoplay": "y",
                "loop": "y",
                "muted": "y",
                "plays_inline": "y",
                "overlay_opacity": "0.65",
                "text_alignment": "left",
                "sort_order": "1",
                "is_active": "y",
                "hero_video": (io.BytesIO(MINIMAL_MP4), "hero-test.mp4"),
                "submit": "Save Slide",
            },
            content_type="multipart/form-data",
            follow_redirects=False,
        )
        if r.status_code not in (302, 200):
            failures.append(f"video upload save returned {r.status_code}")

        from app.providers.website_admin_provider import WebsiteAdminProvider

        row = WebsiteAdminProvider.get_hero_slide(1)
        if not row or not row.video_path:
            failures.append("video path not saved to database")
        elif not row.video_path.startswith("uploads/hero_videos/"):
            failures.append(f"unexpected video path: {row.video_path}")

        home = client.get("/")
        home_html = home.data.decode("utf-8", errors="replace")
        if "hero-slide-video" not in home_html and "hero-slide-bg" not in home_html:
            failures.append("homepage hero missing background media")
        if row and row.video_path and row.background_type == "video":
            if "hero-slide-video" not in home_html:
                failures.append("homepage missing hero video element")

        if row and row.video_path:
            token = extract_csrf(
                client.get("/admin/website/pages/home/hero-slides/1/edit").data.decode()
            )
            r = client.post(
                "/admin/website/pages/home/hero-slides/1/video/delete",
                data={"csrf_token": token},
                follow_redirects=True,
            )
            if r.status_code != 200:
                failures.append(f"video delete returned {r.status_code}")
            row = WebsiteAdminProvider.get_hero_slide(1)
            if row and row.video_path:
                failures.append("video not deleted from database")

    if failures:
        raise AssertionError("; ".join(failures))
    print("Hero video admin and rendering tests passed.")


def test_upload_lifecycle() -> None:
    """File upload, replace, and delete without database."""
    failures: list[str] = []

    with app.app_context():
        from app.utils.hero_video import delete_hero_video_files, save_hero_video_file

        path1, thumb1, err = save_hero_video_file(_file("a.mp4", MINIMAL_MP4, "video/mp4"))
        if err or not path1:
            failures.append(f"save mp4 failed: {err}")

        path2, thumb2, err = save_hero_video_file(_file("b.webm", MINIMAL_WEBM, "video/webm"))
        if err or not path2:
            failures.append(f"save webm failed: {err}")

        if path1 == path2:
            failures.append("video paths should be unique")

        delete_hero_video_files(path1, thumb1)
        delete_hero_video_files(path2, thumb2)

        from pathlib import Path
        static = Path(app.static_folder or "static")
        if (static / path1).exists():
            failures.append("video file not deleted")
        if path2 and (static / path2).exists():
            failures.append("webm file not deleted")

    if failures:
        raise AssertionError("; ".join(failures))
    print("Hero video upload lifecycle tests passed.")


def main() -> None:
    test_validation()
    test_upload_lifecycle()
    test_admin_and_rendering()
    print("All hero video tests passed.")


if __name__ == "__main__":
    main()
