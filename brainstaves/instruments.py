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

def hertz(val):
    if isinstance(val, str): val = char2num(val)
    a0 = 27.5 # Pitch of the lowest note on the piano
    hz = a0 * 2**(val/12.)
    return hz

class Section(sc.prettyobj):
    def __init__(self, instrument=None, nbars=None, mindur=None):
        if instrument is None:
            instrument = 'violin'
        if nbars is None:
            nbars = 4
        if mindur is None:
            mindur = 16
        self.instrument = instrument
        self.nbars = nbars
        self.mindur = mindur
        
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
        self.arr = np.zeros(self.npts)
        return None
    
    def minmax(self):
        return char2num(self.low), char2num(self.high)
    
    def uniform(self):
        minval,maxval = self.minmax()
        for n in range(self.npts):
            self.arr[n] = np.random.randint(low=minval, high=maxval)
        return None
    
    def brownian(self, startval=None):
        minval,maxval = self.minmax()
        if startval is None:
            startval = (minval+maxval)//2
        self.arr[0] = startval
        for n in range(self.npts-1):
            current = self.arr[n]
            step = np.random.randint(-1,2)
            if (current+step) < minval or (current+step) > maxval:
                step = -step
            self.arr[n+1] = current + step
        return None


def play(insts=None, volume=1.0, tempo=120):
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
            x = np.arange(npts)
            y = np.sin(x/fs*hz*2*np.pi)
            y[:nfeather] = y[:nfeather]*featherarr
            y[-nfeather:] = y[-nfeather:]*(1-featherarr)
            data[start:finish] += y
    data = data/abs(data).max()*volume
    sd.play(data, fs, blocking=True)
    return data