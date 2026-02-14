# Ops Toolkit Web App

A Python + Flask web app with four operations tools:

1. CSV Cleaner
2. Invoice Generator
3. Bulk Email Sender
4. File Renamer Automation

## Tech
- Backend: Python (Flask)
- Frontend: HTML/CSS/JS (Flask templates)
- Hosting: GitHub repo (and deployable to Render/Railway/Fly/any WSGI host)

## Quick Start
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Tool Notes
- Bulk Email Sender requires SMTP credentials in environment variables.
- Invoice Generator outputs a PDF to `generated/invoices/`.
- File Renamer works inside a selected directory and supports preview mode.

## SMTP Environment Variables
- `SMTP_HOST`
- `SMTP_PORT` (default `587`)
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `SMTP_FROM`
- `SMTP_USE_TLS` (`true`/`false`, default `true`)

## GitHub
This repo is GitHub-ready. Push as usual:
```bash
git init
git add .
git commit -m "Initial ops-tools app"
```

## Hosting Note
GitHub Pages cannot run a Python backend (Flask). Use GitHub for source control, then deploy from GitHub to a Python host (Render, Railway, Fly.io, etc.).

This repo includes `render.yaml` and `Procfile` for Render deployment.
