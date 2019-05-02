'''
Generate the live score.

Run this script to actually generate the score.
'''

import os
import sciris as sc
import instruments
import musescore

sc.tic()

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

wait = True

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

statusfile = 'status.tmp'
npages = 13
midioffset = 24
usedata = False

#%% Function definitions

def writestatus(sec):
    with open(statusfile,'w') as f:
        f.write(sec)
    return None

def xmlnote(orignote, num):
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
    string = instruments.num2char(num)
    out['pname'] = orignote.part
    out['mname'] = orignote.mname
    out['nname'] = orignote.nname
    out['pitch'] = '%i' % (num+midioffset)
    out['tpc'] = mapping[string[:2]]
    return out


def makequartet(mindur=8, timesig='4/4', nbars=1):
    v1 = instruments.Section(name='v1', instrument='violin', mindur=mindur, timesig=timesig, nbars=nbars)
    v2 = instruments.Section(name='v2', instrument='violin', mindur=mindur, timesig=timesig, nbars=nbars)
    va = instruments.Section(name='va', instrument='viola', mindur=mindur, timesig=timesig, nbars=nbars)
    vc = instruments.Section(name='vc', instrument='cello', mindur=mindur, timesig=timesig, nbars=nbars)
    quartet = [v1,v2,va,vc]
    qd = sc.objdict([(inst.name,inst) for inst in quartet])
    return quartet,qd


def appendnotes(nd, sec, part, verbose=False):
    for n,orignote in enumerate(nd[sec][part]):
        if verbose: print('%s. %s' % (n, instruments.num2char(qd[part].score[n])))
        note = xmlnote(orignote, qd[part].score[n])
        nd.notes.append(note)
    return None


def repeats(ss):
    return list(range(ss[1] - ss[0] + 1))


def write():
    if 'write' in torun:
        print('Writing XML')
        outputxml = musescore.XML()
        outputxml.write(data=nd.notes)
        os.system('mscore live/live.mscx -o live/live.png')
    return None


def begin(sec):
    sc.colorize('blue', '\n'*5+'Creating section %s' % sec)
    return sc.objdict()

