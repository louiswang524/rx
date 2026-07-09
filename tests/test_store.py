import os
from rx_state.schema import Claim
from rx_state.store import (
    default_state, load_state, save_state, write_claim, read_claim,
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
