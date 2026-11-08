from pathlib import Path
import json
from datetime import datetime
import colors
import sys
sys.dont_write_bytecode = True
from workers.hashing import gen_id

def register_project(track_version):
    from pathlib import Path
    import sys
    import os
    current = Path.cwd()
    print("\nCurrent directory:", Path.cwd())
    #print("Can write here:", os.access(Path.cwd(), os.W_OK))
    if not os.access(current, os.W_OK):
        print(f"{colors.RED}Error: No write permission in '{current}'{colors.RESET}")
        sys.exit(1)
    track_path = current / ".track"   
    if Path.exists(track_path):
       print(f"\n{colors.BLUE}This path '{current}' is already registered and has a '.track' directory.\n")
       print(f"Use 'track log' to write a log.{colors.RESET}")
       sys.exit(0)
     
    print(f"\nRegistering '{current}' for tracking.\n")
    
    
    print(f"Creating '.track' directory in the current path...\n")
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
        
        print(f"{colors.GREEN}\r[{percent}%]{colors.RESET}", end=" ", flush=True)

        if item.name in [".git", ".track", "not.track", "__pycache__"] or item.name in ignore or item.resolve() == Path(sys.executable).resolve():
            #print(f"Skipping '{item}'...", end=" ", flush=True)
            continue
        else:
            if item.is_file():
                files.append(str(item))
            else:
                relative_path = item.relative_to(current).as_posix()
                relative_path = item.relative_to(current).as_posix()

                if any(
                    relative_path == path.rstrip("/")
                    or relative_path.startswith(path.rstrip("/") + "/")
                    for path in ignore
                ):
                    continue
                
                scan_directory(item, files, ignore,relative_path)
    
    print(f"{colors.GREEN}Done!{colors.RESET}\n")
    print(f"Obtained {len(files)} files in the current path:\n")
    for file in files:
        print(f"\t{file}") 
                
    create_trackindex(track_path,files)
    
    print(f"\nCreating File Content Storage...\n")
    history = track_path/"history"
    Path.mkdir(history, exist_ok=True)
    from workers.history import init_history, create_delta_home
    for i,file in enumerate(files):
        init_history(i,file,track_path)
        create_delta_home(i,track_path)
    print(f"{colors.GREEN}Done!{colors.RESET}")
        

def scan_directory(directory, files, ignore,relative_path):
    import sys
    
    for item in directory.iterdir():
        if (item.name in [".git", ".track", "not.track"] 
            or item.name in ignore
            or relative_path in ignore
            or item.resolve() == Path(sys.executable).resolve()):
            #print(f"Skipping {item}...", end=" ", flush=True)
            continue
        else:
            #print("ITEM:",item)
            if item.is_file():
                files.append(str(item))

            elif item.is_dir():
                scan_directory(item, files, ignore,relative_path)                   

def create_trackconfig(track_path,track_version):
    project = track_path.parent.name
    length = int(len(str(track_path))/4)
    id = gen_id()
    
    print(f"Generating Configuration Data...")
    now = datetime.now()
    
    config_data = {
        "version" : track_version,
        "project_name":project,
        "project_id": id,
        "created": str(now),
        "ignorefile" : "not.track",
    }
    print(f"Writing Configuration Data to file...")
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
    
    print(f"Writing Tracking Index to files...")
    with open(track_path/"index.json", "w") as index:
        index.write(json.dumps(index_data, indent =4))   