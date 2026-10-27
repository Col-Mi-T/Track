
def track_path(track_version):
    from pathlib import Path
    import sys
    
    current = Path.cwd()
    
    #if Path.exists(current/".track"):
     #   print("Already registered...")
     #   sys.exit()
     
    print(f"Registered '{current}' for tracking.\n")
    items = list(current.iterdir())
    total = len(items)
    print("Obtaining files and directories in the current path...\n")
    
    files = []
    if Path.exists(current/"not.track"):
        with open(current/"not.track", "r") as ignore_file:
            ignore = ignore_file.read().splitlines()
    #print(ignore)
    
    for i,item in enumerate(items,start=1):
        import time
        time.sleep(2)
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
                
    create_trackdata(current,track_version,files)

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
    print("Done!\n")
    print(f"Registered {len(files)} files in the current path:\n")
    #for file in files:
     #   print(file)                    

def create_trackdata(current,track_version,files):
    print("\nCreating '.track' directory in the current path...\n")
    from pathlib import Path
    Path.mkdir(current / ".track", exist_ok=True)
    project = current.name
    
    file_length = len(files)
    id = gen_id(project,file_length)
    
    trackdata_path = current / ".track"
    #print(trackdata_path)
    
    print("Generating Metadata...")
    import json
    from datetime import datetime
    now = datetime.now()
    
    config_data = {
        "version" : track_version,
        "project_name":project,
        "project_id": id,
        "created": str(now),
        "ignore" : "not.track",
    }
    
    index_data = {
        "files": []
    }
    index = 0
    for file in files:
        d = {
            "path":file,
            "index":index,
            "created":str(now),
            "last_updated":str(now),
            "file-size":str(Path(file).stat().st_size)+" bytes",
        }
        index+=1
        index_data["files"].append(d)
    
    print("Writing Metadata to files...")
    with open(trackdata_path/"config.json", "w") as config:
        config.write(json.dumps(config_data, indent=4))
    with open(trackdata_path/"index.json", "w") as index:
        index.write(json.dumps(index_data, indent =4))
    print("Done!\n")
    

def gen_id(project,length):
    id = ""
    for ch in project:
        id+=str(ord(ch)*length)
    #print(id)
    if len(id) > 20:
        id = id[:19] 
        #print(id)
    elif len(id) < 20:
        x = 20-len(id)
        import random
       # print(len(id))
        id+=str(random.randint(int("1"*x), int("9"*x)))
        #print(len(id))
    return id