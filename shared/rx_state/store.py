import json
import os
import yaml
from rx_state.schema import Claim


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
