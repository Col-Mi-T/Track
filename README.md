# Track

Track is a simple version control system written in Python. It tracks project files, detects changes, and stores file history locally.

## Installation

Download the executable from the releases.

Track is run with a cli with its command name being `track`

```bash
track --version
```

If you haven't configured Track as a command on your system, replace `track` with `./track` and run from the root directory of the downloaded executable.



## Commands

### 1. Register a project

```bash
track reg
```

Registers the current working directory for tracking.

During registration, Track:

1. Creates a `.track` directory.
2. Generates project configuration data.
3. Scans the current directory and its subdirectories.
4. Skips `.git`, `.track`, `not.track`, and the executable currently running.
5. Ignores files specified in `not.track`.
6. Generates an index containing information about each tracked file.
7. Creates history storage for every tracked file.

A project must be registered before using the other project commands.

### 2. Log changes

```bash
track log
```

Scans the project and compares its current state against the tracking index.

Track detects:

- New files.
- Deleted files.
- Renamed files.
- Modified files.

For modified files, Track compares the previous content with the current content and records the changes.

When creating a log, Track requests a message:

```text
Log Message:
```

Each modified file receives its own history entry.

### 3. View tracked files

```bash
track files
```

Displays information about the files currently being tracked, including:

- File path.
- File ID.
- Creation date.
- Last updated date.
- File size.
- File hash.

### 4. Restore a file

The restore command requires a file path.

```bash
track restore -f <file>
```

Restores the latest logged version of the specified file.

**Examples:**

```bash
track restore -f "workers/restore.py"
track restore -f "README.md"
```

By default, the restored content is written to the original file path, replacing its current content.

#### Restore a specific log

Use `-i` or `--id` to specify a log ID.

```bash
track restore -f <file> -i <log-id>
```

**Examples:**

```bash
track restore -f "workers/restore.py" -i 1
track restore -f "workers/restore.py" --id 3
```

If the ID is omitted, Track uses the latest log ID:

```bash
track restore -f "workers/restore.py" -i
```

Log IDs start at `1`.

#### Restore to another file

Use `-r` or `--restored` to specify a different output path.

```bash
track restore -f <file> -i <log-id> -r <output-file>
```

**Examples:**

```bash
track restore -f "workers/restore.py" -i 1 -r "restore.py"
track restore -f "README.md" --id 2 --restored "README_old.md"
```

This allows you to recover an older version without overwriting the updated file.

**Note:** The output option currently follows the ID option. You must include `-i` or `--id` before `-r` or `--restored`.

## Options

| Option | Description |
|---|---|
| `-h`, `--help` | Display help information. |
| `-v`, `--version` | Display the current Track version. |
| `-f` | Specify the file to restore. |
| `-i`, `--id` | Specify the log ID to restore. |
| `-r`, `--restored` | Specify an alternative restored-file output path. |

### Help

```bash
track --help
track -h
```

### Version

```bash
track --version
track -v
```

## Ignoring Files

Track uses a file named `not.track` to specify files and directories that should be ignored.

Example:

```text
build/
dist/
node_modules/
temp.txt
```

Entries can refer to individual files or directories.

Track also automatically ignores:

- `.git`
- `.track`
- `not.track`
- The currently running executable.

## Project Structure

```text
Track/
│
|-- track.py
│
|-- workers/
│   |-- register.py
│   |-- log.py
│   |-- restore.py
│   |-- tracked.py
│   |-- hashing.py
│   |-- history.py
│   |-- compare.py
│   |-- info.py
│
|-- .track/
    |-- config.json
    |-- index.json
    |-- history/
```

## How It Works

### `track.py`

The main entry point of Track.

It reads command-line arguments using `sys.argv` and dispatches commands to their corresponding functions.

### `register.py`

Handles project registration, directory scanning, configuration generation, and tracking-index creation.

### `log.py`

Handles project scanning and logging.

It detects new, deleted, renamed, and modified files, then records changes in their individual histories.

### `restore.py`

Handles file restoration.

It can restore the latest logged version or reconstruct an older version using stored deltas.

### `history.py`

Initialises history storage for newly tracked files.

### `hashing.py`

Generates file hashes using SHA-256 and creates file and project IDs.

### `compare.py`

Compares file contents, generates unified diffs, and creates structured changes for history reconstruction.

### `tracked.py`

Displays information about the files currently registered for tracking.

### `info.py`

Contains help, version, and interactive-menu functionality.

## Tracking Data

Track stores its internal data inside the `.track` directory.

### `config.json`

Contains project information:

- Track version.
- Project name.
- Project ID.
- Creation date.
- Ignore-file name.

### `index.json`

Contains information about every tracked file:

- File path.
- File ID.
- Creation date.
- Last updated date.
- File size.
- File hash.

### `history/`

Stores the history of individual files. Each file has its own directory, identified by its file ID.

A file's history directory contains:

| File | Purpose |
|---|---|
| `ORIGIN` | Stores the original file hash at registration. |
| `{hash}.tx` | Stores the original file content. |
| `PREVIOUS` | Stores the most recently logged content. |
| `LASTLOGID` | Stores the latest log ID, useful for logging changes. |
| `{file_id}.tr` | Stores the file's log history, useless to machines but human readable. |
| `deltas/` | Stores structured changes between versions as separate `delta<id>` binary files. |

Track uses the original content and stored deltas to reconstruct previous versions without keeping a complete copy of every version.

## Dependencies

Track's core functionality uses Python's standard library:

- `pathlib`
- `json`
- `datetime`
- `hashlib`
- `difflib`
- `sys`
- `shutil`
- `pickle`

The interactive menu uses the third-party package:

- `questionary`

