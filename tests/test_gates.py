from rx_state.schema import Claim, Evidence, Experiment
from rx_state.gates import evaluate_gate, can_promote


def _linked_experiments(evidence, experiments):
    return experiments


def test_speculative_when_no_positive_evidence():
    claim = Claim(id="C1", text="X helps", strength="speculative", evidence_ids=["E1"])
    ev = [Evidence(id="E1", outcome="negative", experiment_id="EXP1")]
    exps = [Experiment(id="EXP1", seeds=[0])]
    met, _ = evaluate_gate(claim, ev, exps)
    assert met == "speculative"


def test_supported_with_one_positive_experiment():
    claim = Claim(id="C1", text="X helps", strength="supported", evidence_ids=["E1"])
    ev = [Evidence(id="E1", outcome="positive", experiment_id="EXP1")]
    exps = [Experiment(id="EXP1", seeds=[0], baseline="SASRec", commit="abc")]
    met, _ = evaluate_gate(claim, ev, exps)
    assert met == "supported"
    assert can_promote(claim, ev, exps) is True


def test_strong_requires_two_seeds_baseline_and_commit():
    claim = Claim(id="C1", text="X helps", strength="strong", evidence_ids=["E1"])
    ev = [Evidence(id="E1", outcome="positive", experiment_id="EXP1")]
    weak = [Experiment(id="EXP1", seeds=[0], baseline="SASRec", commit="abc")]
    met, reasons = evaluate_gate(claim, ev, weak)
    assert met == "supported"          # only 1 seed -> not strong
    assert can_promote(claim, ev, weak) is False
    assert any("seed" in r for r in reasons)

    strong = [Experiment(id="EXP1", seeds=[0, 1], baseline="SASRec", commit="abc")]
    met2, _ = evaluate_gate(claim, ev, strong)
    assert met2 == "strong"
    assert can_promote(claim, ev, strong) is True


def test_positive_evidence_without_experiment_is_not_supported():
    claim = Claim(id="C1", text="X helps", strength="supported", evidence_ids=["E1"])
    ev = [Evidence(id="E1", outcome="positive", experiment_id=None)]  # no linked experiment
    met, reasons = evaluate_gate(claim, ev, [])
    assert met == "speculative"
    assert can_promote(claim, ev, []) is False
    assert any("experiment" in r for r in reasons)
