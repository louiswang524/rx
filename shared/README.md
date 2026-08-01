# RX foundation contract

Stage skills (rx-ideate … rx-review, rx-pipeline) build on this.

## Python — `rx_state`
- `schema.py`: `STRENGTHS`, `OUTCOMES`, `STAGES`; `Experiment`, `Evidence`, `Claim`; `validate_strength/outcome`.
- `gates.py`: `evaluate_gate(claim, evidence, experiments) -> (strength, reasons)`; `can_promote(...) -> bool`.
  - `supported` = >=1 linked evidence with a positive outcome. `strong` = >=2 distinct seeds + baseline + commit.
- `store.py`: `default_state`, `load_state`, `save_state`, `write_claim`, `read_claim`.

## Scripts
- `kb-init.sh [KB_DIR]` — create/refresh `~/.rx-kb` (system/GPU, secrets gitignored, index.md, `research_root`). Idempotent.
- `research-root.sh [KB_DIR]` — resolve the canonical research catalog root (`RX_RESEARCH_ROOT` → `~/.rx-kb/research_root` → existing `~/research` / Windows mount → `$HOME/research`).
- `bootstrap.sh <NAME> --topic <TOPIC> [KB_DIR]` — create `<research-root>/<topic>/<name>/` with `code/`, `writings/`, `experiments/`, `publication/{arxiv,anon}/`, `.rx/` scaffold, `state.json`, shared `uv venv`, first commit. Validates `NAME` against `^[A-Za-z0-9._-]+$`. Legacy: `bootstrap.sh <DIR> <NAME> [KB_DIR]`.
- `kb-sync.sh <DIR> [KB_DIR]` — promote `notes/{pitfalls,learnings}` back to the KB (filenames prefixed `<projectdir>__`).

## Invariants
- `.rx/state.json` shape is owned by `store.default_state` AND `bootstrap.sh` — keep them in lockstep (a bootstrap test asserts full parity; CI catches drift).
- Claim strength never exceeds what `evaluate_gate` certifies; `rx-write` must mark ungated claims `[UNSUPPORTED]`.

## Slice additions (Plan 2)
- `store.py`: `write_question/read_question`, `write_evidence/read_evidence`, `list_artifacts(rx_dir, kind)`.
- `capture.py`: `capture_run(rx_dir, exp_id, seeds, baseline, config, *, commit, gpu)`, `load_experiment`.
- `anonymize.py`: `anonymize_text`, `lint_anonymity` (used by rx-write on `paper/anon/`).
- `reproduce.py`: `render_reproduce(experiments, run_command)` → `code/REPRODUCE.md`.
- Skills: `rx-ideate` (opus), `rx-experiment` (sonnet), `rx-write` (sonnet). rx-write emits publication/arxiv, publication/anon, code/, blog/.

## Fill-in stages (Plan 3)
- `survey.py`: `PaperNote`, `write_note/read_note`, `collect_baselines(notes)`.
- `planlock.py`: `PlanLock`, `write_lock/read_lock`, `is_locked(rx_dir)` (blocker-first gate for rx-experiment).
- `analysis.py`: `summarize_metric`, `beats_baseline`, `decide_outcome` (feeds evidence outcomes).
- `review.py`: `ReviewFinding`, `recommend`, `repro_checklist`.
- Skills: `rx-survey` (sonnet), `rx-plan` (sonnet), `rx-analyze` (opus), `rx-review` (opus). Full pipeline now: ideate → survey → plan → experiment → analyze → write → review.

## Alignment stage (grill-me)
- `grill.py`: `SharedUnderstanding`, `write_understanding` / `read_understanding` / `is_grilled(rx_dir)`.
- Skill: `rx-grill` (opus) — after survey, before plan; interactive human/agent alignment.
- `stage_blockers`: `plan` requires grill artifact; `experiment` still requires plan lock.
- Full pipeline: ideate → survey → grill → plan → experiment → analyze → write → review.

## Orchestrator + loop (Plan 4)
- `pipeline.py`: `next_stage`, `advance_stage(state)` (pure), `stage_blockers(rx_dir, stage)` (plan needs grill; experiment needs a lock), `loop_step(loop, improved, gate_cleared) -> (loop, action)`.
  - loop actions: `stop_success` (gate cleared) | `stop_no_improve` | `stop_budget` | `continue` (back to ideate with negative evidence).
- Skill: `rx-pipeline` (opus) — chains all stages, enforces gates, runs `--loop`.
