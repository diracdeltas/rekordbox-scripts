# usage: python3 ableton-to-cues.py $ALS_FILENAME $REKORDBOX_XML_FILENAME
# writes output to output.xml

import xml.etree.ElementTree as ET
import sys
import gzip
from urllib.parse import unquote


def als_to_tracks(filename):
    etree = ET.parse(gzip.GzipFile(filename))
    tracks = etree.getroot().findall('./LiveSet/Tracks/AudioTrack')
    print(f'Found {len(tracks)} audio tracks')
    return tracks


def get_memcue(time):
    child = ET.Element('POSITION_MARK')
    child.set('Name', '')
    child.set('Type', '0')
    child.set('Num', '-1')
    child.set('Start', time)
    return child


def get_hotcue(time, num):
    child = ET.Element('POSITION_MARK')
    child.set('Name', '')
    child.set('Type', '0')
    child.set('Red', '40')
    child.set('Green', '226')
    child.set('Blue', '20')
    child.set('Num', str(num))
    child.set('Start', time)
    return child


# get ableton audio tracks
tracks = als_to_tracks(sys.argv[1])

# get rekordbox tracks
tree = ET.parse(sys.argv[2])
rekordbox_tracks = tree.getroot().findall('./COLLECTION/TRACK')

for track in tracks:
    filename = track.find('.//FileRef').find('./Name').get('Value')
    print('processing ' + filename)
    warp_markers = track.findall('.//WarpMarker')
    # Find the corresponding track in rekordbox
    for rekordbox_track in rekordbox_tracks:
        parts = rekordbox_track.get('Location').split('/')
        if (unquote(parts[-1]) == filename):
            # clear all existing cues
            for element in rekordbox_track.findall('./POSITION_MARK'):
                rekordbox_track.remove(element)
            # create a hotcue and mem cue for each warp marker
            num = 0
            for marker in warp_markers:
                time = marker.get('SecTime')
                hotcue = get_hotcue(time, num)
                memcue = get_memcue(time)
                num = num + 1
                rekordbox_track.append(hotcue)
                rekordbox_track.append(memcue)

tree.write('output.xml')
