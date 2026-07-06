from rx_state.capture import capture_run, load_experiment


def test_capture_and_load(tmp_path):
    path = capture_run(
        str(tmp_path), "EXP1", seeds=[0, 1], baseline="SASRec",
        config={"lr": 0.001, "batch": 256},
        commit="abc1234", gpu="NVIDIA RTX 4090, 24GB",
    )
    assert path.endswith("experiments/EXP1/run.md")
    exp = load_experiment(str(tmp_path), "EXP1")
    assert exp.id == "EXP1"
    assert exp.seeds == [0, 1]
    assert exp.baseline == "SASRec"
    assert exp.commit == "abc1234"


def test_capture_records_gpu_and_config(tmp_path):
    capture_run(str(tmp_path), "EXP2", seeds=[7], baseline=None,
                config={"lr": 0.01}, commit="def5678", gpu="CPU-only")
    text = open(str(tmp_path) + "/experiments/EXP2/run.md").read()
    assert "def5678" in text
    assert "CPU-only" in text
    assert "lr" in text
