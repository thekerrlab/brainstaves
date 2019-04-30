'''
The crux of Brainstaves -- Python representation of the different instrumental
parts.
'''

import re
import os
import numpy as np
import pylab as pl
import sounddevice as sd
import sciris as sc

def char2num(val):
    if sc.isnumber(val):
        return val
    if val == '---':
        return np.nan
    assert len(val)==3
    assert type(val)==str
    
    octave = val[2]
    note = val[0:2]
    mapping = {'cn':0,
               'c#':1,
               'd$':1,
               'dn':2,
               'd#':3,
               'e$':3,
               'en':4,
               'fn':5,
               'f#':6,
               'g$':6,
               'gn':7,
               'g#':8,
               'a$':8,
               'an':9,
               'a#':10,
               'b$':10,
               'bn':11,}
    output = 12*int(octave) + mapping[note]
    return output

def num2char(val, which='human'):
    if isinstance(val, str):
        return val
    if not val>=0:
        return '---'
    octave = val//12
    num = val % 12
    mapping = dict()
    mapping['human'] = {
            0:'cn',
            1:'d$',
            2:'dn',
            3:'e$',
            4:'en',
            5:'fn',
            6:'f#',
            7:'gn',
            8:'g#',
            9:'an',
            10:'b$',
            11:'bn',}
    mapping['sharps'] = {
            0:'cn',
            1:'c#',
            2:'dn',
            3:'d#',
            4:'en',
            5:'fn',
            6:'f#',
            7:'gn',
            8:'g#',
            9:'an',
            10:'a#',
            11:'bn',}
    mapping['flats'] = {
            0:'cn',
            1:'d$',
            2:'dn',
            3:'e$',
            4:'en',
            5:'fn',
            6:'g$',
            7:'gn',
            8:'a$',
            9:'an',
            10:'b$',
            11:'bn',}
    output = mapping[which][num] + '%i'%octave
    return output


def num2lily(num):
    ch = num2char(num)
    if ch == '---':
        return 'r'
    letter = ch[0]
    if   ch[1]=='#': acci = 'is'
    elif ch[1]=='$': acci = 'es'
    else:            acci = ''
    octint = int(ch[2]) - 2
    if   octint > 0: octchar = "'"*octint
    elif octint < 0: octchar = ","*-octint
    else:            octchar = ''
    lily = letter + acci + octchar
    return lily


def char2dia(val):
    acci = val[1]
    if acci in ['#', '$']:
        output = val[0]+'n'+val[2]
    else:
        output = val
    return output


def char2octo(val):
    note = val[0:2]
    mapping = {'a#':'b$',
               'bn':'b$',
               'd$':'cn',
               'dn':'c#',
               'd#':'e$',
               'fn':'en',
               'g$':'f#',
               'g#':'gn',
               'a$':'gn'}
    if note in mapping: output = mapping[note]+val[2]
    else:               output = val
    return output

def hertz(val):
    val = char2num(val)
    a0 = 27.5 # Pitch of the lowest note on the piano
    hz = a0 * 2**(val/12.)
    return hz

class Section(sc.prettyobj):
    def __init__(self, name=None, instrument=None, nbars=None, mindur=None, timesig=None, seed=None):
        if name       is None: name = 'v'
        if instrument is None: instrument = 'violin'
        if nbars      is None: nbars = 4
        if mindur     is None: mindur = 8
        if timesig    is None: timesig = '4/4'
        if seed       is None: seed = np.nan
        self.name = name
        self.instrument = instrument
        self.nbars = nbars
        self.mindur = mindur
        self.timesig = timesig
        self.seed = seed
        
        if instrument == 'violin':
            self.low = 'gn2'
            self.high = 'dn5'
        elif instrument == 'viola':
            self.low = 'cn2'
            self.high = 'gn4'
        elif instrument == 'cello':
            self.low = 'cn1'
            self.high = 'gn3'
        
        self.refresh()
        return None
    
    def refresh(self):
        tsig = [int(q) for q in self.timesig.split('/')]
        wholenotes = tsig[0]/tsig[1]
        self.npts = int(round(self.nbars*wholenotes*self.mindur))
        self.arr = np.nan+np.zeros(self.npts)
        self.score = np.zeros(0)
        return None
        
    @property
    def scorepts(self):
        return len(self.score)
    
    def resetseed(self, seed=None):
        if seed is None: # Use supplied seed by default, otherwise use default
            seed = self.seed
        if seed and not np.isnan(seed):
            pl.seed(seed)
        return None
        
    def cat(self):
        self.score = np.concatenate([self.score, self.arr])
        return None
    
    def minmax(self):
        return char2num(self.low), char2num(self.high)
    
    def uniform(self, seed=None):
        self.resetseed(seed)
        minval,maxval = self.minmax()
        for n in range(self.npts):
            self.arr[n] = np.random.randint(low=minval, high=maxval)
        return None
    
    def brownian(self, startval=None, maxstep=None, seed=None, forcestep=True, skipstart=True, verbose=False, inst=None):
        self.resetseed(seed)
        if maxstep is None: maxstep = 1
        minval,maxval = self.minmax()
        if   startval is None:  startval = (minval+maxval)//2
        elif startval == 'min': startval = minval
        elif startval == 'max': startval = maxval
        if not skipstart:
            self.arr[0] = startval
        
        npts = self.npts-1+skipstart
        data = getnumbers(inst, 2*npts)
        for n in range(npts): # If not skipping the start, 1 less point
            if n==0: current = abs(startval)
            else:    current = abs(self.arr[n-1])
            step = 0
            count = 0
            while forcestep and not step:
                count += 1
                if count<10:
                    step = int(round((data[n])*maxstep))
                    if verbose: print('Using step %s (%s)' % (step, data[n]))
                else:
                    if maxstep == 1: step = np.random.randint(-1,2)
                    else:            step = int(round(np.random.randn()*maxstep)) # REPLACE WITH EEG
            if (current+step) < minval or (current+step) > maxval: # Bounce off the ends
                step = -step
            
            proposed = current + step
            if proposed < minval:
                print('Warning, note tried to go too low (%s vs. %s), resetting' % (proposed, minval))
                proposed = minval
            if proposed > maxval:
                print('Warning, note tried to go too high (%s vs. %s), resetting' % (proposed, maxval))
                proposed = maxval
            self.arr[n+1-skipstart] = proposed
            if verbose:
                print(f'n={n}, current={current}, step={step}, proposed={proposed}')
                    
        return None
    
    def addrests(self, p=0.5, seed=None):
        self.resetseed(seed)
        randvals = pl.rand(self.npts)
        addrests = randvals>p
        self.arr[addrests] = -self.arr[addrests] # Set to negative to keep pitch information
        return None
    
    def diatonic(self):
        for n in range(self.npts):
            val = num2char(self.arr[n])
            self.arr[n] = char2num(char2dia(val))
        return None
    
    def octotonic(self):
        for n in range(self.npts):
            val = num2char(self.arr[n])
            self.arr[n] = char2num(char2octo(val))
        return None
        

