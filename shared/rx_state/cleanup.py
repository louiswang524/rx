import glob
import os
import shutil
from dataclasses import dataclass

from rx_state.store import list_artifacts, read_claim, read_evidence

LOG_DIR_NAMES = ("wandb", "tensorboard", "lightning_logs", "logs")
PROMOTED_STRENGTHS = ("supported", "strong")


@dataclass
class CleanupCandidate:
    path: str
    kind: str  # "checkpoints" | "logs"
    size_bytes: int
    experiment_id: str | None = None
    protected: bool = False


def dir_size(path: str) -> int:
    total = 0
    for root, _dirs, files in os.walk(path):
        for name in files:
            fp = os.path.join(root, name)
            if not os.path.islink(fp):
                total += os.path.getsize(fp)
    return total


def promoted_experiment_ids(rx_dir: str) -> set[str]:
    claims = [read_claim(p) for p in list_artifacts(rx_dir, "claims")]
    evidence = [read_evidence(p) for p in list_artifacts(rx_dir, "evidence")]
    promoted_evidence_ids = {
        eid for c in claims if c.strength in PROMOTED_STRENGTHS for eid in c.evidence_ids
    }
    return {
        e.experiment_id for e in evidence
        if e.experiment_id and e.id in promoted_evidence_ids
    }


def _experiment_id_from_path(project_dir: str, path: str) -> str | None:
    experiments_root = os.path.join(project_dir, "experiments")
    rel = os.path.relpath(path, experiments_root)
    if rel.startswith(".."):
        return None
    parts = rel.split(os.sep)
    return parts[0] if parts and parts[0] not in ("", ".") else None


def find_checkpoint_dirs(project_dir: str) -> list[str]:
    pattern = os.path.join(project_dir, "experiments", "**", "checkpoints")
    return sorted(p for p in glob.glob(pattern, recursive=True) if os.path.isdir(p))


def find_log_dirs(project_dir: str) -> list[str]:
    found = []
    for root, dirs, _files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d not in (".rx", ".git")]
        for d in dirs:
            if d in LOG_DIR_NAMES:
                found.append(os.path.join(root, d))
    return sorted(found)


def cleanup_candidates(project_dir: str, rx_dir: str) -> list[CleanupCandidate]:
    promoted = promoted_experiment_ids(rx_dir)
    candidates = []
    for path in find_checkpoint_dirs(project_dir):
        exp_id = _experiment_id_from_path(project_dir, path)
        candidates.append(CleanupCandidate(
            path=path, kind="checkpoints", size_bytes=dir_size(path),
            experiment_id=exp_id, protected=bool(exp_id) and exp_id in promoted,
        ))
    for path in find_log_dirs(project_dir):
        exp_id = _experiment_id_from_path(project_dir, path)
        candidates.append(CleanupCandidate(
            path=path, kind="logs", size_bytes=dir_size(path),
            experiment_id=exp_id, protected=bool(exp_id) and exp_id in promoted,
        ))
    return candidates


def format_report(candidates: list[CleanupCandidate]) -> str:
    if not candidates:
        return "No cleanup candidates found."
    lines = []
    for c in candidates:
        tag = "PROTECTED" if c.protected else "candidate"
        mb = c.size_bytes / (1024 * 1024)
        lines.append(f"[{tag}] {c.kind:11s} {c.path} ({mb:.1f} MB)")
    return "\n".join(lines)


def delete_candidates(candidates: list[CleanupCandidate]) -> list[str]:
    deleted = []
    for c in candidates:
        if c.protected:
            continue
        shutil.rmtree(c.path, ignore_errors=True)
        deleted.append(c.path)
    return deleted
