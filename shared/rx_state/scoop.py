"""Re-scoop checks: periodic mid-loop collision search against the locked question."""

import glob
import os
from dataclasses import dataclass, field

import yaml


@dataclass
class ScoopCheck:
    iteration: int
    checked_at: str
    verdict: str = "clear"  # "clear" | "potential_collision"
    findings: list[str] = field(default_factory=list)


def scoop_recheck_due(iteration: int, every: int = 3) -> bool:
    return iteration > 0 and iteration % every == 0


def _dir(rx_dir: str) -> str:
    return os.path.join(rx_dir, "scoop-checks")


def write_scoop_check(rx_dir: str, check: ScoopCheck) -> str:
    d = _dir(rx_dir)
    os.makedirs(d, exist_ok=True)
    front = {"iteration": check.iteration, "checked_at": check.checked_at, "verdict": check.verdict}
    path = os.path.join(d, f"iter-{check.iteration}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(yaml.safe_dump(front, sort_keys=False))
        f.write("---\n\n")
        if check.findings:
            for line in check.findings:
                f.write(f"- {line}\n")
        else:
            f.write("No new potentially-colliding papers found.\n")
    return path


def read_scoop_check(path: str) -> ScoopCheck:
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    _, front_block, body = raw.split("---", 2)
    front = yaml.safe_load(front_block)
    findings = [line[2:] for line in body.strip().splitlines() if line.startswith("- ")]
    return ScoopCheck(
        iteration=front["iteration"],
        checked_at=front["checked_at"],
        verdict=front.get("verdict") or "clear",
        findings=findings,
    )


def list_scoop_checks(rx_dir: str) -> list[ScoopCheck]:
    return [read_scoop_check(p) for p in sorted(glob.glob(os.path.join(_dir(rx_dir), "iter-*.md")))]


def known_paper_keys(rx_dir: str) -> set[str]:
    """Keys rx-survey already surfaced (hop 1 + hop 2) — diff a re-scoop search against these."""
    from rx_state.survey import read_note

    return {
        read_note(p).key
        for p in glob.glob(os.path.join(rx_dir, "notes", "papers", "*.md"))
    }
