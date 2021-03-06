'''
Class for reading and writing the uncompressed MuseScore .mscx XML files.

Structure:
    
    data
      part [v1,v2,va,vc]
        measure [0,1,2,3,4, ...]
          note [0,1,2, ...]
            pitch
            tpc
            accidental (may be missing)
            tie (may be missing)

Version: 2019may24
'''

import sciris as sc

mscorecmd = 'mscore' # Set the command used to call MuseScore
correctversion = 'MuseScore2 2.1.0'
die = False # Running as root, might get XDG_RUNTIME_DIR not set, can safely ignore

try:
    mscoreversion = sc.runcommand('%s --version' % mscorecmd).lstrip().rstrip()
    assert mscoreversion == correctversion
except Exception as E:
    errormsg = 'Warning: could not run MuseScore or incorrect version, proceed at your own risk! (%s vs. %s; %s)' % (correctversion, mscoreversion, str(E))
    if die: raise Exception(errormsg)
    else:   print(errormsg)


def commentline(line):
    output = '<!-- ' + line[:-1] + ' -->\n'
    return output

class XML(sc.prettyobj):
    
    def __init__(self, infile=None, instnames=None):
        if infile is None:
            infile = 'score/brainstaves.mscx'
        if instnames is None:
            instnames = ['v1','v2','va','vc']
        self.infile = infile
        self.instnames = instnames
        self.load()
        self.parse()
        return None
    
    def load(self):
        print('Loading %s...' % self.infile)
        self.lines = open(self.infile).readlines()
        self.nlines = len(self.lines)
        return None
    
    def parse(self):
        noteattrs = ['pitch', 'tpc', 'accidental', 'tie']
        self.data = sc.objdict()
        partcount = -1
        for l,line in enumerate(self.lines):
            if '<staff id=' in line.lower():
                if '<part>' not in self.lines[l-1].lower():
                    partcount += 1
                    measurecount = -1
                    pname = self.instnames[partcount]
                    self.data[pname] = sc.objdict()
                    self.data[pname]['n'] = l
            if '<measure number=' in line.lower():
                measurecount += 1
                notecount = -1
                mname = 'm%i' % measurecount
                self.data[pname][mname] = sc.objdict()
                self.data[pname][mname]['n'] = l
            if '<note' in line.lower():
                notecount += 1
                nname = 'n%i' % notecount
                self.data[pname][mname][nname] = sc.objdict()
                self.data[pname][mname][nname]['n'] = l
                for attr in noteattrs:
                    self.data[pname][mname][nname][attr] = sc.objdict()
                    self.data[pname][mname][nname][attr]['val'] = None
                    self.data[pname][mname][nname][attr]['n'] = None
            for attr in noteattrs:
                if '<%s' % attr in line.lower():
                    self.data[pname][mname][nname][attr]['val'] = line
                    self.data[pname][mname][nname][attr]['n'] = l
    
    def write(self, data=None, outfile=None, verbose=False):
        accisremoved = 0
        lines = sc.dcp(self.lines) # Don't edit the original
        if outfile is None:
            outfile = 'live/live.mscx'
        if verbose: print('Working on %s notes...' % len(data))
        for ind,newnote in enumerate(data):
            orignote = self.data[newnote.pname][newnote.mname][newnote.nname]
            if orignote.accidental.n is not None: # Remove accidental
                count = -1
                insideblock = True
                while insideblock:
                    count += 1
                    accisremoved += 1
                    l = orignote.accidental.n+count
                    if '</accidental>' in lines[l].lower():
                        insideblock = False
                    lines[l] = commentline(lines[l])
            for attr in ['pitch', 'tpc']:
                val = newnote[attr]
                lineno = orignote[attr].n
                if lineno:
                    lines[lineno] = f'<{attr}>{val}</{attr}>\n'
                else:
                    errormsg = 'Not sure why no line number for\n%s' % orignote
                    raise Exception(errormsg)
            if verbose: print('%s. line %s: %s' % (ind, orignote.n, newnote.pitch))
        
        for l,line in enumerate(lines):
            if 'copyright' in line.lower():
                lines[l] = '<metaTag name="copyright">Last generated: %s</metaTag>' % sc.getdate()
            elif 'stemdirection' in line.lower():
                lines[l] = commentline(lines[l])
                
        print('Writing %s notes, %s lines, removing %s accidentals' % (len(data), len(lines), accisremoved))
        output = ''.join(lines)
        with open(outfile, 'w') as f:
            f.write(output)
        
        return output
    
    def loadnotes(self, part=None, measurerange=None, verbose=False):
        notes = []
        assert len(measurerange)==2
        measures = list(range(measurerange[0]-1, measurerange[1]))
        for measure in measures:
            mname = 'm%i' % measure
            thismeasure = self.data[part][mname]
            for key,note in thismeasure.items():
                if key != 'n': # Skip the measure note counter
                    orignote = sc.objdict()
                    orignote['measure'] = measure
                    orignote['mname'] = mname
                    orignote['part'] = part
                    orignote['nname'] = key
                    orignote['pitch'] = note.pitch
                    orignote['tpc'] = note.tpc
                    orignote['tie'] = note.tie
                    notes.append(orignote)
            if verbose: print(thismeasure)
        return notes