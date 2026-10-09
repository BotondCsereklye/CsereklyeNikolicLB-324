import hashlib
import json
import zipfile

from scripts.package_release import build_package


def test_release_contains_only_runtime_files_and_identifies_commit(tmp_path):
    archive = build_package(tmp_path)
    with zipfile.ZipFile(archive) as package:
        assert set(package.namelist()) == {
            "app.py",
            "requirements.txt",
            "templates/index.html",
            "templates/login.html",
            "static/style.css",
            "release.json",
        }
        assert package.testzip() is None
        metadata = json.loads(package.read("release.json"))
        assert len(metadata["commit"]) == 40
        for name, digest in metadata["files"].items():
            assert hashlib.sha256(package.read(name)).hexdigest() == digest
    assert (
        archive.with_suffix(".zip.sha256").read_text().split()[0]
        == hashlib.sha256(archive.read_bytes()).hexdigest()
    )
