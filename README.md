# B R A I N S T A V E S

Composition for string quartet and EEG headsets.

## Quick start guide

There is none.

## Slow start guide

### Overview

This repository contains a hodgepodge of different things: scores; scripts for recording and analyzing data; code to generate the score; and a webserver. The descriptions below are likely to be incomplete and out of date, even at the time of writing.

### Installation

`python setup.py develop`

Brainstaves is designed to work in Python 3. It may also work in Python 2. But probably not.

You will also need MuseScore (http://musescore.org/) to generate the scores.

### Web server usage

Pretty straightforward: `python brainstaves/bs_app.py`. This will start serving `index.html` on port 8185 (all the JavaScript stuff is in `assets`). This serves the image at `brainstaves/live/brainstaves.png`. If this does not exist, you won't see anything (if it exists and is a picture of a cat, you will, of course, see a cat).

### Score generation

The score generating machinery is defined primarily by `instruments.py`. An example of how to use it is in `test_instruments.py`. Naming is inconsistent, sorry. Note a quirk in LilyPond: if the score is more than one page, the `i.write(export='png')` command won't generate a `brainstaves.png` file (instead e.g. `brainstaves-page1.png`) and rendering will fail.

How the rendering works is:
1. A template LilyPond file (`brainstaves/brainstaves/live/brainstaves.ly`) is opened.
2. The script finds the control marker (e.g. `%!!!v1`), and substitutes the next line with the notes it's generated.
3. The resultant file is exported to PNG with the command `lilypond -dresolution=300 --png brainstaves.ly`.

### Reading and analyzing data from Bluetooth

This is hard. First, install NeuroPy (only works for Python 2):

```
git clone https://github.com/thekerrlab/neuropy.git
cd neuropy
python2 setup.py develop
```

Assuming you have 4 headsets with the following MAC addresses:

```
00:81:F9:08:A1:72
00:81:F9:29:BA:98
00:81:F9:29:EF:80
C4:64:E3:EA:75:6D
```

The procedure that works some of the time on Ubuntu 18.04 is:

1. Unpair all devices (Bluetooth menu -> Remove for each MindWave Mobile)
2. Pair devices (in same terminal):
    1. `bluetoothctl`
    2. `pair 00:81:F9:08:A1:72`
    3. `pair 00:81:F9:29:BA:98`
    4. `pair 00:81:F9:29:EF:80`
    5. `pair C4:64:E3:EA:75:6D`
3. Connect (in 4 separate terminals since blocking):
    1. `sudo rfcomm connect hci0 00:81:F9:08:A1:72` (not sure why this has to be different, but `/  dev/rfcomm0` never works)
    2. `sudo rfcomm connect /dev/rfcomm1 00:81:F9:29:BA:98`
    3. `sudo rfcomm connect /dev/rfcomm2 00:81:F9:29:EF:80`
    4. `sudo rfcomm connect /dev/rfcomm3 C4:64:E3:EA:75:6D`
4. Read (in 4 terminals, in `brainstaves/brainstaves/data`; NB, `headset.py` may require editing):
    1. `sudo python2 headset.py mandhi` (must be `sudo` to have access to `dev/rfcomm0`)
    2. `sudo python2 headset.py pat`
    3. `sudo python2 headset.py rich`
    4. `sudo python2 headset.py val`
5. Notes:
    1. Some connections will probably fail at various stages. Try random permutations of things until they work.

The data analysis script is in `brainstaves/brainstaves/data/stats.py`.