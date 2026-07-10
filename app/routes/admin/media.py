"""Enterprise Media Manager admin routes — Step 16."""

from __future__ import annotations

from flask import abort, flash, jsonify, redirect, render_template, request, url_for

from app.forms.media_forms import (
    MediaCopyForm,
    MediaDeleteForm,
    MediaMetadataForm,
    MediaMoveForm,
    MediaRenameForm,
    MediaReplaceForm,
    MediaUploadForm,
)
from app.services.media_service import MediaService
from app.utils.permissions import can_manage_media


def register_media_routes(admin_bp) -> None:
    """Register media library routes."""

    @admin_bp.route("/media")
    @can_manage_media
    def media_dashboard():
        return render_template("admin/media/dashboard.html", **MediaService.get_dashboard_context())

    @admin_bp.route("/media/library")
    @can_manage_media
    def media_library():
        ctx = MediaService.get_library_context(
            q=request.args.get("q", ""),
            folder=request.args.get("folder", ""),
            media_type=request.args.get("type", ""),
            sort=request.args.get("sort", "date_desc"),
            view=request.args.get("view", "grid"),
            page=request.args.get("page", 1, type=int),
        )
        return render_template("admin/media/library.html", **ctx)

    @admin_bp.route("/media/upload", methods=["GET", "POST"])
    @can_manage_media
    def media_upload():
        form = MediaUploadForm()
        default_folder = request.args.get("folder", "general")
        if request.method == "GET":
            form.folder.data = default_folder

        if form.validate_on_submit():
            results = MediaService.upload_files(
                form.files.data,
                folder=form.folder.data,
                ip_address=request.remote_addr,
                title=form.title.data or "",
                alt_text=form.alt_text.data or "",
            )
            success_count = sum(1 for r in results if r.success)
            if success_count:
                flash(f"{success_count} file(s) uploaded successfully.", "success")
            for result in results:
                if not result.success:
                    flash(result.message, "danger")
            if success_count:
                return redirect(url_for("admin.media_library", folder=form.folder.data))

        ctx = MediaService.get_upload_context(default_folder)
        ctx["form"] = form
        return render_template("admin/media/upload.html", **ctx)

    @admin_bp.route("/media/api/upload", methods=["POST"])
    @can_manage_media
    def media_api_upload():
        folder = request.form.get("folder", "general")
        files = request.files.getlist("files")
        if not files:
            return jsonify({"success": False, "message": "No files provided.", "results": []}), 400

        results = MediaService.upload_files(
            files,
            folder=folder,
            ip_address=request.remote_addr,
            title=request.form.get("title", ""),
            alt_text=request.form.get("alt_text", ""),
        )
        payload = []
        for result in results:
            entry = {"success": result.success, "message": result.message}
            if result.asset:
                entry["asset"] = {
                    "id": result.asset.id,
                    "title": result.asset.title,
                    "storage_path": result.asset.storage_path,
                    "public_url": result.asset.public_url,
                    "media_type": result.asset.media_type,
                    "file_size_label": result.asset.file_size_label,
                }
            payload.append(entry)

        ok = any(item["success"] for item in payload)
        return jsonify({"success": ok, "results": payload}), (200 if ok else 422)

    @admin_bp.route("/media/<int:asset_id>")
    @can_manage_media
    def media_detail(asset_id: int):
        ctx = MediaService.get_detail_context(asset_id)
        if not ctx:
            abort(404)
        ctx["delete_form"] = MediaDeleteForm()
        ctx["copy_form"] = MediaCopyForm()
        ctx["move_form"] = MediaMoveForm()
        ctx["replace_form"] = MediaReplaceForm()
        ctx["rename_form"] = MediaRenameForm()
        asset = ctx["asset"]
        ctx["rename_form"].title.data = asset.title
        ctx["rename_form"].original_filename.data = asset.original_filename
        ctx["move_form"].folder.data = asset.folder
        return render_template("admin/media/detail.html", **ctx)

    @admin_bp.route("/media/<int:asset_id>/edit", methods=["GET", "POST"])
    @can_manage_media
    def media_edit(asset_id: int):
        ctx = MediaService.get_edit_context(asset_id)
        if not ctx:
            abort(404)

        form = MediaMetadataForm()
        asset = ctx["asset"]
        if request.method == "GET":
            form.title.data = asset.title
            form.original_filename.data = asset.original_filename
            form.alt_text.data = asset.alt_text
            form.caption.data = asset.caption
            form.description.data = asset.description
            form.tags.data = asset.tags
            form.category.data = asset.category
            form.seo_title.data = asset.seo_title
            form.seo_description.data = asset.seo_description

        if form.validate_on_submit():
            result = MediaService.save_metadata(
                asset_id,
                {
                    "title": form.title.data,
                    "original_filename": form.original_filename.data,
                    "alt_text": form.alt_text.data,
                    "caption": form.caption.data,
                    "description": form.description.data,
                    "tags": form.tags.data,
                    "category": form.category.data,
                    "seo_title": form.seo_title.data,
                    "seo_description": form.seo_description.data,
                },
                ip_address=request.remote_addr,
            )
            flash(result.message, "success" if result.success else "danger")
            if result.success:
                return redirect(url_for("admin.media_detail", asset_id=asset_id))

        ctx["form"] = form
        return render_template("admin/media/edit.html", **ctx)

    @admin_bp.route("/media/<int:asset_id>/replace", methods=["POST"])
    @can_manage_media
    def media_replace(asset_id: int):
        form = MediaReplaceForm()
        if form.validate_on_submit():
            result = MediaService.replace_asset(
                asset_id, form.file.data, ip_address=request.remote_addr
            )
            flash(result.message, "success" if result.success else "danger")
        else:
            flash("Invalid replacement upload.", "danger")
        return redirect(url_for("admin.media_detail", asset_id=asset_id))

    @admin_bp.route("/media/<int:asset_id>/move", methods=["POST"])
    @can_manage_media
    def media_move(asset_id: int):
        form = MediaMoveForm()
        if form.validate_on_submit():
            result = MediaService.move_asset(
                asset_id, form.folder.data, ip_address=request.remote_addr
            )
            flash(result.message, "success" if result.success else "danger")
        else:
            flash("Invalid move request.", "danger")
        return redirect(url_for("admin.media_detail", asset_id=asset_id))

    @admin_bp.route("/media/<int:asset_id>/copy", methods=["POST"])
    @can_manage_media
    def media_copy(asset_id: int):
        form = MediaCopyForm()
        if form.validate_on_submit():
            result = MediaService.copy_asset(asset_id, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
        else:
            flash("Invalid copy request.", "danger")
        return redirect(url_for("admin.media_library"))

    @admin_bp.route("/media/<int:asset_id>/rename", methods=["POST"])
    @can_manage_media
    def media_rename(asset_id: int):
        form = MediaRenameForm()
        if form.validate_on_submit():
            result = MediaService.rename_asset(
                asset_id,
                form.title.data,
                form.original_filename.data or "",
                ip_address=request.remote_addr,
            )
            flash(result.message, "success" if result.success else "danger")
        else:
            flash("Invalid rename request.", "danger")
        return redirect(url_for("admin.media_detail", asset_id=asset_id))

    @admin_bp.route("/media/<int:asset_id>/delete", methods=["POST"])
    @can_manage_media
    def media_delete(asset_id: int):
        form = MediaDeleteForm()
        if form.validate_on_submit():
            result = MediaService.delete_asset(asset_id, ip_address=request.remote_addr)
            flash(result.message, "success" if result.success else "danger")
            if result.success:
                return redirect(url_for("admin.media_library"))
        else:
            flash("Invalid delete request.", "danger")
        return redirect(url_for("admin.media_detail", asset_id=asset_id))
