# House tone: understated NeurIPS / ICML

Default voice for all `rx-write` drafts unless the project style guide
explicitly overrides a narrower venue rule. Prefer calm precision over sales.

## Voice

1. **Quiet confidence.** State what you did and what the gated evidence shows.
   Do not advertise importance; let the problem and numbers do that work.
2. **Claim only what `can_promote` allows.** Stronger wording requires stronger
   evidence. Speculative ideas stay hedged or marked `[UNSUPPORTED]`.
3. **Specific over glowing.** Prefer mechanisms, metrics, and deltas to
   adjectives.
4. **Fair to prior work.** Describe neighbors accurately; contrast on mechanism
   or assumption, not by belittling them.
5. **Short sentences, one idea each.** Formal but readable — not theatrical.

## Ban / replace list

| Avoid (hype / vague) | Prefer |
|----------------------|--------|
| novel / groundbreaking / state-of-the-art* | name the concrete delta (*“SOTA” only with a cited, gated comparison) |
| powerful / robust / seamless / elegant | say what property improved and by how much |
| remarkable / significant gains† | report the number (†“significant” only for statistical tests) |
| comprehensively / extensively | state the actual suite (N datasets, K seeds, listed ablations) |
| clearly shows / proves‡ | “we find”, “results indicate”, “Table 1 shows” (‡reserve “prove” for proofs) |
| paves the way / opens the door | one concrete implication or future experiment |
| In recent years… / LLMs have revolutionized… | start with the specific problem or result |

## Hedging policy

- **Do hedge** when the claim is out of scope, under-powered, or not gated.
- **Do not hedge** gated main results with decorative “may/might/could potentially”.
- Pattern: unqualified claim ↔ supported/strong evidence; scoped claim ↔ limitation.

Examples:

- Bad: “Our method may potentially achieve remarkable improvements.”
- Good: “On Dataset D, method M improves metric M↑ by 2.1 over baseline B (Table 1; 3 seeds).”
- Bad: “We prove that transformers are obsolete.”
- Good: “Under the locked protocol, M matches B on the primary metric and reduces latency by 18%.”

## Section tone notes

| Section | Tone cue |
|---------|----------|
| Abstract | Dense and factual; headline number; no hype opener |
| Introduction | Motivation via the gap, not via field success stories |
| Method | Neutral engineering prose; motivation without drama |
| Experiments | Report-first; takeaway sentence, then numbers |
| Related Work | Map + precise contrast; no dunking on prior work |
| Limitations | Direct and scoped; not apologetic theater |
| Conclusion | Restate ping + gated finding; concrete future work |

## Relationship to style calibration

If `.rx/notes/style-guide.md` exists, inherit its **structure** and local
wording habits, but **this house tone wins** on hype words, hedging, and
claim strength. If the style guide itself is salesy, do not copy that voice.

## Quick self-check before finishing a draft

- [ ] No banned hype words unless replaced by a gated specific claim
- [ ] Every assertive result sentence points to a table/figure or theorem
- [ ] Prior work is described fairly
- [ ] Limitations are plain, not performative
- [ ] A skeptical reviewer would not call the prose “marketing”
