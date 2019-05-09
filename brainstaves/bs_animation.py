#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 23:43:32 2019

@author: cliffk
"""

#%% Setup

def animate():

    print('Setting up...')
    
    import time
    import pylab as pl
    import sciris as sc
    import matplotlib.font_manager as mfm
    
    fullscreen = False
    black = True
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
    
    if 1: # TEMPPPPP
        if not black:
            fig.set_facecolor((1,1,1))
        mainax = pl.axes(position=mainaxpos)
        mainax.axis('off')
        mainax.set_xlim([0,1])
        mainax.set_ylim([0,1])
        imaxes = sc.odict()
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
            print([imxpos[0],ypos[inst],imwidth,imheight])
            imaxes[inst] = fig.add_axes((imxpos[0],ypos[inst],imwidth,imheight), label='im_'+inst)
            imaxes[inst].axis('off')
            im = pl.imread(f)
            imaxes[inst].imshow(im)
        
        print('Creating lines...')
        lines = sc.odict()
        patches = sc.odict()
        npts = 1000
        plotpts = 500
        newx = pl.linspace(0,npts/plotpts,npts)
        for i,inst in enumerate(insts):
            line, = mainax.plot(newx[:plotpts],newx[:plotpts]*0, c=colors[i], lw=3)
            lines[inst] = line
            rect = pl.Rectangle((0, ypos[inst]+0.06), 1.0, 0.09, color=bgcolor)
            print(rect)
            tmp = mainax.add_patch(rect)
            print(tmp)
            patches[inst] = tmp
        
        pl.pause(0.01)
        pl.show()
        
        maxartists = 200 # Should actually be 128
        txtartists = sc.odict()
        for i,inst in enumerate(insts):
            txtartists[inst] = []
            for ind in range(maxartists):
                txtartist = mainax.text(0, 0, d.note, fontproperties=prop, fontsize=60, color=colors[i])
                txtartists[inst].append(txtartist)
        
    def getlivedata():
        try:
            livedata = sc.loadobj(livedatafile)
            doanimate = livedata.animate
        except Exception as E:
            print('Could not load live data: %s' % str(E))
            livedata = None
            doanimate = False
        return livedata, doanimate
    
    loopcount = 0
    currentsec = None
    while True:
        loopcount += 1
        livedata,doanimate = getlivedata()
        print('Loop step %s, animating? %s' % (loopcount, doanimate))
        if doanimate and livedata.sec != currentsec:
#        pl.pause(1)
            pl.clf()
        
        
        if doanimate:
            
            currentsec = livedata.sec
            
            thesenotes = livedata.notes[livedata.sec]
            thesedata = livedata.data[livedata.sec]
            
            maxnotes = max([len(notes) for notes in thesenotes.values()])
                       
            print('Looping...')
            sc.tic()
            ind = loopcount
                
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
        
        print('Done.')

if __name__ == '__main__':
    animate()