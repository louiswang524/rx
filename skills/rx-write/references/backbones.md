# Backbone skeletons (mined from 25 high-citation and award-winning papers)

## Goal

A **fill-in-the-blank structural starting point** per section, mined by reading
16 canonical/high-citation papers spanning core architecture & scaling, post-training/
alignment, agents, and reasoning/retrieval, plus 9 Best/Outstanding Paper Award
winners from top venues (2023-2025) in the same space. These are rhetorical-move skeletons, not
templates to copy verbatim — paraphrase into your own paper's vocabulary and deviate
whenever the skeleton doesn't fit your story. Use alongside, not instead of, this
section's own guide (`abstract.md`, `introduction.md`, etc.), `tone.md`, and
`writing-craft.md`.

## Source papers

Architecture/scaling: Attention Is All You Need (Vaswani 2017), BERT (Devlin 2018),
GPT-3 (Brown 2020), LLaMA (Touvron 2023), Chinchilla (Hoffmann 2022), Scaling Laws
(Kaplan 2020), GPT-4 Technical Report (OpenAI 2023).
Post-training/alignment: InstructGPT/RLHF (Ouyang 2022), DPO (Rafailov 2023),
Constitutional AI (Bai 2022).
Agents: ReAct (Yao 2022), Reflexion (Shinn 2023), Toolformer (Schick 2023).
Reasoning/retrieval: Chain-of-Thought (Wei 2022), RAG (Lewis 2020).
Efficiency: LoRA (Hu 2021).

**Best/Outstanding Paper Award winners** (top venues, 2023-2025, LLM/agent/post-training
scoped) — same treatment as above, fetched and read in full, not memorized:
- A Watermark for Large Language Models (Kirchenbauer et al.) — ICML 2023 Outstanding Paper
- Are Emergent Abilities of Large Language Models a Mirage? (Schaeffer et al.) — NeurIPS 2023
  Outstanding Paper
- Debating with More Persuasive LLMs Leads to More Truthful Answers (Khan et al.) — ICML 2024
  Best Paper
- Genie: Generative Interactive Environments (Bruce et al.) — ICML 2024 Best Paper
- Rho-1: Not All Tokens Are What You Need (Lin et al.) — NeurIPS 2024 Best Paper Runner-Up
- OLMo: Accelerating the Science of Language Models (Groeneveld et al.) — ACL 2024 Award
- Proving Test Set Contamination in Black-Box Language Models (Oren et al.) — ICLR 2024
  Outstanding Paper
- The PRISM Alignment Dataset (Kirk et al.) — NeurIPS 2024 Datasets & Benchmarks Best Paper
- Faster Cascades via Speculative Decoding (Narasimhan et al.) — ICLR 2025 Outstanding Paper

## Abstract

**Skeleton:**
1. `[Existing paradigm]` is dominant/typically used for `[task/domain]`, but requires
   `[costly/limiting property]`.
2. We `[introduce/propose/show]` `[method name]`, which `[core mechanism, one clause]`.
3. `[Method]` achieves `[headline quantified result]` on `[benchmark(s)]`, `[optionally:
   with X% fewer resources / without Y]`.
4. `[Optional: generalization or scope claim — transfers to Z, or a scaling/ablation
   finding]`.

**When it deviates:** system/technique papers (Attention Is All You Need, LoRA) lead
with the mechanism and a single headline number; empirical-study papers (Chinchilla,
Scaling Laws, GPT-3) lead with the *finding* (an empirical law or capability) rather
than an artifact, and often close on a caveat/scope line instead of a pure win
("...though it still struggles with X"). Exemplars: mechanism-first — Vaswani 2017,
Hu 2021; finding-first — Hoffmann 2022, Brown 2020.

A fourth variant appears in the award-winner set: **critique/audit papers** (Are
Emergent Abilities a Mirage?, Proving Test Set Contamination) open not with a
paradigm+gap but with the *specific claim being challenged*, then state their
counter-finding and how it was validated (analysis + empirical confirmation, not just
a benchmark number). Exemplar: Schaeffer 2023 — "we present an alternative
explanation... and demonstrate this explanation is validated" replaces step 3's
headline result with a headline reinterpretation.

