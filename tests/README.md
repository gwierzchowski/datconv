datconv_test - testing scripts for `datconv` package
==================================

## DESCRIPTION:
This package contains set of testing scripts to test `datconv` package.
Tests are written in standard Unix shell (`/bin/sh`) and use some GNU tools available 
on Unix-like systems. So they best run on Linux or other Posix compliant systems.
In addition to testing function package can be used just for reading - as an example 
how package `datconv` could be used.

INSTALLATION (System wide - for all users):
-------------------------------------------

Note: While working with Python3 on some Linux systems `pip` command should be replaced by `pip3`.

### Prerequisites
This program requires package datconv and all packages required by it.  
**datconv** can be installed from Python Package Index: 
`sudo pip install datconv`  

### Installation Method 1
Recommended method for installation of this package is from Python Package Index:  
Linux: `sudo pip install datconv_test`  
Windows: `pip install datconv_test`

### Installation Method 2
If you want to install particular version, download source-ball and issue:  
Linux: `sudo pip install datconv_test-<ver>.tar.gz`  
Windows: `pip install datconv_test-<ver>.tar.gz`

### Installation Method 3
Alternatively unpack source-ball and from unpacked folder run command:  
Linux: `sudo python setup.py install`  
Windows: `python setup.py install`  
Note: More installation options are possible - see documentation of Python `distutils` package.

### Installation from Source
If you have downloaded archive snapshot, first unpack it and from root folder run command: 
`python setup.py sdist` 
which will create `dist` subfolder and create source-ball in it. Then apply method 2 or 3 above.

### Files deployed by installation script
- Scripts to run tests:  
  Linux: `<BINDATA>/datconv_tests2`, `<BINDATA>/datconv_tests3`, where `<BINDATA>` is by default `/usr/local/bin`  
  Windows: `<BINDATA>\Scripts\datconv_tests2`, `<BINDATA>\Scripts\datconv_tests3`, where `<BINDATA>` is by default `C:\Program Files\PythonXX` 
- Test scripts and sample data:  
  Linux: `<PREFIX>/share/datconv_test/*`, where `<PREFIX>` is by default `/usr/local`  
  Windows: `<PREFIX>\datconv_test\*`, where `<PREFIX>` is by default `C:\Program Files\PythonXX` 
- Documentation:  
  Linux: `<PREFIX>/share/doc/datconv_test/*`, where `<PREFIX>` is by default `/usr/local`  
  Windows: `<PREFIX>\doc\datconv_test\*`, where `<PREFIX>` is by default `C:\Program Files\PythonXX`

RE-INSTALLATION/UPGRADE:
------------------------

To upgrade packages from PyPi use -U option:
`[sudo] pip install -U datconv_test`.  
Other installation methods specified above remain valid when upgrading package.  

USAGE:
------

Run one of installed scripts: `datconv_tests2` or `datconv_tests3`.  
Before running, open them and review/customize the paths.  
`datconv_tests2` is intended to test `datconv` against Python2.  
`datconv_tests3` is intended to test `datconv` against Python3.  

Review test scripts deployed in `/usr/local/share/datconv_test` to understand how to use 'datconv' package.
