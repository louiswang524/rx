---
name: rx-write
description: Draft the paper in LaTeX from evidence-anchored state and emit synchronized outputs — arXiv preprint, double-blind submission, reproducibility code, and a GitHub blog post — with draft and revise modes for the drafting loop.
model: sonnet
---

# rx-write

## Purpose
Turn `.rx/` claims and evidence into a LaTeX paper where every claim traces to evidence, and emit
synchronized outputs from one source of truth so the science never diverges. Runs in two modes:
`draft` (initial paper from evidence) and `revise` (apply the latest review round's findings).

## Modes
- `--mode=draft` (default): write the paper from scratch from claims/evidence.
- `--mode=revise`: read the latest review round via `rx_state.review.latest_round` +
  `rx_state.review.read_round`, and edit the existing `paper/arxiv/main.tex` to address each
  finding, then re-render `paper/anon/`. If `latest_round` returns `0`, stop with an error — run
  `--mode=draft` first. Do not regenerate `preamble.tex`/`refs.bib` unless a finding requires it.

## Style calibration
Before drafting, call `rx_state.style.read_style_guide(rx_dir)`. If it returns `None` (first
`--mode=draft` run only — never regenerate on `revise` or once a guide exists): call
`rx_state.style.select_style_sources(notes, 10)` over the existing `.rx/notes/papers/*` corpus
from `rx-survey` (fewer than 10 is fine, don't fetch more). Actually read those papers' full text
(fetch the source, not just the `PaperNote` fields — method/baselines/claim alone don't capture
structure or wording), summarize their section structure, tone, and wording conventions, and write
it via `rx_state.style.write_style_guide`. If the survey corpus is empty, skip this step entirely
(no guide, no blocker — draft from evidence alone).

When a style guide exists (this run or a prior one), follow its structure/tone/wording conventions
when writing `main.tex` in both `draft` and `revise` modes.

## Steps
1. Assemble claims (`C<n>`) with their linked evidence/experiments.
2. For each claim, call `rx_state.gates.can_promote(claim, evidence, experiments)`. If False, render the claim marked `[UNSUPPORTED]` — never state it as fact.
3. Write `paper/arxiv/preamble.tex` from `rx_state.latex.PREAMBLE`, and `paper/arxiv/refs.bib` from `rx_state.latex.render_bib(notes)` over `.rx/notes/papers/*` (unknown bib fields are left empty for the human to enrich).
4. Write the LaTeX body `paper/arxiv/main.tex` (abstract, method, experiments, related work) that `\input{preamble}` and `\bibliography{refs}`, anchored to evidence.
5. Render `paper/anon/` (same three files) by passing the source through `rx_state.anonymize.anonymize_text(...)`.
6. Generate `code/REPRODUCE.md` via `rx_state.reproduce.render_reproduce(experiments, run_command)`; assemble runnable `code/`.
7. Draft `blog/<slug>.md` (short, public, self-identifying — the opposite of anon; stays markdown).

## Outputs
- `paper/arxiv/{main.tex, preamble.tex, refs.bib}` — LaTeX preprint (full identity)
- `paper/anon/{main.tex, preamble.tex, refs.bib}` — double-blind submission (anonymized)
- `code/` + `code/REPRODUCE.md` — reproducibility bundle
- `blog/<slug>.md` — short GitHub-blog version (markdown)

## Anonymity
Before submission, run `rx_state.anonymize.lint_anonymity(anon_text, author_names, self_urls)` on the
`paper/anon/main.tex` content. If it returns any findings (author names, self URLs, "our prior work",
acknowledgment/funding mentions), fix them and re-lint until the list is empty. In `revise` mode,
re-run this lint after every edit.

## Blog
Prepare `blog/<slug>.md` with static-site front-matter and a link to the arXiv + code. Publishing to
the external personal GitHub blog is outward-facing: NEVER auto-push. Present the prepared commit/PR
and ask the user to confirm before pushing.
