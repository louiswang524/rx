# Table/figure patterns (mined from same 25-paper corpus)

## Goal

Empirical **table-vs-figure decision patterns**, mined by cataloging every Figure and
Table (what it shows, its type, where it sits) across the same 25-paper corpus as
`backbones.md` — see there for the full paper list and award attributions. Where these
patterns confirm, refine, or contradict the hand-written rules in `experiments.md`'s
"Tables vs figures" section, that's noted explicitly. Use this alongside, not instead
of, `experiments.md`.

## The one very consistent rule: continuous trend → figure, discrete comparison → table

No exception found across 25 papers. Anything with a continuous x-axis (model size,
training step, token count, compute, temperature, rank, number of principles/rounds,
dataset duplication count) is **always** a figure/curve — scaling laws, training
curves, ablation sweeps over a continuous knob. Anything comparing a fixed, named set
of methods/variants/benchmarks is **always** a table. This is the sharpest and most
reliable signal in the corpus — sharper than "ablation vs. main result," which is only
a secondary factor (see below). Confirms `experiments.md`'s "trends, curves" → figure
rule; refines "ablation deltas" → table into "ablation deltas across a **small discrete
set** of variants → table; ablation **swept over a continuous parameter** → figure"
(e.g. Constitutional AI's harmlessness-vs-#-principles, Rho-1's token-selection-ratio
sweep, LoRA's rank sweep — all figures, not tables, despite being ablations).

## Figure 1 is not always the architecture diagram — often it's a teaser

`experiments.md` and `introduction.md` already say "Fig. 1 for skimmers" — the mined
corpus shows this splits into two distinct sub-patterns, not one:

- **Diagram-first** (~7/25: Attention Is All You Need, BERT, Constitutional AI, RAG,
  LoRA, Proving Test Set Contamination, DPO) — Figure 1 *is* the architecture/method/
  pipeline diagram.
- **Teaser-first, diagram-second** (majority: GPT-3, InstructGPT, ReAct, Reflexion,
  Toolformer, Chain-of-Thought, Genie, Rho-1, Watermark) — Figure 1 is a qualitative
  example, a headline result/win-rate chart, or a conceptual teaser; the literal
  architecture/pipeline diagram is **Figure 2**.
- **Data-first** (LLaMA, Chinchilla, Scaling Laws, GPT-4, Emergent-Mirage, Faster
  Cascades, Debate) — Figure 1 is a scaling curve or the headline empirical result,
  because there is no novel architecture to diagram; the contribution is a finding.
- **No Figure 1 diagram at all** (OLMo) — resource/framework papers whose architecture
  is a known design (standard Transformer) render it as a **comparison table**
  (OLMo's Table 2: architecture specs vs. LLaMA2/Falcon/PaLM) instead of a figure; the
  paper's first figure doesn't appear until the results section.

Rule of thumb: if the paper's core contribution *is* a new architecture/mechanism,
diagram it in Fig. 1 or Fig. 2. If the contribution is a finding, a dataset, or a
release, Fig. 1 is data (curve/result) or the diagram is skipped/tabled.

## Main results: table, with report-style exceptions

Every paper in the corpus renders its primary numeric comparison as a table — this is
the strongest confirmation of `experiments.md`'s "exact numbers / main baseline
comparison → table" rule, no exceptions among method/system/empirical papers. The one
partial exception: **GPT-4's technical report** presents several headline comparisons
(exam percentiles, MMLU-by-language, factuality evals) as bar-chart **figures** in the
main text, with the exact numbers relegated to an equivalent appendix table — a
report-style pattern (broad audience, many results, precision less critical than
skimmability) rather than a research-paper pattern. Don't use this as license for a
research paper with a small number of RQs; it's specific to breadth-over-depth reports.

## Qualitative examples: figure when visual/situated, table when textual

Two consistent sub-patterns, not interchangeable:
- **Figure**: when the example includes a screenshot, trajectory, generated image, or
  multi-turn interaction that benefits from layout (ReAct's human-in-the-loop
  correction, Reflexion's failed-then-corrected trajectory, Genie's generated
  frames, Toolformer's annotated tool-call example, GPT-3's full generated article).
- **Table**: when the example is a short text span or prompt/response pair, especially
  several side by side (InstructGPT's illustrative prompts, Watermark's
  watermarked-vs-not generation pairs, GPT-4's red-team/refusal examples, RAG's
  BART-vs-RAG generations, Chain-of-Thought's ⟨input, CoT, output⟩ triples).
Both patterns are frequently pushed to an **appendix** rather than the main text
(ReAct, Reflexion, Toolformer §5, RAG) when the paper is result-dense — keep one
compelling in-text example and move the rest.

## A named table type `experiments.md` doesn't call out: the categorical comparison table

Distinct from a main-results table (which reports *your* numbers against baselines on
*your* metric) is a **comparison table** that catalogs categorical/architectural facts
across systems with no single winning metric — OLMo's Table 2 (architecture choices
vs. LLaMA2/Falcon/PaLM), Genie's Table 1 (world-model vs. video-model vs. Genie
capability checklist), Faster Cascades' Table 1 (target distribution / deferral
decision / execution mode across inference algorithms). These typically appear early
(Method or right after Related Work), not in Experiments, and often have text or
checkmarks in cells rather than numbers. Use this pattern when positioning a system
against alternatives on *capabilities*, before Experiments makes the performance case.

