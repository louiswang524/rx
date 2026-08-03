---
name: rx-grill
description: Interview the user relentlessly about the research design until reaching shared understanding, resolving each branch of the decision tree. Runs after survey and before plan/experiment (grill-me for RX).
model: opus
---

# rx-grill

Adapted from Matt Pocock's grill-me skill. Same interview loop; RX wires it between
`rx-survey` and `rx-plan`, and persists the result under `.rx/grill/`.

## Purpose
After `rx-ideate` and `rx-survey`, pause before `rx-plan` / `rx-experiment` so human and
agent reach equal understanding of the research design — then write that understanding to
disk for later stages. This stage is also the **collision + failure-mode audit** gate:
same strategies often accept or reject based on instantiation quality
(see conference-outcome lessons).

## When it runs
- First pass: always, after survey, before plan.
- Research `--loop` with `needs_replan=True` (or no lock yet): after survey again, before re-plan.
- Cheap loop resume (`loop_resume_stage` → `experiment`): **skip** — evaluation contract unchanged.

## First-mile lessons
Read `skills/_shared/references/conference-outcome-lessons.md` before interviewing.
Enforce:

1. **4-axis collision check** vs closest neighbors (framing / mechanism / insight / domain).
2. **Evidence expectations** + **falsifiers** for every primary claim.
3. **Failure-mode audit** (novel-but-empty, sum-of-parts, hidden strongest neighbor, etc.).
4. Contribution language = derived/constructed/measured/tightened — not method labels.

## Steps
1. Read `.rx/questions/`, `.rx/notes/papers/`, and any prior `.rx/grill/shared-understanding.md`
   so the grilling starts from what is already on disk. Identify the survey's closest
   neighbor / collision threat.
2. Run this grill-me loop on the research design (the plan about to be locked):

   Interview me relentlessly about every aspect of this plan until
   we reach a shared understanding. Walk down each branch of the design
   tree resolving dependencies between decisions one by one.

   If a question can be answered by exploring the codebase, explore
   the codebase instead.

   For each question, provide your recommended answer.

   Treat "the codebase" here as the project tree: code, paper notes, and `.rx/` artifacts.

   Required branches (do not skip):
   - Bottleneck: what structural gap do retrieved neighbors leave open?
   - Differentiation: four-axis delta vs the closest neighbor — is mechanism/insight
     actually different, or only the domain?
   - Collision threats: which prior papers could scoop or subsume this claim?
   - Evidence expectations: what table/figure makes each major claim inspectable?
   - Falsifiers: what result kills the idea?
   - Failure-mode audit: novel-but-empty? indistinguishable from sum of parts?
     strongest baseline hidden? constructive move collapsed into vague audit?
   - Metric, baselines, seeds, machine-time budget, scope cuts.
3. When shared understanding is reached, write it via `rx_state.grill.write_understanding`
   including (at minimum) `novelty_gap`, `baselines`, `falsifiers`, `evidence_expectations`,
   `collision_threats`, the four `diff_*` fields, `failure_mode_checks`, and `open_risks`.
   Do **not** advance until the human confirms the summary (or explicitly says "looks good" /
   "lock it").
4. If the audit verdict is abandon (no real delta, or novel-but-empty with no repair),
   stop and send the user back to `rx-ideate` / more survey — do not advance to plan.
5. Advance `.rx/state.json` stage to `plan`.

## Outputs
- `.rx/grill/shared-understanding.md` — agreed research design (the artifact `rx-plan` reads),
  including collision threats, 4-axis differentiation, evidence expectations, and failure-mode checks
- Updated `.rx/state.json` (stage = plan)
