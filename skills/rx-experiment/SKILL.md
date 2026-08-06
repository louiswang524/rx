---
name: rx-experiment
description: Run ML experiments with full reproducibility capture (config/seed/commit/GPU) and log evidence, treating negative results as first-class.
model: sonnet
---

# rx-experiment

## Purpose
Execute the experiment plan, capturing every run reproducibly and recording its outcome as
`E<n>` evidence — including negative results, which are fuel for the next hypothesis, not failures.

## Steps
1. For each hypothesis, implement the experiment (Claude Code writes the training/eval code fast — favor more runs over conservative scoping).
2. Inner implementation loop (this is the "implementation" stage of the hypothesis loop, not a
   single one-shot script): implement → run → judge `clean_run` (did it execute correctly and
   produce a real metric, as opposed to crashing, silently producing NaN/placeholder output, or an
   obvious bug an initial read of the traceback/logs reveals). Call
   `rx_state.pipeline.experiment_loop_step(inner, clean_run)`:
   - `stop_clean` — the run is trustworthy; proceed to capture it as evidence (step 4).
   - `continue` — fix the implementation and re-run, up to `max_inner_iters` (default 3).
   - `stop_budget` — still broken after the cap; capture the last run's evidence as `inconclusive`
     with a note describing the unresolved issue, rather than silently discarding it.
   This loop is about implementation correctness, not tuning for a better number — never keep
   iterating just because the result is negative; a clean negative run is `stop_clean`.
3. Run with ≥2 seeds when a `strong` claim is intended.
4. Capture each run with `rx_state.capture.capture_run(rx_dir, exp_id, seeds, baseline, config, commit=<git rev-parse HEAD>, gpu=<KB GPU string>, goal=..., changes=..., result=..., conclusion=..., next_steps=...)`.
   The five narrative args are required, not optional — fill in all of them every run:
   - `goal` — the hypothesis this specific run tests.
   - `changes` — what differs from the baseline/previous run (params, code, data); plain
     language, not an auto-diff.
   - `result` — the observed metric(s), pre-statistics.
   - `conclusion` — your immediate read of the run. This is informal and distinct from the
     formal `positive|negative|inconclusive` outcome, which rx-analyze decides later from
     rigorous stats — don't treat this as the final verdict.
   - `next_steps` — the concrete next action or follow-up hypothesis.
5. Write an `E<n>` evidence artifact per result via `rx_state.store.write_evidence`, setting `outcome` to `positive|negative|inconclusive` honestly.
6. Advance `.rx/state.json` stage to `analyze`.

## Outputs
- `.rx/experiments/EXP<n>/run.md` (config/seed/commit/GPU per run)
- `.rx/evidence/E<n>.md` (outcome-tagged, linked to its experiment)
- Updated `.rx/state.json` (stage = analyze)
