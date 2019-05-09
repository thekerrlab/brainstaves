#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Webserver that runs and refreshes Brainstaves. Some functions are deprecated.
'''

# Imports
import sys
import sciris as sc
import scirisweb as sw
import brainstaves as bs

__version__ = '2.0.0'
livedatafile = 'live/livedata.obj'
datasecs = ['A','B','C','D','E','F','G','H'] # Not A but...? WARNING, must match bs_makelivescore.py
allparts = ['v1','v2','va','vc']


def loadlivedata():
    livedata = None
    try:
        livedata = sc.loadobj(livedatafile)
    except Exception as E:
        print('Live data file file not found: %s' % str(E))
    return livedata

def savelivedata(livedata):
    sc.saveobj(livedatafile, livedata)
    return None

def checkstatus(which, livedata, fulloutput=False):
    tmp = []
    vals = []
    for key,val in getattr(livedata,which).items(): # Should've made it an objdict...
        tmp.append('%s: %s' % (key,val))
        vals.append(val)
    string = '; '.join(tmp)
    if fulloutput: return string,vals
    else:          return string

def generate_live_score(started):
    if all(started):
        print('GENERATING SCORE!')
        bs.makelivescore()
    else:
        print('Not starting since only %s of %s are started' % (sum(started), len(started)))
    return None


def makeapp():
    ''' Make the Sciris app and define the RPCs '''
    
    print('Initializing live data...')
    bs.initlivedata(livedatafile=livedatafile, datasecs=datasecs, allparts=allparts, overwrite=False)

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
            status,started = checkstatus('started', livedata, fulloutput=True)
            output = '  Started %s; status: %s' % (thisinst, status)
            print(output)
            generate_live_score(started)
        except Exception as E:
            output = 'APP WARNING!!!!! Something went wrong: %s' % str(E)
            print(output)
        return output
    
    @app.register_RPC()
    def stop(thisinst):
        print('Handling stop...')
        try:
            livedata = loadlivedata()
            livedata.started[thisinst] = False
            savelivedata(livedata)
            status = checkstatus('started', livedata)
            output = '  Stopped %s; status: %s' % (thisinst, status)
            print(output)
        except Exception as E:
            output = 'APP WARNING!!!!! Something went wrong: %s' % str(E)
            print(output)
        return output
    
    @app.register_RPC()
    def updatepage(thisinst, thispage):
        print('Handling update page...')
        try:
            livedata = loadlivedata()
            livedata.page[thisinst] = thispage
            savelivedata(livedata)
            status = checkstatus('page', livedata)
            output = '  Changed %s -> %s; status: %s' % (thisinst, thispage, status)
            print(output)
        except Exception as E:
            output = 'APP WARNING!!!!! Something went wrong: %s' % str(E)
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
    finally:
        sc.runcommand('rm %s live/live-*.png' % livedatafile) # rm status.tmp live/live-*.png
        
        