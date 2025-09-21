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