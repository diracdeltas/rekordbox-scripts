# usage: python3 hotcues-to-memory-cues.py $XML_FILENAME

import xml.etree.ElementTree as ET
import sys

print('converting ' + sys.argv[1])

tree = ET.parse(sys.argv[1])
root = tree.getroot()

for track in root.findall('./COLLECTION/TRACK'):
    for position in track.findall('POSITION_MARK'):
        child = ET.Element('POSITION_MARK')
        child.set('Name', '')
        child.set('Type', '0')
        child.set('Num', '-1')
        child.set('Start', position.get('Start'))
        track.append(child)

tree.write('output.xml')
