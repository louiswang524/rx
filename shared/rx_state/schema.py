from dataclasses import dataclass, field

STRENGTHS = ("speculative", "supported", "strong")
OUTCOMES = ("positive", "negative", "inconclusive")
STAGES = ("ideate", "survey", "plan", "experiment", "analyze", "write", "review", "done")


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


@dataclass
class Evidence:
    id: str
    outcome: str
    experiment_id: str | None = None
    note: str = ""

    def __post_init__(self) -> None:
        validate_outcome(self.outcome)


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
