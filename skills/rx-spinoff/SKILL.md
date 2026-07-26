---
name: rx-spinoff
description: Turn an existing paper into a critique plus ranked, novelty-checked follow-up research directions, seed .rx/ from it, and auto-continue the pipeline (stopping at the plan lock before any compute).
model: opus
---

# rx-spinoff

## Purpose
A second cold-start front-end to the pipeline, parallel to `rx-ideate`. Instead of a vague topic,
you hand it an existing paper. It produces a lightweight critique and 2–4 ranked follow-up
directions, seeds `.rx/` (seed paper as a `PaperNote`, directions as `Q<n>` questions, critique as
a note), then auto-continues `rx-pipeline` — which halts at the plan lock so you vet the direction
before any GPU spend. This is distinct from `rx-review`, which reviews *your own* draft for
accept/reject.

## Inputs
One of: arXiv URL, arXiv ID, DOI, or a local PDF path.
- arXiv / DOI → fetch metadata the same way `rx-survey` does (arXiv / Semantic Scholar).
- Local PDF → read the file directly. If text extraction yields empty/garbage output (a scanned
  PDF), stop with a clear message asking for an arXiv ID or a text-based PDF; do not seed `.rx/`.

## Steps
1. **Locate/scaffold the project (auto-detect).** If a `.rx/` directory exists in the current repo,
   seed there. Otherwise run `scripts/bootstrap.sh <dir> <name>` to git-init a fresh project
   (`.rx/` scaffold, `.venv` symlinked to the shared venv with `rx_state` installed) and seed there.
2. **Ingest the paper.** Extract its method, contributions, baselines, and headline claim.
3. **Lightweight critique.** Write strengths, weaknesses, threats-to-validity, and mine the paper's
   own *Limitations / Future Work* — all aimed at extension opportunities, not accept/reject. Read
   `~/.rx-kb/` (system/GPU snapshot, pitfalls, learnings) so directions fit the hardware and avoid
   known dead ends.
4. **Derive 2–4 follow-up directions.** For each, write a **novelty delta** vs. the seed paper
   ("what we do that they don't"). Rank by leverage-given-hardware, and designate the top-ranked
   one as the **primary** direction the pipeline pursues first.
5. **Seed `.rx/`.**
   - Seed paper → `PaperNote` via `rx_state.survey.write_note` (so its baselines join the set
     `rx-plan` compares against — confirm with `rx_state.survey.collect_baselines`).
   - Each direction → `Q<n>` via `rx_state.store.write_question`, **primary question first**, each
     carrying its gap; put the novelty delta in the question body.
   - Critique → `.rx/notes/spinoff-<key>.md` (plain markdown; no new `rx_state` code).
6. **Auto-continue.** Set `state["stage"] = "survey"` and save via `rx_state.store.save_state`, then
   invoke `rx-pipeline`. It flows survey → plan and stops at the **plan lock** —
   `rx_state.pipeline.stage_blockers` blocks `experiment` until `rx-plan` has written a lock — so no
   compute is spent before you approve. State the stop explicitly and how to resume.

## Outputs
- `.rx/notes/papers/<key>.md` — the seed paper as a `PaperNote`.
- `.rx/questions/Q<n>.md` — one per follow-up direction, primary first, each with gap + novelty delta.
- `.rx/notes/spinoff-<key>.md` — the critique (strengths / weaknesses / threats-to-validity /
  mined future-work → extension opportunities).
- `.rx/state.json` advanced to the plan lock by `rx-pipeline`, with an explicit stop message.
