'''
Structure:
    
    data
      part [v1,v2,va,vc]
        measure [0,1,2,3,4, ...]
          note [0,1,2, ...]
            pitch
            step
            octave
            alter (may be missing)
            accidental (may be missing)
'''

import os
import sciris as sc

class XML(sc.prettyobj):
    
    def __init__(self, folder=None, infile=None, instnames=None):
        if folder is None:
            folder = 'live'
        if infile is None:
            infile = 'live.xml'
        if instnames is None:
            instnames = ['v1','v2','va','vc']
        self.folder = folder
        self.infile = infile
        self.load()
        self.parse()
        return None
    
    def load(self):
        infilepath = os.path.join(self.folder,self.infile)
        self.lines = open(infilepath).readlines()
        self.nlines = len(self.lines)
        return None
    
    def parse(self):
        noteattrs = ['pitch', 'step', 'octave', 'alter', 'accidental']
        self.data = sc.objdict()
        partcount = -1
        for l,line in enumerate(self.lines):
            if '<part id=' in line:
                partcount += 1
                measurecount = -1
                pname = instnames[partcount]
                self.data[pname] = sc.objdict()
                self.data[pname]['n'] = l
            if '<measure number=' in line:
                measurecount += 1
                notecount = -1
                mname = 'm%i' % measurecount
                self.data[pname][mname] = sc.objdict()
                self.data[pname][mname]['n'] = l
            if '<note' in line:
                notecount += 1
                nname = 'n%i' % notecount
                self.data[pname][mname][nname] = sc.objdict()
                self.data[pname][mname][nname]['n'] = l
                for attr in noteattrs:
                    self.data[pname][mname][nname][attr] = sc.objdict()
                    self.data[pname][mname][nname][attr]['val'] = None
                    self.data[pname][mname][nname][attr]['n'] = None
            for attr in noteattrs:
                if '<%s' % attr in line:
                    self.data[pname][mname][nname][attr]['val'] = line
                    self.data[pname][mname][nname][attr]['n'] = l