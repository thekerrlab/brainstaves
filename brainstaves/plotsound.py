import os
import sounddevice as sd
import pylab as pl
import spectrogram as s

duration = 5
fs = 44100

print('Recording...')
arr = sd.rec(int(duration * fs), samplerate=fs, channels=2, blocking=True)

print('Plotting...')
pl.plot(arr)
ims = s.plotstft(arr)
pl.pause(0.2)

print('Saving...')
pl.savefig('tmp.png')
print('Publishing...')
os.system('scp -r "tmp.png" cliffker@cliffkerr.com:/home3/cliffker/public_html/thekerrlab/tmp/')

print('Done.')