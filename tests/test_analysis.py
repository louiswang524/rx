from rx_state.analysis import summarize_metric, beats_baseline, decide_outcome


def test_summarize_metric():
    s = summarize_metric([0.10, 0.20, 0.30])
    assert s["n"] == 3
    assert abs(s["mean"] - 0.20) < 1e-9
    assert s["std"] > 0
    empty = summarize_metric([])
    assert empty == {"mean": 0.0, "std": 0.0, "n": 0}


def test_beats_baseline_both_directions():
    assert beats_baseline(0.25, 0.20, higher_is_better=True) is True
    assert beats_baseline(0.25, 0.20, higher_is_better=False) is False
    assert beats_baseline(0.15, 0.20, higher_is_better=False) is True


def test_decide_outcome_returns_valid_outcome():
    assert decide_outcome(0.25, 0.20, True) == "positive"
    assert decide_outcome(0.15, 0.20, True) == "negative"
