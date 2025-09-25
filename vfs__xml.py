import xml.etree.ElementTree as ET

def parse_element(element, parent_path):
        item = {
            'type': element.tag,
            'name': element.attrib.get('name', ''),
            'path': element.attrib.get('path', ''),
        }
        
        if element.tag == 'folder':
            item['children'] = {}
            for child in element:
                child_name = child.attrib.get('name', '')
                item['children'][child_name] = parse_element(child, item['path'])
        
        return item

def parse_vfs_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    vfs_structure = {
        'type': 'folder',
        'name': 'root',
        'path': '/',
        'children': {}
    }
    
    root_folder = root.find('folder')
    if root_folder is not None:
        vfs_structure = parse_element(root_folder, '/')
    
    return vfs_structure

def in_dict(vfs, current_directory):
    # Check if current node matches the path
    if vfs.get("path") == current_directory:
        return True
    
    # Check children recursively
    children = vfs.get("children")
    if children:
        for child_name, child_dict in children.items():
            if in_dict(child_dict, current_directory):
                return True
    
    return False

# def return_children(vfs, current_directory):
#     if vfs.get("path") == current_directory:
#         print(" ".join(vfs.get("children").keys()))
#         return True
    
#     # Check children recursively
#     children = vfs.get("children")
#     if children:
#         for child_name, child_dict in children.items():
#             if in_dict(child_dict, current_directory):
#                 print(" ".join(child_dict.get("children").keys()))
#                 return True
    
#     return False
def return_children(vfs, current_directory):
    # Recursive search function
    def find_and_list_children(vfs_node, search_path):
        if vfs_node.get("path") == search_path:
            # Found the target directory
            children = vfs_node.get("children", {})
            if children:
                print(" ".join(sorted(children.keys())))
            else:
                print("")  # Empty directory
            return True
        
        # Search in children recursively
        children = vfs_node.get("children", {})
        for child_name, child_node in children.items():
            if find_and_list_children(child_node, search_path):
                return True
        
        return False
    
    # Start the recursive search
    if not find_and_list_children(vfs, current_directory):
        print("Введен неверный путь.")
        return False
    
    return True

def uname(arg):
    print("Shlinux")

def tac(vfs, arg, current_directory):
    if not arg:
        pass
    file = arg[0]
    path = current_directory + file
    if in_dict(vfs,path):
        content = 1

def tree(vfs, arg, current_directory, level=0, prefix=""):
    # Determine target path
    if not arg:
        # tree without arguments - show current directory
        target_path = current_directory
    else:
        target = arg[0]
        
        # Use cd to resolve the path
        resolved_path = cd(vfs, [target], current_directory)
        if resolved_path == current_directory:  # Path doesn't exist or invalid
            print("Введен неверный путь.")
            return
        target_path = resolved_path
    
    # Check if path exists
    if not in_dict(vfs, target_path):
        print("Введен неверный путь.")
        return
    
    # Recursive function to find and display tree structure
    def display_tree(vfs_node, search_path, current_level, current_prefix):
        # Check if this is the node we're looking for
        if vfs_node.get("path") == search_path:
            # Display current node
            node_name = vfs_node.get("name", "unknown")
            if current_level == 0:
                print(f"{node_name}/")
            else:
                print(f"{current_prefix}{node_name}/")
            
            # Display children recursively
            children = vfs_node.get("children", {})
            if children:
                child_count = len(children)
                for i, (child_name, child_node) in enumerate(sorted(children.items())):
                    is_last = (i == child_count - 1)
                    
                    if current_level == 0:
                        new_prefix = "    "
                    else:
                        new_prefix = current_prefix + "    "
                    
                    if is_last:
                        connector = "└── "
                        next_prefix = current_prefix + "    "
                    else:
                        connector = "├── "
                        next_prefix = current_prefix + "│   "
                    
                    if child_node.get("type") == "folder":
                        print(f"{current_prefix}{connector}{child_name}/")
                        # Recursively display folder contents
                        display_tree(child_node, child_node.get("path"), current_level + 1, next_prefix)
                    else:
                        print(f"{current_prefix}{connector}{child_name}")
            return True
        
        # Search in children
        children = vfs_node.get("children", {})
        for child_name, child_node in children.items():
            if in_dict(child_node, search_path):
                return display_tree(child_node, search_path, current_level, current_prefix)
        
        return False
    
    # Start displaying tree from root if target is root, otherwise find the target
    if target_path == vfs.get("path", ""):
        display_tree(vfs, target_path, 0, "")
    else:
        # Find the starting node
        found = False
        children = vfs.get("children", {})
        for child_name, child_node in children.items():
            if in_dict(child_node, target_path):
                found = display_tree(child_node, target_path, 0, "")
                if found:
                    break
        
        if not found:
            print("Введен неверный путь.")

