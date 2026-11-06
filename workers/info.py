
def print_help():
    print("""
Track - A simple version control system

Usage:
    track <command> [arguments]

Commands:
    reg                 Register the current directory for tracking
    log                 Record changes to tracked files

Options:
    -h, --help          Display this help message
    -v, --version       Display the current Track version

Examples:
    track reg           Register the current project
    track log           Log changes to the project
    track --version     Show the installed version
    track --help        Display help information

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