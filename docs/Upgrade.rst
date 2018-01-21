.. Keep this file pure reST code (no Sphinx estensions)

Upgrade instructions
====================

From earlier versions to Datconv 0.5.1
--------------------------------------------------
New Filter optional functions ``setHeader()`` and ``setFooter()``:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- If you managed to write custom Reader, it must be updated in following way: 
  call filter optional functions before calling Writer ``writeHeader()`` and ``writeFooter()`` functions as shown below::
  
    if self._flt is not None:
        if hasattr(self._flt, 'setHeader'):
            self._flt.setHeader(self._header)
    self._wri.writeHeader(self._header)

  and in similar way for Footer.
- If you have a filter that does some work at the end of converion process (like writing some statistics) and you implemented it in
  ``__del__()`` fumction, this finalization code can be now moved to ``setFooter()``.

From Datconv version 0.2.x to Datconv 0.3.x
--------------------------------------------------
Changes in parameters default values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed default value for parameter ``encoding`` of ``datconv.writers.dcxml``. It was ``ascii`` and is now ``unicode``.
Note that this parameter is ignored while run against Python3.

From Pandata version 0.1 to Datconv 0.2.x
--------------------------------------------------
Changes in files' layout
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Pandata version 0.1 did not had its own installer. Everything was placed
in one folder. Now Datconv (renamed from Pandata) modules included in
package are being installed in special Python subfolder intended for
3-rd party modules. So all old Pandata core modules may be deleted from
current localisation. Recomended Datconv layout is now to keep user own
modules in subfolders of one folder, and run datconv script from that
folder or add user's "projects' folder" to ``PYTHONPATH`` environment
variable. Datconv core modules should be kept in Python sub-folders 
where installer placed them.

Modules and classes' name changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Names of standard Reader and Writer modules has changed: ``pdxml`` -> ``dcxml``,
``pdcsv`` -> ``dccsv``, ``pdxpaths`` -> ``dcxpaths``. Appropriate changes should be done in user's 
YAML configuration files.

Fixed names of Reader, Filter and Writer classes has changed: ``PDReader`` -> ``DCReader``,
``PDFilter`` -> ``DCFilter``, ``PDWriter`` -> ``DCWriter``. Appropriate changes should be done 
in user's filters' definition files.

All version 0.1 modules were moved to common datconv meta
package as subpackages. So in user's YAML configuration files and in import
statements in filters ``datconv.`` specification should be added.

| *Example 1 (YAML file):*
|   ``Module: writers.pdcsv``  
|   should be changed to:  
|   ``Module: datconv.writers.dccsv``

| *Example 2 (filter definition):*
|   ``from filters import WRITE``  
|   should be changed to:  
|   ``from datconv.filters import WRITE``

Change in main program invocation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Datconv main script is now included into system PATH. On Linux .py
file extension was removed, so it can be called like (without ./ prefix):
``datconv [options]``. On Windows script was renamed, so it can be called
like (without python explicit invocation): ``datconv-run.py [options]``.

.. note::
   Windows Python installer should create file-type entries that allow user to 
   directly call python script (without python explicit invocation). 

   To check that, run following connads from command box: |br|
   ``C:\>assoc .py``                                      |br|
   should give:                                           |br|
   ``.py=Python.File``
    
   and:                                                   |br|
   ``C:\>ftype Python.File``                              |br|
   should give:                                           |br|
   ``Python.File="c:\python27\python.exe" "%1" %*``  
   
   Important is ``%\*`` at end --- what allows to pass additional arguments to program.
