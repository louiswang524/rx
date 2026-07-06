from rx_state.schema import Experiment
from rx_state.reproduce import render_reproduce


def test_render_lists_each_experiment_with_commands():
    exps = [
        Experiment(id="EXP1", seeds=[0, 1], baseline="SASRec", commit="abc1234"),
        Experiment(id="EXP2", seeds=[7], baseline=None, commit="def5678"),
    ]
    md = render_reproduce(exps, run_command="python train.py")
    assert "# Reproducibility" in md or "# REPRODUCE" in md
    assert "uv sync" in md
    assert "EXP1" in md and "EXP2" in md
    assert "python train.py --seed 0" in md
    assert "python train.py --seed 1" in md
    assert "python train.py --seed 7" in md
    assert "abc1234" in md and "def5678" in md
