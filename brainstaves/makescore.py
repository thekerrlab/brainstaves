'''
Generate test score.
'''

import instruments as i
import spectrogram as s
import sciris as sc
import numpy as np

doplot  = 1
doplay  = 0
dowrite = 1

section = 'E'
offset = 2824*6#+np.nan
offsetdict = {'B': 2824*4,
              'C': 2824*4, # Not a typo...
              'E': 2824*6}

v1 = i.Section(name='v1', instrument='violin', seed=1*offset)
v2 = i.Section(name='v2', instrument='violin', seed=2*offset)
va = i.Section(name='va', instrument='viola', seed=3*offset)
vc = i.Section(name='vc', instrument='cello', seed=4*offset)
quartet = [v1,v2,va,vc]


if section == 'B':
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
            inst.addrests(prob)
            inst.cat()

if section == 'C':
    length = 18 # How many bars it's supposed to be
    for inst in quartet:
        inst.mindur = 16
        inst.timesig = '4/4'
        inst.nbars = 1
        inst.refresh()
    
    probs = [1]*4 + [i/10 for i in range(9,2,-1)] + [0.2]*2 + [0.1]*2 + [0.05]*3
    count = 0
    assert len(probs) == length
    for inst in quartet:
        for prob in probs:
            inst.seed += 1
            startval = inst.score[-1] if inst.scorepts else 'max'
            inst.brownian(maxstep=2, startval=startval, forcestep=True, skipstart=True)
            inst.seed += 1
            inst.addrests(prob)
            inst.cat()

if section == 'E':
    length = 6 # How many bars it's supposed to be
    for inst in quartet:
        inst.mindur = 8
        inst.timesig = '4/4'
        inst.nbars = 1
        inst.refresh()
    
    probs = [0.1, 0.1, 0.2, 0.3, 0.4, 0.5]
    count = 0
    assert len(probs) == length
    for inst in quartet:
        for p,prob in enumerate(probs):
            inst.seed += 1
            startval = inst.score[-1] if inst.scorepts else 40
            inst.brownian(maxstep=2, startval=startval, forcestep=True, skipstart=True)
            inst.seed += 1
            inst.addrests(prob, seed=p)
            inst.cat()



#        if inst.name not in ['va','vc']:
#            inst.diatonic()
#        inst.addrests(p=p)
#        inst.cat()
#        inst.diatonic()
#        inst.octotonic()
    
#for maxstep in [1,2,4]:
#    for inst in quartet:
#        inst.brownian(maxstep=maxstep)
#        inst.octotonic()
#        inst.cat()
#
#for repeats in [1,2]:
#    for inst in quartet:
#        inst.brownian(maxstep=maxstep)
#        inst.diatonic()
#        inst.octotonic()
#        inst.addrests(p=0.7)
#        inst.cat()
#
#for repeats in [1,2]:
#    for inst in quartet:
#        inst.brownian(maxstep=maxstep)
#        inst.diatonic()
##        inst.octotonic()
#        inst.addrests(p=1.0)
#        inst.cat()
    


if doplot:    fig = i.plot(quartet)
if doplay:   data = i.play(quartet)
if dowrite: score = i.write(quartet, infile='brainstaves-%s.ly' % section, export='pdf')


print('Done.')