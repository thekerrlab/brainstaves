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

def num2char(val, which='sharps'):
    if isinstance(val, str):
        return val
    if np.isnan(val):
        return '---'
    octave = val//12
    num = val % 12
    mapping = dict()
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
        return 'r16' # WARNING TEMP
    letter = ch[0]
    if   ch[1]=='#': acci = 'is'
    elif ch[1]=='$': acci = 'es'
    else:            acci = ''
    octint = int(ch[2]) - 2
    if   octint > 0: octchar = "'"*octint
    elif octint < 0: octchar = ","*-octint
    else:            octchar = ''
    lily = letter + acci + octchar + '16' # WARNING TEMP
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
    def __init__(self, name=None, instrument=None, nbars=None, mindur=None, seed=None):
        if name is None:
            name = 'v'
        if instrument is None:
            instrument = 'violin'
        if nbars is None:
            nbars = 4
        if mindur is None:
            mindur = 16
        self.name = name
        self.instrument = instrument
        self.nbars = nbars
        self.mindur = mindur
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
        
        self.npts = nbars*self.mindur
        self.arr = np.nan+np.zeros(self.npts)
        return None
    
    def minmax(self):
        return char2num(self.low), char2num(self.high)
    
    def uniform(self):
        if self.seed:
            pl.seed(self.seed)
        minval,maxval = self.minmax()
        for n in range(self.npts):
            self.arr[n] = np.random.randint(low=minval, high=maxval)
        return None
    
    def brownian(self, startval=None, maxstep=None):
        if self.seed:
            pl.seed(self.seed)
        if maxstep is None: maxstep = 1
        minval,maxval = self.minmax()
        if startval is None:
            startval = (minval+maxval)//2
        self.arr[0] = startval
        for n in range(self.npts-1):
            current = self.arr[n]
            if maxstep == 1:
                step = np.random.randint(-1,2)
            else:
                step = int(round(np.random.randn()*maxstep))
            if (current+step) < minval or (current+step) > maxval:
                step = -step
            self.arr[n+1] = current + step
        return None
    
    def addrests(self, p=0.5):
        if self.seed:
            pl.seed(self.seed)
        randvals = pl.rand(self.npts)
        addrests = randvals>p
        self.arr[addrests] = np.nan
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
        


def play(insts=None, volume=1.0, tempo=104, blocking=False):
    fs = 44100
    feather = 0.1
    insts = sc.promotetolist(insts)
    perbar = 60*4/tempo
    pernote = perbar/insts[0].mindur
    npts = int(pernote*fs)
    nfeather = int(npts*feather)
    featherarr = np.linspace(0,1,nfeather)
    data = np.zeros(npts*insts[0].npts)
    for inst in insts:
        for n in range(inst.npts):
            start = n*npts
            finish = start+npts
            hz = hertz(inst.arr[n])
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
        x = np.arange(inst.npts)
        pl.plot(x, inst.arr, lw=3)
        pl.scatter(x, inst.arr, s=200, label=inst.instrument)
        mi,ma = inst.minmax()
        for z in np.arange(mi,ma+1):
            pl.plot([0,inst.npts-1],[z,z], c=0.8*np.ones(3), zorder=-100, lw=2)
    pl.legend()
    pl.show()
    pl.pause(0.1)
    return fig
    

def write(insts=None, folder=None, infile=None, outfile=None, aspng=True):
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
                for note in inst.arr:
                    lilynotes.append(num2lily(note))
                lines[l] = ' '.join(lilynotes) + '\n'
    output = ''.join(lines)
    with open(outfilepath, 'w') as f:
        f.write(output)
    
    if aspng:
        cmd = 'cd %s; lilypond -dresolution=300 --png %s' % (folder, outfile)
        os.system(cmd)
    return output
    