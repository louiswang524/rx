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
2. **Figure check.** Call `rx_state.review.extract_figure_paths(tex, base_dir=publication/arxiv)`
   on `publication/arxiv/main.tex` to resolve every `\includegraphics` target to a file path.
   For each resolved path that exists, **read the image directly** (you're multimodal — open
   the file, don't just infer from the caption) and check: are axis labels/legend/tick text
   legible at print size, does the figure actually show what its caption claims, is the
   comparison-context baseline present if the caption implies one. File any problem as a normal
   `ReviewFinding(reviewer="figure-check", severity=..., comment=...)` in the same findings
   list the panel uses below, so `recommend()` folds it into the panel verdict — an illegible
   headline figure is `major`, a minor labeling nit is `minor`. Skip silently if no figures are
   referenced yet or none of the resolved paths exist (early draft).
3. **AI-tell check.** Run `rx_state.aitells.scan_ai_tells` over the draft's prose (main.tex,
   text outside tables/code). File each hit as `ReviewFinding(reviewer="ai-tell-check",
   severity="minor", comment=...)` — always `minor`, never `major`: prose style should get
   flagged for revision, not sink a paper's recommendation. Skip silently if there are no
   findings.
5. Assemble the panel: several independent reviewers with field-specific expertise + a devil's advocate. If `rx_state.style.read_style_guide(rx_dir)` returns a guide, add a style-conformance reviewer to the panel; if it returns `None`, skip this role (not a blocker).
6. Each reviewer files `ReviewFinding`s (`major|minor|praise`) against the draft's claims, baselines, and ablations. The style-conformance reviewer instead compares the draft against the style guide's structure/tone/wording conventions and files deviations as `minor` findings.
7. Compute the panel recommendation with `rx_state.review.recommend` over **all** findings, including the figure-check, scoop-check, and AI-tell-check ones (any major → reject).
8. Persist the round: `rx_state.review.write_round(rx_dir, n, findings)` → `.rx/reviews/round-<n>.md`. The drafting loop reads this file to drive `rx-write --mode=revise`.
9. Run `rx_state.review.repro_checklist(has_code, has_seeds, has_configs)`; any missing item must be fixed before submission.
10. Draft rebuttal responses to the major/minor findings.

## Outputs
- A reviewer report (findings + panel recommendation)
- `.rx/reviews/round-<n>.md` — the persisted round (findings + recommendation) for the drafting loop
- A reproducibility checklist result (missing items)
- Rebuttal drafts for the substantive findings
