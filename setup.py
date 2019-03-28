#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from setuptools import setup, find_packages

with open("brainstaves/version.py", "r") as f:
    version_file = {}
    exec(f.read(), version_file)
    version = version_file["__version__"]

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
    'Programming Language :: Python :: 3.7',
]

setup(
    name='brainstaves',
    version=version,
    author='Cliff Kerr',
    author_email='info@cliffkerr.com',
    description='Composition for string quartet and EEG',
    url='http://github.com/thekerrlab/brainstaves',
    keywords=['string quartet', 'EEG', 'music', 'MindWave', 'machine learning'],
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'scirisweb',
    ],
)