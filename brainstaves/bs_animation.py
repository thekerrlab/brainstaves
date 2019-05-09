#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 23:43:32 2019

@author: cliffk
"""

#%% Setup

#def animate():

print('Setting up...')

import pylab as pl
import sciris as sc
import matplotlib.font_manager as mfm
#import matplotlib.animation as animation


fullscreen = True
dobegin = True
showfaces = True
shownotes = True
showwaves = True

livedatafile = 'live/livedata.obj'

livedata = sc.loadobj(livedatafile)

print('Animate? %s' % livedata.animate)

thesenotes = livedata.notes[livedata.sec]
thesedata = livedata.data[livedata.sec]


files = sc.odict([
        ('v1','assets/mandhi.png'),
        ('v2','assets/pat.png'),
        ('va','assets/rich.png'),
        ('vc','assets/val.png'),
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
font_path = 'assets/FreeSerif.ttf'
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
if fullscreen:
    pl.get_current_fig_manager().full_screen_toggle()

print('NOte: control dobegin with livedata.dobegin orsomething')
if dobegin:
    pl.pause(0.3)
    fig.set_facecolor((1,1,1))
    mainax = pl.axes(position=mainaxpos)
    mainax.axis('off')
    mainax.set_xlim([0,1])
    mainax.set_ylim([0,1])
    imaxes = sc.odict()
    mainax.text(0.48, 0.95, '§%s' % livedata.sec, fontproperties=prop, fontsize=60)
    
    print('Rendering manuscript...')
    for i,inst in enumerate(insts):
        for staffline in stafflines:
            y = staffline+ypos[inst]
            mainax.plot([0,1], pl.zeros(2)+y, lw=2, c=colors[i])
        if   inst in ['v1','v2']: mainax.text(0.0, ypos[inst], d.treble, fontproperties=prop, fontsize=60, color=colors[i])
        elif inst in ['va']:      mainax.text(0.0, ypos[inst], d.alto,   fontproperties=prop, fontsize=60, color=colors[i])
        elif inst in ['vc']:      mainax.text(0.0, ypos[inst], d.bass,   fontproperties=prop, fontsize=60, color=colors[i])

    print('Rendering faces...')
    for inst,f in files.items():
        print([imxpos[0],ypos[inst],imwidth,imheight])
        imaxes[inst] = fig.add_axes((imxpos[0],ypos[inst],imwidth,imheight), label='im_'+inst)
        imaxes[inst].axis('off')
        im = pl.imread(f)
        imaxes[inst].imshow(im)
    
    print('Creating lines...')
    lines = sc.odict()
    patches = sc.odict()
    npts = 1000
    newx = pl.linspace(0,1,npts)
    for i,inst in enumerate(insts):
        line, = mainax.plot(newx,newx*0, c=colors[i])
        lines[inst] = line
        rect = pl.Rectangle((0, ypos[inst]+0.06), 1.0, 0.08, color='w')
        print(rect)
        tmp = mainax.add_patch(rect)
        print(tmp)
        patches[inst] = tmp
    
    pl.pause(0.01)
    pl.show()
    
    txtartists = sc.odict()
    for inst in insts:
        txtartists[inst] = []
        for ind in range(len(thesenotes[inst])):
            txtartist = mainax.text(0, 0, d.note, fontproperties=prop, fontsize=60)
            txtartists[inst].append(txtartist)
    
    maxnotes = max([len(notes) for notes in thesenotes.values()])
               
    print('Looping...')
    sc.tic()
    for ind in range(maxnotes*2):
        
        for inst in insts:
            if ind<len(thesenotes[inst]):
                minpitch = {'v1':64, 'v2':64, 'va':55, 'vc':45}
                pitch = thesenotes[inst][ind] - minpitch[inst]
                pitch *= 0.002
                ta = txtartists[inst][ind]
                ta.set_x(0.02+ind/1.03/maxnotes)
                ta.set_y(ypos[inst]+pitch)
                mainax.draw_artist(ta)
        
        for i,inst in enumerate(insts):
            rate = 2
            eegyoff = ypos[inst] + 0.1
            origy = pl.roll(thesedata[inst], -rate*ind)
            newy = eegyoff+origy*0.01
            lines[inst].set_ydata(newy)
            mainax.draw_artist(patches[inst])
            mainax.draw_artist(lines[inst])
        
        fig.canvas.update()
        fig.canvas.flush_events()
    sc.toc()
    


print('Done.')
