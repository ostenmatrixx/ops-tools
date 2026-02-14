from pathlib import Path

from flask import Blueprint, flash, redirect, render_template, request, url_for

from services.renamer_service import apply_renames, preview_renames

renamer_bp = Blueprint("renamer", __name__, url_prefix="/file-renamer")


@renamer_bp.get("/")
def form():
    return render_template("file_renamer.html", previews=[], applied=[])


@renamer_bp.post("/run")
def run():
    directory = Path(request.form.get("directory", "").strip())
    pattern = request.form.get("pattern", "")
    replacement = request.form.get("replacement", "")
    mode = request.form.get("mode", "preview")

    if not directory.exists() or not directory.is_dir():
        flash("Directory path is invalid.", "error")
        return redirect(url_for("renamer.form"))

    if not pattern:
        flash("Pattern is required.", "error")
        return redirect(url_for("renamer.form"))

    if mode == "apply":
        applied = apply_renames(directory, pattern, replacement)
        flash(f"Renamed {len(applied)} files.", "success")
        return render_template("file_renamer.html", previews=[], applied=applied)

    previews = preview_renames(directory, pattern, replacement)
    return render_template("file_renamer.html", previews=previews, applied=[])
