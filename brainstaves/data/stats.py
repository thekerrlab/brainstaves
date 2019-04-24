import pylab as pl
import sciris as sc

datadir = 'apr24'
prefix = 'gooddata'
whichcols = ['all','keep'][1]
normalize = True

names = ['ck','mandhi','rich','val']
data = sc.odict()
for name in names:
    infile = datadir+'/gooddata-'+name+'.csv'
    tmpdata = []
    lines = open(infile).readlines()
    for line in lines:
        tmpdata.append([float(v) for v in line.split(', ')])
    data[name] = tmpdata


# Must match headset.py
cols =     ['attention', 'blinkStrength', 'bytesAvailable', 'delta',   'highAlpha', 'highBeta', 'lowAlpha', 'lowBeta',  'lowGamma', 'meditation', 'midGamma', 'packetsReceived', 'poorSignal', 'rawValue', 'theta']
keepcols = ['delta',      'theta',        'lowAlpha',       'highAlpha', 'lowBeta', 'highBeta', 'lowGamma', 'midGamma', 'highvslow'] # , 'poorSignal'

dfs = sc.odict()
highchans = ['lowBeta', 'highBeta', 'lowGamma', 'midGamma']
lowchans = ['delta', 'theta', 'lowAlpha', 'highAlpha']
allchans = lowchans+highchans
nchans = len(allchans)
for name in names:
    dfs[name] = sc.dataframe(cols=cols, data=data[name])
    d = dfs[name]
    high = pl.zeros(d.nrows)
    low = pl.zeros(d.nrows)
    for chan in highchans: high += d[chan].astype(float)
    for chan in lowchans:  low  += d[chan].astype(float)
    dfs[name]['highvslow'] = high/low

if normalize:
    for name in names:
        d = dfs[name]
        tot = 0
        for chan in allchans:
            tot += d[chan].sum()
        tot /= (d.nrows*nchans)
        print('Total for %s: %s' % (name, tot))
        for chan in allchans:
            d[chan] /= tot
        
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
    for name,df in dfs.items():
        pl.plot(df[col], label=name)
    pl.legend()
        
# Plot mean statistics
makefig()
for c,col in enum():
    subplot(c,col)
    for n,name,df in dfs.enumitems():
        x = df[col]
        me = x.mean()
        std = x.std()
        sem = x.std()/pl.sqrt(len(x))
        err = 2*sem
        pl.bar(n+1, me, yerr=err, label=name)
    pl.legend()
        
# Plot CDFs
makefig()
for c,col in enum():
    subplot(c,col)
    for name,df in dfs.items():
        x = df[col]
        x = sorted(x)
        y = pl.linspace(0,1,len(x))
        pl.plot(x, y, label=name)
    pl.legend()

print('Done.')