#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 14:41:19 2019

@author: cliffk
"""

import sciris as sc

def initlivedata(livedatafile=None, datasecs=None, allparts=None, overwrite=False, verbose=True):
    couldload = False
    try:
        livedata = sc.loadobj(livedatafile)
        couldload = True
    except:
        couldload = False
    if not couldload or overwrite:
        livedata = sc.prettyobj()
        livedata.sec = 'n/a'
        livedata.notes = sc.objdict()
        livedata.data = sc.objdict()
        for sec in datasecs:
            livedata.notes[sec] = sc.objdict()
            livedata.data[sec] = sc.objdict()
            for part in allparts:
                livedata.notes[sec][part] = []
                livedata.data[sec][part] = []
        
        livedata.isrunning = False
        livedata.started = sc.objdict()
        livedata.page = sc.objdict()
        for part in allparts:
            livedata.started[part] = False
            livedata.page[part] = 0
        sc.saveobj(livedatafile, livedata)
    if verbose: print(livedata)
    return livedata


def pagestosec(livedata, verbose=True):
    pages = livedata.pages[:]
    minpage = min(pages)
    livesec = ''
    if minpage>=1:  livesec = 'A'
    if minpage>=2:  livesec = 'B'
    if minpage>=4:  livesec = 'C'
    if minpage>=6:  livesec = 'D'
    if minpage>=7:  livesec = 'E'
    if minpage>=8:  livesec = 'F'
    if minpage>=10: livesec = 'G'
    if minpage>=12: livesec = 'H'
    if verbose: print('Pages %s, minpage %s, livesec %s' % (pages, minpage, livesec))
    return livesec


def loadlivedata(livedatafile=None):
    livedata = None
    try:
        livedata = sc.loadobj(livedatafile)
    except Exception as E:
        print('Live data file file not found: %s' % str(E))
    return livedata

def savelivedata(livedatafile=None, livedata=None):
    sc.saveobj(livedatafile, livedata)
    return None

def checkstatus(which=None, livedata=None):
    tmp = []
    for key,val in getattr(livedata,which).items(): # Should've made it an objdict...
        tmp.append('%s: %s' % (key,val))
    string = '; '.join(tmp)
    return string

def allstarted(livedata, verbose=True):
    vals = livedata.started[:].tolist()
    if verbose: print('Checking started: %s' % vals)
    return all(vals)