## Introduction

**Skeleton (backward-derived, written forward):**
1. **Hook** — `[domain]` has become central because `[why it matters now]`
   (1-3 sentences establishing momentum/stakes, not a generic history lesson).
2. **Dominant approach today** — `[prevailing method/paradigm]` works by `[mechanism]`.
3. **Gap** — however, it `[specific limitation]`, because `[technical reason, not a
   strawman]`.
4. **Proposed idea** — we `[introduce X]`, which `[key insight/mechanism]` and
   thereby `[closes the gap from step 3]`.
5. **Contributions** — 2-4 falsifiable bullets, each forward-referencing a table/figure/
   section.
6. **Results preview** — strongest gated number(s) + eval scope, 1-2 sentences.

**When it deviates:** agent papers (ReAct, Reflexion) often open with a cognition
analogy (human reasoning-while-acting) rather than a benchmark-limitation hook — use
this only if the analogy sharpens the gap, not as decoration. Papers proposing an
empirical law (Chinchilla, Scaling Laws, Chain-of-Thought) replace step 5's
"contributions" with a **research question** ("how should X trade off against Y?")
that the rest of the paper answers, since the deliverable is a finding, not an
artifact. Exemplars: gap-then-method — Ouyang 2022, Rafailov 2023; analogy hook —
Yao 2022; research-question framing — Hoffmann 2022, Wei 2022.

Two more variants from the award-winner set. **Resource/dataset-release papers**
(OLMo, PRISM) replace step 3's technical gap with an *access/openness* gap ("the
most capable models are closed off, hindering scientific study") and step 5's
contributions with an enumerated list of what's being released (weights, data,
code, logs) rather than claims — the deliverable is the artifact itself.
**Critique papers** (Are Emergent Abilities a Mirage?, Proving Test Set
Contamination) skip step 2 (no single "dominant approach" to state) and instead
open with the specific prior claim under scrutiny plus why it matters (safety
implications, benchmark trust), then pose their skepticism as a testable
alternative rather than a flat rebuttal. Exemplars: resource/openness gap —
Groeneveld 2024, Kirk 2024; claim-under-scrutiny — Schaeffer 2023, Oren 2023.

## Related Work

**Skeleton:**
1. Group prior work into 2-4 **thematic clusters** (not chronological listing).
2. Per cluster: topic sentence naming the theme → compact synthesis of representative
   methods → the limitation shared by the cluster that motivates this paper.
3. End with an explicit contrast for the closest neighbor: "unlike `[X]`, we `[[Y]]`"
   at the mechanism level.

**When it deviates — placement is the real variable here, not content.** Two patterns
recur about equally often among the 16 papers:
- **Early placement** (Section 2, right after the intro) — used when the paper's
  novelty is orthogonal to the literature review and a reader needs that context
  before Method. Exemplars: Devlin 2018 (BERT), Rafailov 2023 (DPO), Hoffmann 2022.
- **Late placement** (after Method/Experiments) — used to let results speak before
  positioning against prior work, common when the empirical result is the headline.
  Exemplars: Brown 2020 (GPT-3), Yao 2022 (ReAct), Hu 2021 (LoRA), Wei 2022 (CoT),
  Lewis 2020 (RAG), Oren 2023 (contamination test, Related Work is second-to-last
  section), Narasimhan 2024 (speculative cascades, Related Work precedes Experiments
  but follows all theory).
