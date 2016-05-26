#!/usr/bin/env python

# This is only for Python 2.7
from __future__ import print_function

import os, sys
import distutils.core, distutils.file_util
from glob import glob

#sys.path.insert(0, '.')
#from datconv_pkg.version import *


if os.name == 'posix':
    doclocation = 'share/doc/datconv_test'
else:
    doclocation = 'doc/datconv_test'

if os.name == 'posix':
    testlocation = 'share/datconv_test'
else:
    testlocation = 'datconv_test'
testfiles = glob('tests/*')
testfiles.remove('tests/data_in')

if os.name == 'posix':
    datalocation = 'share/datconv_test/data_in'
else:
    datalocation = 'datconv_test/data_in'

with open('README.md') as f:
    long_descr = ''
    in_desc = False
    for line in f:
        if in_desc:
            if line.strip() == '':
                break
            long_descr = long_descr + line
        if line.startswith('## DESCRIPTION:'):
            in_desc = True

dist = distutils.core.setup(name = 'datconv_test',
    version = '0.1.0',
    description = 'Testing scripts for datconv package',
    long_description = long_descr,
    author = 'Grzegorz Wierzchowski',
    author_email = 'gwierzchowski@wp.pl',
    url = 'https://github.com/gwierzchowski/datconv',
    packages = ['datconv_test'],
    scripts = ['datconv_tests2', 'datconv_tests3'],
    data_files = [(doclocation, ['README.md', 'LICENSE.txt', 'Changelog.md']),
                  (testlocation, testfiles),
                  (datalocation, glob('tests/data_in/*'))],
    requires = ['datconv'],
    license = 'PSF',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
    )

if sys.argv[1] in ['install']:
    # Unfotunately while installing using pip those print statements does not work on Windows
    print ('---------------------------------------------------------')
    try:
        import datconv
    except ImportError:
        print ('To run this software install package datconv')
    isobj = dist.get_command_obj('install_data')
    readmedoc = None
    for doc in isobj.get_outputs():
        if 'README.md' in doc:
            readmedoc = doc
            break
    if readmedoc:
        print ('See %s file' % readmedoc)
    else:
        print ('See files deployed to documentation folder')
    print ('---------------------------------------------------------')
