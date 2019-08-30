import xml.etree.ElementTree as ET
import sys

tree = ET.parse(sys.argv[1])
root = tree.getroot()

for track in root.findall('./COLLECTION/TRACK'):
    kind = track.get('Kind')
    if kind and kind != 'MP3 File':
        print(': '.join([track.get('Name'), kind]))
