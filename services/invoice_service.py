from datetime import datetime
from pathlib import Path
from typing import Iterable

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas


def generate_invoice_pdf(
    output_dir: Path,
    client_name: str,
    invoice_number: str,
    line_items: Iterable[dict],
    notes: str = "",
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"invoice_{invoice_number}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    output_path = output_dir / filename

    c = canvas.Canvas(str(output_path), pagesize=LETTER)
    width, height = LETTER

    y = height - 60
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "INVOICE")

    y -= 30
    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Invoice #: {invoice_number}")
    y -= 20
    c.drawString(50, y, f"Client: {client_name}")
    y -= 20
    c.drawString(50, y, f"Date: {datetime.now().strftime('%Y-%m-%d')}")

    y -= 35
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Description")
    c.drawString(380, y, "Amount")

    y -= 18
    c.setFont("Helvetica", 11)
    total = 0.0

    for item in line_items:
        desc = item.get("description", "")
        amount = float(item.get("amount", 0))
        total += amount

        c.drawString(50, y, desc[:60])
        c.drawRightString(500, y, f"${amount:,.2f}")
        y -= 18
        if y < 100:
            c.showPage()
            y = height - 60

    y -= 14
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Total")
    c.drawRightString(500, y, f"${total:,.2f}")

    if notes.strip():
        y -= 30
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Notes: {notes[:120]}")

    c.save()
    return output_path
