"""Persist the post-survey grilling session (shared human/agent understanding)."""

from __future__ import annotations

import os
from dataclasses import dataclass, field

import yaml


@dataclass
class SharedUnderstanding:
    """Decisions locked during rx-grill before rx-plan writes the evaluation contract."""

    primary_question_id: str = ""
    novelty_gap: str = ""
    metric_intent: str = ""
    baselines: list[str] = field(default_factory=list)
    falsifiers: list[str] = field(default_factory=list)
    scope_cuts: list[str] = field(default_factory=list)
    machine_time_budget: str = ""
    open_risks: list[str] = field(default_factory=list)
    # Conference-outcome / Scoop-Check style fields (optional; empty defaults)
    diff_framing: str = ""
    diff_mechanism: str = ""
    diff_insight: str = ""
    diff_domain: str = ""
    collision_threats: list[str] = field(default_factory=list)
    evidence_expectations: list[str] = field(default_factory=list)
    failure_mode_checks: list[str] = field(default_factory=list)
    summary: str = ""


def _path(rx_dir: str) -> str:
    return os.path.join(rx_dir, "grill", "shared-understanding.md")


def write_understanding(rx_dir: str, understanding: SharedUnderstanding) -> str:
    os.makedirs(os.path.join(rx_dir, "grill"), exist_ok=True)
    front = {
        "primary_question_id": understanding.primary_question_id,
        "novelty_gap": understanding.novelty_gap,
        "metric_intent": understanding.metric_intent,
        "baselines": understanding.baselines,
        "falsifiers": understanding.falsifiers,
        "scope_cuts": understanding.scope_cuts,
        "machine_time_budget": understanding.machine_time_budget,
        "open_risks": understanding.open_risks,
        "diff_framing": understanding.diff_framing,
        "diff_mechanism": understanding.diff_mechanism,
        "diff_insight": understanding.diff_insight,
        "diff_domain": understanding.diff_domain,
        "collision_threats": understanding.collision_threats,
        "evidence_expectations": understanding.evidence_expectations,
        "failure_mode_checks": understanding.failure_mode_checks,
    }
    path = _path(rx_dir)
    body = understanding.summary.strip() or (
        "Shared understanding from rx-grill. Do not run rx-plan until this exists and is confirmed."
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(yaml.safe_dump(front, sort_keys=False))
        f.write("---\n\n")
        f.write(body)
        if not body.endswith("\n"):
            f.write("\n")
    return path


def read_understanding(rx_dir: str) -> SharedUnderstanding:
    with open(_path(rx_dir), encoding="utf-8") as f:
        raw = f.read()
    _, front_block, body = raw.split("---", 2)
    front = yaml.safe_load(front_block) or {}
    return SharedUnderstanding(
        primary_question_id=front.get("primary_question_id") or "",
        novelty_gap=front.get("novelty_gap") or "",
        metric_intent=front.get("metric_intent") or "",
        baselines=list(front.get("baselines") or []),
        falsifiers=list(front.get("falsifiers") or []),
        scope_cuts=list(front.get("scope_cuts") or []),
        machine_time_budget=front.get("machine_time_budget") or "",
        open_risks=list(front.get("open_risks") or []),
        diff_framing=front.get("diff_framing") or "",
        diff_mechanism=front.get("diff_mechanism") or "",
        diff_insight=front.get("diff_insight") or "",
        diff_domain=front.get("diff_domain") or "",
        collision_threats=list(front.get("collision_threats") or []),
        evidence_expectations=list(front.get("evidence_expectations") or []),
        failure_mode_checks=list(front.get("failure_mode_checks") or []),
        summary=(body or "").strip(),
    )


def is_grilled(rx_dir: str) -> bool:
    return os.path.exists(_path(rx_dir))
