# Experiments: RQs, design, tables, and figures

## Goal

Provide decisive evidence for the story-board claims. Experiments **serve
claims** — each run states which RQ/claim it tests. Prefer a few sharp
experiments over many vague ones.

## Section skeleton

```latex
\section{Experiments}
\subsection{Setup}                 % data, metrics, baselines, seeds, implementation
\subsection{RQ1: ...}               % one RQ per subsection (mirror .rx/questions)
\subsection{RQ2: ...}
\subsection{Ablations}             % causal support for design choices
\subsection{Analysis}              % optional: stress tests, qualitative, failures
```

## Research questions

1. Promote each advertised `Q<n>` to a subsection title.
2. Open with the RQ in one sentence + which claim it tests.
3. Point to the table/figure that answers it **before** discussing details.
4. Close with an explicit answer matching evidence `outcome`:
   supported / not supported / inconclusive.

## Experimental design (Setup)

Pull from `.rx/plan/lock.md` and capture metadata:

1. Datasets / splits and filtering.
2. Primary metric and direction (as locked).
3. Baselines — locked comparison family; include strongest public ones.
   Say whether numbers are reproduced or cited-as-reported.
4. Seeds — mean±std over locked seed policy (≥2 for `strong` claims).
5. Implementation pointers → `code/REPRODUCE.md`.
6. Fairness — same data, preprocessing, and eval protocol across methods.
7. Compute — training/inference cost when relevant to the claim.

## Three evidence questions

1. **Better than strong baselines?** → main results table for primary RQ(s).
2. **Which design choices cause the gain?** → ablations tied to Method modules.
3. **Where does it break?** → stress / OOD / failure cases (feeds Limitations).

## Tables vs figures

| Use a **table** when… | Use a **figure** when… |
|-----------------------|------------------------|
| Exact numbers / many metrics | Trends, curves, pipelines |
| Main baseline comparison | Qualitative examples |
| Ablation deltas | Method overview (Fig. 1) |

### Table rules

1. Caption **above**; one table, one message; self-contained.
2. `booktabs` only (`\toprule` / `\midrule` / `\bottomrule`); no vertical rules.
3. Metric direction in headers (`Accuracy ↑`, `Loss ↓`); bold best / underline second.
4. Consistent decimals; do not re-dump the whole table in prose — state the takeaway.
5. Cite every table in reading order.

### Figure rules

1. Caption **below**; first sentence = takeaway; readable without main text.
2. No title burned inside the image (caption owns it).
3. Colorblind-safe (Okabe–Ito / Tol); redundant linestyle/markers; check grayscale.
4. Prefer vector plots (PDF); label modules with Method names.
5. Result figures include comparison context (baseline), not only “ours.”

## Checklist

- [ ] Every story-board RQ has a subsection and an answer sentence
- [ ] Every intro contribution has identifiable evidence here
- [ ] Main table uses locked metric and baselines
- [ ] Seeds / uncertainty reported when claiming `strong`
- [ ] Ablations exist for each key design contribution
- [ ] Negatives / failure cases reported, not dropped
- [ ] Captions self-contained; visuals skim-readable
