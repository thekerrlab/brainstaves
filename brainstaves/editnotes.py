'''
Generate test score.
'''

import sciris as sc
import instruments
import parsexml

v1 = instruments.Section(name='v1', instrument='violin')
v2 = instruments.Section(name='v2', instrument='violin')
va = instruments.Section(name='va', instrument='viola')
vc = instruments.Section(name='vc', instrument='cello')
quartet = [v1,v2,va,vc]
qd = {inst.name:inst for inst in quartet}

xml = parsexml.XML()

nd = sc.odict() # For storing all the notes

#if section == 'B':
#    length = 20 # How many bars it's supposed to be
#    for inst in quartet:
#        inst.mindur = 8
#        inst.timesig = '12/8'
#        inst.nbars = 1
#        inst.refresh()
#    
#    probs = [1/12]*4 + [2/12]*2 + [3/12]*2 + [i/12 for i in range(4,12)] + [1]*4
#    count = 0
#    assert len(probs) == length
#    for inst in quartet:
#        for prob in probs:
#            inst.seed += 1
#            startval = inst.score[-1] if inst.scorepts else 'min'
#            inst.brownian(maxstep=2, startval=startval, skipstart=True)
#            inst.seed += 1
#            inst.addrests(prob)
#            inst.cat()
#
#if section == 'C':
#    length = 18 # How many bars it's supposed to be
#    for inst in quartet:
#        inst.mindur = 16
#        inst.timesig = '4/4'
#        inst.nbars = 1
#        inst.refresh()
#    
#    probs = [1]*4 + [i/10 for i in range(9,2,-1)] + [0.2]*2 + [0.1]*2 + [0.05]*3
#    count = 0
#    assert len(probs) == length
#    for inst in quartet:
#        for prob in probs:
#            inst.seed += 1
#            startval = inst.score[-1] if inst.scorepts else 'max'
#            inst.brownian(maxstep=2, startval=startval, forcestep=True, skipstart=True)
#            inst.seed += 1
#            inst.addrests(prob)
#            inst.cat()
#
#if section == 'E':
#    length = 8 # How many bars it's supposed to be
#    for inst in quartet:
#        inst.mindur = 8
#        inst.timesig = '4/4'
#        inst.nbars = 1
#        inst.refresh()
#    
#    probs = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.5, 0.3]
#    count = 0
#    assert len(probs) == length
#    for inst in quartet:
#        for p,prob in enumerate(probs):
#            inst.seed += 1
#            startval = inst.score[-1] if inst.scorepts else 40
#            inst.brownian(maxstep=2, startval=startval, forcestep=True, skipstart=True) # Revise maxstep=2?
#            inst.seed += 1
#            inst.addrests(prob, seed=p+100) # This makes it rhythmic unison
#            inst.cat()
#
#
#if section == 'F':
#    length = 13 # How many bars it's supposed to be
#    for inst in quartet:
#        inst.mindur = 16
#        inst.timesig = '4/4'
#        inst.nbars = 1
#        inst.refresh()
#    
#    probs = [0.4]*13
#    count = 0
#    assert len(probs) == length
#    for ii,inst in enumerate(quartet):
#        for p,prob in enumerate(probs):
#            inst.seed += 1
#            startval = 50-7*ii
#            inst.brownian(maxstep=0, startval=startval, forcestep=False, skipstart=False) # Revise maxstep=2?
#            inst.seed += 1
#            inst.addrests(prob)
#            inst.cat()
#
#
#
#    
#
#
#if doplot:    fig = i.plot(quartet)
#if doplay:   data = i.play(quartet)
#if dowrite: score = i.write(quartet, infile='brainstaves-%s.ly' % section, export='pdf')


print('Done.')