from flask import Blueprint, flash, redirect, render_template, request, send_file, url_for

from services.renamer_service import apply_renames, preview_renames

renamer_bp = Blueprint("renamer", __name__, url_prefix="/file-renamer")


@renamer_bp.get("/")
def form():
    return render_template("file_renamer.html", previews=[], applied=[])


@renamer_bp.post("/run")
def run():
    files = request.files.getlist("files")
    pattern = request.form.get("pattern", "")
    replacement = request.form.get("replacement", "")
    mode = request.form.get("mode", "preview")

    if not files or not any((f.filename or "").strip() for f in files):
        flash("Please upload a folder or files.", "error")
        return redirect(url_for("renamer.form"))

    if not pattern:
        flash("Pattern is required.", "error")
        return redirect(url_for("renamer.form"))

    if mode == "apply":
        archive, applied = apply_renames(files, pattern, replacement)
        if not applied:
            flash("No filenames matched the pattern.", "error")
            return redirect(url_for("renamer.form"))

        return send_file(
            archive,
            mimetype="application/zip",
            as_attachment=True,
            download_name="renamed_files.zip",
        )

    previews = preview_renames(files, pattern, replacement)
    if not previews:
        flash("No filenames matched the pattern.", "error")
        return redirect(url_for("renamer.form"))

    return render_template("file_renamer.html", previews=previews, applied=[])
