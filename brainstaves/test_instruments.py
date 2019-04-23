#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 14:34:56 2019

@author: cliffk
"""

import pylab as pl
import instruments as i

v1 = i.Section(instrument='violin')
v2 = i.Section(instrument='violin')
va = i.Section(instrument='viola')
vc = i.Section(instrument='cello')
quartet = [v1,v2,va,vc]

for inst in quartet:
    inst.brownian(maxstep=4)
#    inst.diatonic()
    inst.octotonic()

for inst in quartet:
    inst.addrests(p=0.8)


fig = i.plot(quartet)

data = i.play(quartet)



print('Done.')