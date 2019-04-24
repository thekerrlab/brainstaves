import pylab as pl
from NeuroPy import NeuroPy

filename = 'data.csv'

attrs = ['attention', 'blinkStrength', 'bytesAvailable', 'delta', 'highAlpha', 'highBeta', 'lowAlpha', 'lowBeta', 'lowGamma', 'meditation', 'midGamma', 'packetsReceived', 'poorSignal', 'rawValue', 'theta']

neuropy = NeuroPy()
neuropy.start()
for i in range(60):
    reading = []
    for attr in attrs:
        reading.append(str(getattr(neuropy, attr)))
    with open(filename,'a') as f:
        f.write(', '.join(reading) + '\n')
    print(reading)
    pl.pause(1)

neuropy.stop()
