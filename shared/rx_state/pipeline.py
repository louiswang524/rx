import copy
from rx_state.schema import STAGES


def next_stage(current: str) -> str:
    idx = STAGES.index(current)
    return STAGES[idx + 1] if idx + 1 < len(STAGES) else "done"


def advance_stage(state: dict) -> dict:
    new_state = copy.deepcopy(state)
    new_state["stage"] = next_stage(state["stage"])
    return new_state
