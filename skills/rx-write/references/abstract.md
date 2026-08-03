# Abstract

## Goal

In ~150–250 words, make a busy reader recover the paper’s **ping** and decide
whether to continue. The abstract is read essentially always — treat it as a
miniature paper.

## Pre-writing

From the story board:

1. One-sentence contribution (the ping).
2. Why the problem is hard / still open.
3. How (named method + specialist keywords for search).
4. Strongest gated result (metric, baseline, dataset).
5. Optional bound on scope if assumptions are load-bearing.

## Recommended formula (5 beats)

Adapted from common ML “5-sentence abstract” practice (e.g. Farquhar-style):

1. **What you achieved** — “We introduce / prove / demonstrate …”
2. **Why it is hard and important**
3. **How** — mechanism teaser + keywords (not a full algorithm dump)
4. **What evidence** — evaluation setting in one clause
5. **Headline number / sharpest finding** — specific, gated, memorable

Alternate classic framing (Peyton Jones / four-move abstract): problem → why
hard → approach + key result → implication.

## Hard rules

1. Start with **this paper’s** contribution — not “In recent years, deep learning…”
   (if the first sentence could open any ML paper, delete it).
2. No claim missing from the story board or failing `can_promote`.
3. Prefer concrete results (“+X on Y vs Z”) over “extensive experiments.”
4. Do not cite other papers in the abstract unless the venue demands it.
5. Self-contained: readable without the body.
6. One message per sentence; do not pack challenge + method + result into one line.
7. **Anti novel-but-empty:** reject abstracts that sound novel but lack a
   headline gated result *and* a clear mechanism/insight (rewrite).
8. **Understated tone** (`tone.md`): no “novel/powerful/remarkable”; let the
   number carry the weight.

## Checklist

- [ ] Ping identifiable in the first 1–2 sentences
- [ ] Challenge, method name, and headline result all present
- [ ] Every quantitative claim maps to a gated `C<n>` / table
- [ ] No generic hype opener; no `[UNSUPPORTED]` stated as fact
- [ ] Scope bound included when a strong assumption is required
