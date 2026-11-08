import colors

def init_history(i,file,track_path): 
    from pathlib import Path
    import json
    from datetime import datetime
    print(file)
    
    with open(track_path/"index.json") as indexfile:
        json_index = indexfile.read()
    
    
    index = json.loads(json_index)
    region = index["files"][i]
    #print(region)
    
    file_history = track_path/f"history/{region['id']}"
    Path.mkdir(file_history, exist_ok =True)
    
    """
    Format:
    Commit timestamp
    
    commit message
    previous datahash
    current datahash
    changes made
    """
    
    with open(file,"r+") as open_file:
        content = open_file.read() # read file
        with open(f"{file_history/region["hash"]}.tx", "w+") as origin:
            origin.write(content) #copy file to origin
            
    with open(file_history/"PREVIOUS", "w+") as prev:
        prev.write(content) #copy file to previous
   
    with open(file_history/"ORIGIN","w+") as genesis:
        genesis.write(region["hash"]) # write origin hash to file
    
    with open(f"{file_history/region["id"]}.tr","w+") as history: # write init log
        original = region["hash"]
        log = f"LOG ID = 1"
        message = "\n\tMessage = Register File"
        time = f"\n\tTime = {datetime.now()}"
        c_hash = f"\n\tCurrent Hash = {original}"
        p_hash = "\n\tPrevious Hash = NONE"
        changes = "\n\tChanges = NONE"
        init_log = f"{log}{message}{time}{c_hash}{p_hash}{changes}\n\nORIGIN = {original}"
        history.write(init_log)
        
    with open(file_history/"LASTLOGID", "w+") as log_id:
        log_id.write("0")
    
    
    #print(original, "ORIGIN")
    
def create_delta_home(i,track_path):
    from pathlib import Path
    import json
    #print(file)
    with open(track_path/"index.json") as indexfile:
        json_index = indexfile.read()
        
        index = json.loads(json_index)
        region = index["files"][i]
    
    file_id = region["id"]
    Path.mkdir(Path.cwd()/f".track/history/{file_id}/deltas", exist_ok =True)
    

def file_history(second_arg,third_arg):
    from pathlib import Path
    import json
    import sys
    if second_arg == None or third_arg == None:
        print(f"{colors.BLUE}Please provide the file path.{colors.RESET}")
        sys.exit(1)
    if second_arg not in ("-f", "--file"):
        print(f"{colors.RED}Invalid option. Use -f or --file to specify a file.{colors.RESET}")
        sys.exit(1)
    if third_arg:
        file = Path(third_arg)
        if not Path.exists(file):
            print(f"{colors.RED}File not found. Please provide a valid relative file path.{colors.RESET}")
            sys.exit(1)
        else:
            track_path = Path.cwd() / ".track"
            file = Path.cwd() / third_arg
            with open(track_path/"index.json") as indexfile:
                json_index = indexfile.read()
                
                index = json.loads(json_index)
                files = index["files"]
                #print(files)
            if not str(file) in [f["path"] for f in files]:
                print(f"{colors.BLUE}File not tracked, check the file path, use a relative path if the file is in the current working directory or a subdirectory or log the file to add to track index.{colors.RESET}")
                sys.exit(1)
            else:
                for f in files:
                    if f["path"] == str(file):
                        history_file = track_path/f"history/{f['id']}/{f['id']}.tr"
                        with open(history_file, "r") as history:
                            history_content = history.read()
                            print(history_content)





