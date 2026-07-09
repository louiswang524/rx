# rx-spinoff Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a new `rx-spinoff` skill — a second pipeline front-end that turns an external paper into a critique + ranked follow-up research directions, seeds `.rx/`, and auto-continues the pipeline (halting at the plan lock).

**Architecture:** `rx-spinoff` is a markdown-only skill (`SKILL.md`) parallel to `rx-ideate`. It reuses existing `rx_state` helpers (`survey.write_note`, `store.write_question`, `store.save_state`, `pipeline` via `rx-pipeline`) — no new Python. It is discovered as a plugin skill under `skills/` and, for standalone use, via a symlink into `~/.claude/skills/`. Its only new persisted artifact is one plain-markdown critique file.

**Tech Stack:** Markdown SKILL.md (Claude/Codex skill format), pytest for frontmatter validation, existing `rx_state` package.

## Global Constraints

- Skills live at `<repo>/skills/<name>/SKILL.md` with YAML frontmatter: `name`, `description`, `model`.
- `rx-spinoff` `model: opus` (creative + critical, matches `rx-ideate`). The `model:` field is Claude-only routing, ignored by Codex.
- Every SKILL.md body must contain the sections `## Purpose`, `## Steps`, `## Outputs` (asserted by `tests/test_skill_frontmatter.py`).
- No new `rx_state` module or artifact type — critique is written as a plain markdown file.
- The skill must NOT run experiments; it stops at the plan lock (`rx_state.pipeline.stage_blockers` blocks `experiment` until `rx-plan` writes a lock).
- Run tests with `python -m pytest` from the repo root (`/mnt/c/Users/louis/rx`); the `rx_state` package is installed editable in `.venv`.

---

## File Structure

- **Create** `skills/rx-spinoff/SKILL.md` — the skill instructions (the whole deliverable).
- **Modify** `tests/test_skill_frontmatter.py` — add a dedicated content test for rx-spinoff and add it to the parametrized valid-frontmatter list.
- **Modify** `AGENTS.md` — update the pipeline diagram to show the two front-ends and add a one-line description.
- **Create** symlink `~/.claude/skills/rx-spinoff -> /mnt/c/Users/louis/rx/skills/rx-spinoff` — standalone discoverability (mirrors the other rx-* symlinks).

---

### Task 1: Author the rx-spinoff skill

**Files:**
- Create: `skills/rx-spinoff/SKILL.md`
- Modify: `tests/test_skill_frontmatter.py`
- Test: `tests/test_skill_frontmatter.py`

**Interfaces:**
- Consumes (referenced in SKILL.md prose, not imported here): `rx_state.survey.write_note(rx_dir, PaperNote)`, `rx_state.store.write_question(rx_dir, Question)`, `rx_state.store.save_state(rx_dir, state)`, `rx_state.survey.collect_baselines(notes)`, `rx_state.pipeline.stage_blockers(rx_dir, stage)`, and `scripts/bootstrap.sh <dir> <name>`.
- Produces: a discoverable skill named `rx-spinoff` whose body names the reused helpers and the plan-lock stop.

- [ ] **Step 1: Write the failing content test**

Add this function to `tests/test_skill_frontmatter.py` (it reuses the module-level `_parse_frontmatter` helper already defined there):

```python
def test_spinoff_skill_frontmatter_and_content():
    front, body = _parse_frontmatter("rx-spinoff/SKILL.md")
    assert front["name"] == "rx-spinoff"
    assert front["model"] == "opus"
    assert front.get("description")
    for section in ("## Purpose", "## Steps", "## Outputs"):
        assert section in body, f"missing {section}"
    # seeds the pipeline via the existing helpers (no new rx_state code)
    assert "write_note" in body        # seed paper -> PaperNote
    assert "write_question" in body     # follow-up directions -> Q<n>
    # critical read + follow-up derivation
    assert "novelty" in body.lower()    # each direction carries a novelty delta
    assert "future work" in body.lower() or "future-work" in body.lower()
    # auto-continue but stop safely before compute
    assert "rx-pipeline" in body
    assert "plan lock" in body.lower()
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python -m pytest tests/test_skill_frontmatter.py::test_spinoff_skill_frontmatter_and_content -v`
Expected: FAIL — `FileNotFoundError` opening `rx-spinoff/SKILL.md` (file does not exist yet).

