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

### Hop 1 — topic search
1. Build a reading queue for the question(s) from `.rx/questions/`. Include:
   - papers named in each question's novelty delta,
   - recent same-task leaves (arXiv / Semantic Scholar / OpenReview when useful),
   - strongest public baselines the field actually reports.
2. For each paper, fetch metadata (arXiv / Semantic Scholar) and extract method, baselines,
   and its headline claim. For the closest neighbors, also fetch full text when open-access
   and note the method mechanism in one sentence.
3. Write each as a `PaperNote` via `rx_state.survey.write_note` under `.rx/notes/papers/`
   with `hop=1`. In the note body (beyond structured fields), add a short **open-gap** line:
   what this paper still does not solve that our `Q<n>` targets. Mark unverifiable citations
   `[CITATION NEEDED]`.

### Hop 2 — citation-graph search (recent-trend pass)
4. For each of the 3–5 closest hop-1 papers (the ones that got full-text treatment in step 2),
   read their related-work / references section and pick the **2–3 most relevant** citations:
   same task or metric, not already covered by a hop-1 note, preferring the most recent.
   Cap the total across all hop-1 papers at **~8 hop-2 papers** — this pass is for surfacing
   the current trend, not exhaustive citation-chasing; stop once it stops adding new signal.
5. Fetch and write each as a full `PaperNote` exactly like hop-1 (method, baselines, claim,
   open-gap line), but set `hop=2` and `via=[<hop-1 key(s) that cited it>]` so provenance is
   traceable.

### Wrap-up
6. Compute the candidate baseline set with `rx_state.survey.collect_baselines(notes)` over
   **all** notes (both hops) — this is what `rx-plan` compares against. Explicitly flag the
   single **closest neighbor** (strongest collision threat, normally a hop-1 note) for
   `rx-grill`.
7. Optionally write `writings/survey-neighborhood.md` summarizing: method-lineage (who
   refines whom), additive vs subtractive gaps, which baselines are mandatory, and a **recent
   trend** subsection drawn from the hop-2 notes (what the field has moved toward since the
   hop-1 papers).
8. Advance `.rx/state.json` stage to `grill` (next: `rx-grill` alignment, then `rx-plan`).

## Outputs
- `.rx/notes/papers/<key>.md` (structured per-paper notes + open-gap; `hop`/`via` mark
  hop-1 topic-search papers vs hop-2 citation-graph papers)
- A de-duplicated baseline set for `rx-plan`, drawn from both hops
- Closest-neighbor / collision-threat signal for `rx-grill`
- Updated `.rx/state.json` (stage = grill)
