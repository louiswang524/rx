# Introduction and contributions

## Goal

Convince a skeptical reader in ~1–1.5 pages (two-column): the problem matters,
prior approaches leave a precise gap, your idea is clear, and the evidence path
is worth reading. By the end, **What / Why / So what** must be obvious.

## Write contributions first

Nail 2–4 falsifiable contribution bullets **before** polishing prose
(Peyton Jones). Each bullet:

1. Is specific (mechanism, setting, or result — not “a novel framework”).
2. Forward-references evidence (`Section~`, `Table~`, `Figure~`).
3. Maps to the story board (`Q<n>` / `C<n>`).

Good: `A <mechanism> that <does X>, improving <metric> by <Δ> vs <baseline>
(Table 1).`

Bad: `We study X` / `We provide extensive experiments` / `We make several
contributions.`

## Logic (think backward, write forward)

**Backward first**

1. What problem do we solve, and why is it still open?
2. What is the single ping + contribution list?
3. Why do those contributions work (insight)?
4. Which prior lines lead to *our* challenge (not a strawman)?

**Then write forward** (template)

1. **Hook** (2–3 sentences) — specific problem + why it matters *now*.
2. **Challenge** (1 paragraph) — what others tried; limitation + technical reason.
3. **Approach** (1 paragraph) — what we do differently; key insight; point to Fig. 1.
4. **Contributions** (2–4 bullets) — falsifiable + forward refs.
5. **Results preview** (2–3 sentences) — strongest gated numbers + eval scope.
6. Optional one-line roadmap only if it adds navigation; prefer forward refs
   inside contributions over a dull “rest of this paper” list.

## Attracting readers

- Open with *your* problem, not a generic field success story.
- Attract by making the **gap and idea clear**, not by hype (`tone.md`).
- Avoid naive-baseline-then-patch storytelling (“a simple approach would…; we
  improve it by…”), which kills curiosity.
- Give intuition before machinery (whiteboard test): a reader who skips Method
  should still leave with the idea.
- State RQs briefly using `.rx/questions/` wording when possible; full protocol
  lives in Experiments.
- Contribution bullets: concrete and falsifiable — never “a novel framework.”

## Differentiation (from conference-outcome lessons)

Include a short contrast against the closest neighbor(s) on the four axes
(framing / mechanism / insight / domain). Prefer a mechanism or insight delta;
domain transfer alone is usually not enough. Do not defend contributions as
“we use technique X while they use Y” — state what new fact or capability
that choice produces.

## Checklist

- [ ] Ping stated explicitly (“The main idea of this paper is …”)
- [ ] What / Why / So what clear without reading further
- [ ] Contribution bullets falsifiable and forward-referenced
- [ ] Fig. 1 referenced when explaining the idea
- [ ] No overclaim beyond `can_promote`
- [ ] Intro not a mini literature survey (defer depth to Related Work)
- [ ] First sentence of each paragraph states its message
