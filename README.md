==================================
Universal Data Converter
==================================

Works only with Python 2.7.

For package description see DESCR.rst file

-------------------------------------------
INSTALLATION (System wide - for all users):
-------------------------------------------
Method 1) <br/>
Unpack and run command:
Linux: ``sudo python setup.py install``
Windows: ``python setup.py install``
Method 2)
Linux: ``sudo pip install datconv-<ver>.tar.gz``
Windows: ``pip install datconv-<ver>.tar.gz``

Note: More installation options are possible - see documentation of distutils package

It will deploy:
- main command line utility:
Linux: ``<BINDATA>/datconv``, where <BINDATA> is by default ``/usr/local/bin``
Windows: ``<BINDATA>\Scripts\datconv-run.py``, where BINDATA> is by default ``C:\Python27``
- datconv package and its sub-packages
- Documentation:
Linux: ``<PREFIX>/share/doc/datconv/*``, where <PREFIX> is by default ``/usr/local``
Windows: ``<PREFIX>\doc\datconv\*``, where <PREFIX> is by default ``C:\Python27``

This program requires following 3-rd party packages: PyYAML, lxml
Install them before using this program.
PyYAML can be installed from PyPi:
``[sudo] pip install PyYAML``

lxml is little bit more involved as it is extension package and installation from pip may fail.
Linux (Debian based): sudo apt-get install python-lxml
Windows: Download from `PyPI <https://pypi.python.org/pypi/>`_ appropriate lxml binary windows installer and instal from it.

----------------------------------
RE-INSTALLATION/UPGRADE:
----------------------------------
Unpack and run command:
Linux: ``sudo python setup.py install``
Windows: ``python setup.py install``
or
Linux: ``sudo pip install datconv-<ver>.tar.gz``
Windows: ``pip install datconv-<ver>.tar.gz``

Note: To upgrade packages from PyPi use -U option:
``[sudo] pip install -U PyYAML``

Note: If you upgrade from prevoius pandata/datconv version check Upgrade.rst file installed in documentation folder.

----------------------------------
USAGE:
----------------------------------
Please refer to Pydoc information in this package, and deployed documentation.
Note: There is pydoc documentation in some script files that are installed into folders 
not in python module search path, therefore standard pydoc browser would not get those descriptions.
It is however possible to hack that:

Linux:
Edit ``/usr/bin/pydoc`` file:
at begin add: ``import sys``
before pydoc.gui() call, add ``sys.path.append('/usr/local/bin')``
Create symlink:
``sudo ln -s /usr/local/bin/datconv /usr/local/bin/datconv-run.py``

Windows:
Edit ``C:\Python27\Tools\Scripts\pydocgui.pyw`` file:
at begin add: ``import sys``
before pydoc.gui() call, add ``sys.path.append('C:\\Python27\\Scripts')``

Obtaining Pydoc information:
Perform above 'hacks', and run conmand:
Linux: ``pydoc -g``
Windows: Start Menu/Python/Module Docs
and then press Open Browser or manually navigate to given URL
Note: This URL does not work with Windows IE browser.
Then go to below sections (near bottom of page):
Linux: /usr/local/lib/python2.7/dist-packages/, /usr/local/bin
Windows: C:\Python27\Lib\site-packages, C:\Python27\Scripts
and go into datconv(package) or datconv-run link.
