import os
import smtplib
from email.message import EmailMessage
from pathlib import Path
from typing import Iterable


class EmailConfigError(Exception):
    pass


def _smtp_settings() -> dict:
    host = os.getenv("SMTP_HOST")
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    from_addr = os.getenv("SMTP_FROM")

    if not all([host, username, password, from_addr]):
        raise EmailConfigError(
            "Missing SMTP config. Set SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD, SMTP_FROM."
        )

    return {
        "host": host,
        "port": int(os.getenv("SMTP_PORT", "587")),
        "username": username,
        "password": password,
        "from_addr": from_addr,
        "use_tls": os.getenv("SMTP_USE_TLS", "true").lower() == "true",
    }


def send_bulk_email(subject: str, body: str, recipients: Iterable[str], log_path: Path) -> dict:
    cfg = _smtp_settings()
    recipients = [r.strip() for r in recipients if r.strip()]

    sent = 0
    failures = []

    with smtplib.SMTP(cfg["host"], cfg["port"], timeout=20) as server:
        if cfg["use_tls"]:
            server.starttls()
        server.login(cfg["username"], cfg["password"])

        for recipient in recipients:
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = cfg["from_addr"]
            msg["To"] = recipient
            msg.set_content(body)

            try:
                server.send_message(msg)
                sent += 1
            except Exception as exc:
                failures.append({"recipient": recipient, "error": str(exc)})

    log_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"sent={sent}", f"failed={len(failures)}"]
    for f in failures:
        lines.append(f"{f['recipient']}: {f['error']}")
    log_path.write_text("\n".join(lines), encoding="utf-8")

    return {"sent": sent, "failed": failures, "total": len(recipients), "log": str(log_path)}
