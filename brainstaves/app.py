#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##################################
# Housekeeping
##################################

# Imports
print('Importing modules...')
import os
import scirisweb as sw
import brainstaves as bs

# Create the app
print('Setting defaults...')
port = 8185
app = sw.ScirisApp(__name__, name="Brainstaves", server_port=port) # Set to a nonstandard port to avoid collisions
app.data = None # Initialize the results


##################################
# Define the RPCs
##################################

@app.register_RPC()
def start():
    ''' Get new notes '''
    print('start() called')
    os.system('touch %s' % st.lockfile)
    bs.generate()
    return 'started'

@app.register_RPC()
def pause():
    return stop()

@app.register_RPC()
def stop():
    ''' Get new notes '''
    print('stop() called')
    os.system('rm %s' % st.lockfile)
    return 'stopped'

@app.register_RPC()
def get_notes():
    ''' Get new notes '''
    print('get_notes() called')
    notes = bs.get_notes()
    return notes

@app.register_RPC()
def test_notes():
    filename = '/u/cliffk/music/brainstaves/assets/mozart-test-excerpt.musicxml'
    with open(filename) as f:
        output = f.read()
    return output

@app.register_RPC()
def get_version():
    return bs.__version__


# Run the server
if __name__ == "__main__":
    app.run()