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


def test_deployment_only_runs_on_main():
    config = read_yaml(".github/workflows/deploy-azure.yml")
    assert set(config["on"]) == {"push"}
    assert config["on"]["push"]["branches"] == ["main"]


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
