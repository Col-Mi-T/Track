import hashlib
from datetime import datetime

def gen_id(path=None):
    if path:
        hash_object = hashlib.sha256(path.encode())
        id = "FILE-"+ hash_object.hexdigest()[:10].upper()
        return id
    else:
        id = "TRK-"
        import random
        random_number = random.randint(1, 1000000)
        hash_object = hashlib.sha256(str(random_number).encode())
        year = datetime.now().year
        id += str(year) + "-" + hash_object.hexdigest()[:8].upper()
        return id

def hash_file(file):
    with open(file,"r+") as file:
        content = file.read()
    hash_obj = hashlib.sha256(content.encode())
    #print(hash_obj)
    hashdata = hash_obj.hexdigest()
    #print(hash_obj.hexdigest())
    #print(hash_obj.digest_size)
    return hashdata