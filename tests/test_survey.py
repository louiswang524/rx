from rx_state.survey import PaperNote, write_note, read_note, collect_baselines


def test_note_roundtrip(tmp_path):
    n = PaperNote(key="kang2018sasrec", title="SASRec", method="self-attention",
                  baselines=["GRU4Rec", "Caser"], claim="beats RNN baselines")
    back = read_note(write_note(str(tmp_path), n))
    assert back == n


def test_note_defaults_to_hop_one_no_via():
    n = PaperNote(key="a", title="A")
    assert n.hop == 1
    assert n.via == []


def test_hop_two_note_roundtrip_with_via(tmp_path):
    n = PaperNote(key="citer2024", title="Citer", hop=2, via=["kang2018sasrec"])
    back = read_note(write_note(str(tmp_path), n))
    assert back == n


def test_legacy_note_without_hop_fields_defaults(tmp_path):
    path = tmp_path / "legacy.md"
    path.write_text(
        "---\nkey: legacy\ntitle: Legacy\nmethod: x\nbaselines: []\n---\n\nclaim text\n",
        encoding="utf-8",
    )
    n = read_note(str(path))
    assert n.hop == 1
    assert n.via == []


def test_collect_baselines_dedup_sorted():
    notes = [
        PaperNote(key="a", title="A", baselines=["GRU4Rec", "Caser"]),
        PaperNote(key="b", title="B", baselines=["Caser", "BERT4Rec"]),
    ]
    assert collect_baselines(notes) == ["BERT4Rec", "Caser", "GRU4Rec"]
