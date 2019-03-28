#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate random notes
"""

import os
import pylab as pl

lockfile = 'running.tmp'
filename = 'notes.txt'

class Note:
    def __init__(self, pitch=None, duration=None, properties=None):
        self.pitch = pitch
        self.duration = duration
        self.properties = properties

def generate():
    while os.path.exists(lockfile):
        output = pl.rand(10)
        pl.savetxt(filename, output)
        pl.pause(1)
    return None

def get_notes():
    output = pl.loadtxt(filename)
    return output
