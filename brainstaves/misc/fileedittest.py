#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 23:45:20 2019

@author: cliffk
"""

import sciris as sc

infile = 'live/template-a.xml'
outfile = 'live/brainstaves-a.xml'

print('Opening file...')
sc.tic()
lines = open(infile).readlines()
sc.toc()

print('Editing file...')
for l,line in enumerate(lines):
    lines[l] = line.replace('<step>G</step>', '<step>A</step>')
    

print('Writing file...')
sc.tic()
output = ''.join(lines)
with open(outfile, 'w') as f:
    f.write(output)
sc.toc()

print('Done.')