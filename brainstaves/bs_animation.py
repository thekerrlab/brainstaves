#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 23:43:32 2019

@author: cliffk
"""

#%% Setup

#def animate():

print('Setting up...')

fullscreen = False
dobegin = True
showfaces = True
shownotes = True
showwaves = True

import pylab as pl
import matplotlib.font_manager as mfm
import sciris as sc
import matplotlib.animation as animation

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
    
    
    fa = sc.odict()
    tmp = 1
    for i,inst in enumerate(insts):
        fa[inst] = sc.odict()
        fa[inst]['delta'] = [1, pl.exp(abs(pl.randn()*tmp))]
        fa[inst]['theta'] = [7, pl.exp(abs(pl.randn()*tmp))]
        fa[inst]['alpha'] = [12, pl.exp(abs(pl.randn()*tmp))]
        fa[inst]['beta'] = [20, pl.exp(abs(pl.randn()*tmp))]
        fa[inst]['gamma'] = [35, pl.exp(abs(pl.randn()*tmp))]
    
    npts = int(1e3)
    x = pl.linspace(0,5*2*pl.pi,npts)
    newx = sc.dcp(x)
    newx /= newx.max()
    
    lines = sc.odict()
    for i,inst in enumerate(insts):
        line, = mainax.plot(newx,newx*0, c=colors[i])
        lines[inst] = line
                
    for ind in range(200):
        n = ind % 50
        
        if n==0:
            fa = sc.odict()
            tmp = 1
            for i,inst in enumerate(insts):
                fa[inst] = sc.odict()
                fa[inst]['delta'] = [1, pl.exp(abs(pl.randn()*tmp))]
                fa[inst]['theta'] = [7, pl.exp(abs(pl.randn()*tmp))]
                fa[inst]['alpha'] = [12, pl.exp(abs(pl.randn()*tmp))]
                fa[inst]['beta'] = [20, pl.exp(abs(pl.randn()*tmp))]
                fa[inst]['gamma'] = [35, pl.exp(abs(pl.randn()*tmp))]
        
        
        if shownotes:
            for inst in insts:
                pitch = 0
#                for n in range(q):
                pitch += pl.randn()*0.01
                mainax.text(0.02+n/51, ypos[inst]+pitch, d.note, fontproperties=prop, fontsize=60)
            
    
        if showwaves:
            
            
            for i,inst in enumerate(insts):
                y = pl.zeros(npts)
                
                for freq,pow in fa[inst].values():
                    y += pl.sin(x*freq)*pow
                
                newy = sc.dcp(y)
                newy /= 300
                newy += ypos[inst]+0.1
                newy = newy.tolist()
                newy = newy[n*10:] + newy[:n*10]
                lines[inst].set_ydata(newy)
        
        pl.pause(0.01)
        pl.show()
    
#    if showwaves:
#        
#        print('Starting waves...')
#        
#        npts = int(2e3)
#        x = pl.linspace(0,20*2*pl.pi,npts)
#        y = pl.zeros(npts)
#        lines = sc.odict()
#        ydatas = sc.odict()
#        for i,inst in enumerate(insts):
#            line, = mainax.plot(x,y, c=colors[i])
#            lines[inst] = line
#        
#        for i,inst in enumerate(insts):
#            y *= 0
#            fa = sc.odict()
#            tmp = 1
#            fa['delta'] = [1, pl.exp(abs(pl.randn()*tmp))]
#            fa['theta'] = [7, pl.exp(abs(pl.randn()*tmp))]
#            fa['alpha'] = [12, pl.exp(abs(pl.randn()*tmp))]
#            fa['beta'] = [20, pl.exp(abs(pl.randn()*tmp))]
#            fa['gamma'] = [35, pl.exp(abs(pl.randn()*tmp))]
#            
#            for freq,pow in fa.values():
#                y += pl.sin(x*freq)*pow
#            
#            newy = sc.dcp(y)
#            newy /= 300
#            newy += ypos[inst]+0.1
#            ydatas[inst] = newy
        
#        def init():  # only required for blitting to give a clean slate.
#            for i,inst in enumerate(insts):
#                line = lines[inst]
#                line.set_ydata([pl.nan] * len(x))
#            return line,
#        
#        
#        def animate(r):
#            for i,inst in enumerate(insts):
#                line = lines[inst]
#                thisy = sc.dcp(ydatas[inst]).tolist()
#                thisy = thisy[r*1:] + thisy[:1*r]
#                line.set_ydata(thisy)  # update the data.
#            return line,
#        
#        ani = animation.FuncAnimation(fig, animate, init_func=init, interval=50, blit=True, save_count=500)
        
        
#        for r in range(200):
#        for i,inst in enumerate(insts):
##                print(r,i)
#                sc.tic()
#                
#                sc.toc()
#                
#                sc.toc()
#                pl.plot(x,ydatas[i])
#                sc.toc()
#                pl.pause(0.001)
#                sc.toc()
        


print('Done.')
