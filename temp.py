import getpass
import os
import sys
import socket

def repl():

    print("Имя скрипта: ", sys.argv[0])
    print("Переданные аргументы: ", *sys.argv[1:])

    VFS = ""

    while True:

        is_command = True

        cmdinput = input('~$'+getpass.getuser()+'.'+socket.gethostname()+ "" + VFS + ": ")

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
