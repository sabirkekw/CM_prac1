import getpass
import os
import sys
import socket
import xml.etree.ElementTree as ET
from logger import LoggerXML

def repl():
    file = False
    try:
        arguments = sys.argv

        print("Имя скрипта: ", arguments[0])
        print("Переданные аргументы: ", *arguments[1:])

        VFS = ET.parse(arguments[1]).getroot()
        vfs_name = VFS.attrib["name"]
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
            cmdinput = input('~$'+getpass.getuser()+'.'+socket.gethostname()+ " " + vfs_name + ": ")
        else:
            cmdinput = f.readline()
            print('~$'+getpass.getuser()+'.'+socket.gethostname()+ " " + vfs_name + ": " + cmdinput.strip())

        command = cmdinput.split()[0]
        args = cmdinput.split()[1:]

        for i, arg in enumerate(args):
            if arg[0] == "$":
                args[i] = os.environ.get(arg[1:])
            
        if command == ('exit'):
            logger.log_command(cmdinput, is_command)
            return
        elif command == "ls":
            print(command, *args)
        elif command == "cd":
            print(command, *args)

        
        elif command[0] == '$':
            print("Неизвестная команда.")
            print(os.environ.get(command[1:]))
                
        else:
            is_command = False
            print("Неизвестная команда.")

        logger.log_command(cmdinput, is_command)
        
repl()