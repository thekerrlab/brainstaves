#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 12:46:15 2019

@author: cliffk
"""

import pylab as pl
import sciris as sc

infile = 'data-off.csv'

# Must match headset.py
cols = ['attention', 'blinkStrength', 'bytesAvailable', 'delta', 'highAlpha', 'highBeta', 'lowAlpha', 'lowBeta', 'lowGamma', 'meditation', 'midGamma', 'packetsReceived', 'poorSignal', 'rawValue', 'theta']
keepcols = ['delta', 'theta', 'lowAlpha', 'highAlpha', 'lowBeta', 'highBeta', 'lowGamma', 'midGamma', 'rawValue'] # , 'poorSignal'


data = []
lines = open(infile).readlines()
for line in lines:
    data.append([float(v) for v in line.split(', ')])
    
data = pl.array(data)

df = sc.dataframe(cols=cols, data=data)

pl.figure(figsize=(30,16))

for c,col in enumerate(keepcols):
    pl.subplot(3,3,c+1)
    pl.plot(df[col])
    pl.title(col)

print('Done.')