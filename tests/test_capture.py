from rx_state.capture import capture_run, load_experiment


def test_capture_and_load(tmp_path):
    path = capture_run(
        str(tmp_path), "EXP1", seeds=[0, 1], baseline="SASRec",
        config={"lr": 0.001, "batch": 256},
        commit="abc1234", gpu="NVIDIA RTX 4090, 24GB",
        goal="Test whether gating improves recall@10",
        changes="Added gating module vs SASRec baseline",
        result="recall@10 0.42 vs baseline 0.40",
        conclusion="Modest improvement, needs more seeds",
        next_steps="Run with 2 more seeds for a strong claim",
    )
    assert path.endswith("experiments/EXP1/run.md")
    exp = load_experiment(str(tmp_path), "EXP1")
    assert exp.id == "EXP1"
    assert exp.seeds == [0, 1]
    assert exp.baseline == "SASRec"
    assert exp.commit == "abc1234"


def test_capture_records_gpu_and_config(tmp_path):
    capture_run(str(tmp_path), "EXP2", seeds=[7], baseline=None,
                config={"lr": 0.01}, commit="def5678", gpu="CPU-only",
                goal="g", changes="c", result="r", conclusion="cc", next_steps="n")
    text = open(str(tmp_path) + "/experiments/EXP2/run.md").read()
    assert "def5678" in text
    assert "CPU-only" in text
    assert "lr" in text


def test_capture_and_load_repeat_count(tmp_path):
    capture_run(
        str(tmp_path), "EXP4", seeds=[0], baseline="torch.matmul",
        config={"reps": 20}, commit="cafe123", gpu="RTX 4060 Laptop",
        goal="benchmark", changes="autotune sweep", result="see table",
        conclusion="mixed", next_steps="widen sweep",
        repeat_count=20,
    )
    exp = load_experiment(str(tmp_path), "EXP4")
    assert exp.repeat_count == 20


def test_capture_defaults_repeat_count_to_zero(tmp_path):
    capture_run(str(tmp_path), "EXP5", seeds=[0], baseline=None,
                config={}, commit="c", gpu="g",
                goal="g", changes="c", result="r", conclusion="cc", next_steps="n")
    exp = load_experiment(str(tmp_path), "EXP5")
    assert exp.repeat_count == 0


def test_capture_records_narrative_log(tmp_path):
    capture_run(str(tmp_path), "EXP3", seeds=[0], baseline="SASRec",
                config={"lr": 0.01}, commit="abc0000", gpu="CPU-only",
                goal="Test the gating hypothesis",
                changes="Swapped attention for gating",
                result="recall@10 0.35, below baseline",
                conclusion="Gating hurts recall here",
                next_steps="Try gating only on long sequences")
    text = open(str(tmp_path) + "/experiments/EXP3/run.md").read()
    assert "## Goal" in text and "Test the gating hypothesis" in text
    assert "## Changes" in text and "Swapped attention for gating" in text
    assert "## Result" in text and "below baseline" in text
    assert "## Conclusion" in text and "Gating hurts recall here" in text
    assert "## Next" in text and "long sequences" in text
