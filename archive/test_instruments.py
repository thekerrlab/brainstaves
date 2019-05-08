'''
Generate test score.
'''

import instruments as i
import spectrogram as s
import sciris as sc
import numpy as np

offset = 2824*2+np.nan

v1 = i.Section(name='v1', instrument='violin', seed=1+offset)
v2 = i.Section(name='v2', instrument='violin', seed=2+offset)
va = i.Section(name='va', instrument='viola', seed=3+offset)
vc = i.Section(name='vc', instrument='cello', seed=4+offset)
quartet = [v1,v2,va,vc]

for p in [0.5, 0.8]:
    for inst in quartet:
        inst.brownian(maxstep=4)
        if inst.name not in ['va','vc']:
            inst.diatonic()
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
data = i.play(quartet)
sc.tic()
score = i.write(quartet, export='png')
sc.toc()
#ims = s.plotstft(data)


print('Done.')