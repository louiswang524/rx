import json
import os
import subprocess

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "bootstrap.sh")


def test_bootstrap_scaffolds_project(tmp_path):
    proj = tmp_path / "myproj"
    kb = tmp_path / "kb"
    subprocess.run(["bash", SCRIPT, str(proj), "myproj", str(kb)], check=True)

    assert (proj / ".git").is_dir()
    for d in ("experiments", "notes", "paper/arxiv", "paper/anon",
              ".rx/questions", ".rx/evidence", ".rx/claims", ".rx/experiments"):
        assert (proj / d).is_dir(), d
    assert (proj / "PROJECT.md").is_file()

    state = json.loads((proj / ".rx" / "state.json").read_text())
    assert state["project"] == "myproj"
    assert state["stage"] == "ideate"
    assert state["kb_path"] == str(kb)

    # first commit exists
    log = subprocess.run(["git", "-C", str(proj), "log", "--oneline"],
                         capture_output=True, text=True, check=True)
    assert log.stdout.strip() != ""