- [ ] **Step 3: Create the skill file**

Create `skills/rx-spinoff/SKILL.md` with exactly this content:

````markdown
---
name: rx-spinoff
description: Turn an existing paper into a critique plus ranked, novelty-checked follow-up research directions, seed .rx/ from it, and auto-continue the pipeline (stopping at the plan lock before any compute).
model: opus
---

# rx-spinoff

## Purpose
A second cold-start front-end to the pipeline, parallel to `rx-ideate`. Instead of a vague topic,
you hand it an existing paper. It produces a lightweight critique and 2–4 ranked follow-up
directions, seeds `.rx/` (seed paper as a `PaperNote`, directions as `Q<n>` questions, critique as
a note), then auto-continues `rx-pipeline` — which halts at the plan lock so you vet the direction
before any GPU spend. This is distinct from `rx-review`, which reviews *your own* draft for
accept/reject.

## Inputs
One of: arXiv URL, arXiv ID, DOI, or a local PDF path.
- arXiv / DOI → fetch metadata the same way `rx-survey` does (arXiv / Semantic Scholar).
- Local PDF → read the file directly. If text extraction yields empty/garbage output (a scanned
  PDF), stop with a clear message asking for an arXiv ID or a text-based PDF; do not seed `.rx/`.

## Steps
1. **Locate/scaffold the project (auto-detect).** If a `.rx/` directory exists in the current repo,
   seed there. Otherwise run `scripts/bootstrap.sh <dir> <name>` to git-init a fresh project (own
   `.venv`, `.rx/` scaffold, `rx_state` installed) and seed there.
2. **Ingest the paper.** Extract its method, contributions, baselines, and headline claim.
3. **Lightweight critique.** Write strengths, weaknesses, threats-to-validity, and mine the paper's
   own *Limitations / Future Work* — all aimed at extension opportunities, not accept/reject. Read
   `~/.rx-kb/` (system/GPU snapshot, pitfalls, learnings) so directions fit the hardware and avoid
   known dead ends.
4. **Derive 2–4 follow-up directions.** For each, write a **novelty delta** vs. the seed paper
   ("what we do that they don't"). Rank by leverage-given-hardware, and designate the top-ranked
   one as the **primary** direction the pipeline pursues first.
5. **Seed `.rx/`.**
   - Seed paper → `PaperNote` via `rx_state.survey.write_note` (so its baselines join the set
     `rx-plan` compares against — confirm with `rx_state.survey.collect_baselines`).
   - Each direction → `Q<n>` via `rx_state.store.write_question`, **primary question first**, each
     carrying its gap; put the novelty delta in the question body.
   - Critique → `.rx/notes/spinoff-<key>.md` (plain markdown; no new `rx_state` code).
6. **Auto-continue.** Set `state["stage"] = "survey"` and save via `rx_state.store.save_state`, then
   invoke `rx-pipeline`. It flows survey → plan and stops at the **plan lock** —
   `rx_state.pipeline.stage_blockers` blocks `experiment` until `rx-plan` has written a lock — so no
   compute is spent before you approve. State the stop explicitly and how to resume.

## Outputs
- `.rx/notes/papers/<key>.md` — the seed paper as a `PaperNote`.
- `.rx/questions/Q<n>.md` — one per follow-up direction, primary first, each with gap + novelty delta.
- `.rx/notes/spinoff-<key>.md` — the critique (strengths / weaknesses / threats-to-validity /
  mined future-work → extension opportunities).
- `.rx/state.json` advanced to the plan lock by `rx-pipeline`, with an explicit stop message.
````

- [ ] **Step 4: Add rx-spinoff to the parametrized frontmatter list**

In `tests/test_skill_frontmatter.py`, find the `@pytest.mark.parametrize` decorator on
`test_all_skills_have_valid_frontmatter` and add `("rx-spinoff", "opus"),` to the list. The edited
decorator reads:

```python
@pytest.mark.parametrize("name,model", [
    ("rx-ideate", "opus"), ("rx-survey", "sonnet"), ("rx-plan", "sonnet"),
    ("rx-experiment", "sonnet"), ("rx-analyze", "opus"),
    ("rx-write", "sonnet"), ("rx-review", "opus"), ("rx-pipeline", "opus"),
    ("rx-spinoff", "opus"),
])
```

