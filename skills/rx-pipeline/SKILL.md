---
name: rx-pipeline
description: Orchestrate the full research pipeline (ideate → survey → grill → plan → experiment → analyze → write → review), enforce blocker-first gates between stages, and run the self-improving loop where negative results drive new hypotheses.
model: opus
---

# rx-pipeline

## Purpose
Chain the stage skills into one run, enforce the gates between them, and — with `--loop` —
keep iterating on hypotheses until a claim clears the gate or the budget is exhausted.

## Project location
If this is a brand-new idea and no `.rx/` exists yet, start with `rx-ideate` or `rx-spinoff` so
the project is bootstrapped under `$RX_RESEARCH_ROOT/<topic>/<project-name>/` (never
`rx-projects/` or a dated Codex chat folder). Then run the pipeline from that project directory.

## Steps
1. Read `.rx/state.json` to find the current `stage` (supports mid-pipeline entry).
2. Before entering a stage, call `rx_state.pipeline.stage_blockers(rx_dir, stage)`; if non-empty, stop and report the blocker (e.g. `plan` before `rx-grill`, or `experiment` before a plan lock).
3. Run the stage skill, then `rx_state.pipeline.advance_stage(state)` to move to `next_stage`.
4. Repeat until `stage == "done"` (after `review`).

Stage order:

```text
ideate → survey → grill → plan → experiment → analyze → write → review → done
```

`rx-grill` is interactive: do **not** auto-skip it on the first pass or after a replan survey,
**unless running in autonomous mode** (see below) — human-confirmed grill remains the default.
It must reach a human-confirmed shared understanding (`.rx/grill/shared-understanding.md`)
before `rx-plan` may lock the evaluation contract.

## Autonomous (full-access) mode
Triggered by `rx-pipeline --autonomous [--max-hours N]` (default `N=24`). On first invocation,
set in `.rx/state.json`: `autonomous: true`, `autonomous_started_at:
datetime.now(timezone.utc).isoformat()` (an offset-bearing, timezone-aware ISO-8601 timestamp),
`max_hours: N`. Entry is unchanged otherwise (`rx-ideate`/`rx-spinoff` still bootstraps a
brand-new project first).

If `state.get("autonomous")` is true but `max_hours` is missing or null (e.g. an older run, or a
project that predates this field), treat it as the default (`24`) and write it back into
`state.json` immediately — don't leave it unresolved for later deadline checks.

While `state.get("autonomous")` is true:
- **Grill is skipped, not automated.** On reaching the `grill` stage, do not invoke interactive
  `rx-grill`. Instead reason through the same fields yourself (primary question, novelty gap,
  metric intent, baselines, falsifiers, scope cuts, collision threats, failure-mode checks) and
  write them with `rx_state.grill.write_understanding`, setting `SharedUnderstanding.mode =
  "self-grilled"` so the file is visibly distinguishable from a human-confirmed one. Advance
  straight to `plan`. `rx-plan` performs an added self-critique step in this mode — see its
  SKILL.md.
- **No confirmation prompts.** `rx-write`'s blog push and the Cleanup pass's deletions proceed
  without asking (see their sections below / their SKILL.md).
- **Deadline check.** Before entering each stage, and at each research-loop and drafting-loop
  iteration, call `rx_state.pipeline.deadline_exceeded(state.get("autonomous_started_at"),
  state.get("max_hours"))`. If true, treat it exactly like a loop's `stop_budget` outcome: stop
  iterating, write up the best result so far, proceed to `write`/`review`, then stop the
  pipeline.
- **Re-scoop check.** At each research-loop iteration (see `## Loop` below), after computing the
  new `loop["iteration"]`, call `rx_state.scoop.scoop_recheck_due(loop["iteration"])` (fires every
  3rd iteration). If due: fetch `rx_state.scoop.known_paper_keys(rx_dir)`, run a fresh arXiv /
  Semantic Scholar search against the locked question's primary claim, and compare hits against
  those known keys plus `.rx/grill/shared-understanding.md`'s `collision_threats`. Write the
  result with `rx_state.scoop.write_scoop_check(rx_dir, ScoopCheck(...))` — `verdict =
  "potential_collision"` only for a genuinely close match (same task + same metric direction), not
  a loose keyword hit. **Never halt the loop on this alone** — log it via
  `rx_state.store.append_autonomy_log` and keep iterating; `rx-review` surfaces any
  `potential_collision` verdicts in the final writeup (see its SKILL.md) so a human reviews the
  risk rather than the loop reacting to a possible false positive.
