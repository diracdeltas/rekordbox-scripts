# rekordbox scripts

a collection of scripts to help organize and prep music collections in
rekordbox.

## demo/tutorial

click below for a video walkthrough of me using the most complicated script in this repo to convert all the warp markers in an ableton DJ set to cue points in rekordbox (both memory and hot cues).

[![demo](https://img.youtube.com/vi/pKQNfJXWcD0/0.jpg)](https://www.youtube.com/watch?v=pKQNfJXWcD0)

## prereqs

* [rekordbox](https://rekordbox.com/en/): i use version 5.6 on mac (free edition)
* [python3](https://www.python.org/downloads/)

## usage

### exporting your rekordbox collection as XML

in Rekordbox select `File` and then `Export Collection in xml format`.

### running

unless otherwise specified, run `python3 <script> <path_to_exported_XML>` where `<script>` is the script you
want to run and `<path_to_exported_XML>` is the path to the exported Rekordbox
XML. for instance `python3 hotcues-to-memory-cues.py ~/Rekordbox.xml`.

#### scripts

scripts marked with `[M]` will modify your collection by creating a new XML
file, `output.xml`, which you can then import back into rekordbox (see
instructions in next section).

* `hotcues-to-memory-cues.py [M]`: replicates all hot cues as memory cues. it
  does not delete any existing hot cues or memory cues.
* `show-low-bitrate.py`: shows tracks with less than a given bitrate; default
  is 320kbps. note that vbr encoded tracks may show a bitrate of 0.
  the bitrate is configurable;
  for instance you can run `python3 show-low-bitrate.py input.xml 256` to set
  the threshold to 256kbps.
* `show-dups.py`: shows tracks with the same title
* `show-non-mp3.py`: shows tracks that are not mp3
* `ableton-to-cues.py [M]`: takes warp markers from an ALS file and converts them
  into hotcues and memcues in rekordbox. this script must be called with the
  ableton file as the first argument; for instance `python3 ableton-to-cues.py
  myset.als ~/Rekordbox.xml`. use the `--reverse true` option to instead
  convert Rekordbox cues to Ableton warp markers.

### importing the modified collection back into Rekordbox

1. in rekordbox, choose `Preferences`, `Advanced` and then `Database`.
2. click on the `Browse` button, find output.xml and click open.
3. choose `Preferences`, `View`, and then check `rekordbox xml` in `Layout`.
4. rekordbox xml appears in your browser window. expand and click `All Tracks`
5. select the track(s) that you want to import and right click and select `Import to Collection`.

## related tools

https://github.com/rougetimelord/keypad by
[@\_caffeinu](https://twitter.com/_caffeinu) 0-pads Camelot keys so that CDJs
sort by key correctly.

## support

if you encounter a bug or have a feature request, open an
[issue](https://github.com/diracdeltas/rekordbox-scripts/issues) or DM me on
[soundcloud](https://soundcloud.com/azuki)
/ [twitter](https://twitter.com/bcrypt).
