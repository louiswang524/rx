# Limitations, conclusion, and future work

## Limitations

### Goal

Bound the claim so reviewers trust the positives. Honest limitations are treated
as a strength at ML venues — burying them is worse than stating them.

### What to include

Pull from negative/inconclusive evidence, plan-lock assumptions, and failure cases:

1. **Data regime** — domains, lengths, languages, scales covered.
2. **Assumptions** — labels, tools, teachers, compute, theory conditions.
3. **Evaluation limits** — metrics that miss a failure mode; missing baselines.
4. **Failure modes** — when the method loses or degrades.

### Tone

- Concrete: “We only evaluate …”
- Distinguish **technical defect** (loses on the main claim) from **scope
  limitation** (competitive inside a stated setting).
- Avoid performative humility that undercuts gated strong results.
- If an assumption is load-bearing, also bound it briefly in Abstract/Intro.

## Conclusion and future work

Keep short (~0.5 page for conference papers).

1. Restate the **ping** in fresh words (not a copy-paste of the abstract).
2. Summarize strongest **gated** evidence (point to main table/RQs).
3. State the practical takeaway / so-what.
4. Acknowledge Limitations (or one-sentence restatement).
5. **Future work** — 2–3 concrete next experiments tied to open gaps,
   inconclusive RQs, or negative loop results.

Good: “Extend the lock to long-context benchmarks where RQ2 was inconclusive.”
Bad: “Apply our method to more exciting applications.”

If the research `--loop` ended on `stop_no_improve` / `stop_budget`, report the
best honest result and treat negatives as knowledge.

## Checklist

- [ ] Limitations do not secretly contradict Abstract claims
- [ ] Conclusion introduces no new ungated numbers
- [ ] Future work maps to real open `Q<n>` / failure modes
- [ ] Negative evidence acknowledged where it shaped scope
