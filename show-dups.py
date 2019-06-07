import xml.etree.ElementTree as ET
import sys

tree = ET.parse(sys.argv[1])
root = tree.getroot()
names = {}

for track in root.findall('./COLLECTION/TRACK'):
    name = track.get('Name')
    if name in names:
        # this is a dupe
        print(name)
    else:
        names[name] = True
