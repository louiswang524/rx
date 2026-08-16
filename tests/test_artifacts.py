import os
from rx_state.schema import Question, Evidence
from rx_state.store import (
    write_question, read_question, write_evidence, read_evidence, list_artifacts,
)


def test_question_roundtrip(tmp_path):
    q = Question(id="Q1", text="Does gating improve recall@20?", gap="no prior ablation")
    back = read_question(write_question(str(tmp_path), q))
    assert back == q


def test_question_roundtrip_with_lineage(tmp_path):
    q = Question(id="Q2", text="Does a longer context window help?", gap="untested",
                 parent_evidence_id="E1")
    back = read_question(write_question(str(tmp_path), q))
    assert back == q


def test_evidence_roundtrip(tmp_path):
    e = Evidence(id="E1", outcome="negative", experiment_id="EXP1", note="no gain")
    back = read_evidence(write_evidence(str(tmp_path), e))
    assert back == e


def test_evidence_roundtrip_with_sub_outcomes(tmp_path):
    e = Evidence(id="E2", outcome="inconclusive", experiment_id="EXP1", note="mixed by size",
                 sub_outcomes={"size=1024": "positive", "size=4096": "negative"})
    back = read_evidence(write_evidence(str(tmp_path), e))
    assert back == e


def test_legacy_evidence_without_sub_outcomes_defaults_empty(tmp_path):
    path = str(tmp_path / "legacy.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("---\nid: E1\noutcome: positive\nexperiment_id: EXP1\n---\n\nnote text\n")
    back = read_evidence(path)
    assert back.sub_outcomes == {}


def test_list_artifacts_sorted(tmp_path):
    write_question(str(tmp_path), Question(id="Q2", text="b"))
    write_question(str(tmp_path), Question(id="Q1", text="a"))
    paths = list_artifacts(str(tmp_path), "questions")
    assert [os.path.basename(p) for p in paths] == ["Q1.md", "Q2.md"]
