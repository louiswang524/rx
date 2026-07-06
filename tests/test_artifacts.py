import os
from rx_state.schema import Question, Evidence
from rx_state.store import (
    write_question, read_question, write_evidence, read_evidence, list_artifacts,
)


def test_question_roundtrip(tmp_path):
    q = Question(id="Q1", text="Does gating improve recall@20?", gap="no prior ablation")
    back = read_question(write_question(str(tmp_path), q))
    assert back == q


def test_evidence_roundtrip(tmp_path):
    e = Evidence(id="E1", outcome="negative", experiment_id="EXP1", note="no gain")
    back = read_evidence(write_evidence(str(tmp_path), e))
    assert back == e


def test_list_artifacts_sorted(tmp_path):
    write_question(str(tmp_path), Question(id="Q2", text="b"))
    write_question(str(tmp_path), Question(id="Q1", text="a"))
    paths = list_artifacts(str(tmp_path), "questions")
    assert [os.path.basename(p) for p in paths] == ["Q1.md", "Q2.md"]
