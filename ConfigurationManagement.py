import getpass
import os
import socket

def repl():
    
    while True:
        cmdinput = input('~$'+getpass.getuser()+'.'+socket.gethostname()+": ")
        command = cmdinput.split()[0]
        args = cmdinput.split()[1:]
        
        for i, arg in enumerate(args):
            if arg[0] == "$":
                args[i] = os.environ.get(arg[1:])
            
        if command == ('exit'):
            return
        elif command == "ls":
            print(command, "\n", *args)
        elif command == "cd":
            print(command, "\n", *args)

        
        elif command[0] == '$':
            print(os.environ.get(command[1:]))
                
        else:
            print("Неизвестная команда.")
        
repl()
