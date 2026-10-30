
def check_hash(hash,files):
    for file in files:
        if file["hash"] == hash:
            return True
    return False

def compare_changes(initial,present):
    if initial!=present:
        print("CHANGES !")
        
        
        
    else:
        return False
