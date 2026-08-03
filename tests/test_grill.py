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
        diff_framing="same task, stricter constraint",
        diff_mechanism="new routing operator",
        diff_insight="sparsity explains the gain",
        diff_domain="long-context only",
        collision_threats=["PaperX 2024"],
        evidence_expectations=["Table 1 vs PaperX on NDCG@10"],
        failure_mode_checks=["not novel-but-empty"],
        summary="Agreed design for Q2.",
    )
    path = write_understanding(rx, original)
    assert path.endswith("shared-understanding.md")
    loaded = read_understanding(rx)
    assert loaded.primary_question_id == "Q2"
    assert loaded.baselines == ["A", "B"]
    assert loaded.falsifiers == ["flat ablation"]
    assert loaded.diff_mechanism == "new routing operator"
    assert loaded.collision_threats == ["PaperX 2024"]
    assert loaded.evidence_expectations == ["Table 1 vs PaperX on NDCG@10"]
    assert "Agreed design" in loaded.summary


def test_legacy_understanding_without_new_fields_still_loads(tmp_path):
    rx = str(tmp_path / "rx")
    grill = tmp_path / "rx" / "grill"
    grill.mkdir(parents=True)
    (grill / "shared-understanding.md").write_text(
        "---\n"
        "primary_question_id: Q1\n"
        "novelty_gap: old\n"
        "metric_intent: acc\n"
        "baselines: [B]\n"
        "falsifiers: [f]\n"
        "scope_cuts: []\n"
        "machine_time_budget: 1h\n"
        "open_risks: []\n"
        "---\n\n"
        "Legacy summary.\n",
        encoding="utf-8",
    )
    loaded = read_understanding(str(tmp_path / "rx"))
    assert loaded.primary_question_id == "Q1"
    assert loaded.diff_mechanism == ""
    assert loaded.collision_threats == []
    assert "Legacy summary" in loaded.summary
