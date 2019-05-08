import sciris as sc

delay = 5

macs = ['00:81:F9:08:A1:72',  # Mandhira -- rfcomm0
        '00:81:F9:29:BA:98', # Pat -- rfcomm1
        '00:81:F9:29:EF:80', # Rich -- rfcomm2
        'C4:64:E3:EA:75:6D' # Val -- rfcomm3
        # Spare: 00:81:F9:29:B4:D4
        ]

for mac in macs:
    print('Pairing %s...' % mac)
    string = 'bluetoothctl pair %s' % mac
    sc.runcommand(string, printinput=True, printoutput=True)
    sc.fixedpause(delay)
    
    