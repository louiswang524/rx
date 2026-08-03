# Research-backed writing principles (RX)

Synthesize these principles into every draft. They come from widely cited CS/ML
writing advice (Simon Peyton Jones; Neel Nanda / Karpathy-style narrative advice;
Sebastian Farquhar’s abstract formula; Gopen & Swan reader-expectation research;
venue norms at NeurIPS/ICML/ICLR; standard scientific figure/table guidance).

## 1. One clear idea (“the ping”)

- A paper sells **one reusable insight**, not a pile of runs.
- If you cannot state the contribution in **one sentence**, do not draft yet —
  sharpen the story board / claims first.
- Everything else (related work, experiments, discussion) exists to support that
  core claim.

## 2. Three pillars (clear by end of Introduction)

| Pillar | Question | Test |
|--------|----------|------|
| **What** | 1–3 specific, falsifiable claims | Can each be refuted by an experiment or proof? |
| **Why** | Evidence that distinguishes hypotheses | Strong baselines, ablations, not “decent results” |
| **So what** | Why the community should care | Ties to a recognized problem, not vanity metrics |

## 3. Contributions drive the paper

- Write contribution bullets **before** filling sections (Peyton Jones).
- Each intro claim must **forward-reference** its evidence
  (`Section~, Table~, Figure~, Theorem~`).
- Bad: “We study X” / “We provide extensive experiments.”
- Good: “We introduce Z, which improves metric M by X% vs baseline B on dataset D
  (Table 1).”

## 4. Reader path (front-load value)

Reviewers typically read: **title → abstract → intro → figures → maybe the rest**.

Spend disproportionate care on abstract, introduction, and figures. Methods can
start early (often by page 2–3 in two-column format); do not bury the idea.

## 5. Section order (default ML/CS conference)

Prefer Related Work **after** Method/Experiments so readers know your approach
before the literature contrast (Peyton Jones; common NeurIPS/ICML practice).
Venue style guides may override.

```text
Abstract
1. Introduction (+ Contributions)
2. Method
3. Experiments (Setup → RQ answers → Ablations → Analysis)
4. Related Work
5. Limitations
6. Conclusion and Future Work
```

## 6. Experiments serve claims / RQs

- Every experiment states **which claim or RQ** it tests.
- Prefer a few decisive experiments over many vague ones.
- Fair baselines, locked metrics, seeds/error bars, ablations for causality,
  and honest negatives/failure cases.

## 7. Figures and tables carry the skim

- Design visuals so a skimmer can recover the story from captions alone.
- Tables for exact comparisons; figures for trends / pipelines / qualitative cases.
- Do not duplicate full table contents in prose — emphasize the takeaway.
- Colorblind-safe palettes; vector plots; no title burned into the image
  (caption owns the title).

## 8. Related work is a map, not a laundry list

- Synthesize by theme/mechanism; cite individuals parenthetically.
- End each cluster with how **this paper** differs.
- Never hide the strongest neighbor; never invent citations
  (`[CITATION NEEDED]` if unverified).

## 9. Limitations are a strength

- Bound claims early when assumptions are load-bearing.
- Prefer scope boundaries over performative humility.
- Future work must be concrete next experiments, not “more applications.”

## 10. Prose craft (reader expectations)

From Gopen & Swan and common ML micro-advice:

1. One idea per sentence / paragraph; topic sentence first.
2. Old information before new; put the stress (key result) at sentence end.
3. Keep subject and verb close; put action in verbs (not nominalizations).
4. Prefer specific nouns (“accuracy +2.1 on ImageNet”) over “performance improves.”
5. Avoid generic openers (“In recent years, deep learning has…”).
6. Active voice with a clear actor (“We show…”) when claiming results.
7. Consistent terminology for each concept.

## Sources (for humans maintaining this skill)

- Simon Peyton Jones — *How to Write a Great Research Paper* (one idea; nail contributions; related work later; examples first).
- Narrative / ML craft compilations drawing on Neel Nanda, Andrej Karpathy, Sebastian Farquhar, Zachary Lipton, Jacob Steinhardt (what/why/so-what; 5-sentence abstract; delete generic openings).
- Gopen & Swan — *The Science of Scientific Writing* (reader structural expectations).
- ICMJE / scientific visualization guidance — self-explanatory tables/figures; caption placement; no data dump duplication.
- Venue practice — NeurIPS/ICML-style contribution bullets, checklists, honest limitations, reproducibility details.
- Zhao et al. — *ResearchStudio-Idea* ([arXiv:2607.04439](https://arxiv.org/abs/2607.04439)): 1,947-paper Oral/HC/Reject analysis; see `conference-outcome-lessons.md` for operational checks (4-axis novelty, novel-but-empty, evidence expectations).
