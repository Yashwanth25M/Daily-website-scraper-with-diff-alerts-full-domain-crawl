import hashlib

def diff(old, new):
    added = new.keys() - old.keys()
    removed = old.keys() - new.keys()
    changed = {
        k for k in old.keys() & new.keys()
        if old[k] != new[k]
    }
    return added, removed, changed
