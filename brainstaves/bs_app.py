#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Webserver that runs and refreshes Brainstaves. Some functions are deprecated.
'''

# Imports
import sys
import traceback
import scirisweb as sw
import brainstaves as bs

__version__ = '2.0.0'
livedatafile = 'live/livedata.obj'
datasecs = ['A','B','C','D','E','F','G','H'] # Not A but...? WARNING, must match bs_makelivescore.py
allparts = ['v1','v2','va','vc']

def loadlivedata():
    return bs.loadlivedata(livedatafile=livedatafile)

def savelivedata(livedata):
    return bs.savelivedata(livedatafile=livedatafile, livedata=livedata)

def generate_live_score(livedata):
    if livedata.isrunning:
        print('Score is already being generated')
    else:
        if bs.allstarted(livedata):
            print('STARTING SCORE GENERATION!')
            livedata.isrunning = True
            savelivedata(livedata)
            bs.makelivescore()
        else:
            started = livedata.started[:].tolist()
            print('Not starting since only %s of %s are started' % (sum(started), len(started)))
    return None

def makeapp():
    ''' Make the Sciris app and define the RPCs '''
    
    print('Initializing live data...')
    bs.initlivedata(livedatafile=livedatafile, datasecs=datasecs, allparts=allparts, overwrite=True)

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
        livedata = loadlivedata()
        if livedata is None: output = 'n/a'
        else:                output = livedata.sec
        return output

    @app.register_RPC()
    def get_version():
        return __version__

    @app.register_RPC()
    def start(thisinst):
        print('Handling start...')
        try:
            livedata = loadlivedata()
            livedata.started[thisinst] = True
            savelivedata(livedata)
            status = bs.checkstatus('started', livedata)
            output = '  Started %s; status: %s' % (thisinst, status)
            print(output)
            generate_live_score(livedata)
        except:
            exception = traceback.format_exc() # Grab the trackback stack
            output = 'START WARNING!!!!! Something went wrong: %s' % exception
            print(output)
        return output
    
    @app.register_RPC()
    def stop(thisinst):
        print('Handling stop...')
        try:
            livedata = loadlivedata()
            livedata.started[thisinst] = False
            livedata.isrunning = False
            savelivedata(livedata)
            status = bs.checkstatus('started', livedata)
            output = '  Stopped %s; status: %s' % (thisinst, status)
            print(output)
        except Exception:
            exception = traceback.format_exc() # Grab the trackback stack
            output = 'STOP WARNING!!!!! Something went wrong: %s' % exception
            print(output)
        return output
    
    @app.register_RPC()
    def updatepage(thisinst, thispage):
        print('Handling update page...')
        try:
            livedata = loadlivedata()
            livedata.pages[thisinst] = thispage
            savelivedata(livedata)
            status = bs.checkstatus('pages', livedata)
            output = '  Changed %s -> %s; status: %s' % (thisinst, thispage, status)
            print(output)
        except Exception:
            exception = traceback.format_exc() # Grab the trackback stack
            output = 'UPDATE PAGE WARNING!!!!! Something went wrong: %s' % exception
            print(output)
        return output
    
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
        print(str(E))
        print('Shutting down server and removing status file and live files...')
#    finally:
#        sc.runcommand('rm %s live/live-*.png' % livedatafile) # rm status.tmp live/live-*.png
        
        