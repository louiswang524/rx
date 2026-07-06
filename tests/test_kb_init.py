import os
import subprocess

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "kb-init.sh")


def test_kb_init_creates_tree(tmp_path):
    kb = tmp_path / "kb"
    subprocess.run(["bash", SCRIPT, str(kb)], check=True)
    for sub in ("system", "secrets", "pitfalls", "learnings", "env"):
        assert (kb / sub).is_dir()
    assert (kb / "index.md").is_file()
    assert (kb / "system" / "system.md").is_file()
    gi = (kb / ".gitignore").read_text()
    assert "secrets/" in gi


def test_kb_init_is_idempotent(tmp_path):
    kb = tmp_path / "kb"
    subprocess.run(["bash", SCRIPT, str(kb)], check=True)
    subprocess.run(["bash", SCRIPT, str(kb)], check=True)  # second run must not fail
    assert (kb / "index.md").is_file()
