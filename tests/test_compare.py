from diff_engine.compare import compare_runs

def test_detect_changed_page():
    old_hashes = {"a.html": "hash1"}
    new_hashes = {"a.html": "hash2"}

    old_texts = {"a.html": "old content"}
    new_texts = {"a.html": "new content"}

    added, removed, changed = compare_runs(
        old_hashes, new_hashes, old_texts, new_texts
    )

    assert "a.html" in changed
    assert added == []
    assert removed == []
