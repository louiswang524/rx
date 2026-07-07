from rx_state.planlock import PlanLock, write_lock, read_lock, is_locked


def test_lock_roundtrip_and_flag(tmp_path):
    rx = str(tmp_path)
    assert is_locked(rx) is False
    lock = PlanLock(metric="recall@20", higher_is_better=True,
                    comparison_family=["ours", "SASRec"], seed_policy=3,
                    baselines=["SASRec", "BERT4Rec"])
    write_lock(rx, lock)
    assert is_locked(rx) is True
    assert read_lock(rx) == lock
