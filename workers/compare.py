
def check_hash(hash,files):
    for file in files:
        if file["hash"] == hash:
            return True
    return False

def compare_changes(previous,present):
    if previous!=present:
        
        import difflib
        
        prev = previous.splitlines()
        pres = present.splitlines()
        diff = difflib.unified_diff(prev, pres)
        return diff
    
    else:
        return False
