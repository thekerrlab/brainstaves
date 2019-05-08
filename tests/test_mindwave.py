'''
Record data from headset. Protocol:

./mindwave_pair
./mindwave_read
./mindwave_record # calls this file
'''

import os
import sys
import pylab as pl
import bsmindwave as bsmw

MAC = '00:81:F9:29:B4:D4'
maxtime = 10
delay = 0.001
filename = 'testdata.csv'

attrs = ['attention', 'blinkStrength', 'bytesAvailable', 'delta', 'highAlpha', 'highBeta', 'lowAlpha', 'lowBeta', 'lowGamma', 'meditation', 'midGamma', 'packetsReceived', 'poorSignal', 'rawValue', 'theta']
maxcount = int(maxtime/delay)
alldata = []
mw = bsmw.Mindwave(port='/dev/rfcomm0')
mw.start()
for i in range(maxcount):
    reading = []
    for attr in attrs:
        reading.append(str(getattr(mw, attr)))
    alldata.append(reading)
    count = '%i/%i: ' % (i+1,maxcount)
    print(count),
    print(reading)
    pl.pause(delay)

with open(filename,'w') as f:
    for reading in alldata:
        f.write(', '.join(reading) + '\n')

mw.stop()
