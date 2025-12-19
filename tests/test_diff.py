from diff_engine.differ import diff

def test_diff():
    old = {"a": "1", "b": "2"}
    new = {"b": "3", "c": "4"}

    added, removed, changed = diff(old, new)

    assert "c" in added
    assert "a" in removed
    assert "b" in changed
