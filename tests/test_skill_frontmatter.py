import os
import yaml

ROOT = os.path.join(os.path.dirname(__file__), "..")


def _parse_frontmatter(rel_path):
    with open(os.path.join(ROOT, rel_path), encoding="utf-8") as f:
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
