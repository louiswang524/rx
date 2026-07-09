# rx-spinoff — spawn follow-up research from a paper

**Date:** 2026-07-08
**Status:** Approved (brainstorm) → ready for implementation plan
**Author:** Louis + Claude

## Problem

The rx pipeline has one cold-start entry, `rx-ideate`, which turns a *vague topic* into
`Q<n>` research questions. But a very common real starting point is not a blank idea — it is
**an existing paper**. You read a paper, you have opinions about its weaknesses and its stated
future work, and you want to run a follow-up study off it.

Today that requires manually distilling the paper into an idea, hand-carrying it into
`rx-ideate`, and separately reviewing the paper. There is no single entry point that:
1. critically reviews an external paper, and
2. turns that review into concrete, novelty-checked follow-up directions, and
3. seeds `.rx/` so the normal pipeline resumes from there.

`rx-review` does **not** cover this — it reviews *your own* draft pre-submission (accept/reject
panel), not an external paper mined for extension opportunities.

## Solution

A new skill, **`rx-spinoff`**, that acts as a **second front-end** to the pipeline, parallel to
`rx-ideate`:

```
rx-spinoff ─┐
rx-ideate ──┴─→ rx-survey → rx-plan → rx-experiment → rx-analyze → rx-write → rx-review
                         \__ rx-pipeline orchestrates all + self-improving --loop __/
```

Given a paper, it produces a lightweight critique and 2–4 ranked follow-up directions, seeds
`.rx/`, and auto-continues into `rx-pipeline`, which naturally halts at the plan lock before any
GPU spend.

**Name:** `rx-spinoff`. `rx-review` is taken; this skill spins off *new* work from *someone
else's* paper.

**Model routing:** `opus` (creative + critical, like `rx-ideate`). Claude-only field; ignored by
Codex.

## Inputs

One of: arXiv URL, arXiv ID, DOI, or a local PDF path.

- arXiv / DOI → fetch metadata the same way `rx-survey` does (arXiv / Semantic Scholar).
- Local PDF → read the file directly.

## Steps (SKILL.md instructions)

1. **Locate/scaffold project (auto-detect):** if `.rx/` exists in the current repo, seed there;
   otherwise run `scripts/bootstrap.sh <dir> <name>` to git-init a fresh project (own `.venv`,
   `.rx/` scaffold, `rx_state` installed) and seed there.
2. **Ingest** the paper → extract method, contributions, baselines, headline claim.
3. **Lightweight critique:** strengths, weaknesses, threats-to-validity, and the paper's own
   *Limitations / Future Work* — all mined for **extension opportunities**, not accept/reject.
   Read `~/.rx-kb/` (system/GPU snapshot, pitfalls, learnings) so proposed directions fit the
   hardware and avoid known dead ends.
4. **Derive 2–4 follow-up directions.** For each, write a **novelty delta** vs. the seed paper
   ("what we do that they don't"). Rank by leverage-given-hardware. Designate the top-ranked
   direction as the **primary** direction the pipeline will pursue first.
5. **Seed `.rx/`:**
   - Seed paper → `PaperNote` via `rx_state.survey.write_note` (so its baselines land in the
     baseline set `rx-plan` compares against).
   - Each direction → `Q<n>` via `rx_state.store.write_question`, **primary question first**,
     each carrying its gap. Novelty delta goes in the question body.
   - The critique → `.rx/notes/spinoff-<key>.md` (plain markdown; **no new `rx_state` code**).
6. **Auto-continue:** set `state.stage = "survey"` via `rx_state.store.save_state`, then invoke
   `rx-pipeline`. It flows survey → plan and **halts at the plan lock** — `rx_state.pipeline.
   stage_blockers` blocks `experiment` until `rx-plan` has written a lock — so the user vets the
   direction before any compute is spent. Make this stop explicit in output.

## Outputs

- `.rx/notes/papers/<key>.md` — the seed paper as a `PaperNote`.
- `.rx/questions/Q<n>.md` — one per follow-up direction, primary first, each with gap + novelty
  delta.
- `.rx/notes/spinoff-<key>.md` — the critique (strengths / weaknesses / threats-to-validity /
  mined future-work → extension opportunities).
- `.rx/state.json` at `stage = survey`, then advanced by `rx-pipeline` up to the plan lock.

## Reuse — no new Python

Uses existing helpers only: `rx_state.survey.write_note`, `rx_state.store.write_question`,
`rx_state.store.save_state`, `rx_state.pipeline` (via `rx-pipeline`). The only new persisted
artifact is one markdown file written directly. `AGENTS.md` is updated with the two-front-end
diagram and a one-line pipeline entry.

## Failure modes & mitigations

- **Scanned PDF with no extractable text** → detect empty/garbage extraction, stop with a clear
  message asking for an arXiv ID or a text PDF.
- **Paper not on arXiv / Semantic Scholar** (e.g. a workshop PDF) → fall back to direct PDF
  parse; do not hard-fail on missing metadata.
- **Auto-continue running unattended** → bounded by the plan-lock gate (no GPU before the lock);
  the skill states explicitly that it has stopped at the plan lock and how to resume.

## Non-goals (YAGNI)

- No new `rx_state` module or artifact type for the critique — a markdown file suffices.
- Not an accept/reject peer-review panel — that is `rx-review`'s job on your own draft.
- Does not auto-run experiments; it stops at the plan lock by design.

## Testing

- Unit: given a fixture `PaperNote` + questions, assert `.rx/` is seeded correctly and
  `state.stage == "survey"`, and that the seed paper's baselines appear in
  `rx_state.survey.collect_baselines`.
- Behavioral: run against a known arXiv ID in a temp dir → assert a critique file, ≥2 `Q<n>`
  questions with novelty deltas, and a `PaperNote` are produced; assert the pipeline halts at the
  plan lock (no experiment artifacts).
- Failure: pass a scanned/text-empty PDF → assert clear stop message, no partial `.rx/` seeding.
