import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import os

class LoggerXML:
    def __init__(self, log_file = "command_log.xml", log_directory="."):
        self.log_file = log_file
        root = ET.Element("command_log")
        tree = ET.ElementTree(root)

        os.makedirs(log_directory, exist_ok=True)
        self.log_file = os.path.join(log_directory, log_file)

        self._write_xml(tree)
    
    def _write_xml(self, tree):

        rough_string = ET.tostring(tree.getroot(), 'utf-8')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")
        
        pretty_xml = os.linesep.join([s for s in pretty_xml.splitlines() if s.strip()])
        
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
    
    def log_command(self, command_name, is_command):

        tree = ET.parse(self.log_file)
        root = tree.getroot()
        
        elem = ET.SubElement(root, "command") if is_command \
            else ET.SubElement(root, "error")
        
        elem.set("name", command_name)
        elem.set("timestamp", datetime.now().isoformat())
        elem.set("error", "") if is_command \
            else elem.set("error", "Unknown command")

        self._write_xml(tree)