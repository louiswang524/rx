"""Scan drafted prose for common LLM-writing tells: stock clichés, overused
transition words, and unnaturally uniform sentence rhythm ("low burstiness")."""

import re
import statistics

# Zero-tolerance: near-universally a generated-text tell in this house tone,
# never a legitimate word choice for understated NeurIPS/ICML prose.
HARD_BANNED_PHRASES = (
    "delve into",
    "boasts",
    "rich tapestry",
    "testament to",
    "stands as a testament",
    "navigate the complexities",
    "unlock the potential",
    "harness the power",
    "game-changer",
    "game changer",
    "cutting-edge",
    "ever-evolving landscape",
    "fast-paced world",
    "plays a crucial role",
    "plays a pivotal role",
)

# Legitimate words that read as an AI tell only when overused across one paper.
TRANSITION_WORDS = (
    "moreover",
    "furthermore",
    "additionally",
    "in conclusion",
    "in summary",
    "it is important to note",
    "it is worth noting",
    "notably",
)

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
_WORD_RE = re.compile(r"\S+")


def scan_ai_tells(text: str, transition_threshold: int = 3) -> list[str]:
    lowered = text.lower()
    findings = []
    for phrase in HARD_BANNED_PHRASES:
        count = lowered.count(phrase)
        if count:
            findings.append(f'AI cliché "{phrase}" found {count}x')
    for word in TRANSITION_WORDS:
        count = lowered.count(word)
        if count > transition_threshold:
            findings.append(
                f'transition word "{word}" overused ({count}x, threshold {transition_threshold})'
            )
    return findings


def sentence_lengths(text: str) -> list[int]:
    sentences = [s.strip() for s in _SENTENCE_SPLIT_RE.split(text) if s.strip()]
    return [len(_WORD_RE.findall(s)) for s in sentences]


def low_burstiness(text: str, min_stdev: float = 4.0, min_sentences: int = 5) -> bool:
    lengths = sentence_lengths(text)
    if len(lengths) < min_sentences:
        return False
    return statistics.pstdev(lengths) < min_stdev
