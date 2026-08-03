# Related work

## Goal

Give readers a **map of the known neighborhood** and make novelty easy to
verify. Related Work demonstrates scholarship; it is not a chronological laundry
list (Spinellis; SE PhD guides; ML venue practice).

## Placement

By default this section comes **after** Method and Experiments (see
`paper-outline.md`). That way contrasts use vocabulary the reader already has.
If the style guide places it earlier, keep the same paragraph craft.

## Workflow

1. Start from `.rx/notes/papers/*` and the locked baseline set.
2. List directly competing / recent methods first (never hide the strongest).
3. Form **2–4 thematic clusters** (mechanism, problem setting, or tool line).
4. For each cluster: synthesize the paradigm → limitation tied to *our* challenge
   → how this paper differs.
5. Cite every paper that appears as a baseline or key comparison.
6. Never invent citations — mark unverifiable keys `[CITATION NEEDED]`.

## Paragraph template (theme synthesis)

1. Topic sentence: what this cluster is about (cite the group).
2. Compact synthesis of representative methods (individuals parenthetical).
3. Limitation tied to the intro’s technical challenge.
4. Distinction on Scoop-Check axes (framing / mechanism / insight / domain):
   “Unlike …, we …” — mechanism-level, not marketing.

For the single closest competitor, make the four-axis contrast explicit
(even if brief). Never hide that neighbor.

## Do / don't

| Do | Don't |
|----|-------|
| Compare assumptions, failure modes, metrics | “A did X. B did Y.” paper-by-paper dumps |
| Cover strongest baselines from the plan lock | Soft-pedal the closest competitor |
| End each cluster with our gap fill | Re-explain the full method here |
| Be fair when characterizing others | Pad with tangential citations |

## Coverage checklist

- [ ] Every locked baseline appears
- [ ] Closest conceptual neighbors appear
- [ ] Organized by theme, not year alone
- [ ] Each topic ends with a technical distinction
- [ ] Bib keys exist; empty author/year enriched when known from notes
