'''
Structure:
    
    data
      part [v1,v2,va,vc]
        measure [0,1,2,3,4, ...]
          note [0,1,2, ...]
            pitch
            alter
            accidental
        [measure][note][pitch][accidental]

'''

import os
import sciris as sc

instnames = ['v1','v2','va','vc']
ninsts = len(instnames)

class XML(sc.prettyobj):
    
    def __init__(self, folder=None, infile=None):
        if folder is None:
            folder = 'live'
        if infile is None:
            infile = 'live.xml'
        infilepath = os.path.join(folder,infile)
        self.lines = open(infilepath).readlines()
        self.nlines = len(self.lines)
        self.parts = self.partlines()
        self.measures = self.measurelines()
        return None
    
    def rangepart(self, name):
        start,stop = self.parts[name]
        return range(start, stop)
        
    def partlines(self):
        parts = sc.odict()
        for n,name in enumerate(instnames):
            ind = self.lines.index('  <part id="P%i">\n' % (n+1))
            parts[name] = [ind]
        for n,name in enumerate(instnames):
            if n<ninsts-1:
                parts[n].append(parts[n+1][0])
            else:
                parts[n].append(self.nlines)
        return parts
    
    def measurelines(lines, measure=None):
        measures = sc.odict()
        measurestr = '<measure number="%i"' % measure
        for n,name in enumerate(instnames):
            for l in rangepart(name):
                if 
            

xml = XML()

print('Done.')