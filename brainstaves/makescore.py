'''
Generate test score.
'''

import instruments as i
import spectrogram as s
import sciris as sc
import numpy as np

doplot  = 1
doplay  = 0
dowrite = 0

offset = 2824*3#+np.nan

section = 'A'

v1 = i.Section(name='v1', instrument='violin', seed=1+offset)
v2 = i.Section(name='v2', instrument='violin', seed=2+offset)
va = i.Section(name='va', instrument='viola', seed=3+offset)
vc = i.Section(name='vc', instrument='cello', seed=4+offset)
quartet = [v1,v2,va,vc]


if section == 'A':
    length = 22 # How many bars it's supposed to be
    for inst in quartet:
        inst.mindur = 8
        inst.timesig = '12/8'
        inst.nbars = 1
        inst.refresh()
    
    probs = [1/12]*4 + [2/12]*3 + [3/12]*2 + [4/12]*2 + [i/12 for i in range(5,12)] + [1]*4
    assert len(probs) == length
    for prob in probs:
        for inst in quartet:
            inst.brownian(maxstep=2, startval='min')
            inst.addrests(prob)
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
if dowrite: score = i.write(quartet, infile='brainstaves-A.ly', export='pdf')


print('Done.')