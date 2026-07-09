# Paper Drafting Subsystem Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give rx a LaTeX paper output and a second self-improving loop — the drafting loop (write → review → revise → review …) — that iterates until the review has no major findings.

**Architecture:** Three new/extended `rx_state` helpers (`latex`, `pipeline.draft_loop_step`, `review` round I/O) plus a `draft_loop` block in `default_state`, wired into the `rx-write`/`rx-review`/`rx-pipeline` SKILLs. `rx-write` renders LaTeX source (no PDF compile) and gains `draft`/`revise` modes; `rx-review` persists each round's findings to `.rx/reviews/`; `rx-pipeline` orchestrates the loop via `draft_loop_step`.

**Tech Stack:** Python 3.11, pyyaml, pytest; markdown SKILL files; LaTeX source output.

## Global Constraints

- Run tests from repo root (`/mnt/c/Users/louis/rx`) with `.venv/bin/python -m pytest`.
- LaTeX output is **source only** — no PDF compilation, no `latexmk`/Makefile, no toolchain dependency.
- The blog output stays markdown (`blog/<slug>.md`) — do not convert it to LaTeX.
- Drafting loop stops when `recommend(findings)` ∈ {`accept`, `minor revision`} OR `iteration >= max_draft_iters` (default 5); mirrors `rx_state.pipeline.loop_step`.
- `recommend` returns exactly one of: `reject` (any major), `minor revision` (any minor, no major), `accept`.
- `ReviewFinding(reviewer, severity, comment)` with `severity ∈ {major, minor, praise}`.
- `PaperNote` fields are `key, title, method, baselines, claim` — bib entries fill only what a note carries; unknown fields (author/year/venue) are emitted empty.
- SKILL bodies must keep the sections asserted by existing tests. `rx-write`: `## Purpose/## Steps/## Outputs/## Anonymity/## Blog` and the tokens `paper/arxiv`, `paper/anon`, `code/`, `blog/`, `can_promote`, `[UNSUPPORTED]`, `lint_anonymity`, `confirm`. `rx-pipeline`: `## Purpose/## Steps/## Outputs/## Loop` and the tokens `stage_blockers`, `loop_step`, `negative`.
- The drafting loop does not run experiments or touch `.rx/` evidence — it only edits the paper.

---

## File Structure

- **Create** `shared/rx_state/latex.py` — `PREAMBLE` constant + `render_bib(notes)`.
- **Create** `tests/test_latex.py` — latex helper tests.
- **Modify** `shared/rx_state/store.py:8-21` — add `draft_loop` block to `default_state`.
- **Modify** `shared/rx_state/pipeline.py` — add `draft_loop_step`.
- **Modify** `tests/test_store.py` — assert the `draft_loop` block.
- **Modify** `tests/test_pipeline.py` — `draft_loop_step` tests + behavioral spine.
- **Modify** `shared/rx_state/review.py` — add `write_round`/`read_round`/`latest_round` + imports.
- **Modify** `tests/test_review.py` — round I/O tests.
- **Modify** `skills/rx-write/SKILL.md` — LaTeX outputs + `draft`/`revise` modes.
- **Modify** `skills/rx-review/SKILL.md` — persist rounds.
- **Modify** `skills/rx-pipeline/SKILL.md` — drafting-loop orchestration.
- **Modify** `tests/test_skill_frontmatter.py` — content tests for the three SKILL changes.
- **Modify** `AGENTS.md` — LaTeX outputs + two-loop description.

---

### Task 1: `rx_state.latex` — preamble + bib rendering

**Files:**
- Create: `shared/rx_state/latex.py`
- Test: `tests/test_latex.py`

**Interfaces:**
- Consumes: `rx_state.survey.PaperNote` (fields `key`, `title`, `method`, `baselines`, `claim`).
- Produces: `PREAMBLE: str`; `render_bib(notes: list[PaperNote]) -> str`.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_latex.py`:

```python
from rx_state.latex import PREAMBLE, render_bib
from rx_state.survey import PaperNote


def test_preamble_has_documentclass():
    assert "\\documentclass" in PREAMBLE


