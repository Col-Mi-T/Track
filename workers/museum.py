def project_museum():
    import json
    from pathlib import Path
    dir = Path.cwd()
    with open(dir/".track/config.json", "r") as f:
        data = json.load(f)
    print(f"Welcome to {data['project_name']}'s Museum!")