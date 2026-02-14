from pathlib import Path

from flask import Blueprint, flash, redirect, render_template, request, send_file, url_for
from werkzeug.utils import secure_filename

from config import UPLOAD_DIR
from services.csv_cleaner_service import clean_csv_file

csv_bp = Blueprint("csv", __name__, url_prefix="/csv-cleaner")


@csv_bp.get("/")
def form():
    return render_template("csv_cleaner.html")


@csv_bp.post("/clean")
def clean():
    uploaded = request.files.get("csv_file")
    if not uploaded or not uploaded.filename:
        flash("Please upload a CSV file.", "error")
        return redirect(url_for("csv.form"))

    safe_name = secure_filename(uploaded.filename)
    source_path = Path(UPLOAD_DIR) / safe_name
    uploaded.save(source_path)

    output_path = clean_csv_file(
        source_path,
        deduplicate=request.form.get("deduplicate") == "on",
        drop_empty_rows=request.form.get("drop_empty_rows") == "on",
        trim_strings=request.form.get("trim_strings") == "on",
    )

    return send_file(output_path, as_attachment=True)
