#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Webserver that runs and refreshes Brainstaves. Some functions are deprecated.
'''


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

__all__ = ['start', 'pause', 'stop', 'get_notes', 'test_notes', 'get_version']

@app.register_RPC()
def start():
    ''' Get new notes '''
    print('start() called')
    os.system('touch %s' % bs.lockfile)
    print('NOT GENERATING')
#    bs.generate()
    output = test_notes()
    return output

@app.register_RPC()
def pause():
    return stop()

@app.register_RPC()
def stop():
    ''' Get new notes '''
    print('stop() called')
    os.system('rm %s' % bs.lockfile)
    return 'stopped'

@app.register_RPC()
def get_notes():
    ''' Get new notes '''
    print('get_notes() called')
    notes = bs.get_notes()
    return notes

@app.register_RPC()
def test_notes():
    filename = '/u/cliffk/music/brainstaves/brainstaves/assets/mozart-test-excerpt.musicxml'
    with open(filename) as f:
        output = f.read()
    return output

@app.register_RPC()
def get_version():
    return bs.__version__


# Run the server
if __name__ == "__main__":
    app.run()