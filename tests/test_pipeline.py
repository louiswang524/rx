from rx_state.store import default_state
from rx_state.pipeline import next_stage, advance_stage, stage_blockers, loop_step, draft_loop_step
from rx_state.planlock import PlanLock, write_lock


def _loop(**kw):
    base = {"enabled": True, "iteration": 0, "max_iterations": 3,
            "no_improve_count": 0, "no_improve_limit": 2}
    base.update(kw)
    return base


def test_loop_stop_success_takes_priority():
    loop, action = loop_step(_loop(), improved=False, gate_cleared=True)
    assert action == "stop_success"
    assert loop["iteration"] == 1


def test_loop_continue_on_improvement():
    loop, action = loop_step(_loop(no_improve_count=1), improved=True, gate_cleared=False)
    assert action == "continue"
    assert loop["no_improve_count"] == 0     # reset on improvement


def test_loop_stop_no_improve():
    loop, action = loop_step(_loop(no_improve_count=1), improved=False, gate_cleared=False)
    assert action == "stop_no_improve"       # 1 -> 2 >= limit(2)
    assert loop["no_improve_count"] == 2


def test_loop_stop_budget():
    loop, action = loop_step(_loop(iteration=2, no_improve_count=0, no_improve_limit=5),
                             improved=True, gate_cleared=False)
    assert action == "stop_budget"           # iteration 2 -> 3 >= max(3)


def test_loop_step_does_not_mutate_input():
    original = _loop()
    loop_step(original, improved=False, gate_cleared=False)
    assert original["iteration"] == 0


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


def test_loop_gate_wins_over_all_limits():
    # iteration 2->3 (budget would trip), no_improve_count 1->2 (no_improve would trip),
    # but gate_cleared wins over both.
    _, action = loop_step(_loop(iteration=2, no_improve_count=1),
                          improved=False, gate_cleared=True)
    assert action == "stop_success"


def test_loop_no_improve_beats_budget():
    # both budget and no_improve trip this step; no_improve is checked first.
    _, action = loop_step(_loop(iteration=2, no_improve_count=1),
                          improved=False, gate_cleared=False)
    assert action == "stop_no_improve"


def _draft(**kw):
    base = {"iteration": 0, "max_draft_iters": 3}
    base.update(kw)
    return base


def test_draft_loop_stop_clean_on_accept():
    dl, action = draft_loop_step(_draft(), "accept")
    assert action == "stop_clean"
    assert dl["iteration"] == 1


def test_draft_loop_stop_clean_on_minor_revision():
    _, action = draft_loop_step(_draft(), "minor revision")
    assert action == "stop_clean"


def test_draft_loop_continue_on_reject_under_budget():
    dl, action = draft_loop_step(_draft(iteration=0), "reject")
    assert action == "continue"
    assert dl["iteration"] == 1


def test_draft_loop_stop_budget_on_persistent_reject():
    dl, action = draft_loop_step(_draft(iteration=2, max_draft_iters=3), "reject")
    assert action == "stop_budget"
    assert dl["iteration"] == 3


def test_draft_loop_reject_then_accept_one_revise_cycle():
    # behavioral spine: one reject drives one revise, then accept stops clean
    dl = _draft(max_draft_iters=5)
    dl, a1 = draft_loop_step(dl, "reject")
    assert a1 == "continue"          # -> triggers one rx-write --mode=revise
    dl, a2 = draft_loop_step(dl, "accept")
    assert a2 == "stop_clean"
    assert dl["iteration"] == 2