def process(sec):
    sc.fixedpause()
    if wait or sec == 'H':
        write()
    writestatus(sec)
    print('Section %s written' % sec)
    sc.toc()
    print('\n'*5)
    nfiles = len(sc.getfilelist('live', pattern='live-*.png'))
    if nfiles != npages:
        print('WARNING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('The number of files is not correct!! %s vs %s' % (nfiles, npages))
    else:
        print('Done and all tests passed!')
    if wait:
        sc.fixedpause(pauses[sec], verbose=True)
    return None
    

#%% Main body
    
writestatus('n/a') # Reset status

if 'load' in torun:
    print('Resetting')
    sc.runcommand('./cleanup')
    print('Loading XML')
    xml = musescore.XML()
    nd = sc.objdict() # For storing all the notes
    nd.notes = []


if 'sectionA' in torun:
    sec = 'A'
    nd[sec] = begin(sec)
    process(sec)
    


if 'sectionB' in torun:
    sec = 'B'
    nd[sec] = begin(sec)
    quartet,qd = makequartet(mindur=8, timesig='12/8', nbars=1)
    
    for part,inst in qd.items():      
        if part == 'v1': ss = [39,40]
        else:            ss = [21,40]
        nd[sec][part] = xml.loadnotes(part=part, measurerange=ss)
        for repeat in repeats(ss):
            inst.seed += 1
            startval = inst.score[-1] if inst.scorepts else 'min'
            inst.brownian(maxstep=2, startval=startval, skipstart=True, inst=part, usedata=usedata)
            inst.seed += 1
            inst.cat()
        
        appendnotes(nd, sec, part)
    process(sec)


if 'sectionC' in torun:
    sec = 'C'
    nd[sec] = begin(sec)
    quartet,qd = makequartet(mindur=16, timesig='4/4', nbars=1)
    
    for part,inst in qd.items():
        if part != 'v2':
            ss = [43,60]
            nd[sec][part] = xml.loadnotes(part=part, measurerange=ss)
            
            for repeat in repeats(ss):
                inst.seed += 1
                if inst.scorepts:  startval = inst.score[-1]
                elif part == 'v1': startval = 'max'
                elif part == 'vc': startval = 'min'
                else:              startval = None
                inst.brownian(maxstep=3, startval=startval, skipstart=True, inst=part, usedata=usedata)
                inst.octotonic()
                inst.seed += 1
                inst.cat()
        
            appendnotes(nd, sec, part)
    process(sec)


if 'sectionD' in torun:
    sec = 'D'
    nd[sec] = begin(sec)
    quartet,qd = makequartet(mindur=8, timesig='4/4', nbars=1)
    
    for part,inst in qd.items():
        ss = [63,83]
        nd[sec][part] = xml.loadnotes(part=part, measurerange=ss)
        for repeat in repeats(ss):
            inst.seed += 1
            if inst.scorepts:  startval = inst.score[-1]
            inst.brownian(maxstep=5, startval=startval, skipstart=True, inst=part, usedata=usedata)
            inst.seed += 1
            inst.cat()
    
        appendnotes(nd, sec, part)
    process(sec)



if 'sectionE' in torun:
    sec = 'E'
    nd[sec] = begin(sec)
    ss = [85,98]
    nm = sc.objdict()
    seq = sc.objdict()
    for part in qd.keys():
        nm[part] = sc.objdict()
        seq[part] = 0
    quartet,qd = makequartet(mindur=8, timesig='4/4', nbars=1)

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
    generate(seq, nm, p='vc', m=86, n=1, t=1)

    generate(seq, nm, p='v2', m=87, n=1, t=1)
    generate(seq, nm, p='va', m=88, n=1, t=0)
    generate(seq, nm, p='vc', m=88, n=1, t=0)
    generate(seq, nm, p='v1', m=88, n=1, t=0)

    generate(seq, nm, p='vc', m=89, n=1, t=1)
    generate(seq, nm, p='v1', m=89, n=1, t=1)
    generate(seq, nm, p='v2', m=90, n=1, t=0)
    generate(seq, nm, p='va', m=90, n=1, t=0)
    
    # Unison
    for part in qd.keys():
        generate(seq, nm, p=part, m=91, n=1, t=0)
        generate(seq, nm, p=part, m=91, n=3, t=0)
        generate(seq, nm, p=part, m=91, n=5, t=1)
        generate(seq, nm, p=part, m=92, n=3, t=1)
        generate(seq, nm, p=part, m=93, n=3, t=0)
        generate(seq, nm, p=part, m=93, n=5, t=0)
        generate(seq, nm, p=part, m=93, n=7, t=1)
        for n in [3,5,7]:
            generate(seq, nm, p=part, m=94, n=n, t=0)
        for n in [1,3,5,7,9]:
            generate(seq, nm, p=part, m=95, n=n, t=0)
        for n in [1,3,5,7,9]:
            generate(seq, nm, p=part, m=96, n=n, t=0)
        generate(seq, nm, p=part, m=96, n=11, t=1)
        generate(seq, nm, p=part, m=97, n=3, t=0)
        generate(seq, nm, p=part, m=97, n=5, t=1)
        generate(seq, nm, p=part, m=98, n=3, t=0)
        generate(seq, nm, p=part, m=98, n=5, t=1)

    startvals1 = sc.odict([
            ('v1',instruments.char2num('en4')),
            ('v2',instruments.char2num('en3')),
            ('va',instruments.char2num('en2')),
            ('vc',instruments.char2num('en1')),
            ])
    startvals2 = sc.odict([
            ('v1',instruments.char2num('cn3')),
            ('v2',instruments.char2num('cn3')),
            ('va',instruments.char2num('cn2')),
            ('vc',instruments.char2num('cn2')),
            ])
    
    for part,inst in qd.items():
        nd[sec][part] = xml.loadnotes(part=part, measurerange=ss)
        assert len(nd[sec][part]) == len(nm[part])
        
        inst.brownian(maxstep=5, startval=startvals1[part], forcestep=True, skipstart=True, npts=3)
        inst.seed += 1
        inst.cat()
        
        inst.brownian(maxstep=3, startval=startvals2[part], forcestep=True, skipstart=True, npts=25)
        inst.octotonic()
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
                nmnotes[key] = nmnotes[val] + interval
            elif key.startswith('tied'):
                nmnotes[key] = nmnotes[val] # e.g. nmnotes['tied0_root_m98_n5'] = nmnotes['root_m98_n5'] = 36
            else:
                raise Exception('Not recognized')

        # Create new score via mapping
        inst.score = sc.dcp(nmnotes[:])
    
        appendnotes(nd, sec, part)
    process(sec)


if 'sectionF' in torun:
    print('~~~ Section F does not use the brain ~~~')
    sec = 'F'
    nd[sec] = begin(sec)
    process(sec)


if 'sectionG' in torun:
    sec = 'G'
    nd[sec] = begin(sec)
    quartet,qd = makequartet(mindur=8, timesig='4/4', nbars=1)
    
    for part,inst in qd.items():
        if   part == 'v1': ss = [143,144]
        elif part == 'vc': ss = [122,144]
        else:              ss = [133,144]
        nd[sec][part] = xml.loadnotes(part=part, measurerange=ss)
        for repeat in repeats(ss):
            inst.seed += 1
            if inst.scorepts: startval = inst.score[-1]
            inst.brownian(maxstep=5, startval=startval, skipstart=True, inst=part, usedata=usedata)
            inst.seed += 1
            inst.cat()
    
        appendnotes(nd, sec, part)
    process(sec)


if 'sectionH' in torun:
    sec = 'H'
    nd[sec] = begin(sec)
    quartet,qd = makequartet(mindur=8, timesig='12/8', nbars=1)
    
    for part,inst in qd.items():      
        if part == 'v1': ss = [147,148]
        else:            ss = [147,166]
        nd[sec][part] = xml.loadnotes(part=part, measurerange=ss)
        for repeat in repeats(ss):
            inst.seed += 1
            if inst.scorepts:         startval = inst.score[-1]
            elif part in ['v1','v2']: startval = 'max'
            elif part in ['va','vc']: startval = 'min'
            inst.brownian(maxstep=2, startval=startval, skipstart=True, inst=part, usedata=usedata)
            inst.diatonic()
            inst.octotonic()
            inst.seed += 1
            inst.cat()
        
        appendnotes(nd, sec, part)
    process(sec)


sc.toc()
print('Done.')