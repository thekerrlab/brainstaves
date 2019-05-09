'''
Record data from headset. Protocol:

./mindwave_pair
./mindwave_read
./mindwave_record # calls this file
'''

import os
import sys
import time
import pylab as pl
import bsmindwave as bsmw

secs = ['B','C','D','E','F','G','H']
names = ['v1','v2','va','vc']
count = 0
for sec in secs:
    for name in names:
        count += 1
        print('\n'*10)
        print('STARTING %s %s (%s/%s)' % (sec, name, count, len(secs)*len(names)))

        MAC = '00:81:F9:29:B4:D4'
        maxtime = 20
        delay = 0.02
        filename = '../data/run8/rawdata-%s-%s.dat' % (sec, name)
        maxcount = int(maxtime/delay)

        mw = bsmw.Mindwave(port='/dev/rfcomm0')
        mw.start()

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

        mw.stop()
        print('Done.')
