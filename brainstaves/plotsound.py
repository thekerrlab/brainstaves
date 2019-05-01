import os
import sounddevice as sd
import pylab as pl
import spectrogram as s

duration = 1
fs = 44100
saveupload = False


arrs = []

print('Recording, Ctrl+C to stop...')
stop = False
while not stop:
    try:
        tmp = sd.rec(int(duration * fs), samplerate=fs, channels=2, blocking=True)
        arrs.append(tmp)
    except:
        print('Stopping...')
        stop = True

arr = pl.concatenate(arrs)

print('Plotting...')
xax = pl.arange(len(arr))/float(fs)
pl.plot(xax, arr)
pl.xlabel('Time (s)')

ims = s.plotstft(arr)
pl.pause(0.2)

if saveupload:
    print('Saving...')
    pl.savefig('tmp.png')
    print('Publishing...')
    os.system('scp -r "tmp.png" cliffker@cliffkerr.com:/home3/cliffker/public_html/thekerrlab/tmp/')

print('Done.')