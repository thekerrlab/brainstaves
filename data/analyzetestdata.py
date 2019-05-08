'''
Process statistics on prerecorded data.
'''

import pylab as pl
import sciris as sc

whichcols = ['all','keep', 'raw'][0]
normalize = True
dosave = True
infile = '../tests/testdata.csv'

data = []
lines = open(infile).readlines()
for line in lines:
    data.append([float(v) for v in line.split(', ')])

# Must match headset.py
cols =     ['attention', 'blinkStrength', 'bytesAvailable', 'delta',   'highAlpha', 'highBeta', 'lowAlpha', 'lowBeta',  'lowGamma', 'meditation', 'midGamma', 'packetsReceived', 'poorSignal', 'rawValue', 'theta']
keepcols = ['delta',      'theta',        'lowAlpha',       'highAlpha', 'lowBeta', 'highBeta', 'lowGamma', 'midGamma', 'highvslow'] # , 'poorSignal'

highchans = ['lowBeta', 'highBeta', 'lowGamma', 'midGamma']
lowchans = ['delta', 'theta', 'lowAlpha', 'highAlpha']
allchans = lowchans+highchans
nchans = len(allchans)

d = sc.dataframe(cols=cols, data=data)
high = pl.zeros(d.nrows)
low = pl.zeros(d.nrows)
for chan in highchans: high += d[chan].astype(float)
for chan in lowchans:  low  += d[chan].astype(float)

if normalize:
    tot = 0
    for chan in allchans:
        tot += d[chan].sum()
    tot /= (d.nrows*nchans)
    print('Total: %s' % (tot))
    for chan in allchans:
        d[chan] /= tot

if dosave:
    sc.saveobj('data-may08.obj', d)
        
def makefig():
    pl.figure(figsize=(30,16))

def enum():
    if   whichcols == 'all':  return enumerate(cols)
    elif whichcols == 'keep': return enumerate(keepcols)

def subplot(c,col):
    if   whichcols == 'all':  pl.subplot(5,3,c+1)
    elif whichcols == 'keep': pl.subplot(3,3,c+1)
    pl.title(col)
    
# Plot time series
makefig()
for c,col in enum():
    subplot(c,col)
    pl.plot(d[col], label='test')
    pl.legend()
        
# Plot mean statistics
makefig()
for c,col in enum():
    subplot(c,col)
    x = d[col]
    me = x.mean()
    std = x.std()
    sem = x.std()/pl.sqrt(len(x))
    err = 2*sem
    pl.bar(1, me, yerr=err, label='test')
    pl.legend()
        
# Plot CDFs
makefig()
for c,col in enum():
    subplot(c,col)
    x = d[col]
    x = sorted(x)
    y = pl.linspace(0,1,len(x))
    pl.plot(x, y, label='test')
    pl.legend()

print('Done.')