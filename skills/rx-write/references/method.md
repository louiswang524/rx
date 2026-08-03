# Method

## Goal

Explain the approach so a reader could re-implement the core idea and see
*why* each piece exists. Intuition first, then details (Peyton Jones “whiteboard”
test; Lead → Development).

## Pre-writing

From grill understanding + code, list modules. For each module answer:

1. **How** does it run? (input → steps → output)
2. **Why** is it needed? (which failure mode / RQ pressure)
3. **Why it works** vs obvious alternatives?

Sketch Fig. 1 (pipeline / idea figure) *before* writing subsections; subsection
headers should match the figure’s boxes.

## Writing pattern

1. Open with a short overview that walks Fig. 1 end-to-end.
2. For each major module/subsection, cover:
   - **Motivation** — problem-driven (“because X fails when…, we…”).
   - **Design** — structures + forward pass in execution order.
   - **Advantage** — preferably tied to a measurable behavior tested later.
3. State training objective / inference algorithm explicitly if they are part of
   the scientific claim.
4. Defer long hyperparameter tables and hardware to Experiments (Setup) or
   appendix / `code/REPRODUCE.md`, unless a hyperparameter *is* the claim.

Sentence skeletons:

- `We represent … as …`
- `Given [input], we first …, then …, finally …`
- `This yields [output], used for …`
- `Unlike [alternative], this … because …`

## Checklist

- [ ] Fig. 1 matches Method subsection structure
- [ ] Reader can state the ping after the overview alone
- [ ] Every contribution bullet has a Method home (or is analysis-only)
- [ ] Notation defined at first use and stable with Experiments
- [ ] No results claimed here that belong in Experiments
