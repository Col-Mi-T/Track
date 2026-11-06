
from pathlib import Path
import json
import sys


def log_project():
    # equivalent to git commit -m "message"
    from datetime import datetime
    from workers.hashing import hash_file

    message = input("Log Message: ")
    old = []
    index_path = Path.cwd() / ".track/index.json"
    index = get_index(index_path)

    prev_hashes = {
        file["id"]: file["hash"]
        for file in index["files"]
    }

    for file in index["files"]:
        f = file["path"]
        old.append(str(f))

    new = scan_dir()
    new_files = [file for file in new if file not in old]

    from workers.compare import check_hash

    for file in index["files"][:]:
        f = Path(file["path"])

        if not f.exists():
            import shutil

            file_id = file["id"]
            match = check_hash(file["hash"], new_files)

            if match:
                print("RENAME:", file["path"], "->", match)
                file["path"] = match
                new_files.remove(match)

            else:
                file_history_path = Path.cwd() / f".track/history/{file_id}"

                if file_history_path.exists():
                    shutil.rmtree(file_history_path)

                index["files"].remove(file)
                print(f"\n\nDELETED {f}\n\n")

        else:
            pass

    for file in index["files"]:
        f = Path(file["path"])
        file["last_updated"] = str(datetime.now())
        file["file_size"] = str(f.stat().st_size) + " bytes"
        file["hash"] = hash_file(file["path"])

    for file in new_files:
        print(f"{file}===NEW")
        index["files"] = append_index(file, index)
        update_index(index, index_path)

        from workers.history import init_history

        track_path = Path.cwd() / ".track"
        i = len(index["files"]) - 1
        init_history(i, file, track_path)

    update_index(index, index_path)

    for file in index["files"]:
        if file["id"] in prev_hashes:
            log_history(file, message, prev_hashes)


def get_index(index_path):
    with open(index_path, "r+") as index:
        index_content = json.loads(index.read())

    return index_content


def scan_dir():
    from workers.register import scan_directory

    current = Path.cwd()
    items = list(current.iterdir())
    files = []

    config_path = Path.cwd() / ".track/config.json"

    with open(config_path, "r+") as config:
        file = json.loads(config.read())

    ignore_file = file["ignorefile"]

    if Path.exists(Path.cwd() / ignore_file):
        with open(Path.cwd() / ignore_file, "r+") as ignorefile:
            ignore = ignorefile.read().splitlines()
    else:
        ignore = []

    for item in items:
        relative_path = item.relative_to(current).as_posix()

        if any(
            relative_path == path.rstrip("/")
            or relative_path.startswith(path.rstrip("/") + "/")
            for path in ignore
        ):
            continue

        if (
            item.name in [".git", ".track", "not.track"]
            or item.name in ignore
            or relative_path in ignore
            or item.resolve() == Path(sys.executable).resolve()
        ):
            continue
        else:
            if item.is_file():
                files.append(str(item))
            else:
                scan_directory(item, files, ignore, relative_path)

    return files


def append_index(i, index):
    files = index["files"]

    from workers.register import gen_id
    from datetime import datetime
    from workers.hashing import hash_file

    hashdata = hash_file(i)
    id = gen_id(i)
    now = datetime.now()

    info = {
        "path": i,
        "id": id,
        "created": str(now),
        "last_updated": str(now),
        "file_size": str(Path(i).stat().st_size) + " bytes",
        "hash": hashdata,
    }

    files.append(info)

    return files


def update_index(index, index_path):
    with open(index_path, "w+") as index_file:
        index_file.write(json.dumps(index, indent=4))


def log_history(file, message, prev_hashes):
    prev_hash = prev_hashes[file["id"]]

    from datetime import datetime
    from workers.compare import compare_changes

    history_path = Path.cwd() / f".track/history/{file['id']}"

    with open(history_path / "ORIGIN", "r+") as origin:
        original = origin.read()

    with open(history_path / f"{original}.tx", "r+") as ancestor:
        initial = ancestor.read()

    with open(history_path / "PREVIOUS", "r+") as prev:
        previous = prev.read()

    with open(file["path"], "r+") as current:
        present = current.read()

    changes = compare_changes(previous, present)

    print(f"\n{file['path']}:")

    if changes == False:
        print("No Changes Detected. Edit/save file and retry.\n")
        pass

    else:
        changes = list(changes)
        print("\n".join(changes))

        with open(history_path / "LASTLOGID", "r") as log_id:
            prev_id = log_id.read()

        with open(history_path / "LASTLOGID", "w") as log_id:
            new_id = int(prev_id) + 1
            log_id.write(str(new_id))

        with open(history_path / f"{file['id']}.tr", "r+") as history:
            log = f"LOG ID = {new_id}"
            log_message = f"\n\tMessage = {message}"
            time = f"\n\tTime = {datetime.now()}"
            c_hash = f"\n\tCurrent Hash = {file['hash']}"
            p_hash = f"\n\tPrevious Hash = {prev_hash}"
            ch = "\n\t\t".join(changes)
            change = f"\n\tChanges =\n\t\t{ch}"

            update_log = (
                f"{log}{log_message}{time}{c_hash}"
                f"{p_hash}{change}\n\n{'-' * 100}\n"
            )

            content = []
            content.append(update_log)
            content.append("\n")
            content.append(history.read())

            history.seek(0)
            history.truncate()
            history.write("".join(content))

        with open(history_path / "PREVIOUS", "w") as prev:
            prev.write(present)

        (history_path / "deltas").mkdir(exist_ok=True)

        with open(history_path / "LASTLOGID", "r") as log_ids:
            log_id = log_ids.read()

        with open(history_path / f"deltas/delta{log_id}", "wb+") as written_delta:
            from workers.compare import structured_changes
            import pickle

            delta_data = structured_changes(previous, present)
            pickle.dump(delta_data, written_delta)
