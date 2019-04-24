import sounddevice as sd
import pylab as pl
import spectrogram as s

duration = 120
fs = 44100

arr = sd.rec(int(duration * fs), samplerate=fs, channels=2, blocking=True)

pl.plot(arr)

ims = s.plotstft(arr)

print('Done.')