from datetime import datetime
from pathlib import Path

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for

from config import EMAIL_LOG_DIR
from services.email_service import EmailConfigError, send_bulk_email

email_bp = Blueprint("email", __name__, url_prefix="/bulk-email")


@email_bp.get("/")
def form():
    if not current_app.config.get("BULK_EMAIL_ENABLED", False):
        return render_template("bulk_email.html", disabled=True)
    return render_template("bulk_email.html")


@email_bp.post("/send")
def send():
    if not current_app.config.get("BULK_EMAIL_ENABLED", False):
        flash("Bulk Email Sender is currently disabled.", "error")
        return redirect(url_for("index"))

    subject = request.form.get("subject", "").strip()
    body = request.form.get("body", "").strip()
    recipients_raw = request.form.get("recipients", "")

    recipients = [r.strip() for r in recipients_raw.splitlines() if r.strip()]

    if not subject or not body or not recipients:
        flash("Subject, body, and at least one recipient are required.", "error")
        return redirect(url_for("email.form"))

    log_name = f"bulk_email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    log_path = Path(EMAIL_LOG_DIR) / log_name

    try:
        result = send_bulk_email(subject, body, recipients, log_path)
    except EmailConfigError as exc:
        flash(str(exc), "error")
        return redirect(url_for("email.form"))
    except Exception as exc:
        flash(f"Failed to send email: {exc}", "error")
        return redirect(url_for("email.form"))

    flash(
        f"Sent {result['sent']} of {result['total']} emails. Failures: {len(result['failed'])}. Log: {result['log']}",
        "success",
    )
    return redirect(url_for("email.form"))
