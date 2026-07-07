import json
import os
import yaml
from rx_state.schema import Experiment


def capture_run(rx_dir, exp_id, seeds, baseline, config, *, commit, gpu) -> str:
    exp_dir = os.path.join(rx_dir, "experiments", exp_id)
    os.makedirs(exp_dir, exist_ok=True)
    front = {"id": exp_id, "seeds": list(seeds), "baseline": baseline,
             "commit": commit, "gpu": gpu}
    path = os.path.join(exp_dir, "run.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(yaml.safe_dump(front, sort_keys=False))
        f.write("---\n\n")
        f.write("## Config\n\n```json\n")
        f.write(json.dumps(config, indent=2))
        f.write("\n```\n")
    return path


def load_experiment(rx_dir, exp_id) -> Experiment:
    path = os.path.join(rx_dir, "experiments", exp_id, "run.md")
    with open(path, encoding="utf-8") as f:
        _, front_block, _ = f.read().split("---", 2)
    front = yaml.safe_load(front_block)
    return Experiment(id=front["id"], seeds=front.get("seeds") or [],
                      baseline=front.get("baseline"), commit=front.get("commit"))
