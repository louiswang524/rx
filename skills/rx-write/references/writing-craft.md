# Sentence and paragraph craft

Apply while drafting every section. Based on Gopen & Swan reader-expectation
research and common ML micro-editing advice.

**Tone first:** follow `tone.md` (understated NeurIPS/ICML). These craft rules
shape clarity; they do not license hype.

## Paragraph architecture

1. **First sentence** — states the paragraph’s one message.
2. **Middle** — evidence, mechanism, or contrast.
3. **Last sentence** — reinforce or transition (put weight here when useful).

If a paragraph needs two messages, split it.

## Sentence-level rules

| Rule | Do | Avoid |
|------|----|-------|
| Subject–verb proximity | Keep them close | Long interruptions between subject and verb |
| Stress position | Put the key result at the **end** | Burying the number in the middle |
| Topic position | Start with familiar context | Starting with unexplained novelty |
| Old → new | Link backward, then introduce new | Jumping to new terms cold |
| Action in verbs | “We analyzed …” | “We performed an analysis of …” |
| Specificity | “+2.1 accuracy on ImageNet” | “improves performance” |
| Pronouns | “This result shows …” | Bare “This shows …” |
| Voice | “We show …” for claims | “It is shown that …” by default |

## Words to prefer / delete

**Delete fillers** unless doing real work: actually, basically, essentially, very,
really, quite, fortunately/unfortunately.

**Hedge only when uncertain.** Prefer precise claims you can gate. Do not spray
“may/can/significant” as decoration (`significant` only for statistical tests).

**Avoid incremental-sounding verbs** when claiming a real idea: prefer
introduce / propose / develop over combine / slightly modify / extend — unless
the contribution truly is a careful extension (then say of *what* and *why*).

**Ban generic openers**: “In recent years…”, “Deep learning has revolutionized…”,
“Large language models have achieved remarkable success…”

## Consistency

Pick one term per concept (`model` vs `network`, `example` vs `instance`) and
keep it for the whole paper. Define symbols at first use.

## Skim test

After drafting a section, skim only first sentences of paragraphs + figure/table
captions. If the argument disappears, rewrite topic sentences and captions
before polishing wording.
