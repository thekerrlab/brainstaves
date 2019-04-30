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
#'sectionC',
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


def makequartet():
    v1 = instruments.Section(name='v1', instrument='violin')
    v2 = instruments.Section(name='v2', instrument='violin')
    va = instruments.Section(name='va', instrument='viola')
    vc = instruments.Section(name='vc', instrument='cello')
    quartet = [v1,v2,va,vc]
    qd = sc.objdict([(inst.name,inst) for inst in quartet])
    return quartet,qd


#%% Main body

if 'load' in torun:
    print('Loading XML')
    xml = musescore.XML()
    nd = sc.objdict() # For storing all the notes
    nd.notes = []


if 'sectionB' in torun:
    print('Creating section B')
    sec = 'B'
    quartet,qd = makequartet()
    nd[sec] = sc.objdict()
    nd.B.startstop = sc.objdict()
    
    for part,inst in qd.items():
        inst.mindur = 8
        inst.timesig = '12/8'
        inst.nbars = 1
        inst.refresh()
        
        if part == 'v1':
            nd[sec].startstop[part] = [39,40]
            probs = [1,1]
        else:
            nd[sec].startstop[part] = [21,40]
            probs = [1/12]*4 + [2/12]*2 + [3/12]*2 + [i/12 for i in range(4,12)] + [1]*4
        
        print(part)
        print(probs)
    
        nd[sec][part] = xml.loadnotes(part=part, measurerange=nd[sec].startstop[part])
        
        for prob in probs:
            inst.seed += 1
            startval = inst.score[-1] if inst.scorepts else 'min'
            inst.brownian(maxstep=2, startval=startval, skipstart=True)
            inst.seed += 1
            inst.cat()
    
        for n,orignote in enumerate(nd[sec][part]):
            print('%s. %s' % (n, instruments.num2char(qd[part].score[n])))
            note = xmlnote(orignote, qd[part].score[n])
            nd.notes.append(note)


if 'sectionC' in torun:
    print('Creating section C')
    sec = 'C'
    quartet,qd = makequartet()
    nd[sec] = sc.objdict()
    nd[sec].startstop = sc.objdict()
    
    for part,inst in qd.items():
        inst.mindur = 16
        inst.timesig = '4/4'
        inst.nbars = 1
        inst.refresh()
        
        if part != 'v2':
            nd[sec].startstop[part] = [43,60]
            probs = [1]*4 + [i/10 for i in range(9,2,-1)] + [0.2]*2 + [0.1]*2 + [0.05]*3
    
        nd.C[part] = xml.loadnotes(part=part, measurerange=nd[sec].startstop[part])
        
        for prob in probs:
            inst.seed += 1
            startval = inst.score[-1] if inst.scorepts else 'min'
            inst.brownian(maxstep=2, startval=startval, skipstart=True)
            inst.seed += 1
            inst.cat()
    
        for n,orignote in enumerate(nd.B[part]):
            print('%s. %s' % (n, instruments.num2char(qd.v1.score[n])))
            note = xmlnote(orignote, qd.v1.score[n])
            nd.notes.append(note)


if 'write' in torun:
    print('Writing XML')
    xml.write(data=nd.notes, verbose=True)


sc.toc()
print('Done.')