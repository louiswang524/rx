from rx_state.schema import Experiment


def render_reproduce(experiments: list[Experiment], run_command: str) -> str:
    lines = ["# Reproducibility", "", "Install: `uv sync`", ""]
    for exp in experiments:
        lines.append(f"## {exp.id}")
        lines.append("")
        lines.append(f"- baseline: {exp.baseline or 'n/a'}")
        lines.append(f"- commit: `{exp.commit or 'n/a'}`")
        lines.append(f"- seeds: {exp.seeds}")
        lines.append("")
        lines.append("```bash")
        for s in exp.seeds:
            lines.append(f"{run_command} --seed {s}")
        lines.append("```")
        lines.append("")
    return "\n".join(lines)
