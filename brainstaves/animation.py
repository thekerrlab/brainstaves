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
shownotes = True

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
mainaxpos = [0.1,0,0.88,1]
imheight = 0.10*screenratio

stafflines = pl.linspace(0,0.03,5)




pl.rcParams['toolbar'] = 'None'
font_path = 'FreeSerif.ttf'
prop = mfm.FontProperties(fname=font_path)

colors = sc.gridcolors(4)

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
    mainax = pl.axes(position=mainaxpos)
    mainax.axis('off')
    mainax.set_xlim([0,1])
    mainax.set_ylim([0,1])
    imaxes = sc.odict()
    
    print('Rendering manuscript...')
    for i,inst in enumerate(insts):
        for staffline in stafflines:
            y = staffline+ypos[inst]
            mainax.plot([0,1], pl.zeros(2)+y, lw=2, c=colors[i])
        if inst in ['v1','v2']:
            mainax.text(0.0, ypos[inst], d.treble, fontproperties=prop, fontsize=60, color=colors[i])
        elif inst in ['va']:
            mainax.text(0.0, ypos[inst], d.alto, fontproperties=prop, fontsize=60, color=colors[i])
        elif inst in ['vc']:
            mainax.text(0.0, ypos[inst], d.bass, fontproperties=prop, fontsize=60, color=colors[i])
            

    if showfaces:
        print('Rendering faces...')
        for inst in insts:
            print([imxpos[0],ypos[inst],imwidth,imheight])
            imaxes[inst] = fig.add_axes((imxpos[0],ypos[inst],imwidth,imheight), label='im_'+inst)
            imaxes[inst].axis('off')
        
        for inst,f in files.items():
            im = pl.imread('visualization/'+f)
            imaxes[inst].imshow(im)
    
    if shownotes:
        for inst in insts:
            pitch = 0
            for n in range(50):
                pitch += pl.randn()*0.01
                mainax.text(0.02+n/51, ypos[inst]+pitch, d.note, fontproperties=prop, fontsize=60)
        
        
    


print('Done.')