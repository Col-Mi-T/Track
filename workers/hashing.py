import hashlib

def hash_file(file):
    with open(file,"r+") as file:
        content = file.read()
    hash_obj = hashlib.sha256(content.encode())
    #print(hash_obj)
    hashdata = hash_obj.hexdigest()
    #print(hash_obj.hexdigest())
    #print(hash_obj.digest_size)
    return hashdata