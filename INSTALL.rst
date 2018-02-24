.. Keep this file pure reST code (no Sphinx estensions)

Installation and Usage
==================================
For package description see README.rst file

Installation (System wide - for all users):
-------------------------------------------
.. note::
   In case of using Python 3 on linux system replace ``pip`` with ``pip3`` and ``python`` with ``python3`` 
   in below commands.

Prerequisites
^^^^^^^^^^^^^
This program requires following 3-rd party packages: ``PyYAML``, ``lxml``. 
They must be installed in order to run Datconv.
In addition JSON readers require ``ijson`` package to be installed.

| **PyYAML** and **ijson** can be installed from Python Package Index:
| Linux: ``sudo pip install PyYAML ijson``
| Windows: ``pip install PyYAML ijson``

| **lxml** is little bit more involved as it is extension package and installation from pip may fail. This package should be installed from system specific installer.  
| Linux (Debian based): `sudo apt-get install python-lxml` or `sudo apt-get install python3-lxml`  
| Windows: Download from `PyPI <https://pypi.python.org/pypi/>`_ appropriate lxml binary windows installer and install from it.

Installation Method 1
^^^^^^^^^^^^^^^^^^^^^
| Recommended method for installation of this package is from Python Package Index:  
| Linux: ``sudo pip install datconv``
| Windows: ``pip install datconv``

Installation Method 2
^^^^^^^^^^^^^^^^^^^^^
| If you want to install particular version, download source-ball and issue:  
| Linux: ``sudo pip install datconv-<ver>.tar.gz``
| Windows: ``pip install datconv-<ver>.tar.gz``

Installation Method 3
^^^^^^^^^^^^^^^^^^^^^
| Alternatively unpack source-ball and from unpacked folder run command:  
| Linux: ``sudo python setup.py install``
| Windows: ``python setup.py install``

.. note::
   More installation options are possible - see documentation of Python ``distutils`` package.

Installation from Source
^^^^^^^^^^^^^^^^^^^^^^^^
If you have downloaded archive snapshot, first unpack it and from root folder run command: 
``python setup.py sdist`` 
which will create ``dist`` subfolder and create source-ball in it. Then apply method 2 or 3 above.

Files deployed by installation script
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Main command line utility: |br|
  Linux: ``<BINDATA>/datconv``, where ``<BINDATA>`` is by default ``/usr/local/bin`` |br|
  Windows: ``<BINDATA>\Scripts\datconv-run.py``, where ``<BINDATA>`` is by default ``C:\Program Files\PythonXX`` where XX is Python version  
- ``datconv`` package and its sub-packages 
- Documentation: |br|
  Linux: ``<PREFIX>/share/doc/datconv/*``, where ``<PREFIX>`` is by default ``/usr/local`` |br|
  Windows: ``<PREFIX>\doc\datconv\*``, where ``<PREFIX>`` is by default ``C:\Program Files\PythonXX``

Re-Installation / Upgrade
--------------------------
| To upgrade packages from PyPi use -U option: ``[sudo] pip install -U PyYAML datconv``.
| Other installation methods specified above remain valid when upgrading package.  

.. note::
   if you upgrade from previous pandata/datconv version check ``Upgrade.rst`` file deployed in documentation folder.

Usage:
------
Please refer to on-line or deployed documentation and Pydoc accesible information contained in this package. 
Consider also installing ``datconv_tests`` package which contain test scripts for this package. 
It can also be used as source of samples of how this package may be used.

Official on-line documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Official program documentation is avaialble 
`here <http://datconv.readthedocs.io>`_.

Additional configuration for Pydoc
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There are some pydoc descriptions in several script files
that are installed into folders not in python module search path,
therefore standard pydoc browser would not get those descriptions. It is
however possible to hack that:  
Linux: edit `/usr/bin/pydoc` file:

- at begin add: ``import sys``
- before ``pydoc.gui()`` call, add ``sys.path.append('/usr/local/bin')``
- create symlink: |br|
  ``sudo ln -s /usr/local/bin/datconv /usr/local/bin/datconv-run.py``.
  
Windows: edit ``C:\Program Files\PythonXX\Tools\Scripts\pydocgui.pyw`` file:

- at begin add: ``import sys``
- before ``pydoc.gui()`` call, add ``sys.path.append('C:\\Program Files\\PythonXX\\Scripts')``

Obtaining Pydoc information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| Perform above 'hacks', and run conmand: 
| Linux (Python2): ``pydoc -g``  
| Linux (Python3): ``pydoc3 -b``  
| Windows: Start Menu/Python/Module Docs  
| and then press 'Open Browser' or manually navigate to given URL.

.. note::
   This URL does not work with Windows IE browser.

| Then go to below sections (near bottom of page): 
| Linux: ``/usr/local/lib/pythonX.X/dist-packages/``, ``/usr/local/bin``
| Windows: ``C:\Program Files\PythonXX\Lib\site-packages``, ``C:\Program Files\PythonXX\Scripts`` and go into ``datconv(package)`` or ``datconv-run`` link.
