# usage: python3 memory-cues-to-hotcues.py $XML_FILENAME

import xml.etree.ElementTree as ET
import sys

print('converting ' + sys.argv[1])

tree = ET.parse(sys.argv[1])
root = tree.getroot()

for track in root.findall('./COLLECTION/TRACK'):
    num = 0
    for position in track.findall('POSITION_MARK'):
        start = position.get('Start')
        currentNum = position.get('Num')
        newNum = str(num)
        if int(currentNum) != -1:
            # This is already a hotcue. Just renumber it.
            position.set('Num', newNum)
        else:
            # This is a memcue. Copy it to a new hotcue.
            child = ET.Element('POSITION_MARK')
            child.set('Name', '')
            child.set('Type', '0')
            child.set('Num', newNum)
            child.set('Start', start)
            track.append(child)
        num = num + 1
    print('done: ' + track.get('Name'))

tree.write('output.xml', encoding='UTF-8', xml_declaration=True)
