#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 00:39:06 2019

@author: cliffk
"""

import os
import pylab as pl
import sciris as sc

names = ['v1','v2','va','vc']

which = 'quartet'
lastline = False # ['v1','v2']
delay = 3

maps = {'quartet':
            {'v1':'mandhi',
             'v2':'pat',
             'va':'rich',
             'vc':'val'},
        'kids':
            {'v1':'dino1',
             'v2':'dino2',
             'va':'dino3',
             'vc':'dino4'},
     }

fig = None

count = 0
while True:
    count += 1
    
    
    data = sc.odict()
    for name in names:
        if lastline and name in lastline: r = -1
        else: r = count
        infile = '../live/data-'+name+'.csv'
        tmpdata = []
        lines = open(infile).readlines()
        for line in lines:
            tmpdata.append([float(v) for v in line.split(', ')])
        data[name] = tmpdata
    
    # Must match recordlive.py
    cols =     ['attention', 'blinkStrength', 'bytesAvailable', 'delta',   'highAlpha', 'highBeta', 'lowAlpha', 'lowBeta',  'lowGamma', 'meditation', 'midGamma', 'packetsReceived', 'poorSignal', 'rawValue', 'theta']
    keepcols = ['delta',      'theta',        'lowAlpha',       'highAlpha', 'lowBeta', 'highBeta', 'lowGamma', 'midGamma', 'highvslow'] # , 'poorSignal'
    
    dfs = sc.odict()
    highchans = ['lowBeta', 'highBeta', 'lowGamma', 'midGamma']
    lowchans = ['delta', 'theta', 'lowAlpha', 'highAlpha']
    allchans = lowchans+highchans
    nchans = len(allchans)
    for name in names:
        dfs[name] = sc.dataframe(cols=cols, data=data[name])
        d = dfs[name]
        high = pl.zeros(d.nrows)
        low = pl.zeros(d.nrows)
        for chan in highchans: high += d[chan].astype(float)
        for chan in lowchans:  low  += d[chan].astype(float)
        dfs[name]['highvslow'] = high/low
    
    data = dfs
    
    highchans = ['lowBeta', 'highBeta', 'lowGamma', 'midGamma']
    lowchans = ['delta', 'theta', 'lowAlpha', 'highAlpha']
    allchans = lowchans+highchans
    nchans = len(allchans)
    
    for name in names:
        for chan in allchans:
            data[name][chan] /= data[name][chan].mean()
    
    ims = sc.odict()
    for name in names:
        ims[name] = pl.imread('%s.png'%maps[which][name])
        
    if fig is None:
        fig = pl.figure(figsize=(20,10))
    t1 = sc.tic()
    pl.clf()
    for n,name in enumerate(names):
        d = data[name]
        size = 0
        for chan in allchans:
            size += d[chan][r]
            
        pl.subplot(2,4,n+1)
        pl.imshow(ims[name])
        pl.ylim()
        pl.ylim([max(300,900/pl.log(size)), 0])
        pl.axis('off')
        pl.title('%s' % count)
        
        pl.subplot(2,4,n+5)
        for c,chan in enumerate(allchans):
            pl.bar(c+1, d[chan][r])
        pl.ylim([0,10])
    pl.pause(0.1)
    print('Saving...')
    pl.savefig('tmp.png')
    print('Publishing...')
    os.system('scp -r "tmp.png" cliffker@cliffkerr.com:/home3/cliffker/public_html/thekerrlab/tmp/')
    t2 = sc.toc(t1, output=True)
    z = delay-t2
    print(z)
    if z>0:
        pl.pause(z)

print('Done.')
