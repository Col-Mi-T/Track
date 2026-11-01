
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