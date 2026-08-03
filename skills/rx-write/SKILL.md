---
name: rx-write
description: Draft the paper in LaTeX from evidence-anchored state and emit synchronized outputs — arXiv preprint, double-blind submission, reproducibility code, and a GitHub blog post — with draft and revise modes for the drafting loop.
model: sonnet
---

# rx-write

## Purpose
Turn `.rx/` questions, claims, and evidence into a well-structured LaTeX paper where
every research question is answered, every claim traces to evidence, and synchronized
outputs share one source of truth. Runs in two modes: `draft` (initial paper from
evidence) and `revise` (apply the latest review round's findings).

## Modes
- `--mode=draft` (default): write the paper from scratch from claims/evidence.
- `--mode=revise`: read the latest review round via `rx_state.review.latest_round` +
  `rx_state.review.read_round`, and edit the existing `publication/arxiv/main.tex` to address each
  finding, then re-render `publication/anon/`. If a legacy project still uses `paper/` instead of
  `publication/`, keep using `paper/` for that project. If `latest_round` returns `0`, stop with an
  error — run `--mode=draft` first. Do not regenerate `preamble.tex`/`refs.bib` unless a finding
  requires it. Keep the story board and section structure intact unless a finding demands a change.

## Style calibration
Before drafting, call `rx_state.style.read_style_guide(rx_dir)`. If it returns `None` (first
`--mode=draft` run only — never regenerate on `revise` or once a guide exists): call
`rx_state.style.select_style_sources(notes, 10)` over the existing `.rx/notes/papers/*` corpus
from `rx-survey` (fewer than 10 is fine, don't fetch more). Actually read those papers' full text
(fetch the source, not just the `PaperNote` fields — method/baselines/claim alone don't capture
structure or wording), summarize their section structure, tone, and wording conventions, and write
it via `rx_state.style.write_style_guide`. If the survey corpus is empty, skip this step entirely
(no guide, no blocker — draft from evidence alone).

When a style guide exists (this run or a prior one), follow its **structure** and local wording
habits when writing `main.tex` in both `draft` and `revise` modes. **House tone** is always
`references/tone.md` (understated NeurIPS/ICML): it overrides a salesy style guide on hype
words, hedging, and claim strength. The canonical RX outline below still applies unless the
venue style guide explicitly reorders sections.

## Paper structure
Load `references/best-practices.md` once at the start of drafting, then follow the
section guides below. Do not improvise a different section set on `--mode=draft`.

Canonical outline (see `references/paper-outline.md`) — Related Work is **after**
Method/Experiments so contrasts are meaningful:

```text
Abstract
1. Introduction          (+ Contributions with forward-refs)
2. Method
3. Experiments           (Setup → one subsection per RQ → Ablations → Analysis)
4. Related Work
5. Limitations
6. Conclusion and Future Work
```

Section guides (load the file for the section you are writing):

| Section | Guide |
|---------|-------|
| Research-backed principles | `references/best-practices.md` |
| House tone (understated NeurIPS/ICML) | `references/tone.md` |
| Conference-outcome lessons (1947-paper study) | `references/conference-outcome-lessons.md` |
| Outline + story board | `references/paper-outline.md` |
| Sentence / paragraph craft | `references/writing-craft.md` |
| Abstract | `references/abstract.md` |
| Introduction + contributions | `references/introduction.md` |
| Method | `references/method.md` |
| Experiments / RQs / tables / figures | `references/experiments.md` |
| Related Work | `references/related-work.md` |
| Limitations / Conclusion / Future work | `references/limitations-conclusion.md` |

## Steps
1. **Story board (required on draft; update on revise if RQs change).** Read
   `references/best-practices.md`, `references/tone.md`, and
   `references/conference-outcome-lessons.md`, then
   `.rx/questions/`, claims, evidence, experiments, plan lock, and grill understanding.
   Write `writings/story-board.md` with:
   (a) one-sentence **ping**, (b) What/Why/So-what, (c) 2–4 falsifiable contribution
   bullets (derived/constructed/measured/tightened — not method labels alone),
   (d) **4-axis differentiation** vs closest neighbors (framing / mechanism / insight / domain),
   (e) each `Q<n>` → `C<n>` → gate → experiment(s) → table/figure → **evidence expectation**
   → falsifier → answer.
   If the ping is unclear, or the draft is **novel-but-empty** (novelty without gated
   result path + falsifier), stop and sharpen — do not draft filler.
   Follow `references/paper-outline.md`.
2. **Style calibration** (see above).
3. Assemble claims (`C<n>`) with their linked evidence/experiments.
4. For each claim, call `rx_state.gates.can_promote(claim, evidence, experiments)`. If False,
   render the claim marked `[UNSUPPORTED]` — never state it as fact.
5. Write `publication/arxiv/preamble.tex` from `rx_state.latex.PREAMBLE`, and
   `publication/arxiv/refs.bib` from `rx_state.latex.render_bib(notes)` over `.rx/notes/papers/*`
   (unknown bib fields are left empty for the human to enrich; never invent citations —
   mark unverifiable keys `[CITATION NEEDED]`). Legacy fallback: `paper/arxiv/`.
6. Write the LaTeX body `publication/arxiv/main.tex` using the canonical outline. For each
   section, load its guide in `references/` and apply `tone.md` + `writing-craft.md`.
   Requirements:
   - Understated house tone throughout (no hype adjectives; gated claims only) — `tone.md`.
   - Abstract follows the 5-beat formula; no generic “In recent years…” opener; reject
     novel-but-empty abstracts.
   - Introduction makes What/Why/So-what obvious; contribution bullets forward-reference
     Tables/Figures/Sections; include a 4-axis differentiation contrast; Fig. 1 for skimmers.
   - Method leads with intuition + pipeline figure, then module motivation/design/advantage.
   - Experiments: every run states which RQ/claim it tests; Setup + RQ subsections +
     ablations; self-contained captions; fair baselines; honest negatives.
   - Related Work synthesizes themes (not laundry lists), contrasts on the four axes after
     the method is known; never hide the strongest neighbor.
   - Limitations and Conclusion/Future Work bound claims and propose concrete next experiments.
   - `main.tex` must `\input{preamble}` and `\bibliography{refs}`.
7. Render `publication/anon/` (same three files) by passing the source through
   `rx_state.anonymize.anonymize_text(...)`.
8. Generate `code/REPRODUCE.md` via `rx_state.reproduce.render_reproduce(experiments, run_command)`;
   assemble runnable `code/`.
9. Draft `blog/<slug>.md` (short, public, self-identifying — the opposite of anon; stays markdown).
   Keep working notes/drafts that are not venue-locked under `writings/`.

## Outputs
- `writings/story-board.md` — ping, pillars, contributions, 4-axis delta, RQ→evidence map
- `publication/arxiv/{main.tex, preamble.tex, refs.bib}` — LaTeX preprint (full identity)
- `publication/anon/{main.tex, preamble.tex, refs.bib}` — double-blind submission (anonymized)
- `code/` + `code/REPRODUCE.md` — reproducibility bundle
- `blog/<slug>.md` — short GitHub-blog version (markdown)
- `writings/` — non-venue working drafts and notes

## Anonymity
Before submission, run `rx_state.anonymize.lint_anonymity(anon_text, author_names, self_urls)` on the
`publication/anon/main.tex` content. If it returns any findings (author names, self URLs, "our prior work",
acknowledgment/funding mentions), fix them and re-lint until the list is empty. In `revise` mode,
re-run this lint after every edit.

## Blog
Prepare `blog/<slug>.md` with static-site front-matter and a link to the arXiv + code. Publishing to
the external personal GitHub blog is outward-facing: NEVER auto-push. Present the prepared commit/PR
and ask the user to confirm before pushing.
