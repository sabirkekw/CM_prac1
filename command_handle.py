import abc
import lxml.etree as ET
import os
from platform import uname
from socket import gethostname

def print_tree(element, level=0):
    indent = "  " * level
    
    if element.get('name'):
        print(f"{indent}{element.get('name')}")
    
    for child in element:
        print_tree(child, level + 1)

class Command(abc.ABC):
    def __init__(self, current_path, vfs, args=[]):
        self.current_path = current_path
        self.args = args
        self.vfs_root = vfs
    @abc.abstractmethod
    def handle(self):
        pass

    def find_elem(self,args=[]):
        folders = os.path.join(self.current_path,args[0]).replace('\\','/').split("/") if args \
            else self.current_path.split('/') # creating path from current directory and argument

        while '.' in folders or '..' in folders: # clearing all ".." and "."
            for folder in folders:
                match folder:
                    case '.':
                        folders.remove(folder)
                    case '..':
                        i = folders.index(folder)
                        folders.pop(i-1)
                        folders.pop(i-1)

        current_dir = self.vfs_root
        for folder in folders[1:]: # checking if directory exists
            for child in current_dir.findall('./'):
                if child.get("name") == folder:
                    current_dir = child
                    break
            else:
                print("Неверный путь.")
                return
            
        
        return current_dir, '/'.join(folders)

class Ls(Command):
    def __init__(self, current_path, vfs_root, args=[]):
        super().__init__(current_path, vfs_root, args)
    def handle(self):
        current_dir = self.find_elem(self.args)
        if current_dir:
            for item in current_dir[0]:
                print(item.get("name"), end="   ")
            print()
            return current_dir
        return

class Cd(Command):
    def __init__(self, current_path, vfs_root, args=[]):
        super().__init__(current_path, vfs_root, args)
    def handle(self):
        elem = self.find_elem(self.args)
        if elem:
            return self.find_elem(self.args)[1]
        return self.current_path
    
class Tree(Command):
    def __init__(self, current_path, vfs_root, args=[]):
        super().__init__(current_path, vfs_root, args)
    def handle(self):
        elem = self.find_elem(self.args)
        if elem:
            elem = elem[0]
            print_tree(elem)

class Uname(Command):
    def __init__(self, current_path, vfs_root, args=[]):
        super().__init__(current_path, vfs_root, args)
    def handle(self):
        info = uname()
        infodict = {'-a':" ".join(info), '-s':info[0], '-n':info[1], '-v':info[2], '-p':info[-1], '-i':info[-2]}
        if self.args:
            for flag in self.args:
                print(infodict.get(flag),end=' ')
            print()
        else:
            print(infodict.get('-s'))


class Tac(Command):
    def __init__(self, current_path, vfs_root, args=[]):
        super().__init__(current_path, vfs_root, args)
    def handle(self):
        if self.args:
            elem = self.find_elem(self.args)
            if elem:
                elem = elem[0].text.split("\n")
                for i in elem[::-1]:
                    print(i)
        else:
            print(input())

class Cat(Command):
    def __init__(self, current_path, vfs_root, args=[]):
        super().__init__(current_path, vfs_root, args)
    def handle(self):
        if self.args:
            elem = self.find_elem(self.args)
            if elem:
                elem = elem[0].text.split("\n")
                for i in elem:
                    print(i)
        else:
            print(input())