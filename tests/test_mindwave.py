'''
Record data from headset. Super abbreviated guide to what you need to do first:

# Test headset
bluetoothctl pair 00:81:F9:29:B4:D4 # in terminal 1
sudo rfcomm connect hci0 00:81:F9:29:B4:D4 # in terminal 2
sudo python3 test_mindwave.py # in terminal 3

OR

# V1 headset
bluetoothctl pair 00:81:F9:08:A1:72 # equivalent of bt_pair
sudo rfcomm connect hci0 00:81:F9:08:A1:72 # equivalent of bt_read v1
python test_mindwave.py

00:81:F9:08:A1:72
'''

import os
import sys
import pylab as pl
import bsmindwave as bsmw

MAC = '00:81:F9:29:B4:D4'

def spacer():
    return print('\n'*5)

# Commands


attrs = ['attention', 'blinkStrength', 'bytesAvailable', 'delta', 'highAlpha', 'highBeta', 'lowAlpha', 'lowBeta', 'lowGamma', 'meditation', 'midGamma', 'packetsReceived', 'poorSignal', 'rawValue', 'theta']

mw = bsmw.Mindwave(port='/dev/rfcomm0')
mw.start()
maxcount = 600
for i in range(maxcount):
   reading = []
   for attr in attrs:
       reading.append(str(getattr(mw, attr)))
   # with open(filename,'a') as f:
   #     f.write(', '.join(reading) + '\n')
   count = '%i/%i: ' % (i+1,maxcount)
   print(count),
   print(reading)
   pl.pause(1)

mw.stop()
