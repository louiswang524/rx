import os

from rx_state.scoop import (
    ScoopCheck,
    scoop_recheck_due,
    write_scoop_check,
    read_scoop_check,
    list_scoop_checks,
    known_paper_keys,
)
from rx_state.survey import PaperNote, write_note


def test_scoop_recheck_due_every_third_iteration():
    assert [i for i in range(1, 10) if scoop_recheck_due(i)] == [3, 6, 9]


def test_scoop_recheck_not_due_at_iteration_zero():
    assert scoop_recheck_due(0) is False


def test_scoop_recheck_due_custom_cadence():
    assert scoop_recheck_due(2, every=2) is True
    assert scoop_recheck_due(3, every=2) is False


def test_scoop_check_roundtrip_clear(tmp_path):
    rx = str(tmp_path)
    check = ScoopCheck(iteration=3, checked_at="2026-08-16T00:00:00+00:00")
    path = write_scoop_check(rx, check)
    assert path.endswith("iter-3.md")
    back = read_scoop_check(path)
    assert back == check


def test_scoop_check_roundtrip_with_findings(tmp_path):
    rx = str(tmp_path)
    check = ScoopCheck(
        iteration=6,
        checked_at="2026-08-16T06:00:00+00:00",
        verdict="potential_collision",
        findings=["Doe et al. 2026 (arxiv:2608.99999) reports the same metric lift on the same task"],
    )
    write_scoop_check(rx, check)
    back = read_scoop_check(os.path.join(rx, "scoop-checks", "iter-6.md"))
    assert back == check


def test_list_scoop_checks_sorted_by_iteration(tmp_path):
    rx = str(tmp_path)
    write_scoop_check(rx, ScoopCheck(iteration=6, checked_at="t2"))
    write_scoop_check(rx, ScoopCheck(iteration=3, checked_at="t1"))
    checks = list_scoop_checks(rx)
    assert [c.iteration for c in checks] == [3, 6]


def test_list_scoop_checks_empty_when_none(tmp_path):
    assert list_scoop_checks(str(tmp_path)) == []


def test_known_paper_keys_collects_hop1_and_hop2(tmp_path):
    rx = str(tmp_path)
    write_note(rx, PaperNote(key="kang2018sasrec", title="SASRec", hop=1))
    write_note(rx, PaperNote(key="citer2024", title="Citer", hop=2, via=["kang2018sasrec"]))
    assert known_paper_keys(rx) == {"kang2018sasrec", "citer2024"}


def test_known_paper_keys_empty_when_no_notes(tmp_path):
    assert known_paper_keys(str(tmp_path)) == set()
