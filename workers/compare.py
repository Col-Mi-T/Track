
def check_hash(hash, files):
    from workers.hashing import hash_file

    for file in files:
        if hash_file(file) == hash:
            return file

    return False


def compare_changes(previous, present):
    if previous != present:
        import difflib

        prev = previous.splitlines()
        pres = present.splitlines()
        diff = difflib.unified_diff(prev, pres)

        return diff

    else:
        return False


def structured_changes(previous, present):
    import difflib

    old = previous.splitlines(keepends=True)
    new = present.splitlines(keepends=True)

    matcher = difflib.SequenceMatcher(None, old, new)

    delta = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue

        delta.append({
            "operation": tag,
            "old_position": i1,
            "new_position": j1,
            "removed": old[i1:i2],
            "added": new[j1:j2]
        })

    return delta if delta else False
