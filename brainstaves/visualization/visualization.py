#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 00:39:06 2019

@author: cliffk
"""

import pylab as pl
import sciris as sc

names = ['mandhi','pat', 'rich','val']
userandom = False

highchans = ['lowBeta', 'highBeta', 'lowGamma', 'midGamma']
lowchans = ['delta', 'theta', 'lowAlpha', 'highAlpha']
allchans = lowchans+highchans
nchans = len(allchans)

if not userandom:
    data = sc.loadobj('../data/data-apr24.obj')
    data.rename('ck','pat')
    for name in names:
        for chan in allchans:
            data[name][chan] /= data[name][chan].mean()

ims = sc.odict()
for name in names:
    ims[name] = pl.imread('%s.png'%name)
    
pl.figure(figsize=(20,10))
for r in range(30):
    print(r)
    t1 = sc.tic()
    pl.clf()
    for n,name in enumerate(names):
        if userandom:
            size = 400*(1+0.3*pl.randn())
        else:
            d = data[name]
            size = 0
            for chan in allchans:
                size += d[chan][r]
            
        pl.subplot(2,4,n+1)
        pl.imshow(ims[name])
        pl.ylim()
        pl.ylim([max(300,900/pl.log(size)), 0])
        pl.axis('off')
        
        pl.subplot(2,4,n+5)
        if userandom:
            for k in range(10):
                pl.bar(k+1, pl.rand())
            pl.ylim([0,1])
        else:
            for c,chan in enumerate(allchans):
                pl.bar(c+1, d[chan][r])
            pl.ylim([0,10])
    t2 = sc.toc(t1, output=True)
    pl.pause(1.0-t2)

print('Done.')
