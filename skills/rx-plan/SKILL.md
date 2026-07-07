---
name: rx-plan
description: Turn questions + survey into a blocker-first experiment plan — lock metric, comparison family, seed policy, and baselines BEFORE any run; estimate in machine-time, not human-days.
model: sonnet
---

# rx-plan

## Purpose
Prevent p-hacking by locking the evaluation contract before results exist, and pick baselines the
field actually uses (from `rx-survey`).

## Steps
1. Read `.rx/questions/` and the survey baseline set (`rx_state.survey.collect_baselines`).
2. Decide the primary `metric`, whether higher is better, the `comparison_family`, and a `seed_policy` (≥2 for any intended `strong` claim).
3. Write the lock via `rx_state.planlock.write_lock` — this is blocker-first: `rx-experiment` must check `is_locked` and refuse to run until the lock exists.
4. Estimate cost in machine-time (iterations / compute / tokens), NOT human-days — Claude Code implements experiments fast, so favor more iterations.
5. Advance `.rx/state.json` stage to `experiment`.

## Outputs
- `.rx/plan/lock.md` (metric, comparison family, seed policy, baselines)
- Updated `.rx/state.json` (stage = experiment)
