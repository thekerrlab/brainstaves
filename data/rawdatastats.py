#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 23:41:34 2019

@author: cliffk
"""

import pylab as pl
import sciris as sc

infile = 'data-may08.obj'

df = sc.loadobj(infile)

raw = df['rawValue'].astype(float)

raw = raw[pl.nonzero(raw)]
raw -= raw.mean()
raw /= 0.7*raw.std()

pl.figure()
pl.plot(raw)

pl.figure()
x = pl.randn(len(raw))
bins = pl.linspace(-8,8,201)
pl.hist(raw, bins)
pl.hist(x, bins, alpha=0.8)

print('Done.')