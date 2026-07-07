# RX — ML/CS Research Skill Set

RX is a unified set of skills for running an ML/CS research project end-to-end, from a
vague idea to a paper, with on-disk traceability and evidence gates. It works on Claude Code
and Codex (skills load natively on both; the `model:` field in each SKILL.md is Claude-only
routing and is ignored by Codex).

## The pipeline

```
rx-ideate -> rx-survey -> rx-plan -> rx-experiment -> rx-analyze -> rx-write -> rx-review
                                  \__ rx-pipeline orchestrates all + self-improving --loop __/
```

Invoke a stage by name (e.g. "use rx-ideate to ...") or run `rx-pipeline` to chain them.

## Two-tier layout

- **Centralized KB** at `~/.rx-kb/` — shared across all projects: system/GPU snapshot,
  API config (secrets, referenced not copied), reusable `pitfalls/` and `learnings/`, and a
  shared `uv` package cache. Create/refresh it with `scripts/kb-init.sh`.
- **Per-project repo** — each research project is a fresh `git init` with its own `.venv` and a
  `.rx/` traceability tree. Create one with `scripts/bootstrap.sh <dir> <name>` (it also installs
  the `rx_state` package into the project venv so the skills' Python helpers work).

## Traceability & rigor (the point of RX)

State lives on disk under `.rx/`, not in chat: `questions/ evidence/ claims/ experiments/` +
`state.json`. Claims carry a strength (`speculative | supported | strong`) and cannot be stated
as fact in the paper unless `rx_state.gates.can_promote` certifies them — otherwise `rx-write`
marks them `[UNSUPPORTED]`. `supported` needs a linked positive experiment; `strong` needs
>=2 seeds + a baseline + a linked commit. Plan in machine-time (iterations/compute), not human-days.

## Python helpers (`rx_state`)

The skills call these; install the package into the active project venv (`uv pip install -e <this-plugin>`):
`schema` (artifacts) · `gates` (evidence gates) · `store` (state + artifact I/O) · `survey`
(paper notes + `collect_baselines`) · `planlock` (blocker-first lock) · `capture` (reproducible runs)
· `analysis` (metric stats + outcomes) · `anonymize` (double-blind, case-insensitive) · `reproduce`
(`REPRODUCE.md`) · `review` (panel + repro checklist) · `pipeline` (stage machine + `loop_step`).

## Outputs of a run

`rx-write` emits four synchronized artifacts: `paper/arxiv/` (preprint), `paper/anon/`
(double-blind, anonymity-linted), `code/` + `code/REPRODUCE.md`, and `blog/<slug>.md`.
The blog is never auto-pushed — it asks for confirmation first.

## Loop mode

`rx-pipeline` with `--loop`: after analyze, decide `improved` and `gate_cleared`, then call
`rx_state.pipeline.loop_step`. A negative result is fuel — the loop feeds it back into a new
hypothesis (`ideate`). It terminates on `stop_success` (gate cleared), `stop_no_improve`
(diminishing returns), or `stop_budget` (iteration budget). Negative/ablation results are
written up honestly rather than discarded.
