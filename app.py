from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    abort,
)
from datetime import datetime
from dataclasses import dataclass, field
import json
import os
import secrets
from pathlib import Path
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
app.config.update(
    SECRET_KEY=os.getenv("SECRET_KEY") or secrets.token_hex(32),
    PASSWORD=os.getenv("PASSWORD"),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=bool(os.getenv("WEBSITE_HOSTNAME")),
    MAX_CONTENT_LENGTH=32 * 1024,
)
if os.getenv("WEBSITE_HOSTNAME") and not os.getenv("SECRET_KEY"):
    raise RuntimeError("SECRET_KEY muss in Azure App settings gesetzt sein.")
VERSION = "0.2.0"
MOODS = {"😃", "😐", "😞"}
release_file = Path(__file__).with_name("release.json")
release = json.loads(release_file.read_text()) if release_file.exists() else {}
entries = []


@dataclass
class Entry:
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    happiness: str = "😐"


@app.before_request
def reject_cross_origin_post():
    origin = request.headers.get("Origin")
    if (
        request.method == "POST"
        and origin
        and origin.rstrip("/") != request.host_url.rstrip("/")
    ):
        abort(403)


@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; style-src 'self'; form-action 'self'; frame-ancestors 'none'"
    )
    response.headers["Cache-Control"] = "no-store"
    return response


@app.route("/health")
def health():
    return {
        "status": "ok",
        "version": VERSION,
        "commit": release.get("commit", "local"),
    }


@app.route("/")
def index():
    return render_template("index.html", entries=entries)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_password = request.form.get("password")
        configured_password = app.config["PASSWORD"]
        if (
            configured_password
            and user_password
            and secrets.compare_digest(
                user_password.encode("utf-8"), configured_password.encode("utf-8")
            )
        ):
            session["logged_in"] = True
            flash("Login successful!", "success")
            return redirect(url_for("index"))
        else:
            flash("Incorrect password. Please try again.", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("Logged out successfully.", "success")
    return redirect(url_for("index"))


@app.route("/add_entry", methods=["POST"])
def add_entry():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    content = request.form.get("content", "").strip()
    if not content or len(content) > 5000:
        abort(400, description="Ein Eintrag braucht 1 bis 5000 Zeichen.")
    happiness = request.form.get("happiness", "😐")
    if happiness not in MOODS:
        abort(400, description="Bitte eine der angebotenen Stimmungen auswählen.")
    entry = Entry(content=content, happiness=happiness)
    entries.append(entry)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0")
