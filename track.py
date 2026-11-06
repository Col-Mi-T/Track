import sys
sys.dont_write_bytecode = True

track_version = "0.1.0"

def track():
    args = sys.argv[1:]
    
    if len(args)<1:
        from workers.info import print_help,options
        print_help()
        options()
        sys.exit(0)
        
    command = args[0]
    second_arg = None if not len(args)>1 else args[1]
    third_arg = None if not len(args)>2 else args[2]
    forth_arg = None if not len(args)>3 else args[3]
    fifth_arg = None if not len(args)>4 else args[4]
        
    if command == "--help" or command == "-h":
        from workers.info import print_help
        print_help()
        
    elif command == "--version" or command == "-v":
        from workers.info import print_version
        print_version(track_version)
    
    elif command == "reg":
        #try:
            from workers.register import register_project
            register_project(track_version)
            """
        except Exception as e:
            print("Unexpected Error:",e,"\n")
            import shutil
            from pathlib import Path
            trackpath=Path.cwd() / ".track"
            if Path.exists(trackpath):
                shutil.rmtree(trackpath)
            sys.exit(1)
        """
        
    elif command == "log":
        from workers.log import log_project
        log_project()
    
    elif command == "restore":
        from workers.restore import restore_files
        #print(second_arg,third_arg)
        if forth_arg and forth_arg not in ("-r", "--restore"):
            forth_arg = None
        print(second_arg,third_arg,forth_arg,fifth_arg)
        restore_files(second_arg,third_arg,forth_arg,fifth_arg)
    
    elif command == "files":
        from workers.tracked import tracked_files
        tracked_files()
    else:
        cli = "track"
        for i in args:
            cli += " " + i
        print("Unknown command: " + cli)
        from workers.info import print_help,options
        print_help()
        options()
        sys.exit(0)
        

if __name__ == "__main__":
    track()