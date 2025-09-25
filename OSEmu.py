import getpass
import os
import sys
import socket
import xml.etree.ElementTree as ET
from logger import LoggerXML
from vfs__xml import *

def repl():
    file = False
    try:
        arguments = sys.argv

        print("Имя скрипта: ", arguments[0])
        print("Переданные аргументы: ", *arguments[1:])

        vfs_dict = parse_vfs_xml(arguments[1])
        #print(vfs_dict)
        current_directory = vfs_dict.get('path')

    except IndexError:
        print("Введено неверное количество аргументов.")
        return
    
    address = arguments[2] if len(arguments)>=3 \
        else '.'

    logger = LoggerXML("command_log.xml",address)
    
    if len(arguments)>=4:
        f = open(arguments[3],'r',encoding='utf8')
        file = True

    while True:
        is_command = True

        if file==False:
            cmdinput = input('~$'+getpass.getuser()+'.'+socket.gethostname()+ " " + current_directory + "> ")
        else:
            cmdinput = f.readline()
            print('~$'+getpass.getuser()+'.'+socket.gethostname()+ " " + current_directory + "> " + cmdinput.strip())

        command = cmdinput.split()[0]
        args = cmdinput.split()[1:]

        for i, arg in enumerate(args):
            if arg[0] == "$":
                args[i] = os.environ.get(arg[1:]) 
        if command == ('exit'):
            logger.log_command(cmdinput, is_command)
            return
        elif command == "ls":
            ls(vfs_dict, args, current_directory)
        elif command == "cd":
            current_directory = cd(vfs_dict, args, current_directory)
        elif command == "tree":
            tree(vfs_dict, args, current_directory)
        elif command == "uname":
            uname(args)
        elif command == "tac":
            tac(vfs_dict, args, current_directory)
        elif command[0] == '$':
            print("Неизвестная команда.")
            print(os.environ.get(command[1:]))
                
        else:
            is_command = False
            print("Неизвестная команда.")

        logger.log_command(cmdinput, is_command)
        
repl()