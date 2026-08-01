---
name: rx-survey
description: Ingest arXiv / Semantic Scholar papers into structured method/baseline notes and a reading queue, and surface the baselines the field actually compares against.
model: sonnet
---

# rx-survey

## Purpose
Turn the reading list into structured `PaperNote`s (method, baselines, headline claim) so later
stages reuse them — especially the baseline set that comparable papers report against.

## Steps
1. Build a reading queue for the question(s) from `.rx/questions/`.
2. For each paper, fetch metadata (arXiv / Semantic Scholar) and extract method, baselines, and its headline claim.
3. Write each as a `PaperNote` via `rx_state.survey.write_note` under `.rx/notes/papers/`.
4. Compute the candidate baseline set with `rx_state.survey.collect_baselines(notes)` — this is what `rx-plan` compares against.
5. Advance `.rx/state.json` stage to `grill` (next: `rx-grill` alignment, then `rx-plan`).

## Outputs
- `.rx/notes/papers/<key>.md` (structured per-paper notes)
- A de-duplicated baseline set for `rx-plan`
- Updated `.rx/state.json` (stage = grill)
