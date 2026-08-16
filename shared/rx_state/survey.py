import glob
import os
from dataclasses import dataclass, field
import yaml


SOURCE_KINDS = ("paper", "library", "tutorial", "docs")


@dataclass
class PaperNote:
    key: str
    title: str
    method: str = ""
    baselines: list[str] = field(default_factory=list)
    claim: str = ""
    hop: int = 1
    via: list[str] = field(default_factory=list)
    # "paper" (default, citable literature) | "library" | "tutorial" | "docs" -- a non-paper
    # baseline (vendor library, code tutorial, reference docs) grounded by a repo/doc URL
    # instead of a citation. hop-2 citation-graph search only applies to source_kind="paper"
    # notes -- a library/tutorial has no related-work section to walk.
    source_kind: str = "paper"


def write_note(rx_dir: str, note: PaperNote) -> str:
    target = os.path.join(rx_dir, "notes", "papers")
    os.makedirs(target, exist_ok=True)
    front = {"key": note.key, "title": note.title, "method": note.method,
             "baselines": note.baselines, "hop": note.hop, "via": note.via,
             "source_kind": note.source_kind}
    path = os.path.join(target, f"{note.key}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(yaml.safe_dump(front, sort_keys=False))
        f.write("---\n\n")
        f.write(note.claim + "\n")
    return path


def read_note(path: str) -> PaperNote:
    with open(path, encoding="utf-8") as f:
        _, front_block, body = f.read().split("---", 2)
    front = yaml.safe_load(front_block)
    return PaperNote(key=front["key"], title=front["title"],
                     method=front.get("method") or "",
                     baselines=front.get("baselines") or [],
                     claim=body.strip(),
                     hop=front.get("hop") or 1,
                     via=front.get("via") or [],
                     source_kind=front.get("source_kind") or "paper")


def collect_baselines(notes: list[PaperNote]) -> list[str]:
    seen = set()
    for n in notes:
        seen.update(n.baselines)
    return sorted(seen)