Some system papers (Vaswani 2017) use a "Background" section instead of a named
Related Work section, folding prior-approach positioning into the setup for Method.
A third pattern in the award-winner set is **no standalone Related Work section at
all** — resource/system papers (OLMo, Genie) fold literature positioning into the
Introduction (a landscape-review paragraph) and/or scatter it into result tables
(e.g. OLMo's Table 2 benchmarking architecture choices against LLaMA2/Falcon/PaLM)
instead of a dedicated section. Treat this as an option specifically for
artifact/resource papers, not a general license to skip Related Work.

## Method

**Skeleton:**
1. **Intuition first** — one paragraph, no notation: what is the core idea and why
   should it work (whiteboard test — a reader who stops here should still get it).
2. **Formalization** — introduce notation/problem setup, then the mechanism
   (architecture component, objective derivation, or pipeline stage) precisely.
3. **Design walk-through** — module-by-module (or stage-by-stage) description, each
   tied back to the gap from the Introduction: this component exists *because*
   `[limitation X]`.
4. **Practical notes** — what changes vs. a naive/standard implementation (memory,
   compute, inference-time cost), stated honestly even when neutral or slightly
   negative.

**When it deviates:** pipeline-style methods (InstructGPT's 3-stage RLHF, RAG's
retriever+generator) organize Method as **sequential stages**, each a subsection,
mirroring execution order rather than a single mechanism. Derivation-style methods
(DPO) organize Method as a **chain of algebraic steps** from a known objective to
the novel one, with the "key insight" step called out explicitly rather than buried.
Exemplars: stage pipeline — Ouyang 2022 §3, Lewis 2020 §2; derivation chain —
Rafailov 2023 §4; module walk-through — Vaswani 2017 §3, Hu 2021 §4.

Two more variants from the award-winner set. **Dataset-description papers** (PRISM)
replace Method entirely with a **Dataset Description** section: collection
instrument/survey design → interface and procedure → sampling/recruitment strategy,
with ethics/consent/compensation stated in the main text (not deferred to an
appendix) whenever the paper involves human subjects. **Resource/framework papers**
(OLMo) split Method into **Framework** (architecture, data-pipeline construction,
adaptation procedure) and **Training** (distributed setup, optimizer, hardware) —
mirroring execution order like the pipeline variant, but oriented toward
reproducing the artifact rather than justifying a design choice. A narrower
addition: security/robustness-adjacent method papers (A Watermark for LLMs) insert
an **Attacks & Defenses** section after core Method and before Related Work —
threat model → attack taxonomy → mitigation → empirical resistance — use this only
when the contribution's main risk is adversarial circumvention. Exemplars: dataset
description — Kirk 2024 §3; framework+training split — Groeneveld 2024 §2-3;
attacks/defenses addendum — Kirchenbauer 2023 §7.

## Experiments/Results

**Skeleton:**
1. **Setup** — data/benchmarks, baselines (strongest public ones, reproduced vs.
   cited-as-reported), metrics with direction, seeds/compute when relevant.
2. One subsection per **research question or task family** (mirror the RQs from the
   plan/story-board) — not one subsection per baseline.
3. Each subsection: point to the table/figure first, then discuss; close with an
   explicit answer (supported / not supported / mixed).
4. **Ablations** — isolate which design choice causes the gain, tied to specific
   Method modules.
5. Optional: **analysis** subsection — qualitative examples, failure cases, scaling/
   robustness checks.

**When it deviates:** breadth-first empirical papers (GPT-3, Chain-of-Thought,
Chinchilla) organize by **task/benchmark category** across many datasets rather than
by a small number of RQs, because the contribution *is* the breadth. Ablations may
appear as their own major section (LoRA §7's rank/structure analysis) rather than a
Experiments subsection when the analysis is a contribution in its own right, not just
a design check. Exemplars: RQ-per-subsection — Yao 2022 (per-benchmark-family with
explicit ablation variant), Rafailov 2023 §6; breadth-first task grouping —
Brown 2020, Wei 2022, Hoffmann 2022 §4.

Two more variants from the award-winner set. **Case-study structure** (PRISM):
rather than RQ subsections or task-category grouping, each subsection is a full
mini-study with its own Methods-then-Results (operationalization → findings),
used when the paper's contribution is the *dataset* and each case study
demonstrates a different downstream research use enabled by it. **Insight-cascade
structure** (Debating with More Persuasive LLMs): results are split by evaluation
axis (e.g. LLM judges vs. human judges) rather than by RQ or task, and within each
split, findings are presented as a numbered sequence of insights that build on each
other (basic efficacy → mechanism → scaling → protocol comparison) instead of
answering a fixed list of pre-stated questions — appropriate when the empirical
story is genuinely exploratory rather than confirmatory. Critique papers
(Are Emergent Abilities a Mirage?) use a related but distinct **escalating-validation**
structure: each subsection is a separate study (API re-analysis → published-results
meta-analysis → deliberately induced counter-example) that independently confirms
the same claim, trading breadth of tasks for depth of confirmation on one claim.
Exemplars: case studies — Kirk 2024 §4; insight cascade — Khan 2024 §3-4;
escalating validation — Schaeffer 2023 §3-5.

## Discussion/Limitations/Conclusion

**Skeleton:**
1. Restate the core finding/ping in fresh words (not a copy of the abstract).
2. **Limitations** — concrete, technical: data regime, assumptions, evaluation
   blind spots, failure modes; distinguish a scope limitation ("competitive within
   X") from a technical defect ("loses on the main claim").
3. **Broader considerations** (only when relevant to the domain — alignment/safety/
   societal impact papers include this as its own subsection; most system/architecture
   papers omit it).
4. **Future work** — 2-4 concrete next experiments tied to open gaps or negative/
   inconclusive results, not "apply to more exciting applications."

**When it deviates:** many system/architecture papers (Vaswani 2017, BERT) have **no
explicit Limitations section at all** — a short Conclusion suffices when the
contribution is narrow and well-scoped. Alignment/agent papers (Ouyang 2022,
Rafailov 2023, Chain-of-Thought) fold limitations into a longer **Discussion** that
also covers open questions and who/what is affected, sometimes with a separate
Broader-Impacts or Ethics subsection. Exemplars: minimal conclusion, no limitations —
Vaswani 2017, Devlin 2018; Discussion-as-limitations — Ouyang 2022 §5, Rafailov 2023
§7, Hoffmann 2022 §5, Lin 2024/Rho-1 §5 (no separate Conclusion at all); separate
Broader Impacts section — Brown 2020 §6.

Resource/artifact papers (OLMo, Genie) go further still: they often **replace**
Discussion/Limitations with an **Artifacts Released** section (enumerating exactly
what's public — weights, data, code, logs — with license terms) and fold limitations
into a line or two inside the Conclusion rather than a dedicated treatment; OLMo adds
a **License** section justifying its permissive choice, and both OLMo and Genie
report a **Broader Impact** paragraph on responsible-release reasoning. This is the
resource-paper's version of Limitations — the honest content (what's incomplete,
what could be misused) still has to appear somewhere, it's just distributed across
these named sections instead of one. Theory-heavy papers (Faster Cascades via
Speculative Decoding) trend the opposite way: a short, forward-looking Discussion
with almost no limitations, deferring caveats to appendix proofs instead. By
contrast, audit/critique papers (Proving Test Set Contamination) tend to have the
*most* explicit Limitations section of any variant here — a clean numbered list of
concrete method boundaries — since the paper's credibility depends on being precise
about what the test does and doesn't prove. Exemplars: Artifacts-Released pattern —
Groeneveld 2024 §5-6, Bruce 2024 (Genie) Broader Impact; theory-paper thin discussion
— Narasimhan 2024 §7; explicit numbered limitations — Oren 2023 §6.

## Checklist

- [ ] Section skeleton chosen (default vs. named deviation) and stated intent, not
      copied on autopilot
- [ ] Placeholders filled with paper-specific claims, not left as `[bracketed]` text
- [ ] Related Work placement matches rx-write's canonical outline unless a named
      deviation reason applies
- [ ] Limitations present in some form — even a single honest sentence beats silence
- [ ] No verbatim sentences reused from the source papers — skeletons only
- [ ] If this is a resource/dataset paper, considered the Artifacts-Released /
      License / Dataset-Description variants instead of forcing the default
      Method/Discussion skeleton
