import instruments as i
import spectrogram as s

offset = 2824

v1 = i.Section(instrument='violin', seed=1+offset)
v2 = i.Section(instrument='violin', seed=2+offset)
va = i.Section(instrument='viola', seed=3+offset)
vc = i.Section(instrument='cello', seed=4+offset)
quartet = [v1,v2,va,vc]

for inst in quartet:
    inst.brownian(maxstep=1)
#    inst.diatonic()
#    inst.octotonic()

for inst in quartet:
    inst.addrests(p=0.8)


#fig = i.plot(quartet)

data = i.play(quartet)

#score = i.write(quartet)

ims = s.plotstft(data, 44100)


print('Done.')