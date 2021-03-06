'''
Generate the live score.

Run this file to actually generate the score!!

Version: 2019may08
'''

import pylab as pl
import sciris as sc
import brainstaves as bs


def makelivescore(version=None, wait=None, makepng=None, makepdf=None, usedata=None, docleanup=None):
    
    sc.tic()
    
    if version is None: version = 'B'   # Which version of the piece to generate -- atonal (A) or blues (B)
    if wait    is None: wait    = False # Whether or not to pause between generating sections
    if makepng is None: makepng = True  # Generate PNG files from MuseScore (needed for the app!)
    if makepdf is None: makepdf = True  # Generate PDF file from MuseScore
    if usedata is None: usedata = True # Use headset data
    if docleanup is None: docleanup = False

    print('STARTING!')

    print('Creating version %s' % version)
    
    datadir = '../data/run4'
    backupdir = '../data/run5'
    livedatafile = 'live/livedata.obj'
    npages = 13
    midioffset = 24
    shortpauses = False

    torun = [
    'load',
    'sectionA',
    'sectionB',
    'sectionC',
    'sectionD',
    'sectionE',
    'sectionF',
    'sectionG',
    'sectionH',
    'write',
    ]
    
    datasecs = ['A','B','C','D','E','F','G','H'] # Not A but...?
    allparts = ['v1','v2','va','vc']
    if shortpauses:
        pauses = sc.odict([
                ('A',10), # 0:20
                ('B',10), # 1:00
                ('C',10), # 1:30
                ('D',10), # 2:00
                ('E',10), # 2:30
                ('F',10), # 3:00
                ('G',10), # 3:30
                ('H',0),  # 4:00
                ])
    else:
        pauses = sc.odict([
                ('A',20), # 0:20
                ('B',40), # 1:00
                ('C',30), # 1:30
                ('D',30), # 2:00
                ('E',30), # 2:30
                ('F',30), # 3:00
                ('G',30), # 3:30
                ('H',0),  # 4:00
                ])
    
    infiles = {'A':'score/brainstaves-A.mscx',
               'B':'score/brainstaves-B.mscx',
              }
    
    #%% Function definitions
    
    def loaddata(sec, part, trim=False):
        return bs.loadrawdata(datadir=datadir, backupdir=backupdir, sec=sec, name=part, trim=trim)

    def writestatus(sec):
        try:
            livedata = bs.loadlivedata(livedatafile)
        except:
            livedata = bs.initlivedata() # Create it if it doesn't exist
