
def init_history(i,file,track_path): 
    print(i,file,track_path)
    
    from pathlib import Path
    import json
    
    with open(track_path/"index.json") as indexfile:
        json_index = indexfile.read()
    
    index = json.loads(json_index)
    region = index["files"][i]
    #print(region)
    
    file_history = track_path/f"history/{region['id']}"
    
    """
    Format:
    Commit timestamp
    commit message
    previous datahash
    current datahash
    
    """
    
    with open(file_history, "w+") as history:
        with open(file,"r+") as open_file:
            content = open_file.read()
        
        history.write("b")