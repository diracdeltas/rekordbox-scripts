import xml.etree.ElementTree as ET
import sys

bitrate = int(sys.argv[2]) if len(sys.argv) > 2 else 320
print('tracks with bitrate less than: ' + str(bitrate))

tree = ET.parse(sys.argv[1])
root = tree.getroot()

for track in root.findall('./COLLECTION/TRACK'):
    track_bitrate = track.get('BitRate')
    if track_bitrate and int(track_bitrate) < bitrate:
        print(': '.join([track.get('Name'), track_bitrate]))