## Data/corpus composition table: an early Setup/Method table, not an Experiments table

Papers introducing a new pretraining corpus, dataset, or participant pool put a
composition/statistics table **before** Experiments — in Method or a dedicated Data
section (LLaMA Table 1: source mix and epochs; GPT-3 Table 2.2: dataset weights;
Toolformer Table 2: augmented-dataset counts; OLMo Table 3: Dolma source breakdown;
PRISM's demographic/geographic tables in §3.3). `experiments.md`'s Setup subsection
already covers "datasets/splits" — this confirms that composition tables belong in
Setup or Method, not buried in an Experiments results table.

## Safety/bias/ethics evaluation: its own late table cluster, table format

When a paper reports toxicity, bias, or truthfulness evaluations (LLaMA §5's four
tables — toxicity, CrowS-Pairs, WinoGender, TruthfulQA; OLMo's Table 7; InstructGPT
Fig. 6-7; Constitutional AI throughout), these are almost always **tables** even though
neighboring main results might be figures, and they cluster in their own subsection
near the end of Experiments (just before Discussion/Limitations), not interleaved with
the primary RQ results. Treat this as a distinct checklist item when the paper makes
any safety/fairness claim.

## Hyperparameter tables: appendix-only, don't confuse with results

The corpus's high table counts (LoRA 15, Genie 17, LLaMA 16) are mostly **appendix
hyperparameter tables** (optimizer settings, learning rates, batch sizes per
model/task variant), not additional results. These exist for reproducibility, not
argument — `experiments.md`'s "implementation pointers → REPRODUCE.md" already covers
this; the corpus confirms these belong in an appendix table, not inflating the main
Experiments table count. Don't let a draft's "many tables" instinct come from padding
this category — main-text table count in the corpus is much smaller (typically 3-6)
than total table count once appendices are included.

## Checklist

- [ ] Every continuous-parameter result (scaling, training curves, ablation sweeps
      over a numeric knob) rendered as a figure, not a table
- [ ] Fig. 1 chosen deliberately: diagram (novel architecture), teaser (qualitative/
      result hook), or data (no architecture — finding-first paper) — not defaulted
      to whichever asset was ready first
- [ ] Main results in a table; any results-as-figure choice justified by breadth
      (many benchmarks, report-style), not convenience
- [ ] Qualitative examples: one compelling in-text example (figure if visual/
      situated, table if textual pairs), rest moved to appendix if paper is
      result-dense
- [ ] A categorical/capability comparison table considered if positioning against
      named alternatives on non-metric properties
- [ ] Dataset/corpus composition table (if any) lives in Setup/Method, not dropped
      into Experiments as a result
- [ ] Safety/bias/fairness evaluations (if any) grouped in their own table cluster
      near the end of Experiments, not interleaved with primary RQ results
- [ ] Hyperparameter tables in an appendix, not inflating the main-text table count
