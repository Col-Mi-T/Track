import sys
import colors
sys.dont_write_bytecode = True

track_version="1.1.0"


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
    sixth_arg =  None if not len(args)>5 else args[5]
    seventh_arg =  None if not len(args)>6 else args[6]
        
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
            sys.exit(0)
        #except Exception as e:
         #   print(f"{colors.RED}Unexpected Error:",e,"\n{colors.RESET}")
          #  import shutil
           # from pathlib import Path
            #trackpath=Path.cwd() / ".track"
            #if Path.exists(trackpath):
             #   shutil.rmtree(trackpath)
            #sys.exit(1)
        
        
    from pathlib import Path
    track_path = Path.cwd() / ".track"
    registered = Path.exists(track_path)
    if not registered:
        print(f"{colors.RED}Project not registered. Please register the project first using 'track reg'.{colors.RESET}")
        sys.exit(1)
        
    elif command == "log":
        from workers.log import log_project
        log_project()
    
    elif command == "restore":
        from workers.restore import restore_files
        #print(second_arg,third_arg)
        if forth_arg and forth_arg not in ("-i", "--id"):
            print(f"{colors.RED}Invalid option. Use -i or --id to specify a log ID.{colors.RESET}")
            sys.exit(1)
        if sixth_arg and sixth_arg not in ("-r", "--restored"):
            print(f"{colors.RED}Invalid option. Use -r or --restored to a file to restore{colors.RESET}")
            sys.exit(1)
        #print(second_arg,third_arg,forth_arg,fifth_arg)
        restore_files(second_arg,third_arg,forth_arg,fifth_arg,sixth_arg,seventh_arg)
    
    elif command == "files":
        from workers.tracked import tracked_files
        tracked_files()
    
    elif command == "history":
        from workers.history import file_history
        file_history(second_arg,third_arg)
    
    else:
        cli = "track"
        for i in args:
            cli += " " + i
        print(f"{colors.RED}Unknown command: " + cli,colors.RESET)
        from workers.info import print_help,options
        print_help()
        options()
        sys.exit(0)
        

if __name__ == "__main__":
    track()