'''
Generate test score.
'''

import sciris as sc
import instruments
import parsexml



class note(sc.prettyobj):
    def __init__(self, part, measure, note, step, octave):
        self.part = part
        self.measure = measure
        self.note = note
        self.step = step
        self.octave = octave
        self.pname = part
        self.mname = 'm%i' % measure
        self.nname = 'n%i' % note

def makequartet():
    v1 = instruments.Section(name='v1', instrument='violin')
    v2 = instruments.Section(name='v2', instrument='violin')
    va = instruments.Section(name='va', instrument='viola')
    vc = instruments.Section(name='vc', instrument='cello')
    quartet = [v1,v2,va,vc]
    qd = {inst.name:inst for inst in quartet}
    return quartet,qd

xml = parsexml.XML()

nd = sc.objdict() # For storing all the notes


## Section B
quartet,qd = makequartet()

nd['B'] = sc.objdict()

nd.B.startstop = sc.objdict()
nd.B.startstop['v1'] = [39,40]
nd.B.notes = []

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
#        inst.addrests(prob)
        inst.cat()

n = note('v2',30,0,'A',4)
nd.B.notes = [n]
xml.write(outfile='live/tmp.xml', data=nd.B.notes)


print('Done.')