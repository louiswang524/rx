import glob
import json
import os
import yaml
from rx_state.schema import Claim, Question, Evidence


def default_state(project: str, kb_path: str) -> dict:
    return {
        "project": project,
        "kb_path": kb_path,
        "stage": "ideate",
        "loop": {
            "enabled": False,
            "iteration": 0,
            "max_iterations": 20,
            "no_improve_count": 0,
            "no_improve_limit": 5,
        },
        "artifacts": {"questions": [], "evidence": [], "claims": [], "experiments": []},
    }


def load_state(rx_dir: str) -> dict:
    with open(os.path.join(rx_dir, "state.json"), encoding="utf-8") as f:
        return json.load(f)


def save_state(rx_dir: str, state: dict) -> None:
    os.makedirs(rx_dir, exist_ok=True)
    with open(os.path.join(rx_dir, "state.json"), "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def write_claim(rx_dir: str, claim: Claim) -> str:
    claims_dir = os.path.join(rx_dir, "claims")
    os.makedirs(claims_dir, exist_ok=True)
    front = {
        "id": claim.id,
        "strength": claim.strength,
        "evidence_ids": claim.evidence_ids,
        "question_id": claim.question_id,
    }
    path = os.path.join(claims_dir, f"{claim.id}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(yaml.safe_dump(front, sort_keys=False))
        f.write("---\n\n")
        f.write(claim.text + "\n")
    return path


def read_claim(path: str) -> Claim:
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    _, front_block, body = raw.split("---", 2)
    front = yaml.safe_load(front_block)
    return Claim(
        id=front["id"],
        text=body.strip(),
        strength=front["strength"],
        evidence_ids=front.get("evidence_ids") or [],
        question_id=front.get("question_id"),
    )


def _write_frontmatter(dir_path: str, subdir: str, ident: str, front: dict, body: str) -> str:
    target = os.path.join(dir_path, subdir)
    os.makedirs(target, exist_ok=True)
    path = os.path.join(target, f"{ident}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(yaml.safe_dump(front, sort_keys=False))
        f.write("---\n\n")
        f.write(body + "\n")
    return path


def _read_frontmatter(path: str) -> tuple[dict, str]:
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    _, front_block, body = raw.split("---", 2)
    return yaml.safe_load(front_block), body.strip()


def write_question(rx_dir: str, q: Question) -> str:
    return _write_frontmatter(rx_dir, "questions", q.id, {"id": q.id, "gap": q.gap}, q.text)


def read_question(path: str) -> Question:
    front, body = _read_frontmatter(path)
    return Question(id=front["id"], text=body, gap=front.get("gap") or "")


def write_evidence(rx_dir: str, e: Evidence) -> str:
    front = {"id": e.id, "outcome": e.outcome, "experiment_id": e.experiment_id}
    return _write_frontmatter(rx_dir, "evidence", e.id, front, e.note)


def read_evidence(path: str) -> Evidence:
    front, body = _read_frontmatter(path)
    return Evidence(id=front["id"], outcome=front["outcome"],
                    experiment_id=front.get("experiment_id"), note=body)


def list_artifacts(rx_dir: str, kind: str) -> list[str]:
    return sorted(glob.glob(os.path.join(rx_dir, kind, "*.md")))
