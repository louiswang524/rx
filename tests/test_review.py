import pytest
from rx_state.review import ReviewFinding, recommend, repro_checklist, write_round, read_round, latest_round


def test_finding_validates_severity():
    ReviewFinding(reviewer="R1", severity="major", comment="weak baseline")
    with pytest.raises(ValueError):
        ReviewFinding(reviewer="R1", severity="nit", comment="x")


def test_recommend_precedence():
    major = [ReviewFinding("R1", "major", "no ablation"),
             ReviewFinding("R2", "minor", "typo")]
    assert recommend(major) == "reject"
    minor = [ReviewFinding("R2", "minor", "typo"),
             ReviewFinding("R3", "praise", "clear")]
    assert recommend(minor) == "minor revision"
    assert recommend([ReviewFinding("R3", "praise", "great")]) == "accept"


def test_repro_checklist_reports_missing():
    assert repro_checklist(True, True, True) == []
    missing = repro_checklist(has_code=False, has_seeds=True, has_configs=False)
    assert "code" in missing and "configs" in missing and "seeds" not in missing


def test_round_roundtrip(tmp_path):
    rx = str(tmp_path)
    findings = [ReviewFinding("R1", "major", "no ablation"),
                ReviewFinding("R2", "minor", "typo: teh")]
    path = write_round(rx, 1, findings)
    back = read_round(path)
    assert [f.severity for f in back] == ["major", "minor"]
    assert back[0].reviewer == "R1"
    assert back[1].comment == "typo: teh"   # comment with a colon survives


def test_latest_round_returns_highest_and_zero_when_none(tmp_path):
    rx = str(tmp_path)
    assert latest_round(rx) == 0
    write_round(rx, 1, [ReviewFinding("R1", "minor", "x")])
    write_round(rx, 2, [ReviewFinding("R1", "major", "y")])
    assert latest_round(rx) == 2
