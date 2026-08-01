from rx_state.grill import (
    SharedUnderstanding,
    write_understanding,
    read_understanding,
    is_grilled,
)


def test_is_grilled_false_until_written(tmp_path):
    rx = str(tmp_path)
    assert is_grilled(rx) is False
    write_understanding(rx, SharedUnderstanding(
        primary_question_id="Q1",
        novelty_gap="no prior work on X under metric Y",
        metric_intent="recall@20 (higher better)",
        baselines=["SASRec"],
        falsifiers=["no lift vs SASRec on 2 seeds"],
        scope_cuts=["no claim about production latency"],
        machine_time_budget="~20 GPU-hours",
        open_risks=["dataset leakage"],
        summary="We will test whether X improves recall@20 vs SASRec.",
    ))
    assert is_grilled(rx) is True


def test_roundtrip_understanding(tmp_path):
    rx = str(tmp_path)
    original = SharedUnderstanding(
        primary_question_id="Q2",
        novelty_gap="gap",
        metric_intent="NDCG@10",
        baselines=["A", "B"],
        falsifiers=["flat ablation"],
        scope_cuts=["no multi-lingual claim"],
        machine_time_budget="10 iters",
        open_risks=["seed variance"],
        summary="Agreed design for Q2.",
    )
    path = write_understanding(rx, original)
    assert path.endswith("shared-understanding.md")
    loaded = read_understanding(rx)
    assert loaded.primary_question_id == "Q2"
    assert loaded.baselines == ["A", "B"]
    assert loaded.falsifiers == ["flat ablation"]
    assert "Agreed design" in loaded.summary
