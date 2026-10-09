"""Verpackt ausschliesslich Laufzeitdateien, nie lokale Geheimnisse."""

import ast
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_FILES = (
    "app.py",
    "requirements.txt",
    "templates/index.html",
    "templates/login.html",
    "static/style.css",
)


def build_package(output_dir=None):
    output_dir = Path(output_dir) if output_dir is not None else ROOT / "dist"
    output_dir.mkdir(parents=True, exist_ok=True)
    commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    version = next(
        ast.literal_eval(node.value)
        for node in ast.parse((ROOT / "app.py").read_text()).body
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "VERSION"
            for target in node.targets
        )
    )
    payload = {name: (ROOT / name).read_bytes() for name in RUNTIME_FILES}
    metadata = {
        "version": version,
        "commit": commit,
        "files": {
            name: hashlib.sha256(data).hexdigest() for name, data in payload.items()
        },
    }
    archive = output_dir / "deploy.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as package:
        for name, data in payload.items():
            package.writestr(name, data)
        package.writestr("release.json", json.dumps(metadata, indent=2) + "\n")
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix(".zip.sha256").write_text(f"{digest}  {archive.name}\n")
    return archive


if __name__ == "__main__":
    print(build_package())
