#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 14:06:19 2019

@author: cliffk
"""

import numpy as np
import sounddevice as sd

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

class Instrument(object):
    def __init__(self, which=None, nbars=None, minlen=None):
        if which is None:
            which = 'violin'
        if nbars is None:
            nbars = 16
        if minlen is None:
            minlen = 16
        self.which = which
        self.nbars = nbars
        self.minlen = minlen
        
        if which == 'violin':
            self.low = 'gn2'
            self.high = 'dn5'
        elif which == 'viola':
            self.low = 'cn2'
            self.high = 'gn3'
        elif which == 'cello':
            self.low = 'cn1'
            self.high = 'gn2'
        
        self.arr = np.zeros(nbars*minlen)