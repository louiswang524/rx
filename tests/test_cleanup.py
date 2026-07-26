import os

from rx_state.cleanup import (
    cleanup_candidates, delete_candidates, dir_size, find_checkpoint_dirs,
    find_log_dirs, format_report, promoted_experiment_ids,
)
from rx_state.schema import Claim, Evidence
from rx_state.store import write_claim, write_evidence


def _make_project(tmp_path):
    proj = tmp_path / "proj"
    rx_dir = proj / ".rx"
    (proj / "experiments" / "EXP1" / "checkpoints").mkdir(parents=True)
    (proj / "experiments" / "EXP1" / "checkpoints" / "model.bin").write_bytes(b"x" * 1000)
    (proj / "experiments" / "EXP2" / "checkpoints").mkdir(parents=True)
    (proj / "experiments" / "EXP2" / "checkpoints" / "model.bin").write_bytes(b"x" * 2000)
    return str(proj), str(rx_dir)


def test_dir_size_sums_files(tmp_path):
    proj, _ = _make_project(tmp_path)
    size = dir_size(os.path.join(proj, "experiments", "EXP2", "checkpoints"))
    assert size == 2000


def test_find_checkpoint_dirs(tmp_path):
    proj, _ = _make_project(tmp_path)
    dirs = find_checkpoint_dirs(proj)
    assert len(dirs) == 2
    assert all(d.endswith("checkpoints") for d in dirs)


def test_find_log_dirs_excludes_rx_and_git(tmp_path):
    proj, rx_dir = _make_project(tmp_path)
    (proj_wandb := os.path.join(proj, "wandb")) and os.makedirs(proj_wandb)
    (os.path.join(rx_dir, "experiments", "EXP1", "wandb"))
    os.makedirs(os.path.join(rx_dir, "experiments", "EXP1", "wandb"))
    os.makedirs(os.path.join(proj, ".git", "wandb"))

    found = find_log_dirs(proj)
    assert found == [proj_wandb]


def test_promoted_experiment_ids_only_supported_or_strong(tmp_path):
    proj, rx_dir = _make_project(tmp_path)
    write_evidence(rx_dir, Evidence(id="E1", outcome="positive", experiment_id="EXP1"))
    write_evidence(rx_dir, Evidence(id="E2", outcome="negative", experiment_id="EXP2"))
    write_claim(rx_dir, Claim(id="C1", text="works", strength="strong", evidence_ids=["E1"]))

    assert promoted_experiment_ids(rx_dir) == {"EXP1"}


def test_cleanup_candidates_protects_promoted_experiment(tmp_path):
    proj, rx_dir = _make_project(tmp_path)
    write_evidence(rx_dir, Evidence(id="E1", outcome="positive", experiment_id="EXP1"))
    write_evidence(rx_dir, Evidence(id="E2", outcome="negative", experiment_id="EXP2"))
    write_claim(rx_dir, Claim(id="C1", text="works", strength="strong", evidence_ids=["E1"]))

    candidates = cleanup_candidates(proj, rx_dir)
    by_exp = {c.experiment_id: c for c in candidates if c.kind == "checkpoints"}
    assert by_exp["EXP1"].protected is True
    assert by_exp["EXP2"].protected is False


def test_delete_candidates_skips_protected(tmp_path):
    proj, rx_dir = _make_project(tmp_path)
    write_evidence(rx_dir, Evidence(id="E1", outcome="positive", experiment_id="EXP1"))
    write_claim(rx_dir, Claim(id="C1", text="works", strength="strong", evidence_ids=["E1"]))

    candidates = cleanup_candidates(proj, rx_dir)
    deleted = delete_candidates(candidates)

    exp1_dir = os.path.join(proj, "experiments", "EXP1", "checkpoints")
    exp2_dir = os.path.join(proj, "experiments", "EXP2", "checkpoints")
    assert exp1_dir not in deleted
    assert exp2_dir in deleted
    assert os.path.isdir(exp1_dir)
    assert not os.path.isdir(exp2_dir)


def test_format_report_tags_protected_and_candidate(tmp_path):
    proj, rx_dir = _make_project(tmp_path)
    write_evidence(rx_dir, Evidence(id="E1", outcome="positive", experiment_id="EXP1"))
    write_claim(rx_dir, Claim(id="C1", text="works", strength="strong", evidence_ids=["E1"]))

    report = format_report(cleanup_candidates(proj, rx_dir))
    assert "PROTECTED" in report
    assert "candidate" in report


def test_format_report_empty():
    assert format_report([]) == "No cleanup candidates found."
