from rx_state.aitells import scan_ai_tells, sentence_lengths, low_burstiness


def test_scan_finds_hard_banned_cliche():
    findings = scan_ai_tells("This paper will delve into the problem of scaling.")
    assert any("delve into" in f for f in findings)


def test_scan_clean_text_has_no_findings():
    assert scan_ai_tells("We evaluate the method on three datasets.") == []


def test_scan_transition_word_below_threshold_not_flagged():
    text = "Furthermore, we test this. Furthermore, it holds. Furthermore, results agree."
    assert scan_ai_tells(text, transition_threshold=3) == []


def test_scan_transition_word_over_threshold_flagged():
    text = "Furthermore, A. Furthermore, B. Furthermore, C. Furthermore, D."
    findings = scan_ai_tells(text, transition_threshold=3)
    assert any("furthermore" in f and "4x" in f for f in findings)


def test_scan_is_case_insensitive():
    findings = scan_ai_tells("We DELVE INTO the results.")
    assert any("delve into" in f for f in findings)


def test_sentence_lengths_counts_words_per_sentence():
    text = "Short one. This sentence has five words. Ok."
    assert sentence_lengths(text) == [2, 5, 1]


def test_low_burstiness_true_when_sentences_uniform():
    text = ". ".join(["one two three four five"] * 6) + "."
    assert low_burstiness(text) is True


def test_low_burstiness_false_when_sentences_vary():
    text = "Short. This one is quite a bit longer than the short one before it. Mid length here now."
    assert low_burstiness(text) is False


def test_low_burstiness_false_when_too_few_sentences():
    assert low_burstiness("Only one sentence here.") is False
