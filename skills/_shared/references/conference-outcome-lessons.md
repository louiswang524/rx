# Lessons from ML conference outcomes (ResearchStudio-Idea)

Evidence-grounded lessons adapted from Zhao et al., *ResearchStudio-Idea*
([arXiv:2607.04439](https://arxiv.org/abs/2607.04439)): analysis of **1,947**
ICLR/ICML/NeurIPS papers (2021–2025), including Oral, high-citation, and Reject.
Use across `rx-ideate`, `rx-survey`, `rx-grill`, and `rx-write`.

## Core findings (what to act on)

1. **Same strategies, different execution.** Rejects usually sit in the same
   high-level move space as Orals. Failure is weak instantiation, thin
   differentiation, or inspectable-evidence gaps — not “wrong idea class.”
2. **Composition is normal.** Modal papers combine **~2** coordinated moves
   (with a tail at ≥3). Prefer one primary move + at most one supporting move.
3. **Novel-but-empty is a real failure mode.** High surface novelty with weak
   mechanism, weak falsifier, or no decisive experiment.
4. **Contribution ≠ method label.** “We use technique X” is process. The claim
   must say what is **derived, constructed, measured, or tightened**.
5. **Literature → bottleneck → move → mechanism.** Ideas are constructed from a
   grounded gap, not brainstormed from model memory.
6. **Traceability.** Every substantive novelty/prior-art claim should cite a
   retrieved paper (or be marked model-supplied / `[CITATION NEEDED]`).

## Novelty / differentiation axes (Scoop-Check style)

When stating a novelty delta or writing Related Work / Intro contrast, score the
candidate against closest neighbors on **all four** axes:

| Axis | Question |
|------|----------|
| **Problem framing** | Same task/setting, or reframed objective/constraints? |
| **Core mechanism** | Same operator/architecture family, or a different mechanism? |
| **Key insight** | Same explanatory story, or a new why-it-works claim? |
| **Application domain** | Transfer-only, or domain-specific hard case that changes the claim? |

A publishable delta usually needs a clear win on **mechanism and/or insight**,
not domain transfer alone.

## Bottleneck quality bar

A usable bottleneck is a **structural gap left open by retrieved neighbors**, not
a topic label (“improve transformers”). Prefer:

- **Additive gap** — no current leaf method achieves X.
- **Subtractive gap** — every leaf inherits assumption A that may be unnecessary.
- **Regression guard** — proposed “fix” was already done by an ancestor → not novel.

## Evidence expectations (make claims inspectable)

For each major claim, write one line:

> Claim C is inspectable if \<table/figure/ablation\> shows \<prediction\>;
> it is falsified if \<outcome\>.

If you cannot name the inspectable artifact, the claim is not ready for plan lock
or for Abstract/Intro prose.

## Failure-mode audit (reject lessons)

Before locking a plan or drafting strong claims, check:

| Failure mode | Red flag |
|--------------|----------|
| Novel-but-empty | Flashy framing; no falsifier; no gated number path |
| Indistinguishable from sum of parts | Ablation would equal “A+B without interaction” |
| Collapsed constructive move | Sounds like vague “we audit an assumption” after losing the construction |
| Hidden strongest neighbor | Closest baseline missing from survey/plan |
| Premature success | Claiming SOTA before seeds/baselines/lock are honest |
| Thin domain grounding | Bottleneck justified only by model memory, not retrieved full text |

## Pattern vocabulary (lightweight, optional)

Use as **diagnostic labels**, never as the contribution sentence. Common moves
seen in the corpus (names paraphrased for RX):

1. Audit and pivot an assumption  
2. Reframe as a solvable object  
3. Decompose for differentiated treatment  
4. Decompose and delegate to solvers  
5. Encode structure by construction  
6. Substitute the operator or representation  
7. Liberate a fixed generative component  
8. Manufacture the supervisory signal  
9. Unify heterogeneous inputs into one space  
10. Adapt by conditioning, not retraining  
11. Design a confound-isolating diagnostic  
12. Design a property-targeting pretext objective  
13. Characterize a limit, then surpass it  
14. Prove equivalence to unify  
15. Relax discrete search to continuous  

Default composition: **one primary + optional secondary** (corpus mode ≈ 2).

## Where each RX stage uses this

| Stage | Use |
|-------|-----|
| `rx-ideate` | Bottleneck + 4-axis novelty delta + falsification prediction + anti novel-but-empty |
| `rx-survey` | Literature-first neighbors; per-paper open gap; full text when possible |
| `rx-grill` | Collision check on 4 axes; failure-mode audit; evidence expectations → shared understanding |
| `rx-write` | Story board carries axes + expectations; Intro/RW contrast; reject novel-but-empty abstracts |
