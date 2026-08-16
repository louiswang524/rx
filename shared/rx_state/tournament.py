"""Tournament-mode candidate question ranking for rx-ideate --tournament."""

import os
from dataclasses import dataclass

RUBRIC_FIELDS = ("novelty", "feasibility", "falsifiability", "evidence_inspectability")


@dataclass
class CandidateScore:
    question_id: str
    novelty: int
    feasibility: int
    falsifiability: int
    evidence_inspectability: int
    rationale: str = ""

    def __post_init__(self) -> None:
        for name in RUBRIC_FIELDS:
            value = getattr(self, name)
            if not (0 <= value <= 3):
                raise ValueError(f"{name} must be 0-3, got {value}")

    @property
    def total(self) -> int:
        return sum(getattr(self, name) for name in RUBRIC_FIELDS)


def rank_candidates(scores: list[CandidateScore]) -> list[CandidateScore]:
    return sorted(scores, key=lambda s: s.total, reverse=True)


def write_tournament(rx_dir: str, scores: list[CandidateScore], winner_id: str) -> str:
    d = os.path.join(rx_dir, "ideate")
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, "tournament.md")
    lines = ["# Ideate tournament", "", f"winner: {winner_id}", ""]
    for s in rank_candidates(scores):
        lines.append(
            f"- {s.question_id}: total={s.total} "
            f"(novelty={s.novelty}, feasibility={s.feasibility}, "
            f"falsifiability={s.falsifiability}, "
            f"evidence_inspectability={s.evidence_inspectability})"
            + (f" — {s.rationale}" if s.rationale else "")
        )
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return path
