#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 23:43:32 2019

@author: cliffk
"""

#%% Setup

print('Setting up...')

dobegin = True
showfaces = True

import pylab as pl
import matplotlib.font_manager as mfm
import sciris as sc

files = sc.odict([
        ('v1','mandhi.png'),
        ('v2','pat.png'),
        ('va','rich.png'),
        ('vc','val.png'),
        ])

imyoff = 0.05
ypos = sc.odict([
        ('v1',0.75+imyoff),
        ('v2',0.50+imyoff),
        ('va',0.25+imyoff),
        ('vc',0.00+imyoff),
        ])

insts = files.keys()

screenratio = 16/9.
imxpos = [0.00, 0.15]
imwidth = 0.10
scorexpos = [0.2, 1.0]
imheight = 0.10*screenratio

stafflines = pl.linspace(0,0.03,5)




#begin = True

pl.rcParams['toolbar'] = 'None'
font_path = 'FreeSerif.ttf'
prop = mfm.FontProperties(fname=font_path)

d = sc.objdict({
     'note':'𝅘',
     'whole':'𝅝',
     'quarter':'♩',
     'sharp':'♯',
     'flat':'♭',
     'natural':'♮',
     'treble':'𝄞',
     'alto':'𝄡',
     'bass':'𝄢',
     })

print('Creating black figure...')
fig = pl.figure(figsize=(16,9), facecolor=(0,0,0))
fig.canvas.window().statusBar().setVisible(False) 
#pl.get_current_fig_manager().full_screen_toggle()

if dobegin:
    pl.pause(1)
    fig.set_facecolor((1,1,1))
    mainax = pl.axes(position=[0,0,1,1])
    imaxes = sc.odict()
    
    print('Rendering manuscript...')
    for inst in insts:
        for staffline in stafflines:
            y = staffline+ypos[inst]
            mainax.plot([0,1], pl.zeros(2)+y, lw=2, c=(0,0,0))

    if showfaces:
        print('Rendering faces...')
        for inst in insts:
            print([imxpos[0],ypos[inst],imwidth,imheight])
            imaxes[inst] = fig.add_axes((imxpos[0],ypos[inst],imwidth,imheight), label='im_'+inst)
            imaxes[inst].axis('off')
        
        for inst,f in files.items():
            im = pl.imread('visualization/'+f)
            imaxes[inst].imshow(im)
        
        
    


#pl.plot([0,1,], [0,1])
#pl.text(0.5, 0.5, d.note, fontproperties=prop, fontsize=50)

print('Done.')