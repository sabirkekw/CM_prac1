import getpass
import os
import sys
import socket
import lxml.etree as ET
from logger import LoggerXML
from command_handle import *

def repl():
    file = False
    try:
        arguments = sys.argv

        print("Имя скрипта: ", arguments[0])
        print("Переданные аргументы: ", *arguments[1:])

        VFS = ET.parse(arguments[1]).getroot()
        current_directory = VFS.get("name")
        #current_directory = "root/home/john"
    except IndexError:
        print("Введено неверное количество аргументов.")
        return
    
    address = arguments[2] if len(arguments)>=3 \
        else '.'
    print(address)
    logger = LoggerXML("command_log.xml",address)
    
    if len(arguments)>=4:
        f = open(arguments[3],'r',encoding='utf8')
        file = True

    while True:

        is_command = True

        if file==False:
            cmdinput = input('~$'+getpass.getuser()+'.'+socket.gethostname()+ " " + current_directory + ": ")
        else:
            cmdinput = f.readline()
            print('~$'+getpass.getuser()+'.'+socket.gethostname()+ " " + current_directory + ": " + cmdinput.strip())

        command = cmdinput.split()[0]
        args = cmdinput.split()[1:]

        for i, arg in enumerate(args):
            if arg[0] == "$":
                args[i] = os.environ.get(arg[1:])
            
        if command == ('exit'):
            logger.log_command(cmdinput, is_command)
            return
        elif command == "ls":
            Ls(current_directory,VFS,args).handle()
        elif command == "cd":
            current_directory = Cd(current_directory,VFS,args).handle()
        elif command == "tree":
            Tree(current_directory,VFS,args).handle()
        elif command == "uname":
            Uname(current_directory,VFS,args).handle()
        elif command == "tac":
            Tac(current_directory,VFS,args).handle()
        elif command == "cat":
            Cat(current_directory,VFS,args).handle()

        
        elif command[0] == '$':
            print("Неизвестная команда.")
            print(os.environ.get(command[1:]))
                
        else:
            is_command = False
            print("Неизвестная команда.")

        logger.log_command(cmdinput, is_command)
        
repl()