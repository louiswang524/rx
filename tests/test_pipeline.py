from rx_state.store import default_state
from rx_state.pipeline import next_stage, advance_stage


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
