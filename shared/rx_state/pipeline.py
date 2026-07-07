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