def getnumbers(inst, npts, window=10):
    if inst is None:
        print('Not using EEG')
        return np.random.rand(npts)
    infile = 'live/data-'+inst+'.csv'
    string = open(infile).read()
    numbers = re.sub("[^0-9]", "", string)
    rev = numbers[::-1]
    try:
        rev = rev[:npts*window]
        raw = [float(r)/10. for r in rev] # Will be uniform
        data = np.zeros(npts)
        for pt in range(npts):
            data[pt] = sum(raw[pt*window:(pt+1)*window])-window/2.
    except Exception as E:
        print('Problem: %s' % str(E))
        data = np.random.rand(npts)
    return data


def play(insts=None, volume=1.0, tempo=104, blocking=False):
    fs = 44100
    feather = 0.1
    insts = sc.promotetolist(insts)
    perbar = 60*4/tempo
    pernote = perbar/insts[0].mindur
    npts = int(pernote*fs)
    nfeather = int(npts*feather)
    featherarr = np.linspace(0,1,nfeather)
    data = np.zeros(npts*insts[0].scorepts)
    for inst in insts:
        for n in range(len(inst.score)):
            start = n*npts
            finish = start+npts
            hz = hertz(inst.score[n])
            if hz>0: # nan used to represent rests
                x = np.arange(npts)
                y = np.sin(x/fs*hz*2*np.pi)
                y[:nfeather] = y[:nfeather]*featherarr
                y[-nfeather:] = y[-nfeather:]*(1-featherarr)
                data[start:finish] += y
    data = data/abs(data).max()*volume
    sd.play(data, fs, blocking=blocking)
    return data


def plot(insts=None):
    fig = pl.figure()
    for inst in insts:
        x = np.arange(inst.scorepts)
        plotscore = sc.dcp(inst.score)
        plotscore[plotscore<0] = np.nan # Remove "rests"
        pl.plot(x, plotscore, lw=3)
        pl.scatter(x, plotscore, s=200, label=inst.instrument)
        mi,ma = inst.minmax()
        for z in np.arange(mi,ma+1):
            pl.plot([0,inst.scorepts-1],[z,z], c=0.8*np.ones(3), zorder=-100, lw=2)
    pl.legend()
    pl.show()
    pl.pause(0.1)
    return fig
    

def write(insts=None, folder=None, infile=None, outfile=None, export='png'):
    insts = sc.promotetolist(insts)
    if folder is None:
        folder = 'live'
    if infile is None:
        infile = 'brainstaves.ly'
    if outfile is None:
        outfile = infile
    infilepath = os.path.join(folder,infile)
    outfilepath = os.path.join(folder,outfile)
    lines = open(infilepath).readlines()
    
    nextline = False
    for l,line in enumerate(lines):
        if line.startswith('%!!!'):
            nextline = True
            name = line[4:-1] # Skip starter and newline
        else:
            if nextline:
                nextline = False
                inst = None
                for tmp in insts:
                    if tmp.name == name:
                        inst = tmp
                if inst is None:
                    errormsg = 'Could not match name %s' % name
                    raise Exception(errormsg)
                lilynotes = []
                for note in inst.score:
                    lilynote = num2lily(note)
                    lilynote += '%s' % inst.mindur
                    lilynotes.append(lilynote)
                lines[l] = ' '.join(lilynotes) + '\n'
    output = ''.join(lines)
    with open(outfilepath, 'w') as f:
        f.write(output)
    
    if export=='png':
        cmd = 'cd %s; lilypond -dresolution=300 --png %s' % (folder, outfile)
        os.system(cmd)
    if export=='pdf':
        cmd = 'cd %s; lilypond %s' % (folder, outfile)
        os.system(cmd)
    return output
    