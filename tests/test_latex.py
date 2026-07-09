from rx_state.latex import PREAMBLE, render_bib
from rx_state.survey import PaperNote


def test_preamble_has_documentclass():
    assert "\\documentclass" in PREAMBLE


def test_render_bib_one_entry_per_note_with_empty_unknowns():
    notes = [PaperNote(key="muon2024", title="Muon Optimizer"),
             PaperNote(key="grok2022", title="Grokking")]
    bib = render_bib(notes)
    assert bib.count("@misc") == 2
    assert "muon2024" in bib and "grok2022" in bib
    assert "title = {Muon Optimizer}" in bib
    assert "author = {}" in bib   # unknown field left empty for the human
    assert "year = {}" in bib


def test_render_bib_empty_list_is_valid_empty():
    assert render_bib([]) == ""
