"""Prüft das isolierte Release-ZIP über einen echten Gunicorn-Prozess."""

import argparse
from http.cookiejar import CookieJar
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import secrets
import socket
import subprocess
import sys
import tempfile
import time
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, build_opener
import zipfile


class EntryParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.entries = []
        self.entry = None
        self.field = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "li" and "entry" in attrs.get("class", "").split():
            self.entry = {"content": "", "happiness": ""}
        if self.entry is not None:
            if tag == "span" and attrs.get("aria-label") == "Stimmung":
                self.field = "happiness"
            elif tag == "p":
                self.field = "content"

    def handle_data(self, data):
        if self.entry is not None and self.field:
            self.entry[self.field] += data

    def handle_endtag(self, tag):
        if tag in {"span", "p"}:
            self.field = None
        if tag == "li" and self.entry is not None:
            self.entries.append(self.entry)
            self.entry = None
            self.field = None


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def verify_runtime(archive, expected_commit, startup_timeout=15):
    with tempfile.TemporaryDirectory(prefix="m324-runtime-") as directory:
        with zipfile.ZipFile(archive) as package:
            package.extractall(directory)
        password = secrets.token_urlsafe(24)
        environment = dict(os.environ)
        environment.pop("WEBSITE_HOSTNAME", None)
        environment.pop("PYTHONPATH", None)
        environment.update(PASSWORD=password, SECRET_KEY=secrets.token_hex(32))
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            listener.listen(128)
            url = f"http://127.0.0.1:{listener.getsockname()[1]}"
            process = subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "gunicorn",
                    "--workers",
                    "1",
                    "--bind",
                    f"fd://{listener.fileno()}",
                    "app:app",
                ],
                cwd=directory,
                env=environment,
                pass_fds=(listener.fileno(),),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            # Gunicorn besitzt nun den geerbten Socket; der Prüfer hält ihn nicht offen.
            listener.close()
            try:
                browser = build_opener(HTTPCookieProcessor(CookieJar()))

                def request(path, data=None):
                    payload = urlencode(data).encode() if data is not None else None
                    with browser.open(url + path, data=payload, timeout=3) as response:
                        return response.geturl(), response.read().decode()

                deadline = time.monotonic() + startup_timeout
                while True:
                    require(process.poll() is None, "Gunicorn konnte nicht starten.")
                    try:
                        _, body = request("/health")
                        health = json.loads(body)
                        break
                    except (URLError, TimeoutError, json.JSONDecodeError):
                        require(
                            time.monotonic() < deadline,
                            "Gunicorn-Startzeit überschritten.",
                        )
                        time.sleep(0.05)
                require(health.get("status") == "ok", "Health-Prüfung fehlgeschlagen.")
                require(
                    health.get("commit") == expected_commit,
                    "Release-Commit stimmt nicht überein.",
                )

                request("/login", {"password": "wrong-" + password})
                destination, _ = request("/add_entry", {"content": "Nicht erlaubt"})
                require(
                    destination == url + "/login",
                    "Falsches Passwort erlaubt Schreibzugriff.",
                )
                destination, _ = request("/login", {"password": password})
                require(destination == url + "/", "Login fehlgeschlagen.")

                content = "Runtime-Prüfung <script>alert(1)</script>"
                destination, body = request(
                    "/add_entry", {"content": content, "happiness": "😃"}
                )
                rendered = EntryParser()
                rendered.feed(body)
                matching = [
                    entry for entry in rendered.entries if entry["content"] == content
                ]
                require(
                    destination == url + "/" and len(matching) == 1,
                    "Eintrag fehlt im Release.",
                )
                require(
                    matching[0]["happiness"].strip() == "😃",
                    "Happiness fehlt am Eintrag im Release.",
                )
                require(
                    "&lt;script&gt;" in body and "<script>" not in body,
                    "HTML-Escaping fehlt.",
                )
                request("/logout")
                _, body = request("/")
                require(
                    "Runtime-Prüfung" not in body, "Logout verbirgt die Einträge nicht."
                )
                return {
                    "commit": health["commit"],
                    "version": health["version"],
                    "url": url,
                    "checks": [
                        "health",
                        "wrong_password",
                        "login",
                        "happiness",
                        "escaping",
                        "logout",
                    ],
                }
            finally:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--expected-commit", required=True)
    arguments = parser.parse_args()
    print(
        json.dumps(
            verify_runtime(arguments.archive, arguments.expected_commit),
            ensure_ascii=False,
        )
    )
