import json
import os
import subprocess

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "bootstrap.sh")


def test_bootstrap_scaffolds_project(tmp_path):
    proj = tmp_path / "myproj"
    kb = tmp_path / "kb"
    subprocess.run(["bash", SCRIPT, str(proj), "myproj", str(kb)], check=True)

    assert (proj / ".git").is_dir()
    for d in (
        "code",
        "writings",
        "experiments",
        "notes",
        "publication/arxiv",
        "publication/anon",
        ".rx/questions",
        ".rx/evidence",
        ".rx/claims",
        ".rx/experiments",
    ):
        assert (proj / d).is_dir(), d
    assert (proj / "PROJECT.md").is_file()

    state = json.loads((proj / ".rx" / "state.json").read_text())
    assert state["project"] == "myproj"
    assert state["stage"] == "ideate"
    assert state["kb_path"] == str(kb)
    assert state["loop"] == {
        "enabled": False, "iteration": 0, "max_iterations": 20,
        "no_improve_count": 0, "no_improve_limit": 5,
    }
    assert state["artifacts"] == {
        "questions": [], "evidence": [], "claims": [], "experiments": [],
    }

    # first commit exists
    log = subprocess.run(["git", "-C", str(proj), "log", "--oneline"],
                         capture_output=True, text=True, check=True)
    assert log.stdout.strip() != ""


def test_bootstrap_under_research_topic(tmp_path, monkeypatch):
    research = tmp_path / "research"
    kb = tmp_path / "kb"
    monkeypatch.setenv("RX_RESEARCH_ROOT", str(research))

    subprocess.run(
        ["bash", SCRIPT, "dawn-memory", "--topic", "llm-agents", str(kb)],
        check=True,
    )

    proj = research / "llm-agents" / "dawn-memory"
    assert (proj / "PROJECT.md").is_file()
    assert (proj / "publication" / "arxiv").is_dir()
    assert (proj / "code").is_dir()
    assert (proj / ".rx" / "state.json").is_file()

    root_file = (kb / "research_root").read_text(encoding="utf-8").strip()
    assert root_file == str(research)

    text = (proj / "PROJECT.md").read_text(encoding="utf-8")
    assert "llm-agents" in text


def test_bootstrap_shares_one_venv_across_projects(tmp_path):
    kb = tmp_path / "kb"
    proj_a = tmp_path / "proja"
    proj_b = tmp_path / "projb"
    subprocess.run(["bash", SCRIPT, str(proj_a), "proja", str(kb)], check=True)
    subprocess.run(["bash", SCRIPT, str(proj_b), "projb", str(kb)], check=True)

    shared_venv = kb / "venv"
    assert shared_venv.is_dir()
    assert os.path.realpath(proj_a / ".venv") == os.path.realpath(shared_venv)
    assert os.path.realpath(proj_b / ".venv") == os.path.realpath(shared_venv)