- [ ] **Step 5: Run the frontmatter tests to verify they pass**

Run: `python -m pytest tests/test_skill_frontmatter.py -v`
Expected: PASS — including `test_spinoff_skill_frontmatter_and_content` and the
`rx-spinoff-opus` parametrized case.

- [ ] **Step 6: Commit**

```bash
git add skills/rx-spinoff/SKILL.md tests/test_skill_frontmatter.py
git commit -m "feat(spinoff): add rx-spinoff skill — spawn follow-up research from a paper"
```

---

### Task 2: Wire rx-spinoff into the ecosystem

**Files:**
- Modify: `AGENTS.md:9-13` (the pipeline diagram block) and the front-ends prose
- Create: symlink `~/.claude/skills/rx-spinoff`

**Interfaces:**
- Consumes: the `skills/rx-spinoff/SKILL.md` created in Task 1.
- Produces: an `AGENTS.md` that documents both front-ends, and a discoverable skill in
  `~/.claude/skills/`.

- [ ] **Step 1: Update the AGENTS.md pipeline diagram**

In `AGENTS.md`, replace the single-line diagram (currently
`rx-ideate -> rx-survey -> rx-plan -> rx-experiment -> rx-analyze -> rx-write -> rx-review` inside
the ```` ``` ```` block under "## The pipeline") with the two-front-end form:

```
rx-spinoff ─┐
rx-ideate ──┴─→ rx-survey -> rx-plan -> rx-experiment -> rx-analyze -> rx-write -> rx-review
                          \__ rx-pipeline orchestrates all + self-improving --loop __/
```

Then, immediately after the sentence beginning "Invoke a stage by name ...", add this line:

```
Two cold-start front-ends feed `rx-survey`: `rx-ideate` (from a vague topic) and `rx-spinoff`
(from an existing paper — it critiques the paper, derives ranked novelty-checked follow-up
directions, seeds `.rx/`, then auto-continues, stopping at the plan lock before any compute).
```

- [ ] **Step 2: Create the standalone symlink**

Run:

```bash
ln -s /mnt/c/Users/louis/rx/skills/rx-spinoff /home/louis/.claude/skills/rx-spinoff
```

- [ ] **Step 3: Verify the symlink resolves to the new SKILL.md**

Run: `cat -n /home/louis/.claude/skills/rx-spinoff/SKILL.md | head -5`
Expected: prints the frontmatter (`--- / name: rx-spinoff / ...`), confirming the symlink resolves.

- [ ] **Step 4: Run the full test suite to confirm nothing regressed**

Run: `python -m pytest -q`
Expected: PASS (all existing tests plus the new rx-spinoff assertions).

- [ ] **Step 5: Commit**

```bash
git add AGENTS.md
git commit -m "docs(spinoff): document rx-spinoff as second pipeline front-end"
```

(The symlink lives under `~/.claude/`, outside the repo, so it is not committed — it is an install
step, consistent with the other rx-* symlinks.)

---

## Self-Review

**Spec coverage:**
- Name/position/model → Task 1 Step 3 frontmatter + Task 2 diagram. ✓
- Inputs (arXiv/DOI/PDF, scanned-PDF failure) → SKILL.md `## Inputs`. ✓
- Auto-detect project vs bootstrap → SKILL.md Step 1. ✓
- Lightweight critique + KB read → SKILL.md Step 3. ✓
- 2–4 ranked directions + novelty delta + primary → SKILL.md Step 4. ✓
- Seed `.rx/` (PaperNote, Q<n>, critique note) via existing helpers → SKILL.md Step 5, asserted by test. ✓
- Auto-continue + plan-lock stop → SKILL.md Step 6, asserted by test (`rx-pipeline`, `plan lock`). ✓
- No new Python → only markdown + test edits. ✓
- AGENTS.md update → Task 2. ✓
- Testing (frontmatter/content) → Task 1 Steps 1–5. ✓

**Placeholder scan:** No TBD/TODO; full SKILL.md content and exact test code included. ✓

**Type consistency:** Helper names used in SKILL.md (`survey.write_note`, `store.write_question`,
`store.save_state`, `survey.collect_baselines`, `pipeline.stage_blockers`) match the assertions in
the Task 1 test and the real `rx_state` API confirmed in the repo. ✓
