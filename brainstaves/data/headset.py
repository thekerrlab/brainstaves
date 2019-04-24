'''
Record data from headset. Super abbreviated guide to what you need to do first:

bluetoothctl
pair <mac>
sudo rfcomm connect hci0 <mac>
'''

import sys
import pylab as pl
from NeuroPy import NeuroPy


if len(sys.argv)>1:
    who = sys.argv[1]
else:
    print('Setting default')
    who = 'mandhi'

print('FIX MAPPING')
mapping = {'val': 'rfcomm0',
           'pat': 'rfcomm1',
           'rich': 'rfcomm2',
           'mandhi': 'rfcomm1',}

macs = ['00:81:F9:08:A1:72',  # Mandhira -- rfcomm3
        '00:81:F9:29:BA:98', # Rich -- rfcomm2
        '00:81:F9:29:EF:80', # Val -- rfcomm0
        'C4:64:E3:EA:75:6D' # Pat -- rfcomm1
        ]

filename = 'newnewdata-%s.csv' % who

attrs = ['attention', 'blinkStrength', 'bytesAvailable', 'delta', 'highAlpha', 'highBeta', 'lowAlpha', 'lowBeta', 'lowGamma', 'meditation', 'midGamma', 'packetsReceived', 'poorSignal', 'rawValue', 'theta']

neuropy = NeuroPy(port='/dev/%s' % mapping[who])
neuropy.start()
maxcount = 300
for i in range(maxcount):
    reading = []
    for attr in attrs:
        reading.append(str(getattr(neuropy, attr)))
    with open(filename,'a') as f:
        f.write(', '.join(reading) + '\n')
    count = '%i/%i: ' % (i+1,maxcount)
    print(count),
    print(reading)
    pl.pause(1)

neuropy.stop()
