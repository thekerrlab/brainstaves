# B R A I N S T A V E S

Composition for string quartet and EEG headsets.

## Quick start guide

There is none.

## Slow start guide

### Overview

This repository contains a hodgepodge of different things: scores; scripts for recording and analyzing data; some sample data files; code to generate the score; and a webserver.

### Installation

`python setup.py develop`

Brainstaves is designed to work in Python 3. It may also work in Python 2. But probably not.

You will also need MuseScore (http://musescore.org/) to generate the scores.

### Testing the backend

If you run `python brainstaves/bs_makelivescore.py`, it should generate PNG files in the `brainstaves/live`.

### Running the web server

The normal usage is to run `brainstaves/run_server`. This will start serving on port 80. If you run `python brainstaves/bs_app.py`, this will start running on port 8185.

### Connecting the headsets

Start in the `brainstaves` subfolder.

1. Pair the headsets with `bt_pair`. This will connect all four headsets.

2. Connect the headsets and start reading data by opening four terminal windows and running `bt_read v1`, `bt_read v2`, `bt_read va`, `bt_read vc`.