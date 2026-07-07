from statistics import fmean, pstdev
from rx_state.schema import validate_outcome


def summarize_metric(values: list[float]) -> dict:
    if not values:
        return {"mean": 0.0, "std": 0.0, "n": 0}
    return {"mean": fmean(values),
            "std": pstdev(values) if len(values) > 1 else 0.0,
            "n": len(values)}


def beats_baseline(value: float, baseline: float, higher_is_better: bool) -> bool:
    return value > baseline if higher_is_better else value < baseline


def decide_outcome(value: float, baseline: float, higher_is_better: bool) -> str:
    outcome = "positive" if beats_baseline(value, baseline, higher_is_better) else "negative"
    validate_outcome(outcome)
    return outcome
