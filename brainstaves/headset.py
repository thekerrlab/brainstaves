'''
bluetoothctl
pair <mac>
sudo rfcomm connect hci0 <mac>
'''

import pylab as pl
from NeuroPy import NeuroPy

macs = ['00:81:F9:08:A1:72', '00:81:F9:29:BA:98','C4:64:E3:EA:75:6D', 'C4:64:E3:EA:75:6D']

filename = 'data-off.csv'

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
