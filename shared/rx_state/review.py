from dataclasses import dataclass

SEVERITIES = ("major", "minor", "praise")


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
