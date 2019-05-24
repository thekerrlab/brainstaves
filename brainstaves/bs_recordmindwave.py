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

if len(sys.argv)>1:
    name = sys.argv[1]
else:
    print('Setting default')
    name = 'v1'

mapping = {'v1': '00:81:F9:08:A1:72',
           'v2': '00:81:F9:29:BA:98',
           'va': '00:81:F9:29:EF:80',
           'vc': 'C4:64:E3:EA:75:6D',}

mapping2 = {'v1': 'rfcomm0',
           'v2': 'rfcomm1',
           'va': 'rfcomm2',
           'vc': 'rfcomm3',}

import os
import sys
import time
import pylab as pl
import bsmindwave as bsmw

secs = ['B','C','D','E','F','G','H']
count = 0

mw = bsmw.Mindwave(port='/dev/%s' % mapping2[name])
mw.start()

for sec in secs:
    count += 1
    print('\n'*10)
    print('STARTING %s %s (%s/%s)' % (sec, name, count, len(secs)))

    MAC = mapping[name]
    maxtime = 20
    delay = 0.02
    filename = '../data/live/rawdata-%s-%s.dat' % (sec, name)
    maxcount = int(maxtime/delay)

    print('Recording for %s s...' % maxtime)
    data = []
    origtime = time.time()
    hz = int(1/delay)
    for i in range(maxcount):
        if not i%hz:
            print('...%s/%s' % (i+1, maxcount))
        data.append(str(mw.rawValue))
        elapsed = time.time() - (origtime + i*delay)
        remaining = delay-elapsed
        if remaining>0:
            pl.pause(remaining)
        else:
            print('Not pausing because time is negative (%s vs %s)' % (delay, elapsed))

    with open(filename,'w') as f:
        f.write('\n'.join(data))

print('Stopping...')
mw.stop()
print('Done.')
