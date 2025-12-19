from diff_engine.hasher import hash_text

def test_hash_text_same_input():
    text = "hello world"
    assert hash_text(text) == hash_text(text)

def test_hash_text_different_input():
    assert hash_text("hello") != hash_text("world")