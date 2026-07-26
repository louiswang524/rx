from rx_state.style import StyleGuide, select_style_sources, write_style_guide, read_style_guide
from rx_state.survey import PaperNote


def test_select_style_sources_caps_at_k():
    notes = [PaperNote(key=str(i), title=str(i)) for i in range(15)]
    assert len(select_style_sources(notes, k=10)) == 10


def test_select_style_sources_fewer_than_k():
    notes = [PaperNote(key=str(i), title=str(i)) for i in range(3)]
    assert len(select_style_sources(notes, k=10)) == 3


def test_style_guide_roundtrip(tmp_path):
    guide = StyleGuide(
        source_keys=["kang2018sasrec", "sun2019bert4rec"],
        structure="Intro, related work, method, experiments, conclusion",
        tone="Confident, hedges claims with ablations",
        wording_conventions="Uses 'we propose' not 'this paper proposes'",
        notes="All sources use algorithm-block pseudocode",
    )
    write_style_guide(str(tmp_path), guide)
    back = read_style_guide(str(tmp_path))
    assert back == guide


def test_read_style_guide_missing_returns_none(tmp_path):
    assert read_style_guide(str(tmp_path)) is None
