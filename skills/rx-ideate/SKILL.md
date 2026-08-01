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

## Project location (required)
All new RX projects live under the canonical research tree:

```text
$RX_RESEARCH_ROOT/<topic>/<project-name>/
```

Default research root (in order): `RX_RESEARCH_ROOT` env, `~/.rx-kb/research_root`, then
`~/research` (or the Windows path `/mnt/c/Users/<you>/research` when that exists).

Allowed topics: `llm-agents`, `llm-reasoning`, `llm-inference`, `recsys`, `multimodal`,
`dl-optimization`, `_archive`.

Never bootstrap into `rx-projects/`, `Documents/Codex/`, or a random home-directory folder.

## Steps
1. If no project repo exists (no `.rx/` in the current workspace):
   - Infer a kebab-case `project-name` and choose a `topic` from the allowed list (ask the
     user if the topic is ambiguous).
   - Run:
     `bash scripts/bootstrap.sh <project-name> --topic <topic>`
   - Continue all later work inside the printed project path
     (`<research-root>/<topic>/<project-name>/`).
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
- Project scaffold under `<research-root>/<topic>/<project-name>/` with
  `code/`, `writings/`, `experiments/`, `publication/{arxiv,anon}/`, and `.rx/`
- `.rx/questions/Q<n>.md` (one per question, with gap + novelty delta)
- Updated `.rx/state.json` (stage = survey)
