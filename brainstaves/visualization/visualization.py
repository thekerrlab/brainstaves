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
    
pl.figure(figsize=(20,10))
for r in range(30):
    print(r)
    pl.clf()
    for n,name in enumerate(names):
        size = 400*(1+0.3*pl.randn())
        pl.subplot(2,4,n+1)
        pl.imshow(ims[name])
        pl.ylim()
        pl.ylim([max(300,size), 0])
        pl.axis('off')
        
        pl.subplot(2,4,n+5)
        pl.bar(0, 300./size)
        for k in range(4):
            pl.bar(k+1, pl.rand())
            
        pl.ylim([0,1])
    pl.pause(0.3)

print('Done.')