- **Audit trail.** After every stage transition and every irreversible action (self-grill
  completed, plan locked, blog commit pushed + hash, cleanup paths deleted + bytes freed, loop
  stop reason), call `rx_state.store.append_autonomy_log(rx_dir, "<one-line description>")`.
  This is a log only — it never blocks anything.

## Outputs
- A completed run with `.rx/state.json` at `done`
- All stage artifacts (questions, notes, grill understanding, lock, experiments, evidence, claims, paper outputs, review)

## Loop
With `--loop`, after `analyze` decide `improved` (beat the locked baseline?) and `gate_cleared`
(a target claim reached `strong` via `gates.can_promote`?). Call
`rx_state.pipeline.loop_step(loop, improved, gate_cleared)`:
- `stop_success` — a claim cleared the gate; proceed to `write`/`review` and finish.
- `stop_no_improve` — too many iterations without improvement; write up the negative/ablation result honestly.
- `stop_budget` — iteration budget exhausted; write up best result so far.
- `continue` — loop back to `ideate` with the prior **negative** evidence fed in as input for a new
  hypothesis (pass its `E<n>` id so `rx-ideate` sets `parent_evidence_id` on the new `Q<n>`,
  keeping an explicit hypothesis1→neg→hypothesis2→... lineage in `.rx/questions/`).
Plan in machine-time (iterations/compute), never human-days.

This is a real hypothesis loop, not a single pass: hypothesis (`ideate`) → experiment
(`implementation` + `experiments`) → results (`analyze`) → new hypothesis, repeated until
`stop_success`/`stop_no_improve`/`stop_budget`. After `rx-ideate` produces the next hypothesis,
decide whether it changes the metric, comparison family, or needs new baselines. Call
`rx_state.pipeline.loop_resume_stage(rx_dir, needs_replan)`:
- Returns `"experiment"` (the common case — same evaluation contract, existing lock still valid):
  set `state["stage"] = "experiment"` directly and skip `survey`/`grill`/`plan` entirely for this iteration.
- Returns `"survey"` (no lock yet, or the new hypothesis needs a different metric/baselines): run
  `survey` → `grill` → `plan` as normal before `experiment`.
This is what keeps loop iterations cheap — most hypothesis-loop iterations should skip straight
from `ideate` to `experiment`.

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

## Cleanup (optional)
Once the drafting loop settles (`stop_clean`/`stop_budget`) — or immediately if the research
`--loop` ended in `stop_no_improve`/`stop_budget` with no drafting to do — offer an optional
cleanup pass. Never run it automatically outside autonomous mode, and never touch anything
under `.rx/` (the traceability record; it's markdown, not the disk hog).
1. Call `rx_state.cleanup.cleanup_candidates(project_dir, rx_dir)`. It finds
   `experiments/**/checkpoints/` dirs and training-log dirs (`wandb/`, `tensorboard/`,
   `lightning_logs/`, `logs/`), each sized and marked `protected` if it backs an experiment whose
   evidence feeds a `supported`/`strong` claim (i.e. still cited in the final paper).
2. Show the report via `rx_state.cleanup.format_report` — only ever propose deleting the
   non-protected candidates (superseded/negative hypotheses from earlier loop iterations).
3. If `state.get("autonomous")` is true, skip the confirmation and call
   `rx_state.cleanup.delete_candidates` directly with the non-protected candidates, then log it
   via `rx_state.store.append_autonomy_log(rx_dir, f"deleted cleanup paths: <paths>, freed
   <bytes> bytes")` (or equivalent) — the same deleted-paths + bytes-freed content the
   Audit-trail bullet above promises. Otherwise ask explicitly before deleting anything, and on
   confirmation call `rx_state.cleanup.delete_candidates` with just the approved (non-protected)
   candidates.
4. If not autonomous and the user declines, or there are no non-protected candidates either
   way, skip silently — this step never blocks the pipeline from being considered done.
