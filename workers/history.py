
def init_history(i,file,track_path): 
    from pathlib import Path
    import json
    from datetime import datetime
    
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
    added lines
    removed lines
    chnaged lines
    """
    
    with open(file,"r+") as open_file:
        content = open_file.read() # read file
        with open(file_history/region["hash"], "w+") as origin:
            origin.write(content) #copy file to origin
            
    with open(file_history/"PREVIOUS", "w+") as prev:
        prev.write(content) #copy file to previous
   
    with open(file_history/"ORIGIN","w+") as genesis:
        genesis.write(region["hash"]) # write origin hash to file
    
    with open(file_history/region["id"],"w+") as history: # write init log
        original = region["hash"]
        log = f"LOG ID = 1"
        message = "\n\tMessage = Register File"
        time = f"\n\tTime = {datetime.now()}"
        c_hash = f"\n\tCurrent Hash = {original}"
        p_hash = "\n\tPrevious Hash = NONE"
        changes = "\n\tChanges = NONE"
        init_log = f"{log}{message}{time}{c_hash}{p_hash}{changes}\n\nORIGIN = {original}"
        history.write(init_log)
        
    
    
    with open(file_history/region["id"], "r+") as history:
        content = []
        content.append("hello")
        content.append("\n")
        content.append(history.read())
        history.seek(0)
        history.truncate()
        history.write("".join(content))
    #print(original, "ORIGIN")