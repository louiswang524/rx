---
name: rx-survey
description: Ingest arXiv / Semantic Scholar papers into structured method/baseline notes and a reading queue, and surface the baselines the field actually compares against.
model: sonnet
---

# rx-survey

## Purpose
Turn the reading list into structured `PaperNote`s (method, baselines, headline claim) so later
stages reuse them — especially the baseline set that comparable papers report against.
Literature grounding is the input to bottleneck diagnosis in `rx-grill` / plan lock.

## First-mile lessons
Read `skills/_shared/references/conference-outcome-lessons.md`. For survey:

1. **Literature first** — bottleneck and novelty claims must cite retrieved neighbors.
2. Prefer **full text** (method section) for the closest 3–5 papers when available; abstracts
   alone are weak for differentiation.
3. For each note, capture not only what they do, but **what they leave open**.
4. Never hide the **strongest / closest** competitor.

## Steps
1. Build a reading queue for the question(s) from `.rx/questions/`. Include:
   - papers named in each question's novelty delta,
   - recent same-task leaves (arXiv / Semantic Scholar / OpenReview when useful),
   - strongest public baselines the field actually reports.
2. For each paper, fetch metadata (arXiv / Semantic Scholar) and extract method, baselines,
   and its headline claim. For the closest neighbors, also fetch full text when open-access
   and note the method mechanism in one sentence.
3. Write each as a `PaperNote` via `rx_state.survey.write_note` under `.rx/notes/papers/`.
   In the note body (beyond structured fields), add a short **open-gap** line: what this
   paper still does not solve that our `Q<n>` targets. Mark unverifiable citations
   `[CITATION NEEDED]`.
4. Compute the candidate baseline set with `rx_state.survey.collect_baselines(notes)` — this
   is what `rx-plan` compares against. Explicitly flag the single **closest neighbor**
   (strongest collision threat) for `rx-grill`.
5. Optionally write `writings/survey-neighborhood.md` summarizing: method-lineage (who
   refines whom), additive vs subtractive gaps, and which baselines are mandatory.
6. Advance `.rx/state.json` stage to `grill` (next: `rx-grill` alignment, then `rx-plan`).

## Outputs
- `.rx/notes/papers/<key>.md` (structured per-paper notes + open-gap)
- A de-duplicated baseline set for `rx-plan`
- Closest-neighbor / collision-threat signal for `rx-grill`
- Updated `.rx/state.json` (stage = grill)
