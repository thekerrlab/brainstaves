'''
Generate test score.
'''

import sciris as sc
import instruments
import musescore

sc.tic()

torun = [
'load',
'sectionB',
'sectionC',
'sectionD',
'sectionE',
'sectionF',
'sectionG',
'sectionH',
'write',
]

midioffset = 24

#%% Function definitions

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

#%% Main body

if 'load' in torun:
    print('Loading XML')
    xml = musescore.XML()
    nd = sc.objdict() # For storing all the notes
    nd.notes = []


if 'sectionB' in torun:
    print('Creating section B')
    sec = 'B'
    quartet,qd = makequartet(mindur=8, timesig='12/8', nbars=1)
    nd[sec] = sc.objdict()
    
    for part,inst in qd.items():      
        if part == 'v1': ss = [39,40]
        else:            ss = [21,40]
        nd[sec][part] = xml.loadnotes(part=part, measurerange=ss)
        for repeat in repeats(ss):
            inst.seed += 1
            startval = inst.score[-1] if inst.scorepts else 'min'
            inst.brownian(maxstep=2, startval=startval, skipstart=True)
            inst.seed += 1
            inst.cat()
        
        appendnotes(nd, sec, part)


if 'sectionC' in torun:
    print('Creating section C')
    sec = 'C'
    quartet,qd = makequartet(mindur=16, timesig='4/4', nbars=1)
    nd[sec] = sc.objdict()
    
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
                inst.brownian(maxstep=3, startval=startval, skipstart=True)
                inst.seed += 1
                inst.cat()
        
            appendnotes(nd, sec, part)


if 'sectionD' in torun:
    print('Creating section D')
    sec = 'D'
    quartet,qd = makequartet(mindur=8, timesig='4/4', nbars=1)
    nd[sec] = sc.objdict()
    
    for part,inst in qd.items():
        ss = [63,83]
        nd[sec][part] = xml.loadnotes(part=part, measurerange=ss)
        for repeat in repeats(ss):
            inst.seed += 1
            if inst.scorepts:  startval = inst.score[-1]
            inst.brownian(maxstep=5, startval=startval, skipstart=True)
            inst.seed += 1
            inst.cat()
    
        appendnotes(nd, sec, part)


if 'sectionE' in torun:
    print('*********E NOT READY***************')
#    sec = 'D'
#    quartet,qd = makequartet(mindur=8, timesig='4/4', nbars=1)
#    nd[sec] = sc.objdict()
#    
#    for part,inst in qd.items():
#        ss = [63,83]
#        nd[sec][part] = xml.loadnotes(part=part, measurerange=ss)
#        for repeat in repeats(ss):
#            inst.seed += 1
#            if inst.scorepts:  startval = inst.score[-1]
#            inst.brownian(maxstep=5, startval=startval, skipstart=True)
#            inst.seed += 1
#            inst.cat()
#    
#        appendnotes(nd, sec, part)


if 'sectionG' in torun:
    print('Creating section G')
    sec = 'G'
    quartet,qd = makequartet(mindur=8, timesig='4/4', nbars=1)
    nd[sec] = sc.objdict()
    
    for part,inst in qd.items():
        if   part == 'v1': ss = [140,141]
        elif part == 'vc': ss = [119,141]
        else:              ss = [130,163]
        nd[sec][part] = xml.loadnotes(part=part, measurerange=ss)
        for repeat in repeats(ss):
            inst.seed += 1
            if inst.scorepts: startval = inst.score[-1]
            inst.brownian(maxstep=5, startval=startval, skipstart=True)
            inst.seed += 1
            inst.cat()
    
        appendnotes(nd, sec, part)


if 'sectionH' in torun:
    print('Creating section H')
    sec = 'H'
    quartet,qd = makequartet(mindur=8, timesig='12/8', nbars=1)
    nd[sec] = sc.objdict()
    
    for part,inst in qd.items():      
        if part == 'v1': ss = [144,145]
        else:            ss = [144,163]
        nd[sec][part] = xml.loadnotes(part=part, measurerange=ss)
        for repeat in repeats(ss):
            inst.seed += 1
            if inst.scorepts:         startval = inst.score[-1]
            elif part in ['v1','v2']: startval = 'max'
            elif part in ['va','vc']: startval = 'min'
            inst.brownian(maxstep=2, startval=startval, skipstart=False)
            inst.seed += 1
            inst.cat()
        
        appendnotes(nd, sec, part)


if 'write' in torun:
    print('Writing XML')
    xml.write(data=nd.notes)


sc.toc()
print('Done.')