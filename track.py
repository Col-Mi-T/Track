def track():
    import sys
    args = sys.argv[1:]
    
    command = args[0]
    second_arg = None if not len(args)>1 else args[1]
    third_arg = None if not len(args)>2 else args[2]
    forth_arg = None if not len(args)>3 else args[3]
    
    if len(args)<1:
        from workers.info import print_help
        print_help()
    
    
    elif command == "--help" or command == "-h":
        from workers.info import print_help
        print_help()
        
    elif command == "version" or command == "-v":
        from workers.info import print_version
        print_version()
    
    else:
        cli = "track"
        for i in args:
            cli += " " + i
        print("Unknown command: " + cli)
        from workers.info import print_help
        print_help()
        

if __name__ == "__main__":
    track()