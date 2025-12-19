from diff_engine.text_diff import generate_text_diff

def compare_runs(old_hashes, new_hashes, old_texts, new_texts):
    added = []
    removed = []
    changed = {}

    old_urls = set(old_hashes.keys())
    new_urls = set(new_hashes.keys())

    added = list(new_urls - old_urls)
    removed = list(old_urls - new_urls)

    for url in old_urls & new_urls:
        if old_hashes[url] != new_hashes[url]:
            changed[url] = generate_text_diff(
                old_texts.get(url, ""),
                new_texts.get(url, "")
            )

    return added, removed, changed
