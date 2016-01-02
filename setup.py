#!/usr/bin/env python

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

with open('DESCR.md') as f:
    long_description = f.read()
    #long_description = ''.join(f.readlines()).strip()

dist = distutils.core.setup(name = 'datconv',
    version = datconv_version,
    description = 'Universal data converter - pandoc for data',
    long_description = long_description,
    author = 'Grzegorz Wierzchowski',
    author_email = 'gwierzchowski@wp.pl',
    url = 'https://github.com/gwierzchowski/datconv',
    packages = ['datconv','datconv.filters','datconv.readers','datconv.writers'],
    package_dir = {'datconv': 'datconv_pkg'},
    package_data = {'datconv': ['conf_template.yaml', 'Logger.yaml'],
                    'datconv.filters': ['conf_template.yaml'],
                    'datconv.readers': ['conf_template.yaml'],
                    'datconv.writers': ['conf_template.yaml']},
    scripts = scripts,
    data_files = [(doclocation, ['README.md', 'LICENSE.txt', 'DESCR.md', 'docs/Changelog.md', 'docs/Upgrade.md'])],
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
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
    )
      
#isobj = dist.get_command_obj('install_scripts')
#print isobj.get_outputs()
