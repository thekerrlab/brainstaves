#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 23:43:32 2019

@author: cliffk
"""

import pylab as pl
pl.rc('font', family='Arial')

import matplotlib.font_manager as mfm

font_path = 'FreeSerif.ttf'

prop = mfm.FontProperties(fname=font_path)

d = {'note':'𝅘',
     'quarter':'♩',
     'whole':'𝅝',
     'sharp':'♯',
     'flat':'♭',
     'natural':'♮',
     'treble':'𝄞',
     'alto':'𝄡',
     'bass':'𝄢',
     }

fig = pl.figure()

pl.plot([0,1,], [0,1])
pl.text(0.5, 0.5, d['note'], fontproperties=prop, fontsize=50)

print('Done.')