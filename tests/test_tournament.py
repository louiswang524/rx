import pytest

from rx_state.tournament import CandidateScore, rank_candidates, write_tournament


def test_candidate_score_total_sums_rubric():
    s = CandidateScore(question_id="Q1", novelty=3, feasibility=2,
                        falsifiability=3, evidence_inspectability=1)
    assert s.total == 9


def test_candidate_score_validates_rubric_range():
    with pytest.raises(ValueError):
        CandidateScore(question_id="Q1", novelty=4, feasibility=2,
                        falsifiability=3, evidence_inspectability=1)
    with pytest.raises(ValueError):
        CandidateScore(question_id="Q1", novelty=-1, feasibility=2,
                        falsifiability=3, evidence_inspectability=1)


def test_rank_candidates_descending_by_total():
    low = CandidateScore(question_id="Q1", novelty=1, feasibility=1,
                          falsifiability=1, evidence_inspectability=1)
    high = CandidateScore(question_id="Q2", novelty=3, feasibility=3,
                           falsifiability=3, evidence_inspectability=3)
    mid = CandidateScore(question_id="Q3", novelty=2, feasibility=2,
                          falsifiability=2, evidence_inspectability=2)
    ranked = rank_candidates([low, high, mid])
    assert [s.question_id for s in ranked] == ["Q2", "Q3", "Q1"]


def test_write_tournament_records_winner_and_ranked_scores(tmp_path):
    rx = str(tmp_path)
    low = CandidateScore(question_id="Q1", novelty=1, feasibility=1,
                          falsifiability=1, evidence_inspectability=1,
                          rationale="too incremental")
    high = CandidateScore(question_id="Q2", novelty=3, feasibility=3,
                           falsifiability=3, evidence_inspectability=3,
                           rationale="clear falsifier, strong delta")
    path = write_tournament(rx, [low, high], winner_id="Q2")
    assert path.endswith("tournament.md")
    content = open(path, encoding="utf-8").read()
    assert "winner: Q2" in content
    assert content.index("Q2: total=12") < content.index("Q1: total=4")
    assert "clear falsifier, strong delta" in content
