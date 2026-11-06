from pathlib import Path
import sys
import pickle
"""Reconstruction"""

def restore_files(second_arg=None,third_arg=None,forth_arg=None, fifth_arg=None):
    import json
    from pathlib import Path
    dir = Path.cwd()
    
    with open(dir/".track/index.json", "r") as index:
        index_data = json.load(index)
    files = index_data["files"]
    
    if second_arg == "-f" and third_arg != None:
        file = third_arg
        indexed_file = find_file(file, files)
        if indexed_file == False:
            print("File not found in the folder, check the file path, use a relative path if the file is in the current working directory or a subdirectory.")
            sys.exit(1)
        #print(indexed_file)
        file_id = indexed_file["id"]
        file_history = dir/".track/history"/file_id
        delta = forth_arg
        
        if forth_arg == None:
            with open(file_history/"LASTLOGID", "r") as log_id:
                last_log_id = log_id.read()
            delta = f"delta{last_log_id}"
        
            if str(last_log_id) == "0":
                print("This is the original version of the file, no changes have been made yet.")
                sys.exit(0)
            
        with open(file_history/f"deltas/{delta}", "rb") as delta_file:
            delta_content = pickle.load(delta_file)
            #print(delta_content)
        
        with open(file_history/f"ORIGIN", "r") as origin:
            origin_hash = origin.read()
        with open(file_history/f"{origin_hash}.tx", "r") as origin_file:
            origin_content = origin_file.read()
        #print(origin_content)
        
        if forth_arg == None:
            with open(indexed_file["path"], "r") as file_to_restore:
                current_file = file_to_restore.read()
                current_lines = current_file.splitlines(keepends=True)
                print("".join(current_lines))
                print("-"*50)
            
        for d in delta_content:
            operation = d["operation"]
            old_pos = d["old_position"]
            new_pos = d["new_position"]
            removed = d["removed"]
            added = d["added"]
            print(operation,old_pos,new_pos,removed,added)
            print("-"*50)
            #original_lines = origin_content.splitlines(keepends=True)
            
            if forth_arg == None:                
            #    if operation == "insert":
             #       del current_lines[new_pos:new_pos + len(added)]
              #  elif operation == "delete":
               #      current_lines[new_pos:new_pos] = removed
                #elif operation == "replace":
                 #   current_lines[new_pos:new_pos + len(added)] = removed
                 with open(dir/f".track/history/{file_id}/PREVIOUS", "r") as prev_file:
                    current_lines = prev_file.read()
        with open("bob","w+") as bob:
            bob.write("".join(current_lines))


def find_file(file_path, files):
    root = Path.cwd()

    path = Path(file_path)

    if path.is_absolute():
        print("WARNING: Using absolute paths is discouraged.")
        path = path.resolve()

        for file in files:
            if Path(file["path"]).resolve() == path:
                return file

        return False

    for file in files:
        relative_path = Path(file["path"]).relative_to(root)

        if relative_path.as_posix() == path.as_posix():
            return file

    return False
    
       
    """ 
    import questionary

    choice = questionary.select(
        "What would you like to do?",
        choices=[
            "Register project",
            "Create log",
            "View history",
            "Restore version",
            "Exit"
        ]
    ).ask()

    print(f"You selected: {choice}")
    """