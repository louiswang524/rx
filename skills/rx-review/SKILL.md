---
name: rx-review
description: Simulate an ML peer-review panel (ICML/NeurIPS rubric) plus a reproducibility review, and draft rebuttals — stress-test the paper before submission.
model: opus
---

# rx-review

## Purpose
Adversarially review the draft the way a real program committee would, surface the blocking issues,
check reproducibility, and prepare rebuttal material.

## Steps
1. Call `rx_state.scoop.list_scoop_checks(rx_dir)`. If any have `verdict ==
   "potential_collision"` (written by `rx-pipeline`'s autonomous-mode re-scoop check), surface
   them as a `major` finding — a possible scoop needs a human's eyes on it before submission, even
   though the automated check didn't halt the research loop. Skip silently if the list is empty
   or the project never ran in autonomous mode.
2. Assemble the panel: several independent reviewers with field-specific expertise + a devil's advocate. If `rx_state.style.read_style_guide(rx_dir)` returns a guide, add a style-conformance reviewer to the panel; if it returns `None`, skip this role (not a blocker).
3. Each reviewer files `ReviewFinding`s (`major|minor|praise`) against the draft's claims, baselines, and ablations. The style-conformance reviewer instead compares the draft against the style guide's structure/tone/wording conventions and files deviations as `minor` findings.
4. Compute the panel recommendation with `rx_state.review.recommend` (any major → reject).
5. Persist the round: `rx_state.review.write_round(rx_dir, n, findings)` → `.rx/reviews/round-<n>.md`. The drafting loop reads this file to drive `rx-write --mode=revise`.
6. Run `rx_state.review.repro_checklist(has_code, has_seeds, has_configs)`; any missing item must be fixed before submission.
7. Draft rebuttal responses to the major/minor findings.

## Outputs
- A reviewer report (findings + panel recommendation)
- `.rx/reviews/round-<n>.md` — the persisted round (findings + recommendation) for the drafting loop
- A reproducibility checklist result (missing items)
- Rebuttal drafts for the substantive findings
