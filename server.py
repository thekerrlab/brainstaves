#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##################################
# Housekeeping
##################################

# Imports
print('Importing modules...')
import os
import scirisweb as sw
import stochastic as st

# Create the app
print('Setting defaults...')
__version__ = '0.1.0'
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
    st.generate()
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
    notes = st.get_notes()
    return notes

# Get the version
@app.register_RPC()
def get_version():
    return __version__


# Run the server
if __name__ == "__main__":
    app.run()