def test_render_bib_one_entry_per_note_with_empty_unknowns():
    notes = [PaperNote(key="muon2024", title="Muon Optimizer"),
             PaperNote(key="grok2022", title="Grokking")]
    bib = render_bib(notes)
    assert bib.count("@misc") == 2
    assert "muon2024" in bib and "grok2022" in bib
    assert "title = {Muon Optimizer}" in bib
    assert "author = {}" in bib   # unknown field left empty for the human
    assert "year = {}" in bib


def test_render_bib_empty_list_is_valid_empty():
    assert render_bib([]) == ""
```

- [ ] **Step 2: Run to verify it fails**

Run: `.venv/bin/python -m pytest tests/test_latex.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'rx_state.latex'`.

- [ ] **Step 3: Create the module**

Create `shared/rx_state/latex.py`:

```python
from rx_state.survey import PaperNote

PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage{natbib}
"""


def render_bib(notes: list[PaperNote]) -> str:
    entries = []
    for n in notes:
        entries.append(
            f"@misc{{{n.key},\n"
            f"  title = {{{n.title}}},\n"
            f"  author = {{}},\n"
            f"  year = {{}},\n"
            f"}}"
        )
    return "\n\n".join(entries) + ("\n" if entries else "")
```

- [ ] **Step 4: Run to verify it passes**

Run: `.venv/bin/python -m pytest tests/test_latex.py -v`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add shared/rx_state/latex.py tests/test_latex.py
git commit -m "feat(latex): add rx_state.latex — LaTeX preamble + bib from PaperNotes"
```

---

### Task 2: `draft_loop` state + `draft_loop_step`

**Files:**
- Modify: `shared/rx_state/store.py:8-21` (`default_state`)
- Modify: `shared/rx_state/pipeline.py` (add `draft_loop_step`)
- Test: `tests/test_store.py`, `tests/test_pipeline.py`

**Interfaces:**
- Produces: `default_state(...)["draft_loop"] == {"iteration": 0, "max_draft_iters": 5}`;
  `draft_loop_step(draft_loop: dict, recommendation: str) -> tuple[dict, str]` where the second
  element is one of `"stop_clean"`, `"stop_budget"`, `"continue"` and `iteration` is incremented.

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_store.py`:

```python
def test_default_state_has_draft_loop():
    st = default_state("p", "/kb")
    assert st["draft_loop"] == {"iteration": 0, "max_draft_iters": 5}
```

Add to `tests/test_pipeline.py` (extend the existing `from rx_state.pipeline import ...` line to also import `draft_loop_step`):

```python
def _draft(**kw):
    base = {"iteration": 0, "max_draft_iters": 3}
    base.update(kw)
    return base


def test_draft_loop_stop_clean_on_accept():
    dl, action = draft_loop_step(_draft(), "accept")
    assert action == "stop_clean"
    assert dl["iteration"] == 1


def test_draft_loop_stop_clean_on_minor_revision():
    _, action = draft_loop_step(_draft(), "minor revision")
    assert action == "stop_clean"


def test_draft_loop_continue_on_reject_under_budget():
    dl, action = draft_loop_step(_draft(iteration=0), "reject")
    assert action == "continue"
    assert dl["iteration"] == 1


def test_draft_loop_stop_budget_on_persistent_reject():
    dl, action = draft_loop_step(_draft(iteration=2, max_draft_iters=3), "reject")
    assert action == "stop_budget"
    assert dl["iteration"] == 3


def test_draft_loop_reject_then_accept_one_revise_cycle():
    # behavioral spine: one reject drives one revise, then accept stops clean
    dl = _draft(max_draft_iters=5)
    dl, a1 = draft_loop_step(dl, "reject")
    assert a1 == "continue"          # -> triggers one rx-write --mode=revise
    dl, a2 = draft_loop_step(dl, "accept")
    assert a2 == "stop_clean"
    assert dl["iteration"] == 2
```

- [ ] **Step 2: Run to verify they fail**

Run: `.venv/bin/python -m pytest tests/test_store.py::test_default_state_has_draft_loop tests/test_pipeline.py -k draft_loop -v`
Expected: FAIL — `KeyError: 'draft_loop'` and `ImportError: cannot import name 'draft_loop_step'`.

- [ ] **Step 3: Add the `draft_loop` block to `default_state`**

In `shared/rx_state/store.py`, inside `default_state`'s returned dict, insert the `draft_loop` block
between the `loop` block and `artifacts` so it reads:

```python
        "loop": {
            "enabled": False,
            "iteration": 0,
            "max_iterations": 20,
            "no_improve_count": 0,
            "no_improve_limit": 5,
        },
        "draft_loop": {
            "iteration": 0,
            "max_draft_iters": 5,
        },
        "artifacts": {"questions": [], "evidence": [], "claims": [], "experiments": []},
```

- [ ] **Step 4: Add `draft_loop_step` to pipeline**

In `shared/rx_state/pipeline.py`, append (the module already imports `copy`):

```python
def draft_loop_step(draft_loop: dict, recommendation: str) -> tuple[dict, str]:
    draft_loop = copy.deepcopy(draft_loop)
    draft_loop["iteration"] = draft_loop.get("iteration", 0) + 1

    if recommendation in ("accept", "minor revision"):
        return draft_loop, "stop_clean"
    if draft_loop["iteration"] >= draft_loop.get("max_draft_iters", 5):
        return draft_loop, "stop_budget"
    return draft_loop, "continue"
```

- [ ] **Step 5: Run to verify they pass**

Run: `.venv/bin/python -m pytest tests/test_store.py tests/test_pipeline.py -v`
Expected: PASS (existing store/pipeline tests + the 6 new ones).

- [ ] **Step 6: Commit**

```bash
git add shared/rx_state/store.py shared/rx_state/pipeline.py tests/test_store.py tests/test_pipeline.py
git commit -m "feat(pipeline): draft_loop state + draft_loop_step (inner drafting loop)"
```

---

### Task 3: Review round persistence

**Files:**
- Modify: `shared/rx_state/review.py` (imports + three functions)
- Test: `tests/test_review.py`

**Interfaces:**
- Consumes: `ReviewFinding`, `recommend` (already in `review.py`).
- Produces: `write_round(rx_dir: str, n: int, findings: list[ReviewFinding]) -> str` (writes
  `<rx_dir>/reviews/round-<n>.md`); `read_round(path: str) -> list[ReviewFinding]`;
  `latest_round(rx_dir: str) -> int` (highest round number, 0 if none).

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_review.py` (extend the top import to add `write_round, read_round, latest_round`):

```python
def test_round_roundtrip(tmp_path):
    rx = str(tmp_path)
    findings = [ReviewFinding("R1", "major", "no ablation"),
                ReviewFinding("R2", "minor", "typo: teh")]
    path = write_round(rx, 1, findings)
    back = read_round(path)
    assert [f.severity for f in back] == ["major", "minor"]
    assert back[0].reviewer == "R1"
    assert back[1].comment == "typo: teh"   # comment with a colon survives


def test_latest_round_returns_highest_and_zero_when_none(tmp_path):
    rx = str(tmp_path)
    assert latest_round(rx) == 0
    write_round(rx, 1, [ReviewFinding("R1", "minor", "x")])
    write_round(rx, 2, [ReviewFinding("R1", "major", "y")])
    assert latest_round(rx) == 2
```

- [ ] **Step 2: Run to verify it fails**

Run: `.venv/bin/python -m pytest tests/test_review.py -k "round" -v`
Expected: FAIL — `ImportError: cannot import name 'write_round'`.

- [ ] **Step 3: Implement the round helpers**

At the top of `shared/rx_state/review.py`, add imports above the `SEVERITIES` line:

```python
import glob
import os
```

Then append to `shared/rx_state/review.py`:

```python
def write_round(rx_dir: str, n: int, findings: list[ReviewFinding]) -> str:
    reviews_dir = os.path.join(rx_dir, "reviews")
    os.makedirs(reviews_dir, exist_ok=True)
    path = os.path.join(reviews_dir, f"round-{n}.md")
    lines = [f"# Review round {n}", "", f"recommendation: {recommend(findings)}", ""]
    for f in findings:
        lines.append(f"- [{f.severity}] {f.reviewer}: {f.comment}")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return path


def read_round(path: str) -> list[ReviewFinding]:
    findings = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line.startswith("- ["):
                continue
            severity = line[line.index("[") + 1:line.index("]")]
            rest = line[line.index("]") + 1:].strip()
            reviewer, comment = rest.split(":", 1)
            findings.append(ReviewFinding(reviewer=reviewer.strip(),
                                          severity=severity,
                                          comment=comment.strip()))
    return findings


def latest_round(rx_dir: str) -> int:
    nums = []
    for p in glob.glob(os.path.join(rx_dir, "reviews", "round-*.md")):
        base = os.path.basename(p)
        try:
            nums.append(int(base[len("round-"):-len(".md")]))
        except ValueError:
            continue
    return max(nums) if nums else 0
```

- [ ] **Step 4: Run to verify it passes**

Run: `.venv/bin/python -m pytest tests/test_review.py -v`
Expected: PASS (existing review tests + the 2 new ones).

- [ ] **Step 5: Commit**

```bash
git add shared/rx_state/review.py tests/test_review.py
git commit -m "feat(review): persist review rounds to .rx/reviews (loop handoff)"
```

---

### Task 4: `rx-write` SKILL — LaTeX output + draft/revise modes

**Files:**
- Modify: `skills/rx-write/SKILL.md` (full rewrite of body)
- Test: `tests/test_skill_frontmatter.py`

**Interfaces:**
- Consumes: `rx_state.latex.PREAMBLE`, `rx_state.latex.render_bib`, `rx_state.review.latest_round`,
  `rx_state.review.read_round` (from Tasks 1 and 3).
- Produces: a `rx-write/SKILL.md` whose body names LaTeX outputs and both modes.

- [ ] **Step 1: Write the failing content test**

Add to `tests/test_skill_frontmatter.py`:

```python
def test_write_skill_latex_and_modes():
    front, body = _parse_frontmatter("rx-write/SKILL.md")
    assert "main.tex" in body and "preamble.tex" in body and "refs.bib" in body
    assert "render_bib" in body
    assert "--mode=draft" in body and "--mode=revise" in body
    assert "latest_round" in body
    # existing guarantees still hold
    for token in ("paper/arxiv", "paper/anon", "code/", "blog/",
                  "can_promote", "[UNSUPPORTED]", "lint_anonymity", "confirm"):
        assert token in body
```

- [ ] **Step 2: Run to verify it fails**

Run: `.venv/bin/python -m pytest tests/test_skill_frontmatter.py::test_write_skill_latex_and_modes -v`
Expected: FAIL — `main.tex` not in body (current SKILL is markdown-only).

- [ ] **Step 3: Rewrite the SKILL body**

Replace the entire contents of `skills/rx-write/SKILL.md` with:

````markdown
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
````

- [ ] **Step 4: Run to verify it passes**

Run: `.venv/bin/python -m pytest tests/test_skill_frontmatter.py -v`
Expected: PASS — the new `test_write_skill_latex_and_modes` and the existing
`test_write_skill_covers_four_outputs_and_gates` both green.

- [ ] **Step 5: Commit**

```bash
git add skills/rx-write/SKILL.md tests/test_skill_frontmatter.py
git commit -m "feat(rx-write): LaTeX output + draft/revise modes"
```

---

### Task 5: `rx-review` SKILL — persist rounds

**Files:**
- Modify: `skills/rx-review/SKILL.md` (Steps + Outputs)
- Test: `tests/test_skill_frontmatter.py`

**Interfaces:**
- Consumes: `rx_state.review.write_round` (from Task 3).
- Produces: a `rx-review/SKILL.md` whose body names `write_round` and the round file path.

- [ ] **Step 1: Write the failing content test**

Add to `tests/test_skill_frontmatter.py`:

```python
def test_review_skill_persists_rounds():
    front, body = _parse_frontmatter("rx-review/SKILL.md")
    assert "write_round" in body
    assert ".rx/reviews/round-" in body
```

- [ ] **Step 2: Run to verify it fails**

Run: `.venv/bin/python -m pytest tests/test_skill_frontmatter.py::test_review_skill_persists_rounds -v`
Expected: FAIL — `write_round` not in body.

- [ ] **Step 3: Edit the SKILL**

In `skills/rx-review/SKILL.md`, replace the `## Steps` list with (adds a persistence step 4,
renumbering the rebuttal step to 5):

```markdown
## Steps
1. Assemble the panel: several independent reviewers with field-specific expertise + a devil's advocate.
2. Each reviewer files `ReviewFinding`s (`major|minor|praise`) against the draft's claims, baselines, and ablations.
3. Compute the panel recommendation with `rx_state.review.recommend` (any major → reject).
4. Persist the round: `rx_state.review.write_round(rx_dir, n, findings)` → `.rx/reviews/round-<n>.md`. The drafting loop reads this file to drive `rx-write --mode=revise`.
5. Run `rx_state.review.repro_checklist(has_code, has_seeds, has_configs)`; any missing item must be fixed before submission.
6. Draft rebuttal responses to the major/minor findings.
```

Then replace the `## Outputs` list with:

```markdown
## Outputs
- A reviewer report (findings + panel recommendation)
- `.rx/reviews/round-<n>.md` — the persisted round (findings + recommendation) for the drafting loop
- A reproducibility checklist result (missing items)
- Rebuttal drafts for the substantive findings
```

- [ ] **Step 4: Run to verify it passes**

Run: `.venv/bin/python -m pytest tests/test_skill_frontmatter.py -v`
Expected: PASS — `test_review_skill_persists_rounds` green and the parametrized rx-review case
(`## Purpose/## Steps/## Outputs`) still green.

- [ ] **Step 5: Commit**

```bash
git add skills/rx-review/SKILL.md tests/test_skill_frontmatter.py
git commit -m "feat(rx-review): persist each review round to .rx/reviews"
```

---

### Task 6: `rx-pipeline` SKILL + AGENTS.md — drafting loop orchestration

**Files:**
- Modify: `skills/rx-pipeline/SKILL.md` (add `## Drafting loop`)
- Modify: `AGENTS.md` (Outputs of a run + two-loop description)
- Test: `tests/test_skill_frontmatter.py`

**Interfaces:**
- Consumes: `rx_state.pipeline.draft_loop_step` (Task 2), `rx_state.review.write_round` (Task 3),
  `rx-write` modes (Task 4).
- Produces: a `rx-pipeline/SKILL.md` documenting the drafting loop.

- [ ] **Step 1: Write the failing content test**

Add to `tests/test_skill_frontmatter.py`:

```python
def test_pipeline_skill_covers_drafting_loop():
    front, body = _parse_frontmatter("rx-pipeline/SKILL.md")
    assert "## Drafting loop" in body
    assert "draft_loop_step" in body
    assert "stop_clean" in body and "stop_budget" in body
    assert "--mode=revise" in body
```

- [ ] **Step 2: Run to verify it fails**

Run: `.venv/bin/python -m pytest tests/test_skill_frontmatter.py::test_pipeline_skill_covers_drafting_loop -v`
Expected: FAIL — `## Drafting loop` not in body.

- [ ] **Step 3: Add the `## Drafting loop` section to rx-pipeline**

In `skills/rx-pipeline/SKILL.md`, append after the existing `## Loop` section:

```markdown
## Drafting loop
A second, inner loop — separate from the research `## Loop` above and independent of `--loop`.
Once the research loop settles and the pipeline reaches `write`, iterate the paper:
1. `rx-write --mode=draft`.
2. `rx-review` — writes `.rx/reviews/round-<n>.md` and yields a `recommendation`.
3. `rx_state.pipeline.draft_loop_step(state["draft_loop"], recommendation)`:
   - `stop_clean` — recommendation is `accept` or `minor revision`; finish.
   - `stop_budget` — `iteration >= max_draft_iters`; finish and report the residual major findings honestly.
   - `continue` — run `rx-write --mode=revise`, then back to step 2.
The drafting loop only edits the paper; it never re-runs experiments or touches `.rx/` evidence.
```

- [ ] **Step 4: Run to verify the SKILL test passes**

Run: `.venv/bin/python -m pytest tests/test_skill_frontmatter.py -v`
Expected: PASS — `test_pipeline_skill_covers_drafting_loop` green and the existing
`test_pipeline_skill_covers_loop_and_gates` (checks `## Loop`, `stage_blockers`, `loop_step`,
`negative`) still green.

- [ ] **Step 5: Update AGENTS.md — Outputs of a run**

In `AGENTS.md`, replace this paragraph under `## Outputs of a run`:

```
`rx-write` emits four synchronized artifacts: `paper/arxiv/` (preprint), `paper/anon/`
(double-blind, anonymity-linted), `code/` + `code/REPRODUCE.md`, and `blog/<slug>.md`.
The blog is never auto-pushed — it asks for confirmation first.
```

with:

```
`rx-write` emits four synchronized artifacts: `paper/arxiv/` and `paper/anon/` as LaTeX source
(`main.tex` + `preamble.tex` + `refs.bib`; the anon copy is anonymity-linted), `code/` +
`code/REPRODUCE.md`, and `blog/<slug>.md` (markdown). The blog is never auto-pushed — it asks
for confirmation first.
```

- [ ] **Step 6: Update AGENTS.md — two loops**

In `AGENTS.md`, at the end of the `## Loop mode` section, append:

```
There is also a second, inner **drafting loop** at the `write`/`review` stage: `rx-write` drafts,
`rx-review` files findings to `.rx/reviews/round-<n>.md`, and `rx_state.pipeline.draft_loop_step`
decides `stop_clean` (no majors), `stop_budget`, or `continue` (→ `rx-write --mode=revise`). So rx
has two loops — the outer research loop (evidence-driven) and the inner drafting loop (review-driven).
```

- [ ] **Step 7: Run the full suite**

Run: `.venv/bin/python -m pytest -q`
Expected: PASS (all prior tests + every test added in Tasks 1–6).

- [ ] **Step 8: Commit**

```bash
git add skills/rx-pipeline/SKILL.md AGENTS.md tests/test_skill_frontmatter.py
git commit -m "feat(rx-pipeline): drafting-loop orchestration + AGENTS two-loop docs"
```

---

## Self-Review

**Spec coverage:**
- Component 1 (LaTeX output) → Task 1 (`latex` helper) + Task 4 (rx-write SKILL emits `main.tex`/`preamble.tex`/`refs.bib`). ✓
- Component 2 (persisted findings) → Task 3 (`write_round`/`read_round`/`latest_round`) + Task 5 (rx-review persists). ✓
- Component 3 (revise mode) → Task 4 (`--mode=draft`/`--mode=revise`, `latest_round==0` error). ✓
- Component 4 (drafting loop) → Task 2 (`draft_loop` state + `draft_loop_step`) + Task 6 (rx-pipeline orchestration). ✓
- New `rx_state` API (latex, draft_loop_step, review rounds, default_state.draft_loop) → Tasks 1–3, all unit-tested. ✓
- Prose/SKILL updates (rx-write, rx-review, rx-pipeline, AGENTS.md) → Tasks 4, 5, 6. ✓
- Failure modes: empty PaperNotes → Task 1 `render_bib([]) == ""`; never-converge → Task 2 `stop_budget`; revise-with-no-round → Task 4 `latest_round==0` error; anonymity re-lint on revise → Task 4 Anonymity section. ✓
- Testing (latex, draft_loop_step incl. behavioral spine, review round I/O, default_state, SKILL content) → Tasks 1–6. ✓
- Non-goals honored: no PDF compile (source only, Global Constraints); blog stays markdown (Task 4); research loop/evidence untouched (Task 6 prose + Global Constraints). ✓

**Placeholder scan:** No TBD/TODO. All code and test bodies are complete; `[UNSUPPORTED]` and empty bib fields are defined behaviors, not placeholders. ✓

**Type consistency:** `draft_loop_step(draft_loop, recommendation) -> tuple[dict, str]` returns exactly `stop_clean`/`stop_budget`/`continue` — consistent across Tasks 2 and 6. `recommend` outputs `accept`/`minor revision`/`reject` — consistent with the stop condition. `write_round(rx_dir, n, findings)` / `read_round(path)` / `latest_round(rx_dir)` signatures identical in Tasks 3, 4, 5, 6. `PaperNote` fields (`key`, `title`) match `render_bib` usage in Task 1. ✓
