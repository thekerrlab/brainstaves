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
    
    def __init__(self, infile=None, instnames=None):
        if infile is None:
            infile = 'brainstaves.xml'
        if instnames is None:
            instnames = ['v1','v2','va','vc']
        self.infile = infile
        self.instnames = instnames
        self.load()
        self.parse()
        return None
    
    def load(self):
        self.lines = open(self.infile).readlines()
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
                pname = self.instnames[partcount]
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
    
    def write(self, data=None, outfile=None, verbose=False):
        if outfile is None:
            outfile = 'live/live.xml'
        if verbose: print('Working on %s notes...' % len(data))
        for ind,newnote in enumerate(data):
            orignote = self.data[newnote.pname][newnote.mname][newnote.nname]
            if orignote.accidental.n is not None: # Remove accidental
                self.lines[orignote.accidental.n] = '<!-- Accidental removed -->\n'
            for attr in ['step', 'octave', 'alter']:
                val = newnote[attr]
                lineno = orignote[attr].n
                if lineno:
                    self.lines[lineno] = f'<{attr}>{val}</{attr}>\n'
                elif lineno is None and attr == 'alter':
                    step = self.lines[orignote.step.n][:-1] # Remove newline
                    self.lines[orignote.step.n] = step + f'<{attr}>{val}</{attr}>\n'
                else:
                    errormsg = 'Not sure why no line number for\n%s' % orignote
                    raise Exception(errormsg)
            if verbose: print('%s. line %s: %s %s %s' % (ind, orignote.n, newnote.step, newnote.alter, newnote.octave))
            
        output = ''.join(self.lines)
        with open(outfile, 'w') as f:
            f.write(output)
        
        return output
    
    def loadnotes(self, part=None, measurerange=None):
        notes = []
        assert len(measurerange)==2
        measures = list(range(measurerange[0]-1, measurerange[1]))
        print(measures)
        for measure in measures:
            mname = 'm%i' % measure
            thismeasure = self.data[part][mname]
            for key,note in thismeasure.items():
                if key != 'n': # Skip the counter
                    orignote = sc.objdict()
                    orignote['measure'] = measure
                    orignote['mname'] = mname
                    orignote['part'] = part
                    orignote['nname'] = key
                    notes.append(orignote)
            print(thismeasure)
        return notes