import pytest
from rx_state.schema import (
    STRENGTHS, OUTCOMES, STAGES,
    Experiment, Evidence, Claim,
    validate_strength, validate_outcome,
)


def test_constant_literals():
    assert STRENGTHS == ("speculative", "supported", "strong")
    assert OUTCOMES == ("positive", "negative", "inconclusive")
    assert STAGES[0] == "ideate" and STAGES[-1] == "done"
    assert STAGES == (
        "ideate", "survey", "grill", "plan", "experiment",
        "analyze", "write", "review", "done",
    )


def test_dataclasses_construct():
    exp = Experiment(id="EXP1", seeds=[0, 1], baseline="SASRec", commit="abc123")
    ev = Evidence(id="E1", outcome="positive", experiment_id="EXP1", note="beats baseline")
    c = Claim(id="C1", text="X helps", strength="supported", evidence_ids=["E1"], question_id="Q1")
    assert exp.seeds == [0, 1]
    assert ev.outcome == "positive"
    assert c.evidence_ids == ["E1"]


def test_experiment_repeat_count_defaults_zero():
    exp = Experiment(id="EXP1", seeds=[0])
    assert exp.repeat_count == 0
    assert Experiment(id="EXP2", seeds=[], repeat_count=20).repeat_count == 20


def test_evidence_sub_outcomes_default_empty_and_roundtrip():
    ev = Evidence(id="E1", outcome="inconclusive")
    assert ev.sub_outcomes == {}
    mixed = Evidence(id="E2", outcome="inconclusive",
                      sub_outcomes={"size=1024": "positive", "size=4096": "negative"})
    assert mixed.sub_outcomes["size=1024"] == "positive"


def test_evidence_sub_outcomes_validates_each_value():
    with pytest.raises(ValueError):
        Evidence(id="E1", outcome="positive", sub_outcomes={"a": "meh"})


def test_validators_reject_bad_values():
    with pytest.raises(ValueError):
        validate_strength("kinda-strong")
    with pytest.raises(ValueError):
        validate_outcome("meh")
    validate_strength("strong")   # no raise
    validate_outcome("negative")  # no raise
