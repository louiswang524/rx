from rx_state.schema import Claim, Evidence, Experiment, STRENGTHS


def _linked(claim: Claim, evidence: list[Evidence]) -> list[Evidence]:
    return [e for e in evidence if e.id in claim.evidence_ids]


def _experiments_for(evs: list[Evidence], experiments: list[Experiment]) -> list[Experiment]:
    ids = {e.experiment_id for e in evs if e.experiment_id}
    return [x for x in experiments if x.id in ids]


def evaluate_gate(
    claim: Claim, evidence: list[Evidence], experiments: list[Experiment]
) -> tuple[str, list[str]]:
    evs = _linked(claim, evidence)
    exps = _experiments_for(evs, experiments)
    reasons: list[str] = []

    has_positive = any(e.outcome == "positive" for e in evs)
    if not has_positive:
        reasons.append("no linked evidence with positive outcome")
        return "speculative", reasons

    if not exps:
        reasons.append("supported requires a linked positive experiment")
        return "speculative", reasons

    all_seeds = {s for x in exps for s in x.seeds}
    has_baseline = any(x.baseline for x in exps)
    has_commit = any(x.commit for x in exps)

    if len(all_seeds) < 2:
        reasons.append("strong requires >=2 distinct seeds")
    if not has_baseline:
        reasons.append("strong requires a baseline comparison")
    if not has_commit:
        reasons.append("strong requires a linked commit")

    if not reasons:
        return "strong", reasons
    return "supported", reasons


def can_promote(
    claim: Claim, evidence: list[Evidence], experiments: list[Experiment]
) -> bool:
    met, _ = evaluate_gate(claim, evidence, experiments)
    return STRENGTHS.index(met) >= STRENGTHS.index(claim.strength)
