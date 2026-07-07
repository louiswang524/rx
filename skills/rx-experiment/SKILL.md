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
2. Run with ≥2 seeds when a `strong` claim is intended.
3. Capture each run with `rx_state.capture.capture_run(rx_dir, exp_id, seeds, baseline, config, commit=<git rev-parse HEAD>, gpu=<KB GPU string>)`.
4. Write an `E<n>` evidence artifact per result via `rx_state.store.write_evidence`, setting `outcome` to `positive|negative|inconclusive` honestly.
5. Advance `.rx/state.json` stage to `analyze`.

## Outputs
- `.rx/experiments/EXP<n>/run.md` (config/seed/commit/GPU per run)
- `.rx/evidence/E<n>.md` (outcome-tagged, linked to its experiment)
- Updated `.rx/state.json` (stage = analyze)
