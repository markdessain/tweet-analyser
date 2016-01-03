from processes.adjectives import run


def test_run_with_empty_string():
    assert len(list(run(''))) == 0


def test_run_with_no_adjectives():
    assert len(list(run('the event'))) == 0


def test_run_with_two_adjectives():
    assert len(list(run('the great fantastic event'))) == 2


def test_run_with_punctuation():
    assert len(list(run('the great, fantastic event.'))) == 2


def test_run_with_hash_tag():
    assert len(list(run('the #great #fantastic event.'))) == 2

