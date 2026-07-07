---
name: rx-write
description: Draft the paper from evidence-anchored state and emit four synchronized outputs — arXiv preprint, double-blind submission, reproducibility code, and a GitHub blog post.
model: sonnet
---

# rx-write

## Purpose
Turn `.rx/` claims and evidence into a paper where every claim traces to evidence, and emit
four synchronized outputs from one source of truth so the science never diverges.

## Steps
1. Assemble claims (`C<n>`) with their linked evidence/experiments.
2. For each claim, call `rx_state.gates.can_promote(claim, evidence, experiments)`. If False, render the claim marked `[UNSUPPORTED]` — never state it as fact.
3. Write the source draft (abstract, method, experiments, related work) anchored to evidence.
4. Render `paper/arxiv/` (full authors, acknowledgments, repo links).
5. Render `paper/anon/` by passing the source through `rx_state.anonymize.anonymize_text(...)`.
6. Generate `code/REPRODUCE.md` via `rx_state.reproduce.render_reproduce(experiments, run_command)`; assemble runnable `code/`.
7. Draft `blog/<slug>.md` (short, public, self-identifying — the opposite of anon).

## Outputs
- `paper/arxiv/` — preprint (full identity)
- `paper/anon/` — double-blind submission (anonymized)
- `code/` + `code/REPRODUCE.md` — reproducibility bundle
- `blog/<slug>.md` — short GitHub-blog version

## Anonymity
Before submission, run `rx_state.anonymize.lint_anonymity(anon_text, author_names, self_urls)` on the
`paper/anon/` content. If it returns any findings (author names, self URLs, "our prior work",
acknowledgment/funding mentions), fix them and re-lint until the list is empty.

## Blog
Prepare `blog/<slug>.md` with static-site front-matter and a link to the arXiv + code. Publishing to
the external personal GitHub blog is outward-facing: NEVER auto-push. Present the prepared commit/PR
and ask the user to confirm before pushing.
