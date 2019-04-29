'''
Generate test score.
'''

import sciris as sc
import instruments
import parsexml

sc.tic()

class note(sc.prettyobj):
    def __init__(self, part, mname, nname, step, octave):
        self.part = part
        self.step = step
        self.octave = octave
        self.pname = part
        self.mname = mname
        self.nname = nname

def makequartet():
    v1 = instruments.Section(name='v1', instrument='violin')
    v2 = instruments.Section(name='v2', instrument='violin')
    va = instruments.Section(name='va', instrument='viola')
    vc = instruments.Section(name='vc', instrument='cello')
    quartet = [v1,v2,va,vc]
    qd = {inst.name:inst for inst in quartet}
    return quartet,qd


print('Loading XML')
xml = parsexml.XML()
nd = sc.objdict() # For storing all the notes


# Section B
print('Creating Section B')
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
#        inst.addrests(prob)
        inst.cat()


print('Creating notes')
for n,orignote in enumerate(nd.B.notes):
    nd.B.notes[n] = note(orignote.part,orignote.mname,orignote.nname,'Q',4)

print('Writing XML')
xml.write(outfile='live/tmp.xml', data=nd.B.notes, verbose=True)


sc.toc()
print('Done.')