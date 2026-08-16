import glob
import os
import re
from dataclasses import dataclass

SEVERITIES = ("major", "minor", "praise")
_INCLUDEGRAPHICS_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")


@dataclass
class ReviewFinding:
    reviewer: str
    severity: str
    comment: str

    def __post_init__(self) -> None:
        if self.severity not in SEVERITIES:
            raise ValueError(f"invalid severity {self.severity!r}; expected {SEVERITIES}")


def recommend(findings: list[ReviewFinding]) -> str:
    severities = {f.severity for f in findings}
    if "major" in severities:
        return "reject"
    if "minor" in severities:
        return "minor revision"
    return "accept"


def repro_checklist(has_code: bool, has_seeds: bool, has_configs: bool) -> list[str]:
    missing = []
    if not has_code:
        missing.append("code")
    if not has_seeds:
        missing.append("seeds")
    if not has_configs:
        missing.append("configs")
    return missing


def extract_figure_paths(tex: str, base_dir: str | None = None) -> list[str]:
    """Pull \\includegraphics targets out of a rendered .tex source.

    If base_dir is given, each path is resolved relative to it and, when the literal
    path doesn't exist (LaTeX allows omitting the extension), the first of
    .pdf/.png/.jpg/.jpeg that does exist is substituted.
    """
    paths = _INCLUDEGRAPHICS_RE.findall(tex)
    if base_dir is None:
        return paths
    resolved = []
    for p in paths:
        candidate = os.path.join(base_dir, p)
        if not os.path.exists(candidate) and "." not in os.path.basename(p):
            for ext in (".pdf", ".png", ".jpg", ".jpeg"):
                if os.path.exists(candidate + ext):
                    candidate = candidate + ext
                    break
        resolved.append(candidate)
    return resolved


def write_round(rx_dir: str, n: int, findings: list[ReviewFinding]) -> str:
    reviews_dir = os.path.join(rx_dir, "reviews")
    os.makedirs(reviews_dir, exist_ok=True)
    path = os.path.join(reviews_dir, f"round-{n}.md")
    lines = [f"# Review round {n}", "", f"recommendation: {recommend(findings)}", ""]
    for f in findings:
        lines.append(f"- [{f.severity}] {f.reviewer}: {f.comment}")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return path


def read_round(path: str) -> list[ReviewFinding]:
    findings = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line.startswith("- ["):
                continue
            severity = line[line.index("[") + 1:line.index("]")]
            rest = line[line.index("]") + 1:].strip()
            reviewer, comment = rest.split(":", 1)
            findings.append(ReviewFinding(reviewer=reviewer.strip(),
                                          severity=severity,
                                          comment=comment.strip()))
    return findings


def latest_round(rx_dir: str) -> int:
    nums = []
    for p in glob.glob(os.path.join(rx_dir, "reviews", "round-*.md")):
        base = os.path.basename(p)
        try:
            nums.append(int(base[len("round-"):-len(".md")]))
        except ValueError:
            continue
    return max(nums) if nums else 0
