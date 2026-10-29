
def file_to_bin(i,file,track_path):
    from pathlib import Path
    import json
    with open(track_path/"index.json") as indexfile:
        json_index = indexfile.read()
    index = json.loads(json_index)
    region = index["files"][i]
    #print(region)
    file_home = track_path/f"obj/{region['id']}"
    Path.mkdir(file_home, exist_ok=True)
    with open(file_home/region["hash"], "wb+") as file_rep:
        with open(file,"r+") as open_file:
            content = open_file.read()
        
        val = ""
        binary = bytearray()
        #print(content)
        for i in content:
            #print(i)
            val+=str((binary.append(ord(i))))
        #print(val)
        data=binary
        file_rep.write(data)
    
    #print(region["file_size"])
    #print(Path(f"{file_home}/{region["hash"]}.hsh").stat().st_size)