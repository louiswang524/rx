import os
from rx_state.schema import Claim
from rx_state.store import (
    default_state, load_state, save_state, write_claim, read_claim, append_autonomy_log,
)


def test_default_state_shape():
    st = default_state("recsys-proj", "/home/u/.rx-kb")
    assert st["project"] == "recsys-proj"
    assert st["kb_path"] == "/home/u/.rx-kb"
    assert st["stage"] == "ideate"
    assert st["loop"] == {
        "enabled": False, "iteration": 0, "max_iterations": 20,
        "no_improve_count": 0, "no_improve_limit": 5,
    }
    assert st["artifacts"] == {"questions": [], "evidence": [], "claims": [], "experiments": []}


def test_state_roundtrip(tmp_path):
    rx_dir = str(tmp_path)
    st = default_state("p", "/kb")
    st["stage"] = "experiment"
    save_state(rx_dir, st)
    assert os.path.exists(os.path.join(rx_dir, "state.json"))
    assert load_state(rx_dir)["stage"] == "experiment"


def test_claim_roundtrip(tmp_path):
    rx_dir = str(tmp_path)
    claim = Claim(id="C1", text="X helps recall@20", strength="supported",
                  evidence_ids=["E1", "E2"], question_id="Q1")
    path = write_claim(rx_dir, claim)
    assert path.endswith(os.path.join("claims", "C1.md"))
    back = read_claim(path)
    assert back == claim


def test_claim_roundtrip_none_question(tmp_path):
    claim = Claim(id="C9", text="baseline holds", strength="speculative",
                  evidence_ids=[], question_id=None)
    back = read_claim(write_claim(str(tmp_path), claim))
    assert back == claim


def test_default_state_has_draft_loop():
    st = default_state("p", "/kb")
    assert st["draft_loop"] == {"iteration": 0, "max_draft_iters": 5}


def test_default_state_has_autonomous_fields():
    st = default_state("p", "/kb")
    assert st["autonomous"] is False
    assert st["autonomous_started_at"] is None
    assert st["max_hours"] is None


def test_append_autonomy_log_creates_file_with_timestamped_line(tmp_path):
    rx_dir = str(tmp_path)
    path = append_autonomy_log(rx_dir, "self-grill completed", now="2026-08-15T00:00:00+00:00")
    assert path == os.path.join(rx_dir, "autonomy-log.md")
    content = open(path, encoding="utf-8").read()
    assert content == "- 2026-08-15T00:00:00+00:00 self-grill completed\n"


def test_append_autonomy_log_appends_multiple_lines(tmp_path):
    rx_dir = str(tmp_path)
    append_autonomy_log(rx_dir, "first", now="2026-08-15T00:00:00+00:00")
    append_autonomy_log(rx_dir, "second", now="2026-08-15T01:00:00+00:00")
    lines = open(os.path.join(rx_dir, "autonomy-log.md"), encoding="utf-8").read().splitlines()
    assert lines == [
        "- 2026-08-15T00:00:00+00:00 first",
        "- 2026-08-15T01:00:00+00:00 second",
    ]
