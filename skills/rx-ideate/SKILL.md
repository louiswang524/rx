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

## First-mile lessons
Before drafting questions, read
`skills/_shared/references/conference-outcome-lessons.md` (same file under
`rx-write/references/` if that path is easier). Key rules for this stage:

1. **Literature → bottleneck → move → mechanism** (not unconstrained brainstorming).
2. Novelty delta uses **four axes**: framing / mechanism / insight / domain.
3. Reject **novel-but-empty** ideas (flashy, no falsifier, no inspectable evidence path).
4. Contribution is what you derive/construct/measure/tighten — not a method label.
5. Prefer **one primary move + optional secondary** (composition mode ≈ 2).

## Steps
1. If no project repo exists (no `.rx/` in the current workspace):
   - Infer a kebab-case `project-name` and choose a `topic` from the allowed list (ask the
     user if the topic is ambiguous).
   - Run:
     `bash scripts/bootstrap.sh <project-name> --topic <topic>`
   - Continue all later work inside the printed project path
     (`<research-root>/<topic>/<project-name>/`).
2. Read the KB at `~/.rx-kb/` (system/GPU, pitfalls, learnings) so ideas fit the hardware and avoid known dead ends.
3. **Ground lightly before inventing.** Search recent arXiv / Semantic Scholar for the
   neighborhood of the user's topic (enough to name closest leaves). Identify one
   **bottleneck**: a structural gap those neighbors leave open (additive unmet need, or
   subtractive inherited assumption). If the direction is too broad or unanchored, ask
   the user to narrow — do not emit generic questions.
4. Draft 2–4 candidate research questions rooted in that bottleneck. For each, state:
   - the **gap** it fills,
   - a **4-axis novelty delta** vs the closest prior work ("what we do that they don't"
     on framing / mechanism / insight / domain),
   - a **falsification prediction** (what outcome would kill the idea),
   - an **evidence expectation** (what table/figure would make the claim inspectable).
   Prefer one primary question + supporting questions that form a single paper
   (composition), not unrelated threads.
   **When re-entering from a `rx-pipeline --loop continue`** (a prior hypothesis's
   evidence came back negative), read that `E<n>` and root the new hypothesis in what
   it ruled out — don't just generate an unrelated idea.

   **Tournament mode** (`rx-ideate --tournament [N]`, default `N=4`): instead of one
   composed set, draft `N` fully **independent** candidates, each rooted in a *different*
   bottleneck from step 3 (not variations on one bottleneck — the point is diverse
   competing framings). Score each with `rx_state.tournament.CandidateScore(question_id,
   novelty, feasibility, falsifiability, evidence_inspectability)` — each rubric axis is
   an integer 0–3, judged the same way you'd judge any candidate under steps 4–6 (novelty
   delta strength, KB/hardware fit, whether a falsifier is nameable, whether the evidence
   expectation is genuinely inspectable). Persist the field with
   `rx_state.tournament.write_tournament(rx_dir, scores, winner_id)` for the audit trail,
   then carry only the winning candidate through steps 5–7 below (do not write `Q<n>`
   artifacts for the runners-up — the tournament record already preserves why they lost).
5. **Anti novel-but-empty gate.** Drop or rewrite any candidate that cannot name both a
   falsifier and an evidence expectation, or whose only delta is domain transfer with
   the same mechanism+insight.
6. Novelty check (finalize): re-search for the closest prior work on the chosen
   mechanism; keep the delta honest. Mark unverifiable citations `[CITATION NEEDED]`.
7. Write each question as a `Q<n>` artifact via `rx_state.store.write_question` (put gap
   in the `gap` field; put novelty axes + falsifier + evidence expectation in the
   question body). On a loop `continue`, set `parent_evidence_id` to the prior negative
   `E<n>` so the hypothesis lineage (hypothesis1 → neg → hypothesis2 → ...) is explicit
   in `.rx/questions/`. Advance `.rx/state.json` stage to `survey`.

## Engineering-optimization mode

Triggered by `rx-ideate --engineering`, or infer it yourself when the user's ask is phrased
as "make X faster / beat Y" rather than "advance the state of the art on X" — a kernel,
system, or config-tuning optimization with no publication intent. Confirm with the user if
it's genuinely unclear which mode applies; don't silently guess on an ambiguous ask.

The default mode's novelty machinery (steps 3–6 above) assumes a citable-literature space
and a contribution worth publishing. An engineering-optimization question usually has
neither — it's applying known technique to a specific system/hardware target, and "novel"
isn't even the goal. Forcing it through the novelty-delta framing produces a hollow,
padded-out 4-axis table for a question that was never trying to be novel. In this mode:

- **Step 3 becomes technique grounding, not novelty grounding.** Instead of searching for a
  literature gap, identify the concrete target to beat (a specific library/tool/prior
  version — see `rx-survey`'s non-paper baseline handling) and the known technique(s) that
  apply to this problem class (fusion, tiling, autotuning, caching, algorithmic
  substitution — whatever fits). No "bottleneck in the literature" is required.
- **Step 4's novelty delta is replaced by an honest scope statement**: name the target
  baseline explicitly, and state plainly that the technique is not novel (cite what it's
  known from, if anything) — don't manufacture a 4-axis delta where none exists. Falsifier
  and evidence expectation are still required and still concrete (e.g. "within N% of
  baseline at all tested configs → no real gap here").
- **Step 5's gate becomes an anti-vague-empty gate**, not an anti-novel-but-empty gate: drop
  or rewrite any candidate that cannot name both a falsifier and an evidence expectation, or
  that has no concrete baseline to beat. Do **not** reject a candidate merely for lacking a
  novelty delta — that's expected and fine in this mode.
- **Step 6 becomes a baseline check, not a novelty check**: confirm the named baseline is
  actually the best-known one for this problem (not stale or already superseded), rather
  than re-searching for prior work to differentiate from.
- **Step 7 is unchanged**, except the question body should read as an honest engineering
  scope statement (see `triton-gemm-opt`/`sol-execbench-rmsnorm` dogfood projects' `Q1.md`
  for the shape this takes) rather than force-fitting the default mode's novelty template.

Tournament mode (above) still applies in engineering mode if useful — rank candidate
optimization targets/techniques on feasibility/falsifiability/evidence-inspectability, just
score `novelty` as `0` for all candidates rather than omitting the rubric axis (keeps
`CandidateScore`'s schema uniform across modes).

## Outputs
- Project scaffold under `<research-root>/<topic>/<project-name>/` with
  `code/`, `writings/`, `experiments/`, `publication/{arxiv,anon}/`, and `.rx/`
- `.rx/questions/Q<n>.md` (one per question, with gap + novelty delta + falsifier, or —
  engineering mode — gap + scope statement + falsifier)
- `.rx/ideate/tournament.md` (tournament mode only — ranked candidates + rationale)
- Updated `.rx/state.json` (stage = survey)
