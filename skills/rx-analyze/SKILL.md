---
name: rx-analyze
description: Turn experiment results into rigorous statistics and honest evidence outcomes — decide what beats the baseline and what does not, and set each evidence record's outcome.
model: opus
---

# rx-analyze

## Purpose
Convert raw runs into defensible numbers and honest `positive|negative|inconclusive` outcomes that
feed the evidence gates — no p-hacking, no overclaiming.

## Steps
1. Aggregate per-seed metric values with `rx_state.analysis.summarize_metric` (mean/std/n).
2. Compare against the locked baseline using the plan's `higher_is_better` via `rx_state.analysis.beats_baseline`.
3. Set each `E<n>` evidence outcome with `rx_state.analysis.decide_outcome` — report negatives honestly (they fuel the loop).
4. Produce figures/tables and note which claims the evidence supports vs. does not.
5. Advance `.rx/state.json` stage to `write`.

## Outputs
- Metric summaries (mean/std/n) per experiment
- Updated `E<n>` evidence outcomes
- Updated `.rx/state.json` (stage = write)
