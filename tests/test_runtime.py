import json
import os
import socket
import subprocess
import zipfile
from urllib.parse import urlparse

import pytest

from scripts.package_release import build_package
from scripts.smoke_runtime import verify_runtime

pytestmark = pytest.mark.skipif(
    os.name == "nt", reason="Gunicorn benötigt macOS oder Linux; CI läuft auf Linux."
)


def current_commit():
    return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()


def test_packaged_app_passes_real_http_acceptance_and_stops(tmp_path):
    commit = current_commit()
    result = verify_runtime(build_package(tmp_path), commit)
    assert result["commit"] == commit
    assert result["checks"] == [
        "health",
        "wrong_password",
        "login",
        "happiness",
        "escaping",
        "logout",
    ]
    address = urlparse(result["url"])
    with socket.socket() as connection:
        connection.settimeout(1)
        assert connection.connect_ex((address.hostname, address.port)) != 0


def test_packaged_app_with_wrong_release_commit_is_rejected(tmp_path):
    with pytest.raises(RuntimeError, match="Commit"):
        verify_runtime(build_package(tmp_path), "0" * 40)


def test_packaged_app_with_broken_happiness_is_rejected(tmp_path):
    archive = build_package(tmp_path)
    with zipfile.ZipFile(archive) as package:
        files = {name: package.read(name) for name in package.namelist()}
    files["app.py"] = files["app.py"].replace(
        b"happiness=happiness", b'happiness="broken"'
    )
    metadata = json.loads(files["release.json"])
    assert metadata["commit"] == current_commit()
    with zipfile.ZipFile(archive, "w") as package:
        for name, data in files.items():
            package.writestr(name, data)
    with pytest.raises(RuntimeError, match="Happiness"):
        verify_runtime(archive, current_commit())
