#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Webserver that runs and refreshes Brainstaves. Some functions are deprecated.
'''


##################################
# Housekeeping
##################################

__version__ = '2.0.0'

# Imports
print('Importing modules...')
import sys
import scirisweb as sw
import sciris as sc

secpages = sc.odict([
        ('A',[1]),
        ('B',[2,3]),
        ('C',[4,5]),
        ('D',[6,7]),
        ('E',[8]),
        ('F',[9,10,11]),
        ('G',[12,13]),
        ('H',[14,15]),
        ])

# Create the app
print('Setting defaults...')
if len(sys.argv)>1: port = sys.argv[1]
else:               port = 8185
app = sw.ScirisApp(__name__, name="Brainstaves", server_port=port) # Set to a nonstandard port to avoid collisions
app.data = None # Initialize the results


##################################
# Define the RPCs
##################################

@app.register_RPC()
def get_status():
    filename = 'status.tmp'
    with open(filename) as f:
        output = f.read().rstrip()
    return output


@app.register_RPC()
def get_version():
    return __version__


# Run the server
if __name__ == "__main__":
    app.run()