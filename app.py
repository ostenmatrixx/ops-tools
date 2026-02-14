from flask import Flask, render_template

from config import SECRET_KEY, MAX_CONTENT_LENGTH
from routes.csv_cleaner import csv_bp
from routes.invoice import invoice_bp
from routes.bulk_email import email_bp
from routes.file_renamer import renamer_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

    app.register_blueprint(csv_bp)
    app.register_blueprint(invoice_bp)
    app.register_blueprint(email_bp)
    app.register_blueprint(renamer_bp)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/healthz")
    def healthz():
        return {"ok": True}, 200

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