#        livedata.isrunning = True # WARNING, should this be in or out?
        livedata.sec = sec
        if sec != 'A':
            livedata.animate = True
            for part in allparts:
                # Save notes
                for note in secnotes[sec][part]:
                    thispitch = float(note['pitch'])
                    livedata.notes[sec][part].append(thispitch)
                # Save data
                raw = loaddata(sec, part)
                livedata.data[sec][part] = raw
        try:
            sc.saveobj(livedatafile, livedata)
        except Exception as E:
            print('Warning, could not write status file -- not running as sudo? %s' % str(E))
        return None
    
    
    def xmlnote(orignote, string):
        mapping = {'c$': 7,
                    'cn': 14,
                    'c#': 21,
                    'd$': 9,
                    'dn': 16,
                    'd#': 23,
                    'e$': 11,
                    'en': 18,
                    'e#': 25,
                    'f$': 6,
                    'fn': 13,
                    'f#': 20,
                    'g$': 8, 
                    'gn': 15,
                    'g#': 22,
                    'a$': 10,
                    'an': 17,
                    'a#': 24,
                    'b$': 12,
                    'bn': 19,
                    'b#': 26,}
        out = sc.objdict()
        num = bs.char2num(string)
        out['pname'] = orignote.part
        out['mname'] = orignote.mname
        out['nname'] = orignote.nname
        out['pitch'] = '%i' % (num+midioffset)
        out['tpc'] = mapping[string[:2]]
        return out
    
    
    def appendnotes(nd, sec, part, useties=False, verbose=False):
        nextnotetied = False
        thesenotes = []
        for n,orignote in enumerate(nd[sec][part]):
            if nextnotetied and useties: notetouse = n-1
            else:                        notetouse = n
            if orignote.tie.val is not None: nextnotetied = True # Has to come after using the tie!
            else:                            nextnotetied = False
            if verbose: print('%s. %s' % (n, bs.num2char(qd[part].score[notetouse])))
            note = xmlnote(orignote, qd[part].score[notetouse])
            thesenotes.append(note)
        nd.notes.extend(thesenotes)
        secnotes[sec][part].extend(thesenotes)
        return None
    
    
    def repeats(ss):
        return list(range(ss[1] - ss[0] + 1))
    
    
    def write():
        if 'write' in torun:
            print('Writing XML')
            outputxml = bs.XML(infile=infiles[version])
            outputxml.write(data=nd.notes)
            if makepng:
                sc.runcommand('%s live/live.mscx -o live/live.png' % bs.mscorecmd, printoutput=True)
            if makepdf:
                sc.runcommand('%s live/live.mscx -o live/live.pdf' % bs.mscorecmd, printoutput=True)
        return None
    
    
    def begin(sec):
        sc.colorize('blue', '\n'*3+'Creating section %s' % sec)
        ndsec = sc.objdict() # This is used for each section
        return ndsec
    
    
    def process(sec):
        sc.fixedpause()
        dowrite = (wait or sec == 'H')
        if dowrite:
            write()
        pl.pause(0.1) # So the image has time to load
        writestatus(sec)
        print('Section %s written' % sec)
        sc.toc()
        print('\n'*3)
        nfiles = len(sc.getfilelist('live', pattern='live-*.png'))
        if dowrite:
            if nfiles != npages:
                print('WARNING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                print('The number of files is not correct!! %s vs %s' % (nfiles, npages))
            else:
                print('Done and all tests passed! (i.e. correct number of files)')
        if wait:
            sc.fixedpause(pauses[sec], verbose=True)
        return None
        
    
    def getstart(inst, default=None, verbose=False):
        if inst.scorepts:
            startval = bs.char2num(inst.score[-1])
        else:
            startval = default
        if verbose:
            print('For %s, seed=%s, scorepts=%s, using startval = %s' % (inst.name, inst.seed, inst.scorepts, startval))
        return startval
        
    
    #%% Main body
        
    if 'load' in torun:
        sc.colorize('blue', '\n'*3+'Resetting')
        if docleanup:
            sc.runcommand('rm -v live/live-*.png', printoutput=True)
        print('Loading XML')
        xml = bs.XML(infile=infiles[version])
        nd = sc.objdict() # For storing all the notes
        nd.notes = []
        print('Creating livedata object')
        bs.initlivedata(livedatafile=livedatafile, datasecs=datasecs, allparts=allparts, overwrite=False)
        secnotes = sc.objdict() # WARNING, could tidy up!
        for sec in datasecs:
            secnotes[sec] = sc.objdict()
            for part in allparts:
                secnotes[sec][part] = []
    
    
    if 'sectionA' in torun:
        sec = 'A'
        nd[sec] = begin(sec)
        process(sec)
        
    
    
    if 'sectionB' in torun:
        sec = 'B'
        nd[sec] = begin(sec)
        quartet,qd = bs.makequartet(mindur=8, timesig='12/8', nbars=1, datadir=datadir, backupdir=backupdir)
        
        for part,inst in qd.items():      
            if part == 'v1': ss = [39,40]
            else:            ss = [21,40]
            nd[sec][part] = xml.loadnotes(part=part, measurerange=ss)
            for repeat in repeats(ss):
                inst.seed += 1
                startval = getstart(inst, 'min')
                inst.brownian(maxstep=2, startval=startval, skipstart=True, usedata=usedata, sec=sec, repeat=repeat, ss=ss)
                if version == 'A': inst.noteify('atonal')
                if version == 'B': inst.noteify('blues')
                inst.seed += 1
                inst.cat()
            
            appendnotes(nd, sec, part)
        process(sec)
    
    
    if 'sectionC' in torun:
        sec = 'C'
        nd[sec] = begin(sec)
        quartet,qd = bs.makequartet(mindur=16, timesig='4/4', nbars=1, datadir=datadir, backupdir=backupdir)
        
        for part,inst in qd.items():
            if part != 'v2':
                ss = [43,60]
                nd[sec][part] = xml.loadnotes(part=part, measurerange=ss)
                
                for repeat in repeats(ss):
                    inst.seed += 1
                    if   part == 'v1': startval = getstart(inst, 'max')
                    elif part == 'vc': startval = getstart(inst, 'min')
                    else:              startval = getstart(inst)
                    inst.brownian(maxstep=3, startval=startval, skipstart=True, usedata=usedata, sec=sec, repeat=repeat, ss=ss)
                    if version == 'A': inst.noteify('octo')
                    if version == 'B': inst.noteify('blues')
                    inst.seed += 1
                    inst.cat()
            
                appendnotes(nd, sec, part)
        process(sec)
    
    
    if 'sectionD' in torun:
        sec = 'D'
        nd[sec] = begin(sec)
        quartet,qd = bs.makequartet(mindur=8, timesig='4/4', nbars=1, datadir=datadir, backupdir=backupdir)
        
        for part,inst in qd.items():
            ss = [63,83]
            if   part == 'v1': ss = [63,83]
            elif part == 'v2': ss = [65,83]
            elif part == 'va': ss = [64,83]
            elif part == 'vc': ss = [64,83]
            nd[sec][part] = xml.loadnotes(part=part, measurerange=ss)
            for repeat in repeats(ss):
                inst.seed += 1
                startval = getstart(inst)
                inst.brownian(maxstep=5, startval=startval, skipstart=True, usedata=usedata, sec=sec, repeat=repeat, ss=ss)
                if version == 'A': inst.noteify('atonal', breakties=True)
                if version == 'B': inst.noteify('blues', breakties=True)
                inst.seed += 1
                inst.cat()
        
            appendnotes(nd, sec, part)
        process(sec)
    
    
    
    if 'sectionE' in torun:
        sec = 'E'
        nd[sec] = begin(sec)
        ss = [85,101]
        nm = sc.objdict()
        seq = sc.objdict()
        for part in qd.keys():
            nm[part] = sc.objdict()
            seq[part] = 0
        quartet,qd = bs.makequartet(mindur=8, timesig='4/4', nbars=1, datadir=datadir, backupdir=backupdir)
    
        def generate(seq, nm, p, m, n, t, verbose=False):
            if verbose: print('Input: %s, %s, %s, %s, %s' % (seq[:], p, m, n, t))
            genkeys = []
            np = nm[p]
            basekey = 'm%i_n%i' % (m, n)
            rootkey = 'root_' + basekey
            doublekey = 'double_' + basekey
            np[rootkey] = seq[p]
            np[doublekey] = rootkey
            genkeys.extend([rootkey, doublekey])
            for tind in range(t):
                for rd in ['root_','double_']:
                    tiedkey = ('tied%i_' % tind) + rd + basekey
                    np[tiedkey] = rd + basekey
                    genkeys.append(tiedkey)
            seq[p] += 1
            if verbose: print('Output: %s' % genkeys)
            return None
    
        # Intro
        generate(seq, nm, p='va', m=85, n=1, t=2)
        generate(seq, nm, p='v2', m=86, n=1, t=1)
        generate(seq, nm, p='v1', m=86, n=1, t=1)
        generate(seq, nm, p='vc', m=87, n=1, t=0)
    
        generate(seq, nm, p='v2', m=88, n=1, t=2)
        generate(seq, nm, p='va', m=89, n=1, t=1)
        generate(seq, nm, p='vc', m=89, n=1, t=1)
        generate(seq, nm, p='v1', m=90, n=1, t=0)
    
        generate(seq, nm, p='vc', m=91, n=1, t=2)
        generate(seq, nm, p='v1', m=91, n=1, t=2)
        generate(seq, nm, p='va', m=92, n=1, t=1)
        generate(seq, nm, p='v2', m=93, n=1, t=0)
        
        # Unison
        for part in qd.keys():
            generate(seq, nm, p=part, m=94, n=1, t=0)
            generate(seq, nm, p=part, m=94, n=3, t=0)
            generate(seq, nm, p=part, m=94, n=5, t=1)
            generate(seq, nm, p=part, m=95, n=3, t=1)
            generate(seq, nm, p=part, m=96, n=3, t=0)
            generate(seq, nm, p=part, m=96, n=5, t=0)
            generate(seq, nm, p=part, m=96, n=7, t=1)
            for n in [3,5,7]:
                generate(seq, nm, p=part, m=97, n=n, t=0)
            for n in [1,3,5,7,9]:
                generate(seq, nm, p=part, m=98, n=n, t=0)
            for n in [1,3,5,7,9]:
                generate(seq, nm, p=part, m=99, n=n, t=0)
            generate(seq, nm, p=part, m=99, n=11, t=1)
            generate(seq, nm, p=part, m=100, n=3, t=0)
            generate(seq, nm, p=part, m=100, n=5, t=1)
            generate(seq, nm, p=part, m=101, n=3, t=0)
            generate(seq, nm, p=part, m=101, n=5, t=1)
    
        startvals1 = sc.odict([
                ('v1',bs.char2num('en4')),
                ('v2',bs.char2num('en3')),
                ('va',bs.char2num('en2')),
                ('vc',bs.char2num('en1')),
                ])
        startvals2 = sc.odict([
                ('v1',bs.char2num('cn3')),
                ('v2',bs.char2num('cn3')),
                ('va',bs.char2num('cn2')),
                ('vc',bs.char2num('cn2')),
                ])
        
        for part,inst in qd.items():
            nd[sec][part] = xml.loadnotes(part=part, measurerange=ss)
            assert len(nd[sec][part]) == len(nm[part])
            
            inst.brownian(maxstep=5, startval=startvals1[part], forcestep=True, skipstart=True, npts=3, usedata=usedata, sec=sec, repeat=0, ss=[0,1])
            if version == 'A': inst.noteify('atonal')
            if version == 'B': inst.noteify('blues')
            inst.seed += 1
            inst.cat()
            
            inst.brownian(maxstep=3, startval=startvals2[part], forcestep=True, skipstart=True, npts=25, usedata=usedata, sec=sec, repeat=1, ss=[0,1])
            if version == 'A': inst.noteify('octo')
            if version == 'B': inst.noteify('blues')
            inst.seed += 1
            inst.cat()
            
            tmpscore = sc.dcp(inst.score)
            assert len(tmpscore) == seq[part]
            
            # Replace sequence numbers with notes
            nmnotes = sc.dcp(nm[part])
            unisonsec = False
            for k,key in nmnotes.enumkeys():
                val = nmnotes[key]
                if key.startswith('root'): # Create the random notes
                    nmnotes[key] = tmpscore[val] # e.g. map sequence number 0 to pitch 53
                    if val>2: unisonsec = True
                elif key.startswith('double'): # Add a 6th higher
                    if unisonsec: interval = 9 # 7
                    else:         interval = 9
                    origchar = nmnotes[val]
                    orignum = bs.char2num(origchar)
                    newnum = orignum + interval
                    newchar = bs.num2char(newnum)
                    if version == 'A': newchar = bs.char2octo(newchar) # WARNING, should match noteify() calls above!
                    if version == 'B': newchar = bs.char2blues(newchar)
                    nmnotes[key] = newchar
                elif key.startswith('tied'):
                    nmnotes[key] = nmnotes[val] # e.g. nmnotes['tied0_root_m98_n5'] = nmnotes['root_m98_n5'] = 36
                else:
                    raise Exception('Not recognized')
    
            # Create new score via mapping
            inst.score = sc.dcp(nmnotes[:])
        
            appendnotes(nd, sec, part)
        process(sec)
    
    
    if 'sectionF' in torun:
        sec = 'F'
        nd[sec] = begin(sec)
        quartet,qd = bs.makequartet(mindur=8, timesig='4/4', nbars=1, datadir=datadir, backupdir=backupdir)
        
        parttosub = {
                'A':'va', 
                'B':'v1'}
        ssparts = {
                'A':[106,118], 
                'B':[106,110]}
        
        # Random melody part
        for part,inst in qd.items():
            if part == parttosub[version]:
                ss = ssparts[version]
                nd[sec][part] = xml.loadnotes(part=part, measurerange=ss)
                for repeat in repeats(ss):
                    inst.seed += 1
                    startval = getstart(inst, startval) # WARNING, default should probably be used here, think it's picking up the cello part?
                    inst.brownian(maxstep=3, startval=startval, skipstart=True, usedata=usedata, sec=sec, repeat=repeat, ss=ss)
                    if version == 'A': inst.noteify('atonal', breakties=True)
                    if version == 'B': inst.noteify('blues', breakties=True)
                    inst.seed += 1
                    inst.cat()
            
                appendnotes(nd, sec, part)
        
        # Melodic part
        if version == 'A':
            print('Keeping prewritten melody for version A')
        elif version == 'B':
            for part,inst in qd.items():
                if   part == 'v1': ss = [111,124]
                elif part == 'v2': ss = [117,124]
                elif part == 'va': ss = [119,124]
                elif part == 'vc': ss = [106,124]
                nd[sec][part] = xml.loadnotes(part=part, measurerange=ss)
                for repeat in repeats(ss):
                    inst.seed += 1
                    startval = getstart(inst, startval)
                    inst.brownian(maxstep=3, startval=startval, skipstart=True, usedata=usedata, sec=sec, repeat=repeat, ss=ss)
                    if version == 'A': inst.noteify('atonal') # WARNING, not used
                    if version == 'B': inst.noteify('blues')
                    inst.seed += 1
                    inst.cat()
                appendnotes(nd, sec, part, useties=True)
        
        process(sec)
    
    
    if 'sectionG' in torun:
        sec = 'G'
        nd[sec] = begin(sec)
        quartet,qd = bs.makequartet(mindur=8, timesig='4/4', nbars=1, datadir=datadir, backupdir=backupdir)
        
        # Glissando part
        for part,inst in qd.items():
            if   part == 'v2': ss = [146,147]
            elif part == 'vc': ss = [125,147]
            else:              ss = [136,147]
            nd[sec][part] = xml.loadnotes(part=part, measurerange=ss)
            for repeat in repeats(ss):
                inst.seed += 1
                startval = getstart(inst, startval)
                inst.brownian(maxstep=5, startval=startval, skipstart=True, usedata=usedata, sec=sec, repeat=repeat, ss=ss)
                if version == 'A': inst.noteify('atonal', breakties=True)
                if version == 'B': inst.noteify('blues', breakties=True)
                inst.seed += 1
                inst.cat()
        
            appendnotes(nd, sec, part)
        
        # Melodic part
        if version == 'A':
            print('Keeping prewritten melody for version A')
        elif version == 'B':
            for part,inst in qd.items():
                if part in ['v2','va']:
                    if   part == 'v2': ss = [135,144]
                    elif part == 'va': ss = [125,135]
                    nd[sec][part] = xml.loadnotes(part=part, measurerange=ss)
                    for repeat in repeats(ss):
                        inst.seed += 1
                        startval = getstart(inst, startval)
                        inst.brownian(maxstep=3, startval=startval, skipstart=True, usedata=usedata, sec=sec, repeat=repeat, ss=ss)
                        if version == 'A': inst.noteify('atonal') # WARNING, not used
                        if version == 'B': inst.noteify('blues')
                        inst.seed += 1
                        inst.cat()
                    appendnotes(nd, sec, part, useties=True)
        
        process(sec)
    
    
    if 'sectionH' in torun:
        sec = 'H'
        nd[sec] = begin(sec)
        quartet,qd = bs.makequartet(mindur=8, timesig='12/8', nbars=1, datadir=datadir, backupdir=backupdir)
        
        for part,inst in qd.items():      
            if part == 'v1': ss = [150,151]
            else:            ss = [150,169]
            nd[sec][part] = xml.loadnotes(part=part, measurerange=ss)
            for repeat in repeats(ss):
                inst.seed += 1
                if   part in ['v1','v2']: startval = getstart(inst, 'max')
                elif part in ['va','vc']: startval = getstart(inst, 'min')
                inst.brownian(maxstep=2, startval=startval, skipstart=True, usedata=usedata, sec=sec, repeat=repeat, ss=ss)
                if version == 'A': inst.noteify('acoustic') # Or inst.noteify('acoustic') # inst.noteify(['dia','octo'])
                if version == 'B': inst.noteify('blues')
                inst.seed += 1
                inst.cat()
            
            appendnotes(nd, sec, part)
        process(sec)
    
    
    sc.toc()
    print('Done.')


if __name__ == '__main__':
    makelivescore()