# RX — ML/CS Research Skill Set

RX is a unified set of skills for running an ML/CS research project end-to-end, from a
vague idea to a paper, with on-disk traceability and evidence gates. It works on Claude Code
and Codex (skills load natively on both; the `model:` field in each SKILL.md is Claude-only
routing and is ignored by Codex).

## The pipeline

```
rx-spinoff ─┐
rx-ideate ──┴─→ rx-survey -> rx-plan -> rx-experiment -> rx-analyze -> rx-write -> rx-review
                          \__ rx-pipeline orchestrates all + self-improving --loop __/
```

Invoke a stage by name (e.g. "use rx-ideate to ...") or run `rx-pipeline` to chain them.

Two cold-start front-ends feed `rx-survey`: `rx-ideate` (from a vague topic) and `rx-spinoff`
(from an existing paper — it critiques the paper, derives ranked novelty-checked follow-up
directions, seeds `.rx/`, then auto-continues, stopping at the plan lock before any compute).

## Two-tier layout

- **Centralized KB** at `~/.rx-kb/` — shared across all projects: system/GPU snapshot,
  API config (secrets, referenced not copied), reusable `pitfalls/` and `learnings/`, a shared
  `uv` package cache, and the shared `venv/` (see below). Create/refresh it with `scripts/kb-init.sh`.
- **Per-project repo** — each research project is a fresh `git init` with its own `.rx/`
  traceability tree. Create one with `scripts/bootstrap.sh <dir> <name>`.
- **Shared venv** — one Python venv lives at `~/.rx-kb/venv/` (override with `RX_VENV_DIR`) with
  `rx_state` installed editable. Every project's `.venv` is a symlink to it, so packages are
  installed once instead of once per project. `bootstrap.sh` creates/updates the shared venv and
  points the new project's `.venv` at it.

## Traceability & rigor (the point of RX)

State lives on disk under `.rx/`, not in chat: `questions/ evidence/ claims/ experiments/` +
`state.json`. Claims carry a strength (`speculative | supported | strong`) and cannot be stated
as fact in the paper unless `rx_state.gates.can_promote` certifies them — otherwise `rx-write`
marks them `[UNSUPPORTED]`. `supported` needs a linked positive experiment; `strong` needs
>=2 seeds + a baseline + a linked commit. Plan in machine-time (iterations/compute), not human-days.

## Python helpers (`rx_state`)

The skills call these; installed once into the shared venv (`uv pip install --python ~/.rx-kb/venv/bin/python -e <this-plugin>`):
`schema` (artifacts) · `gates` (evidence gates) · `store` (state + artifact I/O) · `survey`
(paper notes + `collect_baselines`) · `planlock` (blocker-first lock) · `capture` (reproducible runs)
· `analysis` (metric stats + outcomes) · `anonymize` (double-blind, case-insensitive) · `reproduce`
(`REPRODUCE.md`) · `review` (panel + repro checklist) · `pipeline` (stage machine + `loop_step`).

## Outputs of a run

`rx-write` emits four synchronized artifacts: `paper/arxiv/` and `paper/anon/` as LaTeX source
(`main.tex` + `preamble.tex` + `refs.bib`; the anon copy is anonymity-linted), `code/` +
`code/REPRODUCE.md`, and `blog/<slug>.md` (markdown). The blog is never auto-pushed — it asks
for confirmation first.

## Loop mode

`rx-pipeline` with `--loop`: after analyze, decide `improved` and `gate_cleared`, then call
`rx_state.pipeline.loop_step`. A negative result is fuel — the loop feeds it back into a new
hypothesis (`ideate`). It terminates on `stop_success` (gate cleared), `stop_no_improve`
(diminishing returns), or `stop_budget` (iteration budget). Negative/ablation results are
written up honestly rather than discarded.

There is also a second, inner **drafting loop** at the `write`/`review` stage: `rx-write` drafts,
`rx-review` files findings to `.rx/reviews/round-<n>.md`, and `rx_state.pipeline.draft_loop_step`
decides `stop_clean` (no majors), `stop_budget`, or `continue` (→ `rx-write --mode=revise`). So rx
has two loops — the outer research loop (evidence-driven) and the inner drafting loop (review-driven).
