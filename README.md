Datconv - Universal Data Converter
==================================

For package description see DESCR.md file

INSTALLATION (System wide - for all users):
-------------------------------------------

### Prerequisites
This program requires following 3-rd party packages: PyYAML, lxml. 
They must be installed in order to run datconv program.  
**PyYAML** can be installed from Python Package Index:  
Linux: `sudo pip install PyYAML`  
Windows: `pip install PyYAML`  
**lxml** is little bit more involved as it is extension package and
installation from pip may fail. This package should be installed from system specific installer.  
Linux (Debian based): `sudo apt-get install python-lxml`  
Windows: Download from [PyPI](https://pypi.python.org/pypi/) appropriate lxml binary windows installer 
and install from it.

### Installation Method 1
Recommended method for installation of this package is from Python Package Index:  
Linux: `sudo pip install datconv`  
Windows: `pip install datconv`

### Installation Method 2
If you want to install particular version, download source-ball and issue:  
Linux: `sudo pip install datconv-<ver>.tar.gz`  
Windows: `pip install datconv-<ver>.tar.gz`

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
- Main command line utility:  
  Linux: `<BINDATA>/datconv`, where `<BINDATA>` is by default `/usr/local/bin`  
  Windows: `<BINDATA>\Scripts\datconv-run.py`, where `<BINDATA>` is by default `C:\Program Files\PythonXX` where XX is Python version  
- `datconv` package and its sub-packages 
- Documentation:  
  Linux: `<PREFIX>/share/doc/datconv/*`, where `<PREFIX>` is by default `/usr/local`  
  Windows: `<PREFIX>\doc\datconv\*`, where `<PREFIX>` is by default `C:\Program Files\PythonXX`

RE-INSTALLATION/UPGRADE:
------------------------

To upgrade packages from PyPi use -U option:
`[sudo] pip install -U PyYAML datconv`.  
Other installation methods specified above remain valid when upgrading package.  
Note: if you upgrade from previous pandata/datconv version check
Upgrade.md file deployed in documentation folder.

USAGE:
------

Please refer to  deployed documentation and Pydoc accesible information contained in this package.  
Consider also installing `datconv_tests` package which contain test scripts for this package. 
It can also be used as source of samples of how this package may be used.

### Additional configuration: 
There are some pydoc descriptions in several script files
that are installed into folders not in python module search path,
therefore standard pydoc browser would not get those descriptions. It is
however possible to hack that:  
Linux: edit `/usr/bin/pydoc` file:  
- at begin add: `import sys`  
- before `pydoc.gui()` call, add `sys.path.append('/usr/local/bin')`  
- create symlink:  
  `sudo ln -s /usr/local/bin/datconv /usr/local/bin/datconv-run.py`.
  
Windows: edit `C:\Program Files\PythonXX\Tools\Scripts\pydocgui.pyw` file:  
- at begin add: `import sys`  
- before pydoc.gui() call, add `sys.path.append('C:\\Program Files\\PythonXX\\Scripts')`

### Obtaining Pydoc information: 
Perform above 'hacks', and run conmand:  
Linux: `pydoc -g`  
Windows: Start Menu/Python/Module Docs  
and then press 'Open Browser' or manually navigate to given URL.
Note: this URL does not work with Windows IE browser. 
Then go to below sections (near bottom of page):  
Linux: `/usr/local/lib/python2.7/dist-packages/`, `/usr/local/bin`  
Windows: `C:\Program Files\PythonXX\Lib\site-packages`, `C:\Program Files\PythonXX\Scripts`  
and go into `datconv(package)` or `datconv-run` link.
