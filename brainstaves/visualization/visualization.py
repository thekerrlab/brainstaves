#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 00:39:06 2019

@author: cliffk
"""

import pylab as pl
import sciris as sc

names = ['mandhi','pat', 'rich','val']

ims = sc.odict()
for name in names:
    ims[name] = pl.imread('%s.png'%name)
    
pl.figure(figsize=(20,5))
for n,name in enumerate(names):
    pl.subplot(1,4,n+1)
    pl.imshow(ims[name])

print('Done.')
