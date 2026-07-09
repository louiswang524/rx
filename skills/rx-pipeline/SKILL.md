---
name: rx-pipeline
description: Orchestrate the full research pipeline (ideate → survey → plan → experiment → analyze → write → review), enforce blocker-first gates between stages, and run the self-improving loop where negative results drive new hypotheses.
model: opus
---

# rx-pipeline

## Purpose
Chain the seven stage skills into one run, enforce the gates between them, and — with `--loop` —
keep iterating on hypotheses until a claim clears the gate or the budget is exhausted.

## Steps
1. Read `.rx/state.json` to find the current `stage` (supports mid-pipeline entry).
2. Before entering a stage, call `rx_state.pipeline.stage_blockers(rx_dir, stage)`; if non-empty, stop and report the blocker (e.g. `experiment` before a plan lock).
3. Run the stage skill, then `rx_state.pipeline.advance_stage(state)` to move to `next_stage`.
4. Repeat until `stage == "done"` (after `review`).

## Outputs
- A completed run with `.rx/state.json` at `done`
- All stage artifacts (questions, notes, lock, experiments, evidence, claims, paper outputs, review)

## Loop
With `--loop`, after `analyze` decide `improved` (beat the locked baseline?) and `gate_cleared`
(a target claim reached `strong` via `gates.can_promote`?). Call
`rx_state.pipeline.loop_step(loop, improved, gate_cleared)`:
- `stop_success` — a claim cleared the gate; proceed to `write`/`review` and finish.
- `stop_no_improve` — too many iterations without improvement; write up the negative/ablation result honestly.
- `stop_budget` — iteration budget exhausted; write up best result so far.
- `continue` — loop back to `ideate` with the prior **negative** evidence fed in as input for a new hypothesis.
Plan in machine-time (iterations/compute), never human-days.

## Drafting loop
A second, inner loop — separate from the research `## Loop` above and independent of `--loop`.
Once the research loop settles and the pipeline reaches `write`, iterate the paper:
1. `rx-write --mode=draft`.
2. `rx-review` — writes `.rx/reviews/round-<n>.md` and yields a `recommendation`.
3. `rx_state.pipeline.draft_loop_step(state["draft_loop"], recommendation)`:
   - `stop_clean` — recommendation is `accept` or `minor revision`; finish.
   - `stop_budget` — `iteration >= max_draft_iters`; finish and report the residual major findings honestly.
   - `continue` — run `rx-write --mode=revise`, then back to step 2.
The drafting loop only edits the paper; it never re-runs experiments or touches `.rx/` evidence.
