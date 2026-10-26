from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def read_yaml(path):
    # BaseLoader erhält den GitHub-Schlüssel 'on' als Zeichenkette.
    return yaml.load((ROOT / path).read_text(), Loader=yaml.BaseLoader)


def test_commit_formats_and_push_tests_every_time():
    config = read_yaml(".pre-commit-config.yaml")
    assert set(config["default_install_hook_types"]) == {"pre-commit", "pre-push"}
    hooks = {hook["id"]: hook for repo in config["repos"] for hook in repo["hooks"]}
    assert hooks["black"]["entry"] == "python -m black"
    assert hooks["black"]["stages"] == ["pre-commit"]
    assert hooks["pytest"]["entry"] == "python -m pytest"
    assert hooks["pytest"]["stages"] == ["pre-push"]
    assert hooks["pytest"]["always_run"] == "true"
    assert hooks["pytest"]["pass_filenames"] == "false"


def test_ci_only_runs_for_pull_requests_to_dev():
    config = read_yaml(".github/workflows/ci.yml")
    assert set(config["on"]) == {"pull_request"}
    assert config["on"]["pull_request"]["branches"] == ["dev"]
    assert set(config["jobs"]) == {"test"}
    steps = config["jobs"]["test"]["steps"]
    assert any(step.get("run") == "python -m pytest" for step in steps)


def test_release_is_verified_before_main_deployment():
    config = read_yaml(".github/workflows/deploy-azure.yml")
    assert set(config["on"]) == {"push", "workflow_dispatch"}
    assert config["on"]["push"]["branches"] == ["main"]
    verify = config["jobs"]["verify"]
    assert verify["if"] == "github.ref == 'refs/heads/main'"
    assert "AZURE_WEBAPP_NAME" not in verify["if"]
    steps = verify["steps"]
    commands = [step.get("run", "") for step in steps]
    assert any("scripts/smoke_runtime.py dist/deploy.zip" in run for run in commands)
    deploy = config["jobs"]["deploy"]
    assert deploy["needs"] == "verify"
    assert "github.ref == 'refs/heads/main'" in deploy["if"]
    uploaded = next(
        step["with"]["name"]
        for step in steps
        if step.get("uses", "").startswith("actions/upload-artifact@")
    )
    downloaded = next(
        step["with"]["name"]
        for step in deploy["steps"]
        if step.get("uses", "").startswith("actions/download-artifact@")
    )
    assert uploaded == downloaded == "tagebbbuch-${{ github.sha }}"


def test_template_covers_the_lb_requirement_structure():
    config = read_yaml(".github/ISSUE_TEMPLATE/anforderung.yml")
    ids = {field["id"] for field in config["body"] if "id" in field}
    assert {
        "zielsystem",
        "prioritaet",
        "aktivitaet",
        "ergaenzungen",
        "funktionalitaet",
        "bedingungen",
        "satz",
        "abnahme",
    } <= ids
    assert "labels" not in config  # Der Anforderungstyp bleibt manuell wählbar.
