import copy
from rx_state.schema import STAGES
from rx_state.planlock import is_locked


def next_stage(current: str) -> str:
    idx = STAGES.index(current)
    return STAGES[idx + 1] if idx + 1 < len(STAGES) else "done"


def advance_stage(state: dict) -> dict:
    new_state = copy.deepcopy(state)
    new_state["stage"] = next_stage(state["stage"])
    return new_state


def stage_blockers(rx_dir: str, stage: str) -> list[str]:
    if stage == "experiment" and not is_locked(rx_dir):
        return ["experiment requires a plan lock (run rx-plan first)"]
    return []


def loop_step(loop: dict, improved: bool, gate_cleared: bool) -> tuple[dict, str]:
    loop = copy.deepcopy(loop)
    loop["iteration"] = loop.get("iteration", 0) + 1

    if gate_cleared:
        return loop, "stop_success"

    if improved:
        loop["no_improve_count"] = 0
    else:
        loop["no_improve_count"] = loop.get("no_improve_count", 0) + 1

    if loop["no_improve_count"] >= loop.get("no_improve_limit", 5):
        return loop, "stop_no_improve"
    if loop["iteration"] >= loop.get("max_iterations", 20):
        return loop, "stop_budget"
    return loop, "continue"
