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
1. Assemble the panel: several independent reviewers with field-specific expertise + a devil's advocate.
2. Each reviewer files `ReviewFinding`s (`major|minor|praise`) against the draft's claims, baselines, and ablations.
3. Compute the panel recommendation with `rx_state.review.recommend` (any major → reject).
4. Run `rx_state.review.repro_checklist(has_code, has_seeds, has_configs)`; any missing item must be fixed before submission.
5. Draft rebuttal responses to the major/minor findings.

## Outputs
- A reviewer report (findings + panel recommendation)
- A reproducibility checklist result (missing items)
- Rebuttal drafts for the substantive findings
