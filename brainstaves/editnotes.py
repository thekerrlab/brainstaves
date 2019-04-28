'''
Generate test score.
'''

import sciris as sc
import instruments
import parsexml

v1 = instruments.Section(name='v1', instrument='violin')
v2 = instruments.Section(name='v2', instrument='violin')
va = instruments.Section(name='va', instrument='viola')
vc = instruments.Section(name='vc', instrument='cello')
quartet = [v1,v2,va,vc]
qd = {inst.name:inst for inst in quartet}

xml = parsexml.XML()

nd = sc.odict() # For storing all the notes

data = []
xml.write(outfile='tmp.xml', data=data)


print('Done.')