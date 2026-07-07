from rx_state.anonymize import anonymize_text, lint_anonymity

AUTHORS = ["Louis Wang", "J. Smith"]
URLS = ["github.com/louis/rx"]


def test_anonymize_removes_names_urls_and_selfref():
    src = "Louis Wang extends our prior work at github.com/louis/rx."
    out = anonymize_text(src, AUTHORS, URLS)
    assert "Louis Wang" not in out
    assert "github.com/louis/rx" not in out
    assert "our prior work" not in out.lower()
    assert "Anonymous" in out
    assert "[ANONYMIZED-URL]" in out


def test_lint_flags_leaks():
    dirty = "Thanks to funding from X. See github.com/louis/rx. By J. Smith."
    findings = lint_anonymity(dirty, AUTHORS, URLS)
    assert any("J. Smith" in f for f in findings)
    assert any("github.com/louis/rx" in f for f in findings)
    assert any("funding" in f.lower() or "acknowledg" in f.lower() for f in findings)


def test_lint_clean_returns_empty():
    clean = "Anonymous proposes a gating mechanism. See [ANONYMIZED-URL]."
    assert lint_anonymity(clean, AUTHORS, URLS) == []


def test_case_insensitive_name_matching():
    authors = ["Louis Wang"]
    urls = ["github.com/louis/rx"]
    # uppercase variant in the source must still be caught + anonymized
    src = "LOUIS WANG and louis wang; see GITHUB.COM/louis/rx"
    out = anonymize_text(src, authors, urls)
    assert "LOUIS WANG" not in out and "louis wang" not in out
    assert lint_anonymity(out, authors, urls) == []
    # the linter must flag a casing variant in dirty text
    assert lint_anonymity("By LOUIS WANG", authors, urls) != []
