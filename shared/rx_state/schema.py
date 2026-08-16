from dataclasses import dataclass, field

STRENGTHS = ("speculative", "supported", "strong")
OUTCOMES = ("positive", "negative", "inconclusive")
STAGES = (
    "ideate",
    "survey",
    "grill",
    "plan",
    "experiment",
    "analyze",
    "write",
    "review",
    "done",
)


def validate_strength(s: str) -> None:
    if s not in STRENGTHS:
        raise ValueError(f"invalid strength {s!r}; expected one of {STRENGTHS}")


def validate_outcome(o: str) -> None:
    if o not in OUTCOMES:
        raise ValueError(f"invalid outcome {o!r}; expected one of {OUTCOMES}")


@dataclass
class Experiment:
    id: str
    seeds: list[int] = field(default_factory=list)
    baseline: str | None = None
    commit: str | None = None
    # Repeat-based reliability (e.g. N timed benchmark runs) for experiments with no
    # meaningful RNG-seed axis -- deterministic-input timing/config sweeps, not stochastic
    # training. Distinct from `seeds`: use whichever reliability mechanism actually applies;
    # `evaluate_gate` accepts either toward the "strong" tier's >=2 requirement.
    repeat_count: int = 0


@dataclass
class Evidence:
    id: str
    outcome: str
    experiment_id: str | None = None
    note: str = ""
    # Optional per-condition breakdown (e.g. {"size=1024": "positive", "size=4096":
    # "negative"}) for a result that's genuinely mixed across sub-conditions rather than a
    # single positive/negative/inconclusive verdict. `outcome` stays the honest top-level
    # call (often "inconclusive" for a mixed result); `sub_outcomes` lets `evaluate_gate`
    # still recognize real positive signal underneath instead of treating the whole record
    # as having none.
    sub_outcomes: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        validate_outcome(self.outcome)
        for v in self.sub_outcomes.values():
            validate_outcome(v)


@dataclass
class Claim:
    id: str
    text: str
    strength: str
    evidence_ids: list[str] = field(default_factory=list)
    question_id: str | None = None

    def __post_init__(self) -> None:
        validate_strength(self.strength)


@dataclass
class Question:
    id: str
    text: str
    gap: str = ""
    parent_evidence_id: str | None = None
