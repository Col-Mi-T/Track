from pathlib import Path
import json
from datetime import datetime
from workers.hashing import gen_id

def register_project(track_version):
    from pathlib import Path
    import sys
    current = Path.cwd()
    track_path = current / ".track"   
    #if Path.exists(track_path):
     #  print(f"\nThis path '{current}' is already registered and has a '.track' directory.\n")
      # sys.exit()
     
    print(f"Registering '{current}' for tracking.\n")
    
    
    print("\nCreating '.track' directory in the current path...\n")
    Path.mkdir(track_path, exist_ok=True)
    create_trackconfig(track_path,track_version)
    
    items = list(current.iterdir())
    total = len(items)
    print("Obtaining files and directories in the current path...\n")
    
    files = []
    if Path.exists(current/"not.track"):
        with open(current/"not.track", "r") as ignore_file:
            ignore = ignore_file.read().splitlines()
    else:
        ignore = []
    #print(ignore)
    
    for i,item in enumerate(items,start=1):
        percent = int(i/total*100) if total else 100
        
        print(f"\r[{percent}%]", end=" ", flush=True)

        if item.name in [".git", ".track", "not.track"] or item.name in ignore:
            #print(f"Skipping '{item}'...", end=" ", flush=True)
            continue
        else:
            if item.is_file():
                files.append(str(item))
            else:
                scan_directory(item, files, ignore)
    
    print("Done!\n")
    print(f"Obtained {len(files)} files in the current path:\n")
    for file in files:
        print(f"\t{file}") 
                
    create_trackindex(track_path,files)
    
    print("\nCreating File Content Storage...\n")
    history = track_path/"history"
    Path.mkdir(history, exist_ok=True)
    from workers.history import init_history
    for i,file in enumerate(files):
        init_history(i,file,track_path)
        

def scan_directory(directory, files, ignore):
    for item in directory.iterdir():
        if item.name in [".git", ".track", "not.track"] or item.name in ignore:
            #print(f"Skipping {item}...", end=" ", flush=True)
            continue
        else:
            #print("ITEM:",item)
            if item.is_file():
                files.append(str(item))

            elif item.is_dir():
                scan_directory(item, files, ignore)                   

def create_trackconfig(track_path,track_version):
    project = track_path.parent.name
    length = int(len(str(track_path))/4)
    id = gen_id()
    
    print("Generating Configuration Data...")
    now = datetime.now()
    
    config_data = {
        "version" : track_version,
        "project_name":project,
        "project_id": id,
        "created": str(now),
        "ignorefile" : "not.track",
    }
    print("Writing Configuration Data to file...")
    with open(track_path/"config.json", "w") as index:
        index.write(json.dumps(config_data, indent =4))
    
def create_trackindex(track_path,files):
    print("\nGenerating Tracking Index...")
    now = datetime.now()
    index_data = {
        "files": []
    }
    
    for file in files:
        #print(f"Generating Hash for file: {file} ...")
        from workers.hashing import hash_file
        hashdata=hash_file(file)
        path = file
        id = gen_id(path)
        d = {
            "path":file,
            "id":id,
            "created":str(now),
            "last_updated":str(now),
            "file_size":str(Path(file).stat().st_size)+" bytes",
            "hash":hashdata,
        }
        index_data["files"].append(d)
    
    print("Writing Tracking Index to files...")
    with open(track_path/"index.json", "w") as index:
        index.write(json.dumps(index_data, indent =4))   