'''
The crux of Brainstaves -- Python representation of the different instrumental
parts.
'''

import re
import os
import numpy as np
import pylab as pl
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
    ''' WARNING, choices other than human might break things! '''
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


def char2dia(val):
    output = val[0]+'n'+val[2]
    return output


def char2acoustic(val):
    dia = char2dia(val)
    if   dia[0] == 'f': output = 'f#' + val[2] # Map F onto F#
    elif dia[0] == 'b': output = 'b$' + val[2] # Map B onto Bb
    else:               output = dia # Otherwise, diatonic
    return output


def char2octo(val):
    ''' WARNING, relies on the human mapping in num2char! '''
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

def char2blues(val):
    note = val[0:2]
    mapping = {
            'cn':'cn',
            'd$':'cn',
            'dn':'e$',
            'e$':'e$',
            'en':'en',
            'fn':'fn',
            'f#':'f#',
            'gn':'gn',
            'g#':'gn',
            'an':'gn',
            'b$':'b$',
            'bn':'b$',}
    if note in mapping: output = mapping[note]+val[2]
    else:               raise Exception('Note %s not found in blues scale!' % note)
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
    
    def refresh(self, npts=None, resetscore=True):
        if npts is None: # Calculate npts from bars and beats
            tsig = [int(q) for q in self.timesig.split('/')]
            wholenotes = tsig[0]/tsig[1]
            npts = int(round(self.nbars*wholenotes*self.mindur))
        self.npts = npts
        self.arr = np.nan+np.zeros(self.npts)
        self.notearr = []
        if resetscore:
            self.score = []
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
        self.score = self.score + self.notearr
        return None
    
    def minmax(self):
        return char2num(self.low), char2num(self.high)
    
    def uniform(self, seed=None):
        self.resetseed(seed)
        minval,maxval = self.minmax()
        for n in range(self.npts):
            self.arr[n] = np.random.randint(low=minval, high=maxval)
        return None
    
    def brownian(self, startval=None, maxstep=None, seed=None, forcestep=True, skipstart=True, verbose=False, usedata=True, npts=None):
        if not skipstart:
            raise Exception('Sorry, not skipstart is not working!')
        if maxstep is None: maxstep = 1
        minval,maxval = self.minmax()
        if   startval is None:  startval = (minval+maxval)//2
        elif startval == 'min': startval = minval
        elif startval == 'max': startval = maxval
        if not skipstart:
            self.arr[0] = startval
        
        if npts is not None: # Manually reset npts
            self.refresh(npts=npts, resetscore=False)
        else:
            self.notearr = [] # WARNING, could do this more elegantly!
            
        npts = self.npts-1+skipstart
        data = getnumbers(self.name, 2*npts, usedata, seed)
        for n in range(npts): # If not skipping the start, 1 less point
            if n==0: current = abs(startval)
            else:    current = abs(self.arr[n-1])
            step = np.nan
            count = 0
            if np.isnan(current):
                import traceback; traceback.print_exc(); import pdb; pdb.set_trace()
            while np.isnan(step) or (forcestep and not step):
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
        print('WARNING, may not work any more due to changing from arr to notearr!')
        self.resetseed(seed)
        randvals = pl.rand(self.npts)
        addrests = randvals>p
        self.arr[addrests] = -self.arr[addrests] # Set to negative to keep pitch information
        return None
    
    def noteify(self, tonality=None, breakties=False, verbose=False):
        if tonality is None: tonality = 'atonal'
        tonalities = sc.promotetolist(tonality)
        mapping = {'atonal': lambda note: note, # Just the identity function
                   'dia': char2dia,
                   'acoustic': char2acoustic,
                   'octo': char2octo,
                   'blues': char2blues,}
        for n in range(self.npts):
            thisnote = self.arr[n]
            
            def mapnote(thisnote):
                note = num2char(thisnote, which='human')
                for thistonality in tonalities:
                    note = mapping[thistonality](note)
                return note
            
            note = mapnote(thisnote)
            
            if len(self.notearr) and breakties: # Only start this if it's not the first note, and we're breaking ties
                lastnote = self.notearr[-1]
                tiecount = 0
                while note == lastnote: # There is a tie to be broken
                    tiecount += 1
                    thisnote += 1 # Just increment upwards
                    note = mapnote(thisnote)
                    if verbose: print('Breaking tie (try %s): (%s -> %s, %s -> %s)' % (tiecount, thisnote-1, thisnote, note, lastnote))
            self.notearr.append(note)
        
        return None
    

def getnumbers(inst, npts, usedata, seed=None, window=10):
    if seed:
        inst.resetseed(seed)
    if inst is None or not usedata:
        if usedata: print('Not using EEG because inst is None')
        return np.random.randn(npts)
    infile = 'live/data-'+inst+'.csv'
    string = open(infile).read()
    numbers = re.sub("[^0-9]", "", string)
    rev = numbers[::-1]
    try:
        rev = rev[:npts*window]
        raw = [float(r)/10. for r in rev] # Will be uniform
        data = np.zeros(npts)
        for pt in range(npts):
            thesum = sum(raw[pt*window:(pt+1)*window])
            if thesum == 0:
                print('Warning, sum was 0')
                data[pt] = np.random.randn() # Give up
            else:
                data[pt] = thesum-window/2.
    except Exception as E:
        print('Problem: %s' % str(E))
        data = np.random.rand(npts)
    return data


def play(insts=None, volume=1.0, tempo=104, blocking=False):
    import sounddevice as sd
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
    