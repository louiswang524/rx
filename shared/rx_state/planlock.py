import os
from dataclasses import dataclass, field
import yaml


@dataclass
class PlanLock:
    metric: str
    higher_is_better: bool
    comparison_family: list[str] = field(default_factory=list)
    seed_policy: int = 1
    baselines: list[str] = field(default_factory=list)


def _lock_path(rx_dir: str) -> str:
    return os.path.join(rx_dir, "plan", "lock.md")


def write_lock(rx_dir: str, lock: PlanLock) -> str:
    os.makedirs(os.path.join(rx_dir, "plan"), exist_ok=True)
    front = {"metric": lock.metric, "higher_is_better": lock.higher_is_better,
             "comparison_family": lock.comparison_family,
             "seed_policy": lock.seed_policy, "baselines": lock.baselines}
    path = _lock_path(rx_dir)
    with open(path, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(yaml.safe_dump(front, sort_keys=False))
        f.write("---\n\nBlocker-first lock. Do not start experiments until this exists.\n")
    return path


def read_lock(rx_dir: str) -> PlanLock:
    with open(_lock_path(rx_dir), encoding="utf-8") as f:
        _, front_block, _ = f.read().split("---", 2)
    front = yaml.safe_load(front_block)
    return PlanLock(metric=front["metric"], higher_is_better=front["higher_is_better"],
                    comparison_family=front.get("comparison_family") or [],
                    seed_policy=front.get("seed_policy") or 1,
                    baselines=front.get("baselines") or [])


def is_locked(rx_dir: str) -> bool:
    return os.path.exists(_lock_path(rx_dir))
