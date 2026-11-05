# Track

Track is a simple version control system written in Python. It tracks project files, generates hashes to identify file changes, and stores file history locally.

## Project Structure

```text
Track/
|-- track.py
|-- workers/
│   |-- register.py
│   |-- log.py
│   |-- hashing.py
│   |-- history.py
│   |-- compare.py
|-- .track/
    |-- config.json
    |-- index.json
    |-- history/
```

## How It Works

### `track.py`

The main entry point of Track. It reads command-line arguments using `sys.argv` and sends commands to their corresponding functions.

Current commands:
- `reg` – Registers the current directory.
- `log` – Checks for changes and records them.
- `--help` – Displays help information.
- `--version` – Displays the current version.

### `workers/register.py`

Handles project registration.

When a project is registered, Track:

1. Creates a `.track` directory.
2. Generates a project configuration.
3. Scans the current directory and its subdirectories.
4. Skips `.git`, `.track`, `not.track`, and ignored entries found in `not.track` (my version of `.gitignore`).
5. Generates an index containing information about each tracked file.
6. Initialises history storage for the files.

### `workers/log.py`

Handles project logging.

It scans the project again and compares the current files against the tracking index.

It handles:
- New files.
- Deleted files.
- Renamed files.
- Modified files.

For modified files, it compares the previous content with the current content and records the changes in the file's history.

## Tracking Data

Track stores its data inside `.track`.

### `config.json`

Contains project information:

- Track version.
- Project name.
- Project ID.
- Creation date.
- Ignore file name.

### `index.json`

Contains information about tracked files:

- File path.
- File ID.
- Creation date.
- Last updated date.
- File size.
- File hash.

### `history/`

Stores the history data for individual files. Each file has its own history directory, identified by its file ID.

The history data includes the original content, previous content, last log ID, and recorded changes.

## Other Modules

| Module | Responsibility |
|---|---|
| `hashing.py` | Generates file hashes and IDs. |
| `compare.py` | Compares file hashes and detects changes. |
| `history.py` | Initialises file history storage. |

## Dependencies

Track currently uses Python's standard library for its core functionality, including:

- `pathlib`
- `json`
- `datetime`
- `hashlib`
- `difflib`
- `sys`
- `shutil`
- `pickle`

No third-party Python packages are currently required.