def print_help():
    print("""
Track - A simple version control system

Usage:
    track <command> [arguments]

Commands:

    reg
        Register the current directory for tracking.

    log
        Scan the project and record changes.
        Detects new, modified, deleted and renamed files.

    files
        Display all tracked files and their information.

    restore -f <file>
        Restore the latest logged version of a file.

    restore -f <file> -i
    restore -f <file> --id
        Restore the latest logged version using its log ID.

    restore -f <file> -i <id> -r <output>
    restore -f <file> --id <id> --restored <output>
        Restore a version to a different output file.

Options:

    -h, --help
        Display this help message.

    -v, --version
        Display the current Track version.

    -f <file>
        Specify the file to restore.

    -i, --id <id>
        Specify the log ID to restore.

    -r, --restored <output>
        Specify an alternative output path for the restored file.

Examples:

    track reg
    track log
    track files

    track restore -f "README.md"
    track restore -f "workers/restore.py"

    track restore -f "README.md" -i 1
    track restore -f "README.md" --id 2

    track restore -f "README.md" -i 1 -r "README_old.md"
    track restore -f "README.md" --id 2 --restored "README_old.md"

    track --version
    track -v

    track --help
    track -h

For more information, see the Track documentation.
""")
def print_version(track_version):
    print(f"{track_version}")

def options():
    import sys
    import questionary
    choice = questionary.select(
        "What would you like to do?",
        choices=[
            "Register a project",
            "Create a log",
            "View a file history",
            "Restore a file version",
            "Exit"
        ]
    ).ask()
    if choice.lower() == "exit":
        sys.exit(0)
    elif choice.lower() == "register a project":
        from workers.register import register_project
        from track import track_version
        register_project(track_version)
    elif choice.lower() == "create a log":
        from workers.log import log_project
        log_project()
    elif choice.lower() == "restore a file version":
        from workers.restore import project_museum
        project_museum()
    elif choice.lower()=="exit":
        sys.exit(0)