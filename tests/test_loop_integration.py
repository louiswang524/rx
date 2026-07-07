from rx_state.pipeline import loop_step, advance_stage
from rx_state.store import default_state


def test_loop_runs_until_success():
    # start a loop; two negative iterations, then a gate-clearing one
    loop = {"enabled": True, "iteration": 0, "max_iterations": 10,
            "no_improve_count": 0, "no_improve_limit": 5}
    loop, a1 = loop_step(loop, improved=False, gate_cleared=False)
    assert a1 == "continue"
    loop, a2 = loop_step(loop, improved=True, gate_cleared=False)   # progress, no gate yet
    assert a2 == "continue" and loop["no_improve_count"] == 0
    loop, a3 = loop_step(loop, improved=True, gate_cleared=True)    # clears the gate
    assert a3 == "stop_success"
    assert loop["iteration"] == 3


def test_loop_gives_up_after_no_improvement():
    loop = {"enabled": True, "iteration": 0, "max_iterations": 100,
            "no_improve_count": 0, "no_improve_limit": 2}
    loop, _ = loop_step(loop, improved=False, gate_cleared=False)   # count 1
    loop, action = loop_step(loop, improved=False, gate_cleared=False)  # count 2 >= 2
    assert action == "stop_no_improve"


def test_stage_advance_reaches_done():
    st = default_state("p", "/kb")
    for _ in range(len(("ideate survey plan experiment analyze write review").split())):
        st = advance_stage(st)
    assert st["stage"] == "done"
