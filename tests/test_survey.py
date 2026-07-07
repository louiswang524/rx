from rx_state.survey import PaperNote, write_note, read_note, collect_baselines


def test_note_roundtrip(tmp_path):
    n = PaperNote(key="kang2018sasrec", title="SASRec", method="self-attention",
                  baselines=["GRU4Rec", "Caser"], claim="beats RNN baselines")
    back = read_note(write_note(str(tmp_path), n))
    assert back == n


def test_collect_baselines_dedup_sorted():
    notes = [
        PaperNote(key="a", title="A", baselines=["GRU4Rec", "Caser"]),
        PaperNote(key="b", title="B", baselines=["Caser", "BERT4Rec"]),
    ]
    assert collect_baselines(notes) == ["BERT4Rec", "Caser", "GRU4Rec"]
