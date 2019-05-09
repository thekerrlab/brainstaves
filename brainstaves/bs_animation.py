#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 23:43:32 2019

@author: cliffk
"""

import time
import pylab as pl
import sciris as sc
import matplotlib.font_manager as mfm
import brainstaves as bs
import matplotlib.pyplot as ppl
ppl.switch_backend('Qt5Agg') # WARNING, this is because ScirisWeb resets it

animatedsecs = ['B','C','D','E','F','G','H']

def animate():

    print('Setting up...')

    pl.ion()
    fullscreen = False
    black = True
    showsec = True # WARNING, does not re-render properly!
    livedatafile = 'live/livedata.obj'
    
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
    
    
    if black: 
        fontcolor = (1,1,1)
        bgcolor = (0,0,0)
    else:
        fontcolor = (0,0,0)
        bgcolor = (1,1,1)
    
    pl.rcParams['toolbar'] = 'None'
    font_path = 'assets/FreeSerif.ttf'
    prop = mfm.FontProperties(fname=font_path)
    
    colors = sc.gridcolors(4)
    
    d = sc.objdict({
         'note':   '𝅘',
         'whole':  '𝅝',
         'quarter':'♩',
         'sharp':  '♯',
         'flat':   '♭',
         'natural':'♮',
         'treble': '𝄞',
         'alto':   '𝄡',
         'bass':   '𝄢',
         })
    
    
    print('Creating black figure...')
    fig = pl.figure(figsize=(16,9), facecolor=(0,0,0))
    fig.canvas.window().statusBar().setVisible(False) 
    if fullscreen:
        pl.get_current_fig_manager().full_screen_toggle()
    
    
    currentsec = ''
    
    npts = 1000
    plotpts = 500
    maxartists = 200 # Should actually be 128
    mainax = None
    
    def refreshfig(mainax, renderitems=True):
        if mainax is not None:
            mainax.clear()
        if not black:
            fig.set_facecolor((1,1,1))
        mainax = pl.axes(position=mainaxpos)
        mainax.axis('off')
        mainax.set_xlim([0,1])
        mainax.set_ylim([0,1])
        imaxes = sc.odict()
        lines = sc.odict()
        patches = sc.odict()
        txtartists = sc.odict()
        
        if not renderitems:
            pl.pause(0.1)
            pl.show()
        
        if renderitems:
            if showsec:
                mainax.text(0.48, 0.96, '§%s' % currentsec, fontproperties=prop, fontsize=60, color=fontcolor)
            
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
                imaxes[inst] = fig.add_axes((imxpos[0],ypos[inst],imwidth,imheight), label='im_'+inst)
                imaxes[inst].axis('off')
                im = pl.imread(f)
                imaxes[inst].imshow(im)
            
            print('Creating lines...')
            
            newx = pl.linspace(0,npts/plotpts,npts)
            for i,inst in enumerate(insts):
                line, = mainax.plot(newx[:plotpts],newx[:plotpts]*0, c=colors[i], lw=3)
                lines[inst] = line
                rect = pl.Rectangle((0, ypos[inst]+0.06), 1.0, 0.09, color=bgcolor)
                tmp = mainax.add_patch(rect)
                patches[inst] = tmp
            
            pl.pause(0.01)
            pl.show()
            
            for i,inst in enumerate(insts):
                txtartists[inst] = []
                for ind in range(maxartists):
                    txtartist = mainax.text(0, 0, d.note, fontproperties=prop, fontsize=60, color=colors[i])
                    txtartists[inst].append(txtartist)
        
        return mainax, imaxes, lines, patches, txtartists
        
    def getlivedata():
        try:
            livedata = sc.loadobj(livedatafile)
            doanimate = livedata.isrunning and (livedata.sec in animatedsecs)
        except:
            print('Could not load live data')
            livedata = None
            doanimate = False
        return livedata, doanimate
    
    ind = 0
    loopcheck = 20
    livedata = None
    doanimate = False
    livedata,doanimate = getlivedata()
    mainax, imaxes, lines, patches, txtartists = refreshfig(mainax, renderitems=False)
    while True:
        time.sleep(0.01)
        ind += 1
        if not doanimate or not ind%loopcheck:
            livedata,doanimate = getlivedata()
            print('Loop step %s, animating? %s' % (ind, doanimate))
        
        if not doanimate or (currentsec not in animatedsecs):
            time.sleep(1)
        else:
            print('Animating step %s' % ind)
            
            livesec = bs.pagestosec(livedata)
            if currentsec != livesec:
                print('Updating section: %s -> %s' % (currentsec, livesec))
                ind = 0
                currentsec = livesec
                refreshfig(mainax)
            
            thesenotes = livedata.notes[currentsec]
            thesedata = livedata.data[currentsec]
            
            maxnotes = max([len(notes) for notes in thesenotes.values()])
                       
            # Plot notes
            for inst in insts:
                if ind<len(thesenotes[inst]):
                    minpitch = {'v1':64, 'v2':64, 'va':55, 'vc':45}
                    pitch = thesenotes[inst][ind] - minpitch[inst]
                    pitch *= 0.002
                    ta = txtartists[inst][ind]
                    ta.set_x(0.02+ind/1.03/maxnotes)
                    ta.set_y(ypos[inst]+pitch)
                    mainax.draw_artist(ta)
            
            # Plot waves
            for i,inst in enumerate(insts):
                eegscale = 0.04
                rate = 1# int(pl.ceil(npts/maxnotes))
                roll = True
                eegyoff = ypos[inst] + 0.1
                origeeg = thesedata[inst] # pl.cumsum(thesedata[inst])
                smoothdata = sc.smooth(origeeg, 1)
                smoothdata /= abs(smoothdata).max()
                if roll:
                    origy = pl.roll(smoothdata, -rate*ind)
                else:
                    origy = sc.dcp(smoothdata)
                    origy[rate*ind:] = pl.nan
                newy = eegyoff+origy*eegscale
                lines[inst].set_ydata(newy[:plotpts])
                mainax.draw_artist(patches[inst])
                mainax.draw_artist(lines[inst])
            
            fig.canvas.update() # time.sleep(0.02)
            fig.canvas.flush_events()

if __name__ == '__main__':
    animate()