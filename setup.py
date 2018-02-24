#!/usr/bin/env python

# This is only for Python 2.7
from __future__ import print_function

import os, sys
import distutils.core, distutils.file_util

sys.path.insert(0, '.')
from datconv_pkg.version import *


if os.name == 'posix':
    doclocation = 'share/doc/datconv'
else:
    doclocation = 'doc/datconv'

if os.name == 'nt':
    distutils.file_util.copy_file('datconv', 'datconv-run.py')
    scripts = ['datconv-run.py']
else:
    scripts = ['datconv']

with open('README.rst') as f:
    long_description = f.read()

dist = distutils.core.setup(name = 'datconv',
    version = datconv_version,
    description = 'Universal data converter - pandoc for data; XML, CSV, JSON are supported',
    long_description = long_description,
    author = 'Grzegorz Wierzchowski',
    author_email = 'gwierzchowski@wp.pl',
    url = 'https://github.com/gwierzchowski/datconv',
    packages = ['datconv','datconv.filters','datconv.readers','datconv.writers',
                'datconv.outconn','datconv.outconn.crate','datconv.outconn.postgresql','datconv.outconn.sqlite'],
    package_dir = {'datconv': 'datconv_pkg'},
    package_data = {'datconv': ['conf_template.yaml', 'Logger.yaml'],
                    'datconv.filters': ['conf_template.yaml'],
                    'datconv.readers': ['conf_template.yaml'],
                    'datconv.writers': ['conf_template.yaml'],
                    'datconv.outconn': ['conf_template.yaml'],
                    'datconv.outconn.crate': ['conf_template.yaml'],
                    'datconv.outconn.postgresql': ['conf_template.yaml'],
                    'datconv.outconn.sqlite': ['conf_template.yaml']},
    scripts = scripts,
    data_files = [(doclocation, ['README.rst', 'LICENSE.txt', 'INSTALL.rst', 'docs/Changelog.rst', 'docs/Upgrade.rst'])],
    requires = ['PyYAML', 'lxml'],
    license = 'PSF',
    platforms = 'any',
    classifiers = [
        'Development Status :: ' + datconv_status,
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
    )

if sys.argv[1] in ['install']:
    # Unfotunately while installing using pip those print statements does not work on Windows
    print ('---------------------------------------------------------')
    try:
        import yaml, lxml
    except ImportError:
        print ('To run this software install packages PyYAML, lxml')
    isobj = dist.get_command_obj('install_data')
    readmedoc = None
    for doc in isobj.get_outputs():
        if 'README.rst' in doc:
            readmedoc = doc
            break
    if readmedoc:
        print ('See %s file' % readmedoc)
    else:
        print ('See files deployed to documentation folder')
    print ('---------------------------------------------------------')
