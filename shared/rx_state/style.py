import os
from dataclasses import dataclass, field

from rx_state.survey import PaperNote


@dataclass
class StyleGuide:
    source_keys: list[str] = field(default_factory=list)
    structure: str = ""
    tone: str = ""
    wording_conventions: str = ""
    notes: str = ""


def select_style_sources(notes: list[PaperNote], k: int = 10) -> list[PaperNote]:
    return notes[:k]


def write_style_guide(rx_dir: str, guide: StyleGuide) -> str:
    target = os.path.join(rx_dir, "notes")
    os.makedirs(target, exist_ok=True)
    path = os.path.join(target, "style-guide.md")
    lines = [
        "# Style guide",
        "",
        f"source_keys: {', '.join(guide.source_keys)}",
        "",
        "## Structure",
        guide.structure,
        "",
        "## Tone",
        guide.tone,
        "",
        "## Wording conventions",
        guide.wording_conventions,
    ]
    if guide.notes:
        lines += ["", "## Notes", guide.notes]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return path


def read_style_guide(rx_dir: str) -> StyleGuide | None:
    path = os.path.join(rx_dir, "notes", "style-guide.md")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        text = f.read()

    def section(name: str) -> str:
        marker = f"## {name}\n"
        if marker not in text:
            return ""
        start = text.index(marker) + len(marker)
        rest = text[start:]
        end = rest.find("\n## ")
        return (rest if end == -1 else rest[:end]).strip()

    source_keys: list[str] = []
    for line in text.splitlines():
        if line.startswith("source_keys:"):
            raw = line[len("source_keys:"):].strip()
            source_keys = [k.strip() for k in raw.split(",") if k.strip()]
            break

    return StyleGuide(
        source_keys=source_keys,
        structure=section("Structure"),
        tone=section("Tone"),
        wording_conventions=section("Wording conventions"),
        notes=section("Notes"),
    )
