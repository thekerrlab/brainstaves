'''
Generate test score.
'''

import sciris as sc
import instruments
import parsexml

sc.tic()

torun = [
'load',
'sectionB',
'create',
'write',
]

#%% Function definitions

def xmlnote(orignote, step, alter, octave):
    out = sc.objdict()
    out['pname'] = orignote.part
    out['mname'] = orignote.mname
    out['nname'] = orignote.nname
    out['step'] = str(step).upper() # A
    out['alter'] = str(alter) # s
    if sc.isnumber(out['alter']):
        out['alter'] = str(out['alter'])
    if out['alter'] not in ['0','1','-1']:
        mapping = {'#':'1', 'n':'0', '$':'-1'}
        if out['alter'] in mapping:
            out['alter'] = mapping[out['alter']]
        else:
            errormsg = 'Not sure how to process accidental %s' % alter
            raise Exception(errormsg)
    out['octave'] = str(octave) # 4
    return out


def makequartet():
    v1 = instruments.Section(name='v1', instrument='violin')
    v2 = instruments.Section(name='v2', instrument='violin')
    va = instruments.Section(name='va', instrument='viola')
    vc = instruments.Section(name='vc', instrument='cello')
    quartet = [v1,v2,va,vc]
    qd = {inst.name:inst for inst in quartet}
    return quartet,qd


#%% Main body

if 'load' in torun:
    print('Loading XML')
    xml = parsexml.XML()
    nd = sc.objdict() # For storing all the notes


if 'sectionB' in torun:
    print('Creating section B')
    quartet,qd = makequartet()
    
    nd['B'] = sc.objdict()
    
    nd.B.startstop = sc.objdict()
    nd.B.startstop['v1'] = [39,40]
    nd.B.notes = xml.loadnotes(part='v1', measurerange=nd.B.startstop['v1'])
    
    length = 20 # How many bars it's supposed to be
    for inst in quartet:
        inst.mindur = 8
        inst.timesig = '12/8'
        inst.nbars = 1
        inst.refresh()
    
    probs = [1/12]*4 + [2/12]*2 + [3/12]*2 + [i/12 for i in range(4,12)] + [1]*4
    count = 0
    assert len(probs) == length
    for inst in quartet:
        for prob in probs:
            inst.seed += 1
            startval = inst.score[-1] if inst.scorepts else 'min'
            inst.brownian(maxstep=2, startval=startval, skipstart=True)
            inst.seed += 1
            inst.cat()


if 'create' in torun:
    print('Creating notes')
    for n,orignote in enumerate(nd.B.notes): # WARNING FIX
        nd.B.notes[n] = xmlnote(orignote,'a','$','4')


if 'write' in torun:
    print('Writing XML')
    xml.write(data=nd.B.notes, verbose=True)


sc.toc()
print('Done.')