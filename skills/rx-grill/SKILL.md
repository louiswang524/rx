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
disk for later stages.

## When it runs
- First pass: always, after survey, before plan.
- Research `--loop` with `needs_replan=True` (or no lock yet): after survey again, before re-plan.
- Cheap loop resume (`loop_resume_stage` → `experiment`): **skip** — evaluation contract unchanged.

## Steps
1. Read `.rx/questions/`, `.rx/notes/papers/`, and any prior `.rx/grill/shared-understanding.md`
   so the grilling starts from what is already on disk.
2. Run this grill-me loop on the research design (the plan about to be locked):

   Interview me relentlessly about every aspect of this plan until
   we reach a shared understanding. Walk down each branch of the design
   tree resolving dependencies between decisions one by one.

   If a question can be answered by exploring the codebase, explore
   the codebase instead.

   For each question, provide your recommended answer.

   Treat "the codebase" here as the project tree: code, paper notes, and `.rx/` artifacts.
3. When shared understanding is reached, write it via `rx_state.grill.write_understanding`.
   Do **not** advance until the human confirms the summary (or explicitly says "looks good" /
   "lock it").
4. Advance `.rx/state.json` stage to `plan`.

## Outputs
- `.rx/grill/shared-understanding.md` — agreed research design (the artifact `rx-plan` reads)
- Updated `.rx/state.json` (stage = plan)
