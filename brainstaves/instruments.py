#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 14:06:19 2019

@author: cliffk
"""

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
    mapping = {'an':0,
               'a#':1,
               'b$':1,
               'bn':2,
               'cn':3,
               'c#':4,
               'd$':4,
               'dn':5,
               'd#':6,
               'e$':6,
               'en':7,
               'fn':8,
               'f#':9,
               'g$':9,
               'gn':10,
               'g#':11,
               'a$':11}
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
            0:'an',
            1:'a#',
            2:'bn',
            3:'cn',
            4:'c#',
            5:'dn',
            6:'d#',
            7:'en',
            8:'fn',
            9:'f#',
            10:'gn',
            11:'g#',}
    mapping['flats'] = {
            0:'an',
            1:'b$',
            2:'bn',
            3:'cn',
            4:'d$',
            5:'dn',
            6:'e$',
            7:'en',
            8:'fn',
            9:'g$',
            10:'gn',
            11:'a$',}
    output = mapping[which][num] + '%i'%octave
    return output


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
    def __init__(self, instrument=None, nbars=None, mindur=None, seed=None):
        if instrument is None:
            instrument = 'violin'
        if nbars is None:
            nbars = 4
        if mindur is None:
            mindur = 16
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
        pl.plot(x, inst.arr)
        pl.scatter(x, inst.arr, s=100, label=inst.instrument)
        mi,ma = inst.minmax()
        for z in np.arange(mi,ma+1):
            pl.plot([0,inst.npts-1],[z,z], c=0.8*np.ones(3), zorder=-100)
    pl.legend()
    pl.show()
    pl.pause(0.1)
    return fig
    

def write(insts=None, infile=None, outfile=None):
    insts = sc.promotetolist(insts)
    if infile is None:
        infile = 'live/brainstaves-test-flight.xml'
    if outfile is None:
        outfile = infile
    lines = open(infile).readlines()
    
    notesfound = -1
    allnotes = []
    for inst in insts:
        allnotes.extend(list(inst.arr))
    for n,note in enumerate(allnotes):
        allnotes[n] = num2char(note)
    for l,line in enumerate(lines):
        if '<note' in line:
            notesfound += 1
            thisnote = allnotes[notesfound]
            thisletter = thisnote[0].upper()
            thisoctave = int(thisnote[2])
            if thisletter not in ['A','B']:
                thisoctave += 1
            thisoctave = str(thisoctave)
        if '<step>' in line:
            loc = line.find('>')+1
            parts = lines[l].partition(lines[l][loc])
            lines[l] = parts[0] + thisletter + parts[2]
        if '<octave>' in line:
            loc = line.find('>')+1
            parts = lines[l].partition(lines[l][loc])
            lines[l] = parts[0] + thisoctave + parts[2]
        
    output = ''.join(lines)
    with open(outfile, 'w') as f:
        f.write(output)
    
    output = ''
    return output
    