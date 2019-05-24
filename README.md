# B R A I N S T A V E S

Composition for string quartet and EEG headsets.

## Quick start guide

There is none.

## Slow start guide

### Overview

This repository contains a hodgepodge of different things: scores; scripts for recording and analyzing data; some sample data files; code to generate the score; and a webserver.

### Installation

Install the web server and analysis code, which is designed to work with Python 3: `python3 setup.py develop`

Install the Mindwave Mobile reading code, which unfortunately only works with Python 2: `python2 setup-mindwave.py develop`

You will also need MuseScore (http://musescore.org/) to generate the scores.

### Creating the score

If you run `python brainstaves/bs_makelivescore.py`, it should generate PNG files in the folder `brainstaves/live`.

#### Options

The key options to set are:

* `version`: you can choose 'A' or 'B'. Version 'A' is atonal (mostly), version 'B' uses the blues scale.

* `wait`: whether or not to wait for one section to finish before generating the next. Note, this is necessary if you're using live data!

* `datadir`, `backupdir`: this sets the folders from which the data will be read. Normal usage would be to set `datadir = ../data/live`, but you can use a backup folder if you are scared. The backup folder should contain pre-recorded data that doesn't suck, in the event that the headsets fail to record live.

* `makepdf`: pretty self explanatory, also renders a PDF version of the score along with the PNG version.


### Running the web server

The normal usage is to run `brainstaves/run_server`. This will start serving on port 80. If you run `python brainstaves/bs_app.py`, this will start running on port 8185.

### Connecting the headsets

Start in the `brainstaves` subfolder, and then:

#### Pair the headsets

Pair the headsets with `bt_pair`. This will connect all four headsets. If it works, you should see:

```
bluetoothctl pair C4:64:E3:EA:75:6D

Attempting to pair with C4:64:E3:EA:75:6D
[CHG] Device C4:64:E3:EA:75:6D Connected: yes
[CHG] Device C4:64:E3:EA:75:6D UUIDs: 00001101-0000-1000-8000-00805f9b34fb
[CHG] Device C4:64:E3:EA:75:6D ServicesResolved: yes
[CHG] Device C4:64:E3:EA:75:6D Paired: yes
Pairing successful
```

If it doesn't work, you might see:

```
Pairing 00:81:F9:29:BA:98...
bluetoothctl pair 00:81:F9:29:BA:98

Device 00:81:F9:29:BA:98 not available
```

Note: at least on Linux, if the devices are listed in the Bluetooth applet (i.e. visible in the Ubuntu GUI), you will need to "Remove device" before you can pair with them via this command-line method (`bluetoothctl`).

#### Connect the headsets to the serial port

Connect the headsets and start reading data by opening four terminal windows and running `bt_read v1`, `bt_read v2`, `bt_read va`, `bt_read vc`. You should see:

```
finzi:~/music/brainstaves/brainstaves> ./bt_read v1
Connected /dev/rfcomm0 to 00:81:F9:08:A1:72 on channel 1
Press CTRL-C for hangup
```

If it says "Disconnected", then simply reconnect. This will, unfortunately, probably happen a lot.

#### Record the data from the serial port

Open four terminal windows and run e.g. `bt_record v1`. If it worked, you should see:

```
finzi:~/music/brainstaves/brainstaves> ./bt_record v1

STARTING B v1 (1/7)
Recording for 20 s...
...1/1000
...51/1000
...101/1000
...151/1000
```

This means it is recording data for section B, violin 1 part. The folder is currently hard-coded (`../data/live`).
