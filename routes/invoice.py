from flask import Blueprint, flash, redirect, render_template, request, send_file, url_for

from config import INVOICE_OUTPUT_DIR
from services.invoice_service import generate_invoice_pdf

invoice_bp = Blueprint("invoice", __name__, url_prefix="/invoice-generator")


@invoice_bp.get("/")
def form():
    return render_template("invoice_generator.html")


@invoice_bp.post("/generate")
def generate():
    client_name = request.form.get("client_name", "").strip()
    invoice_number = request.form.get("invoice_number", "").strip()
    notes = request.form.get("notes", "").strip()

    descriptions = request.form.getlist("item_description")
    amounts = request.form.getlist("item_amount")

    if not client_name or not invoice_number:
        flash("Client name and invoice number are required.", "error")
        return redirect(url_for("invoice.form"))

    line_items = []
    for d, a in zip(descriptions, amounts):
        d = d.strip()
        a = a.strip()
        if not d and not a:
            continue
        try:
            line_items.append({"description": d, "amount": float(a)})
        except ValueError:
            flash("Line item amount must be a valid number.", "error")
            return redirect(url_for("invoice.form"))

    if not line_items:
        flash("Add at least one line item.", "error")
        return redirect(url_for("invoice.form"))

    pdf_path = generate_invoice_pdf(
        output_dir=INVOICE_OUTPUT_DIR,
        client_name=client_name,
        invoice_number=invoice_number,
        line_items=line_items,
        notes=notes,
    )
    return send_file(pdf_path, as_attachment=True)
