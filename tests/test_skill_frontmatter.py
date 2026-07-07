import os
import pytest
import yaml

ROOT = os.path.join(os.path.dirname(__file__), "..")


def _parse_frontmatter(rel_path):
    # skills live under <repo>/skills/<name>/SKILL.md
    with open(os.path.join(ROOT, "skills", rel_path), encoding="utf-8") as f:
        raw = f.read()
    assert raw.startswith("---\n"), f"{rel_path} missing frontmatter"
    _, front_block, body = raw.split("---", 2)
    return yaml.safe_load(front_block), body


def test_ideate_skill_frontmatter_and_sections():
    front, body = _parse_frontmatter("rx-ideate/SKILL.md")
    assert front["name"] == "rx-ideate"
    assert front["model"] == "opus"
    assert front.get("description")
    for section in ("## Purpose", "## Steps", "## Outputs"):
        assert section in body, f"missing {section}"


def test_experiment_skill_frontmatter_and_sections():
    front, body = _parse_frontmatter("rx-experiment/SKILL.md")
    assert front["name"] == "rx-experiment"
    assert front["model"] == "sonnet"
    assert front.get("description")
    for section in ("## Purpose", "## Steps", "## Outputs"):
        assert section in body
    assert "capture_run" in body
    assert "negative" in body  # negative results are first-class


def test_write_skill_covers_four_outputs_and_gates():
    front, body = _parse_frontmatter("rx-write/SKILL.md")
    assert front["name"] == "rx-write"
    assert front["model"] == "sonnet"
    for section in ("## Purpose", "## Steps", "## Outputs", "## Anonymity", "## Blog"):
        assert section in body
    for out in ("paper/arxiv", "paper/anon", "code/", "blog/"):
        assert out in body
    assert "can_promote" in body and "[UNSUPPORTED]" in body
    assert "lint_anonymity" in body
    assert "confirm" in body.lower()  # blog push requires confirmation


@pytest.mark.parametrize("name,model", [
    ("rx-ideate", "opus"), ("rx-survey", "sonnet"), ("rx-plan", "sonnet"),
    ("rx-experiment", "sonnet"), ("rx-analyze", "opus"),
    ("rx-write", "sonnet"), ("rx-review", "opus"), ("rx-pipeline", "opus"),
])
def test_all_skills_have_valid_frontmatter(name, model):
    front, body = _parse_frontmatter(f"{name}/SKILL.md")
    assert front["name"] == name
    assert front["model"] == model
    assert front.get("description")
    for section in ("## Purpose", "## Steps", "## Outputs"):
        assert section in body, f"{name} missing {section}"


def test_pipeline_skill_covers_loop_and_gates():
    front, body = _parse_frontmatter("rx-pipeline/SKILL.md")
    assert front["name"] == "rx-pipeline"
    assert front["model"] == "opus"
    for section in ("## Purpose", "## Steps", "## Outputs", "## Loop"):
        assert section in body
    assert "stage_blockers" in body      # enforces blocker-first
    assert "loop_step" in body           # drives the loop
    assert "negative" in body.lower()    # negative results feed the loop
