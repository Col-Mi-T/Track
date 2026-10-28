import sys
sys.dont_write_bytecode = True

track_version = "0.1.0"

def track():
    args = sys.argv[1:]
    
    if len(args)<1:
        from workers.info import print_help
        print_help()
        sys.exit(0)
        
    command = args[0]
    second_arg = None if not len(args)>1 else args[1]
    third_arg = None if not len(args)>2 else args[2]
    forth_arg = None if not len(args)>3 else args[3]
        
    if command == "--help" or command == "-h":
        from workers.info import print_help
        print_help()
        
    elif command == "version" or command == "-v":
        from workers.info import print_version
        print_version(track_version)
    
    elif command == "reg":
        
        from workers.register import register_project
        register_project(track_version)
        
    elif command == "log":
        from workers.log import log_project
        log_project()
    
    else:
        cli = "track"
        for i in args:
            cli += " " + i
        print("Unknown command: " + cli)
        from workers.info import print_help
        print_help()
        sys.exit(1)
        

if __name__ == "__main__":
    track()