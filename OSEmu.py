import getpass
import os
import sys
import socket
import logging
import xml.etree.ElementTree as ET
from logger import LoggerXML

def repl():

    print("Имя скрипта: ", sys.argv[0])
    print("Переданные аргументы: ", *sys.argv[1:])

    VFS = (os.path.basename(sys.argv[1]) + os.path.dirname(__file__)[2:]) if len(sys.argv[1:]) != 0 \
        else os.path.dirname(__file__) 

    # logging.basicConfig(filename="info.log", level=logging.INFO, format="%(message)s")
    # with open("info.log", 'r+') as f:
    #     f.truncate(0)

    logger = LoggerXML("command_log.xml")

    while True:

        is_command = True

        cmdinput = input('~$'+getpass.getuser()+'.'+socket.gethostname()+ " " + VFS + ": ")

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
            is_command = False
            print("Неизвестная команда.")

        logger.log_command(cmdinput, is_command)
        
repl()
