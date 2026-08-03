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
    for out in ("publication/arxiv", "publication/anon", "code/", "blog/"):
        assert out in body
    assert "can_promote" in body and "[UNSUPPORTED]" in body
    assert "lint_anonymity" in body
    assert "confirm" in body.lower()  # blog push requires confirmation


def test_write_skill_latex_and_modes():
    front, body = _parse_frontmatter("rx-write/SKILL.md")
    assert "main.tex" in body and "preamble.tex" in body and "refs.bib" in body
    assert "render_bib" in body
    assert "--mode=draft" in body and "--mode=revise" in body
    assert "latest_round" in body
    # existing guarantees still hold
    for token in ("publication/arxiv", "publication/anon", "code/", "blog/",
                  "can_promote", "[UNSUPPORTED]", "lint_anonymity", "confirm"):
        assert token in body


def test_write_skill_paper_structure_and_references():
    _, body = _parse_frontmatter("rx-write/SKILL.md")
    assert "## Paper structure" in body
    assert "story-board" in body
    assert "best-practices.md" in body
    assert "conference-outcome-lessons.md" in body
    assert "tone.md" in body
    assert "understated" in body.lower()
    assert "ping" in body.lower()
    assert "novel-but-empty" in body.lower()
    assert "framing" in body.lower() and "mechanism" in body.lower()
    for section in (
        "Abstract",
        "Introduction",
        "Method",
        "Experiments",
        "Related Work",
        "Limitations",
        "Conclusion and Future Work",
    ):
        assert section in body, f"missing outline section {section}"
    # Related Work comes after Method/Experiments inside the fenced outline
    fence_start = body.index("```text")
    outline = body[fence_start: body.index("```", fence_start + 3)]
    assert outline.index("Method") < outline.index("Related Work")
    assert outline.index("Experiments") < outline.index("Related Work")
    ref_dir = os.path.join(ROOT, "skills", "rx-write", "references")
    for name in (
        "best-practices.md",
        "tone.md",
        "conference-outcome-lessons.md",
        "paper-outline.md",
        "writing-craft.md",
        "abstract.md",
        "introduction.md",
        "related-work.md",
        "method.md",
        "experiments.md",
        "limitations-conclusion.md",
    ):
        path = os.path.join(ref_dir, name)
        assert os.path.isfile(path), f"missing reference guide {name}"
        assert f"references/{name}" in body
    shared = os.path.join(
        ROOT, "skills", "_shared", "references", "conference-outcome-lessons.md"
    )
    assert os.path.isfile(shared)


def test_ideate_survey_grill_use_conference_outcome_lessons():
    _, ideate = _parse_frontmatter("rx-ideate/SKILL.md")
    _, survey = _parse_frontmatter("rx-survey/SKILL.md")
    _, grill = _parse_frontmatter("rx-grill/SKILL.md")
    for body in (ideate, survey, grill):
        assert "conference-outcome-lessons" in body
        assert "bottleneck" in body.lower()
    assert "falsif" in ideate.lower()
    assert "novel-but-empty" in ideate.lower()
    assert "open-gap" in survey.lower() or "open gap" in survey.lower()
    assert "closest" in survey.lower()
    assert "collision" in grill.lower()
    assert "evidence_expectations" in grill
    assert "failure_mode" in grill.lower()
    assert "write_understanding" in grill


def test_ideate_and_spinoff_use_research_root():
    _, ideate = _parse_frontmatter("rx-ideate/SKILL.md")
    _, spinoff = _parse_frontmatter("rx-spinoff/SKILL.md")
    for body in (ideate, spinoff):
        assert "--topic" in body
        assert "llm-agents" in body
        assert "rx-projects/" in body  # explicitly forbidden


def test_spinoff_skill_frontmatter_and_content():
    front, body = _parse_frontmatter("rx-spinoff/SKILL.md")
    assert front["name"] == "rx-spinoff"
    assert front["model"] == "opus"
    assert front.get("description")
    for section in ("## Purpose", "## Steps", "## Outputs"):
        assert section in body, f"missing {section}"
    # seeds the pipeline via the existing helpers (no new rx_state code)
    assert "write_note" in body        # seed paper -> PaperNote
    assert "write_question" in body     # follow-up directions -> Q<n>
    # critical read + follow-up derivation
    assert "novelty" in body.lower()    # each direction carries a novelty delta
    assert "future work" in body.lower() or "future-work" in body.lower()
    # auto-continue but stop safely before compute
    assert "rx-pipeline" in body
    assert "plan lock" in body.lower()


def test_review_skill_persists_rounds():
    front, body = _parse_frontmatter("rx-review/SKILL.md")
    assert "write_round" in body
    assert ".rx/reviews/round-" in body


@pytest.mark.parametrize("name,model", [
    ("rx-ideate", "opus"), ("rx-survey", "sonnet"), ("rx-grill", "opus"),
    ("rx-plan", "sonnet"), ("rx-experiment", "sonnet"), ("rx-analyze", "opus"),
    ("rx-write", "sonnet"), ("rx-review", "opus"), ("rx-pipeline", "opus"),
    ("rx-spinoff", "opus"),
])
def test_all_skills_have_valid_frontmatter(name, model):
    front, body = _parse_frontmatter(f"{name}/SKILL.md")
    assert front["name"] == name
    assert front["model"] == model
    assert front.get("description")
    for section in ("## Purpose", "## Steps", "## Outputs"):
        assert section in body, f"{name} missing {section}"


def test_grill_skill_is_interactive_alignment():
    front, body = _parse_frontmatter("rx-grill/SKILL.md")
    assert front["name"] == "rx-grill"
    # core grill-me loop (Matt Pocock)
    assert "interview me relentlessly" in body.lower()
    assert "shared understanding" in body.lower()
    assert "recommended answer" in body.lower()
    assert "exploring the codebase" in body.lower()
    assert "write_understanding" in body
    assert "shared-understanding.md" in body
    # sits between survey and plan/experiment
    assert "survey" in body.lower() and "plan" in body.lower()
    # conference-outcome audit gate
    assert "collision" in body.lower()
    assert "diff_" in body or "four-axis" in body.lower() or "4-axis" in body.lower()


def test_pipeline_skill_covers_loop_and_gates():
    front, body = _parse_frontmatter("rx-pipeline/SKILL.md")
    assert front["name"] == "rx-pipeline"
    assert front["model"] == "opus"
    for section in ("## Purpose", "## Steps", "## Outputs", "## Loop"):
        assert section in body
    assert "stage_blockers" in body      # enforces blocker-first
    assert "loop_step" in body           # drives the loop
    assert "negative" in body.lower()    # negative results feed the loop
    assert "grill" in body.lower()       # alignment stage before plan


def test_pipeline_skill_covers_drafting_loop():
    front, body = _parse_frontmatter("rx-pipeline/SKILL.md")
    assert "## Drafting loop" in body
    assert "draft_loop_step" in body
    assert "stop_clean" in body and "stop_budget" in body
    assert "--mode=revise" in body
