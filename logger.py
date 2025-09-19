import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import os

class LoggerXML:
    def __init__(self, log_file = "command_log.xml"):
        self.log_file = log_file
        root = ET.Element("command_log")
        tree = ET.ElementTree(root)
        self._write_xml(tree)
    
    def _write_xml(self, tree):
        #"""Записывает XML в файл с красивым форматированием"""
        rough_string = ET.tostring(tree.getroot(), 'utf-8')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")
        
        # Убираем лишние пустые строки, которые добавляет toprettyxml
        pretty_xml = os.linesep.join([s for s in pretty_xml.splitlines() if s.strip()])
        
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
    
    def log_command(self, command_name, is_command):
        #"""Логирует выполнение команды, добавляя ее в конец файла"""
        
        # Читаем существующий XML
        
        tree = ET.parse(self.log_file)
        root = tree.getroot()
        
        
        # Создаем элемент команды с временной меткой
        
        elem = ET.SubElement(root, "command") if is_command \
            else ET.SubElement(root, "error")
        
        elem.set("name", command_name)
        elem.set("timestamp", datetime.now().isoformat())

        # Записываем обратно в файл
        self._write_xml(tree)
        
    