from rx_state.store import default_state
from rx_state.pipeline import next_stage, advance_stage, stage_blockers
from rx_state.planlock import PlanLock, write_lock


def test_next_stage_walks_the_pipeline():
    assert next_stage("ideate") == "survey"
    assert next_stage("write") == "review"
    assert next_stage("review") == "done"
    assert next_stage("done") == "done"


def test_advance_stage_is_pure():
    st = default_state("p", "/kb")           # stage == "ideate"
    nxt = advance_stage(st)
    assert nxt["stage"] == "survey"
    assert st["stage"] == "ideate"           # original unchanged


def test_experiment_blocked_until_locked(tmp_path):
    rx = str(tmp_path)
    blockers = stage_blockers(rx, "experiment")
    assert blockers and any("lock" in b for b in blockers)
    write_lock(rx, PlanLock(metric="recall@20", higher_is_better=True,
                            comparison_family=["ours"], seed_policy=2, baselines=["SASRec"]))
    assert stage_blockers(rx, "experiment") == []


def test_other_stages_have_no_blockers(tmp_path):
    assert stage_blockers(str(tmp_path), "survey") == []
    assert stage_blockers(str(tmp_path), "write") == []
