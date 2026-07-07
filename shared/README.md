# RX foundation contract

Stage skills (rx-ideate … rx-review, rx-pipeline) build on this.

## Python — `rx_state`
- `schema.py`: `STRENGTHS`, `OUTCOMES`, `STAGES`; `Experiment`, `Evidence`, `Claim`; `validate_strength/outcome`.
- `gates.py`: `evaluate_gate(claim, evidence, experiments) -> (strength, reasons)`; `can_promote(...) -> bool`.
  - `supported` = >=1 linked evidence with a positive outcome. `strong` = >=2 distinct seeds + baseline + commit.
- `store.py`: `default_state`, `load_state`, `save_state`, `write_claim`, `read_claim`.

## Scripts
- `kb-init.sh [KB_DIR]` — create/refresh `~/.rx-kb` (system/GPU, secrets gitignored, index.md). Idempotent.
- `bootstrap.sh <DIR> <NAME> [KB_DIR]` — fresh git repo + `.rx/` scaffold + `state.json` + `uv venv` + first commit. Validates `NAME` against `^[A-Za-z0-9._-]+$`.
- `kb-sync.sh <DIR> [KB_DIR]` — promote `notes/{pitfalls,learnings}` back to the KB (filenames prefixed `<projectdir>__`).

## Invariants
- `.rx/state.json` shape is owned by `store.default_state` AND `bootstrap.sh` — keep them in lockstep (a bootstrap test asserts full parity; CI catches drift).
- Claim strength never exceeds what `evaluate_gate` certifies; `rx-write` must mark ungated claims `[UNSUPPORTED]`.

## Slice additions (Plan 2)
- `store.py`: `write_question/read_question`, `write_evidence/read_evidence`, `list_artifacts(rx_dir, kind)`.
- `capture.py`: `capture_run(rx_dir, exp_id, seeds, baseline, config, *, commit, gpu)`, `load_experiment`.
- `anonymize.py`: `anonymize_text`, `lint_anonymity` (used by rx-write on `paper/anon/`).
- `reproduce.py`: `render_reproduce(experiments, run_command)` → `code/REPRODUCE.md`.
- Skills: `rx-ideate` (opus), `rx-experiment` (sonnet), `rx-write` (sonnet). rx-write emits paper/arxiv, paper/anon, code/, blog/.
