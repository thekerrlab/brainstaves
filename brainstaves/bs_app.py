#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Webserver that runs and refreshes Brainstaves. Some functions are deprecated.
'''


def makeapp():
    ''' Make the Sciris app and define the RPCs '''

    # Imports
    print('Importing modules...')
    import sys
    import scirisweb as sw
    import sciris as sc

    __version__ = '3.0.0'
    statusfile = 'status.tmp'

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
        try:
            with open(statusfile) as f:
                output = f.read().rstrip()
        except Exception as E:
            print('Status file not found: %s' % str(E))
            output = 'n/a'
        return output


    @app.register_RPC()
    def get_version():
        return __version__

    return app



def run():
    ''' Actually run the app!!! '''
    app = makeapp()
    app.run()
    return None



# Run the server
if __name__ == "__main__":
    try: # WARNING -- this try-catch doesn't work
        run()
    except Exception as E:
        print('Shutting down server and removing status file and live files...')
        sc.runcommand('rm %s live/live-*.png' % statusfile) # rm status.tmp live/live-*.png
        raise E
        
        