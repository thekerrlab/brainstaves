'''
Generate test score.
'''

import instruments as i
import spectrogram as s
import sciris as sc
import numpy as np

offset = 2824*3#+np.nan

v1 = i.Section(name='v1', instrument='violin', seed=1+offset, mindur=16)
v2 = i.Section(name='v2', instrument='violin', seed=2+offset, mindur=16)
va = i.Section(name='va', instrument='viola', seed=3+offset, mindur=16)
vc = i.Section(name='vc', instrument='cello', seed=4+offset, mindur=16)
quartet = [v1,v2,va,vc]

for p in [1.0, 1.0]:
    for inst in quartet:
        inst.brownian(maxstep=4)
#        if inst.name not in ['va','vc']:
#            inst.diatonic()
        inst.addrests(p=p)
        inst.cat()
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
    


#fig = i.plot(quartet)
#data = i.play(quartet)
sc.tic()
score = i.write(quartet, infile='brainstaves-B.ly', export='png')
sc.toc()
#ims = s.plotstft(data)


print('Done.')