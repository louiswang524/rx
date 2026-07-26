---
name: rx-ideate
description: Turn a vague ML/CS research topic into sharp research questions with a novelty check against recent arXiv, and bootstrap the project repo.
model: opus
---

# rx-ideate

## Purpose
Convert a fuzzy idea into `Q<n>` research questions with an explicit gap and a novelty
delta vs. recent prior work, and stand up the project repo so every later stage has state
to write into.

## Steps
1. If no project repo exists, run `scripts/bootstrap.sh <dir> <name>` (fresh git repo, `.rx/` scaffold, `uv venv`).
2. Read the KB at `~/.rx-kb/` (system/GPU, pitfalls, learnings) so ideas fit the hardware and avoid known dead ends.
3. Draft 2–4 candidate research questions. For each, state the gap it fills. **When re-entering from
   a `rx-pipeline --loop continue`** (a prior hypothesis's evidence came back negative), read that
   `E<n>` and root the new hypothesis in what it ruled out — don't just generate an unrelated idea.
4. Novelty check: search recent arXiv / Semantic Scholar for the closest prior work; write the delta ("what we do that they don't").
5. Write each question as a `Q<n>` artifact via `rx_state.store.write_question`. On a loop
   `continue`, set `parent_evidence_id` to the prior negative `E<n>` so the hypothesis lineage
   (hypothesis1 → neg → hypothesis2 → ...) is explicit in `.rx/questions/`. Advance
   `.rx/state.json` stage to `survey`.

## Outputs
- `.rx/questions/Q<n>.md` (one per question, with gap + novelty delta)
- Updated `.rx/state.json` (stage = survey)
