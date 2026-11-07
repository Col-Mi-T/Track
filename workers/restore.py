
from pathlib import Path
import sys
import pickle
"""Reconstruction"""

def restore_files(second_arg=None,third_arg=None,forth_arg=None, fifth_arg=None,sixth_arg=None,seventh_arg=None):
    import json
    dir = Path.cwd()

    if sixth_arg and seventh_arg:
        restored = seventh_arg #Path(seventh_arg).relative_to(dir)
    else:
        restored = Path(third_arg)
    
    if fifth_arg != None:
        try:
            fifth_arg = int(fifth_arg)
        except ValueError:
            print("Invalid log ID. Please provide a valid integer.")
            sys.exit(1)

    with open(dir/".track/index.json", "r") as index:
        index_data = json.load(index)
    files = index_data["files"]

    if second_arg == "-f" and third_arg != None:
        file = third_arg
        indexed_file = find_file(file, files)

        if indexed_file == False:
            print("File not found in the folder, check the file path, use a relative path if the file is in the current working directory or a subdirectory.")
            sys.exit(1)

        file_id = indexed_file["id"]
        file_history = dir/".track/history"/file_id

        with open(file_history/"LASTLOGID", "r") as log_id:
            last_log_id = int(log_id.read())

        if forth_arg == None:
            if last_log_id == 0:
                print("This is the original version of the file, no changes have been made yet.")
                sys.exit(0)

            with open(file_history/"PREVIOUS", "r") as prev_file:
                current_content = prev_file.read()

        else:
            if fifth_arg == None:
                fifth_arg = last_log_id

            if fifth_arg > last_log_id or fifth_arg < 1:
                print(f"Invalid log ID. The last log ID for this file is {last_log_id}.")
                sys.exit(1)

            with open(file_history/"ORIGIN", "r") as origin:
                origin_hash = origin.read()

            with open(file_history/f"{origin_hash}.tx", "r") as origin_file:
                origin_content = origin_file.read()
                current_lines = origin_content.splitlines(keepends=True)

            current_delta = 1

            while current_delta <= fifth_arg:
                print(current_delta)
                delta = f"delta{current_delta}"

                with open(file_history/f"deltas/{delta}", "rb") as delta_file:
                    delta_content = pickle.load(delta_file)

                new_lines = []
                position = 0

                for d in delta_content:
                    operation = d["operation"]
                    old_pos = d["old_position"]
                    new_pos = d["new_position"]
                    removed = d["removed"]
                    added = d["added"]

                    print(f"Operation: {operation}\n Old Position: {old_pos}\n New Position: {new_pos}\n Removed: {removed}\n Added: {added}")

                    # Copy unchanged lines
                    new_lines.extend(current_lines[position:old_pos])

                    # Add the new lines
                    new_lines.extend(added)

                    # Move past the removed lines
                    position = old_pos + len(removed)

                # Copy whatever remains
                new_lines.extend(current_lines[position:])

                current_lines = new_lines
                current_delta += 1

            current_content = "".join(current_lines)

        with open(restored, "w+") as restored_file:
            restored_file.write(current_content)


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
