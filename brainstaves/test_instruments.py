import instruments as i
import spectrogram as s
import sciris as sc

offset = 2824*2

v1 = i.Section(name='v1', instrument='violin', seed=1+offset)
v2 = i.Section(name='v2', instrument='violin', seed=2+offset)
va = i.Section(name='va', instrument='viola', seed=3+offset)
vc = i.Section(name='vc', instrument='cello', seed=4+offset)
quartet = [v1,v2,va,vc]

for inst in quartet:
    inst.brownian(maxstep=4)
    inst.diatonic()
    inst.octotonic()

for inst in quartet:
    inst.addrests(p=1.0)


#fig = i.plot(quartet)
#data = i.play(quartet)
sc.tic()
score = i.write(quartet)
sc.toc()
#ims = s.plotstft(data)


print('Done.')