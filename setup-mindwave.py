#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from setuptools import setup, find_packages

try:
    from pypandoc import convert
except ImportError:
    import io

    def convert(filename, fmt):
        with io.open(filename, encoding='utf-8') as fd:
            return fd.read()

CLASSIFIERS = [
    'Environment :: Console',
    'Intended Audience :: Music',
    'License :: OSI Approved :: GPLv3',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Development Status :: 1',
    'Programming Language :: Python :: 2.7',
]

setup(
    name='bsmindwave',
    version='2.0.0',
    author='Cliff Kerr',
    author_email='info@cliffkerr.com',
    description='Mindwave Mobile for Brainstaves',
    url='http://github.com/thekerrlab/brainstaves',
    keywords=['string quartet', 'EEG', 'music', 'MindWave', 'machine learning'],
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'matplotlib==3.0.3',
        'scipy==1.2.1', # Note: also need package serial, but should be pre-installed for Python 2
    ],
)