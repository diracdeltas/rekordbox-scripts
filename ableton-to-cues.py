# usage: python3 ableton-to-cues.py $ALS_FILENAME $REKORDBOX_XML_FILENAME
# converts ableton warp markers to rekordbox cue points.
# use '--reverse' to convert rekordbox cues to ableton warp markers instead
# writes output to output.xml if converting ableton to rekordbox
# in reverse mode, it writes to output.als

import xml.etree.ElementTree as ET
import gzip
from urllib.parse import unquote
import argparse

parser = argparse.ArgumentParser(
        description='convert between cues and warp markers')
parser.add_argument(
        'als_file', type=str, help='path to ALS file')
parser.add_argument(
        'rekordbox_file', type=str, help='path to Rekordbox xml file')
parser.add_argument(
        '--reverse', type=bool, default=False,
        help='set to true to convert Rekordbox to Ableton')
args = parser.parse_args()


def normalize_time(time):
    if time == "0":
        return "0.001"
    else:
        return "{0:.3f}".format(float(time))


def get_memcue(time):
    child = ET.Element('POSITION_MARK')
    child.set('Name', '')
    child.set('Type', '0')
    child.set('Num', '-1')
    child.set('Start', normalize_time(time))
    return child


def get_hotcue(time, num):
    child = ET.Element('POSITION_MARK')
    child.set('Name', '')
    child.set('Type', '0')
    child.set('Red', '40')
    child.set('Green', '226')
    child.set('Blue', '20')
    child.set('Num', str(num))
    child.set('Start', normalize_time(time))
    return child


def get_warp_marker(time, num, bpm):
    child = ET.Element('WarpMarker')
    child.set('Id', str(num))
    child.set('SecTime', time)
    beat_time = float(time) * bpm / 60
    child.set('BeatTime', str(beat_time))
    return child


def get_rekordbox_filename(track):
    parts = rekordbox_track.get('Location').split('/')
    return unquote(parts[-1])


def get_ableton_filename(track):
    return track.find('.//FileRef').find('./Name').get('Value')


# get ableton audio tracks
tree = ET.parse(gzip.GzipFile(args.als_file))
tracks = tree.getroot().findall('.//AudioClip')

# get rekordbox tracks
rekordbox_tree = ET.parse(args.rekordbox_file)
rekordbox_tracks = rekordbox_tree.getroot().findall('./COLLECTION/TRACK')

if not args.reverse:
    outfile = 'output.xml'
    print('Converting Ableton warp markers to Rekordbox cues.')
    for track in tracks:
        filename = get_ableton_filename(track)
        warp_markers = track.findall('.//WarpMarker')
        # Find the corresponding track in rekordbox
        for rekordbox_track in rekordbox_tracks:
            if (get_rekordbox_filename(rekordbox_track) == filename):
                print('processing ' + filename)
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
    rekordbox_tree.write(outfile, encoding='UTF-8', xml_declaration=True)
else:
    outfile = 'output.als'
    print('Converting Rekordbox cues to Ableton warp markers.')
    for rekordbox_track in rekordbox_tracks:
        filename = get_rekordbox_filename(rekordbox_track)
        # find the corresponding ableton track
        for track in tracks:
            if (get_ableton_filename(track) == filename):
                print('processing ' + filename)
                # clear all existing warp markers
                for markers in track.findall('./WarpMarkers'):
                    track.remove(markers)
                # create new <WarpMarkers> group
                child = ET.Element('WarpMarkers')
                # ableton warp marker IDs seem to start at 2??
                num = 2
                # get rekordbox bpm
                bpm = float(rekordbox_track.find('./TEMPO').get('Bpm'))
                time = None
                for element in rekordbox_track.findall('./POSITION_MARK'):
                    time = element.get('Start')
                    marker = get_warp_marker(time, num, bpm)
                    num = num + 1
                    child.append(marker)
                # append the last marker a 2nd time; for some reason this seems
                # needed otherwise it doesn't show up in ableton.
                if time:
                    marker = get_warp_marker(str(float(time) + 0.1), num, bpm)
                    child.append(marker)
                # attach the new WarpMarkers group
                track.append(child)
    tree.write(outfile, encoding='UTF-8', xml_declaration=True)

print('Finished writing ' + outfile)
