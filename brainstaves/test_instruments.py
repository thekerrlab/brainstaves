#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 14:34:56 2019

@author: cliffk
"""

import pylab as pl
import instruments as i

v1 = i.Section(instrument='violin')
v1.brownian()
pl.plot(v1.arr)

v2 = i.Section(instrument='violin')
v2.brownian()
pl.plot(v2.arr)

va = i.Section(instrument='viola')
va.brownian()
pl.plot(va.arr)

vc = i.Section(instrument='cello')
vc.brownian()
pl.plot(vc.arr)

data = i.play([v1, v2, va, vc])

print('Done.')