import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
GENERATED_DIR = BASE_DIR / "generated"
INVOICE_OUTPUT_DIR = GENERATED_DIR / "invoices"
EMAIL_LOG_DIR = GENERATED_DIR / "emails"

for _dir in [UPLOAD_DIR, GENERATED_DIR, INVOICE_OUTPUT_DIR, EMAIL_LOG_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
MAX_CONTENT_LENGTH = 25 * 1024 * 1024
BULK_EMAIL_ENABLED = os.getenv("BULK_EMAIL_ENABLED", "false").lower() == "true"
