
def check_hash(hash,files):
    for file in files:
        if file["hash"] == hash:
            return True
    return False