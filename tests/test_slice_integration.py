from rx_state.schema import Question, Evidence, Experiment, Claim
from rx_state.store import write_question, write_evidence, read_evidence, list_artifacts
from rx_state.capture import capture_run, load_experiment
from rx_state.gates import can_promote
from rx_state.anonymize import anonymize_text, lint_anonymity
from rx_state.reproduce import render_reproduce


def test_spine_end_to_end(tmp_path):
    rx = str(tmp_path)
    # ideate
    write_question(rx, Question(id="Q1", text="Does gating help?", gap="no ablation"))
    # experiment (2 seeds, baseline, commit -> strong-eligible)
    capture_run(rx, "EXP1", seeds=[0, 1], baseline="SASRec",
                config={"lr": 1e-3}, commit="abc1234", gpu="RTX 4090",
                goal="Does gating help recall?", changes="Added gating vs SASRec",
                result="recall@10 +2%", conclusion="Positive, promotable",
                next_steps="Add ablation for gating variant")
    exp = load_experiment(rx, "EXP1")
    # evidence
    write_evidence(rx, Evidence(id="E1", outcome="positive", experiment_id="EXP1", note="+2%"))
    ev = [read_evidence(p) for p in list_artifacts(rx, "evidence")]
    # gate: a 'strong' claim is promotable given 2 seeds + baseline + commit
    strong_claim = Claim(id="C1", text="gating improves recall", strength="strong",
                         evidence_ids=["E1"])
    assert can_promote(strong_claim, ev, [exp]) is True
    # anonymize + lint
    src = "Louis Wang shows our prior work at github.com/louis/rx."
    anon = anonymize_text(src, ["Louis Wang"], ["github.com/louis/rx"])
    assert lint_anonymity(anon, ["Louis Wang"], ["github.com/louis/rx"]) == []
    # reproduce
    md = render_reproduce([exp], "python train.py")
    assert "python train.py --seed 0" in md
