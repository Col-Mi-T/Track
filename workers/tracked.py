def tracked_files():
    import json
    from pathlib import Path
    dir = Path.cwd()
    with open(dir/".track/config.json", "r") as f:
        data = json.load(f)
    print(f"Welcome to {data['project_name']}'s Museum!")
    with open(dir/".track/index.json", "r") as index:
        index_data = json.load(index)
    files = index_data["files"]
    print(f"\nFiles Tracked({len(files)}):")
    for file in files:
        print(f"\nFile: {file['path']}")
        print(f"ID: {file['id']}")
        print(f"Created: {file['created']}")
        print(f"Last Updated: {file['last_updated']}")
        print(f"File Size: {file['file_size']}")
        print(f"Hash: {file['hash']}")