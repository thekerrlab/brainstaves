#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 14:34:56 2019

@author: cliffk
"""

import pylab as pl
import instruments as i

v1 = i.Section(instrument='violin', seed=1)
v2 = i.Section(instrument='violin', seed=2)
va = i.Section(instrument='viola', seed=3)
vc = i.Section(instrument='cello', seed=4)
quartet = [v1,v2,va,vc]

for inst in quartet:
    inst.brownian(maxstep=4)
    inst.diatonic()
#    inst.octotonic()

for inst in quartet:
    inst.addrests(p=1.0)


fig = i.plot(quartet)

data = i.play(quartet)

score = i.write(quartet)


print('Done.')