from pathlib import Path
import json

def log_project():
    # equivalent to git commit -m "message"#
    from datetime import datetime
    from pathlib import Path
    from workers.hashing import hash_file
    message = input("Log Message: ")
    
    old = []
    index_path = Path.cwd()/".track/index.json"
    index = get_index(index_path)
    for file in index["files"]:
        f = file["path"]
        old.append(str(f))
        
    new = scan_dir()
    for file in new:
        if file not in old:
            print(f"{file}===NEW")
            append_index(file,index)
            update_index(index,index_path)
            
            from workers.history import init_history
            track_path = Path.cwd()/".track"
            i = len(new)-1
            init_history(i,file,track_path)
            
    for file in index["files"]:
        f = Path(file["path"])
        if not Path.exists(f):
            import shutil
            file_id = file["id"]
            #print(index)
            
            from workers.compare import check_hash
            # Evaluation (Not personal)
            if check_hash(file["hash"],index["files"]):
                print("RENAME: ",file)
                index["files"].remove(file)
            else:
                file_history_path = Path.cwd()/f".track/history/{file_id}"
                shutil.rmtree(file_history_path)
                index["files"].remove(file)
                update_index(index, index_path)   
                print(f"\n\nDELETED {f}\n\n")
            
        else:
            #print(file["path"])
            file["last_updated"]=str(datetime.now())
            file["file_size"] = str(Path(f).stat().st_size)+" bytes"
            #print(file["file_size"])
            file["hash"] = hash_file(file["path"])
    #print(index)
    
    for file in index["files"]:
        for i in index["files"]:
            if file["path"] == i :
                index["files"].remove(file)
            # remove previous duplicates
                
    update_index(index,index_path)
    
    for file in index["files"]:
        log_history(file,message)  
        
        
        
def get_index(index_path):
    with open(index_path, "r+") as index:
        #print(index.read())
        index_content = json.loads(index.read())
    return index_content

def scan_dir():
    from workers.register import scan_directory
    current = Path.cwd()
    items = list(current.iterdir())
    files = []
    config_path = Path.cwd()/".track/config.json"
    with open(config_path, "r+") as config:
        file = json.loads(config.read())
    ignore_file = file["ignorefile"]
    if Path.exists(Path.cwd()/ignore_file):
        with open(Path.cwd()/ignore_file, "r+")as ignorefile:
            ignore = ignorefile.read().splitlines()
    else:
        ignore = []
    for item in items:
        if item.name in [".git", ".track", "not.track"] or item.name in ignore:
            #print(f"Skipping '{item}'...", end=" ", flush=True)
            continue
        else:
            if item.is_file():
                files.append(str(item))
            else:
                scan_directory(item, files, ignore)
    return files
    
def append_index(i, index):
    files = index["files"]
    from workers.register import gen_id
    from datetime import datetime
    from workers.hashing import hash_file
    hashdata=hash_file(i)
    id = gen_id(i)
    now = datetime.now()
    info = {
        "path":i,
        "id":id,
        "created":str(now),
        
        "last_updated":str(now),
        "file_size":str(Path(i).stat().st_size)+" bytes",
        "hash":hashdata,
    }
 
    files.append(info)
    #print(files)

def update_index(index,index_path):
    with open(index_path, "w+") as index_file:
        index_file.write(json.dumps(index,indent =4))
        
def log_history(file,message):
    from datetime import datetime
    from workers.compare import compare_changes
    with open(Path.cwd()/f".track/history/{file["id"]}/ORIGIN","r+") as origin:
        original = origin.read()
    with open(Path.cwd()/f".track/history/{file["id"]}/{original}","r+") as ancestor:
        initial = ancestor.read()
    with open(Path.cwd()/f".track/history/{file["id"]}/PREVIOUS","r+") as prev:
        previous = prev.read()
    with open(file["path"],"r+") as current:
        present = current.read()
    
    changes = compare_changes(previous,present)
    
    if changes == False:
        pass
    else:
        print(changes)
    
    with open(Path.cwd()/f".track/history/{file["id"]}/PREVIOUS","w") as prev:
        prev.write(present)
    