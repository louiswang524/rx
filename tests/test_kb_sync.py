import os
import subprocess

INIT = os.path.join(os.path.dirname(__file__), "..", "scripts", "kb-init.sh")
SYNC = os.path.join(os.path.dirname(__file__), "..", "scripts", "kb-sync.sh")


def test_kb_sync_promotes_notes(tmp_path):
    kb = tmp_path / "kb"
    subprocess.run(["bash", INIT, str(kb)], check=True)

    proj = tmp_path / "proj"
    (proj / "notes" / "pitfalls").mkdir(parents=True)
    (proj / "notes" / "learnings").mkdir(parents=True)
    (proj / "notes" / "pitfalls" / "oom.md").write_text("batch too big -> OOM on 8GB")
    (proj / "notes" / "learnings" / "amp.md").write_text("bf16 amp stable for this model")

    subprocess.run(["bash", SYNC, str(proj), str(kb)], check=True)

    assert (kb / "pitfalls" / "proj__oom.md").read_text() == "batch too big -> OOM on 8GB"
    assert (kb / "learnings" / "proj__amp.md").read_text() == "bf16 amp stable for this model"


def test_kb_sync_skips_missing_dirs(tmp_path):
    kb = tmp_path / "kb"
    subprocess.run(["bash", INIT, str(kb)], check=True)
    proj = tmp_path / "empty"
    proj.mkdir()
    subprocess.run(["bash", SYNC, str(proj), str(kb)], check=True)  # must not fail
