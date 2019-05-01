import sounddevice as sd
import pylab as pl
import spectrogram as s

duration = 1
fs = 44100

arrs = []

print('Recording...')
stop = False
while not stop:
    try:
        tmp = sd.rec(int(duration * fs), samplerate=fs, channels=2, blocking=True)
        arrs.append(tmp)
    except:
        stop = True

arr = pl.concatenate(arrs)

print('Plotting...')
pl.plot(arr)
ims = s.plotstft(arr)
#pl.ylim([0,1000])
pl.pause(0.2)

#import os
#print('Saving...')
#pl.savefig('tmp.png')
#print('Publishing...')
#os.system('scp -r "tmp.png" cliffker@cliffkerr.com:/home3/cliffker/public_html/thekerrlab/tmp/')

print('Done.')