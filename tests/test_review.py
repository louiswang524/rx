import pytest
from rx_state.review import ReviewFinding, recommend, repro_checklist


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