def ls(vfs, arg, current_directory):
    if not arg:
        return return_children(vfs, current_directory)
    
    target = arg[0]

    if target == '~':
        return return_children(vfs, "root/home")
    if target == '/':
        return return_children(vfs, "root/")
    if target == '.':
        return return_children(vfs, current_directory)
    
    if target.startswith('root/'):
        if not in_dict(vfs, target):
            print("Введен неверный путь.")
            return False
        return return_children(vfs, target)
    
    # Handle parent directory cases first
    if target == '..':
        components = current_directory.rstrip('/').split('/')
        if len(components) <= 1:
            print("Неверная команда.")
            return False
        components.pop()
        new_path = '/'.join(components) if components else 'root'
        return return_children(vfs, new_path + '/') if new_path == 'root' else return_children(vfs, new_path)
    
    if target.startswith('../'):
        components = current_directory.rstrip('/').split('/')
        if len(components) <= 1:
            print("Неверная команда.")
            return False
        remaining_path = target[3:]
        components.pop()
        
        if remaining_path:
            remaining_components = remaining_path.split('/')
            for comp in remaining_components:
                if comp == '..':
                    if components:
                        components.pop()
                elif comp != '.' and comp != '':
                    components.append(comp)
        
        new_path = '/'.join(components) if components else 'root'
        new_path = new_path + '/' if new_path == 'root' else new_path

        if not in_dict(vfs, new_path):
            print("Введен неверный путь.")
            return False
        
        return return_children(vfs, new_path)
    
    if target.startswith('/'):
        # Absolute path
        base_components = ['root']
        target_path = target[1:]
    else:
        # Relative path
        base_components = current_directory.rstrip('/').split('/')
        target_path = target
    
    components = target_path.split('/')
    for component in components:
        if component == '' or component == '.':
            continue
        elif component == '..':
            if len(base_components) > 1:  # Don't remove 'root'
                base_components.pop()
        else:
            base_components.append(component)
    
    full_dir = '/'.join(base_components)
    if full_dir == 'root':
        full_dir = 'root/'
    
    if not in_dict(vfs, full_dir):
        print("Введен неверный путь.")
        return False
    
    return return_children(vfs, full_dir)
    

def cd(vfs, arg, current_directory):
    if not arg:
        return "root/home"
    
    target = arg[0]
    
    if target == '~':
        return "root/home"
    if target == '/':
        return "root/"
    if target == '.':
        return current_directory
    
    if target.startswith('root/'):
        if not in_dict(vfs, target):
            print("Введен неверный путь.")
            return current_directory
        return target
    
    # Handle parent directory cases first
    if target == '..':
        components = current_directory.rstrip('/').split('/')
        if len(components) <= 1:
            print("Неверная команда.")
            return current_directory
        components.pop()
        new_path = '/'.join(components) if components else 'root'
        return new_path + '/' if new_path == 'root' else new_path
    
    if target.startswith('../'):
        components = current_directory.rstrip('/').split('/')
        if len(components) <= 1:
            print("Неверная команда.")
            return current_directory
        remaining_path = target[3:]
        components.pop()
        
        if remaining_path:
            remaining_components = remaining_path.split('/')
            for comp in remaining_components:
                if comp == '..':
                    if components:
                        components.pop()
                elif comp != '.' and comp != '':
                    components.append(comp)
        
        new_path = '/'.join(components) if components else 'root'
        new_path = new_path + '/' if new_path == 'root' else new_path

        if not in_dict(vfs, new_path):
            print("Введен неверный путь.")
            return current_directory
        
        return new_path
    
    if target.startswith('/'):
        # Absolute path
        base_components = ['root']
        target_path = target[1:]
    else:
        # Relative path
        base_components = current_directory.rstrip('/').split('/')
        target_path = target
    
    components = target_path.split('/')
    for component in components:
        if component == '' or component == '.':
            continue
        elif component == '..':
            if len(base_components) > 1:  # Don't remove 'root'
                base_components.pop()
        else:
            base_components.append(component)
    
    full_dir = '/'.join(base_components)
    if full_dir == 'root':
        full_dir = 'root/'
    
    if not in_dict(vfs, full_dir):
        print("Введен неверный путь.")
        return current_directory
    
    return full_dir