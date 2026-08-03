# Canonical paper outline

Read `references/best-practices.md` first. Write `publication/arxiv/main.tex` in
this order unless the style guide explicitly requires a different venue layout.
Keep one job per section.

```text
Abstract
1. Introduction          (+ Contributions bullet list; forward-refs to evidence)
2. Method
3. Experiments           (Setup → one subsection per RQ → Ablations → Analysis)
4. Related Work
5. Limitations
6. Conclusion and Future Work
```

Why Related Work is late: readers need your approach before a literature contrast
is meaningful (Peyton Jones; common ML conference practice). If the calibrated
style guide places Related Work after the introduction, follow the style guide.

## Narrative gate (before drafting prose)

Answer in `writings/story-board.md` (also load
`references/conference-outcome-lessons.md`):

1. **One-sentence ping** — the single reusable idea.
2. **What / Why / So what** — three short bullets.
3. **Contribution list** (2–4 falsifiable items) that will drive the paper.
   Contributions state what is derived/constructed/measured/tightened — not
   method labels alone.
4. **Differentiation axes** vs closest neighbor(s): framing / mechanism /
   insight / domain (Scoop-Check style).
5. **Composition** — primary move (+ optional secondary); avoid unrelated piles.
6. RQ table (include evidence expectation + falsifier):

| RQ | Claim | Gate | Experiment(s) | Visual | Evidence expectation | Falsifier | Answer |
|----|-------|------|---------------|--------|----------------------|-----------|--------|
| Q1 | C1 | … | X1 | T1 | Inspectable if … | Falsified if … | … |

Rules:

1. If the ping is unclear, stop and sharpen claims/RQs — do not draft filler.
2. **Anti novel-but-empty:** if Abstract/Intro novelty has no gated number path
   and no falsifier, rewrite before drafting body sections.
3. Every advertised `Q<n>` appears in Experiments with an explicit answer
   (positive, negative, or inconclusive).
4. Every major Abstract/Intro claim maps to a gated `C<n>`. If `can_promote`
   is false, mark `[UNSUPPORTED]` — never state as fact.
5. Every contribution bullet forward-references Method and/or Experiments
   evidence (`Section`, `Table`, `Figure`).
6. Negative / inconclusive evidence is first-class; do not omit failed loop
   hypotheses that the paper's RQs cover.

## Section → artifact sources

| Section | Primary `.rx/` / plan inputs |
|---------|------------------------------|
| Abstract / Intro | ping, questions, claims, grill understanding, plan lock |
| Method | grill shared understanding, code design, plan lock |
| Experiments | experiments, evidence, analysis summaries, plan lock |
| Related Work | `.rx/notes/papers/*`, survey baselines, closest neighbors |
| Limitations | negative/inconclusive evidence, scope of lock/datasets |
| Conclusion | same as Abstract, plus concrete future work from open gaps |

## Visual budget (minimum)

Reviewers often skim figures before Methods — design for that path.

| Visual | Purpose |
|--------|---------|
| Fig. 1 (teaser / pipeline) | Idea at a glance; referenced from Introduction |
| Table 1 (main results) | Answer the primary RQ vs locked baselines |
| Ablation table or figure | Causal support for key design choices |
| Optional qualitative figure | Failure cases or illustrative examples |

Captions must be self-contained and state the takeaway, not only the setup.
Use colorblind-safe encoding (color + linestyle/markers). Prefer vector plots.
