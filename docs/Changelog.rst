Changelog
=========

Development plans for future
----------------------------------
Points are specified in priority (and probably implementation) order:

- Add more options to Excel Output connector
- Add cinsert (working with csv writer) Output connectiors to sqlite and postgresql modules.
- Introduce option to run connectors as separate process with queue between writer and connector for better performance 
  (espacially with database connectors).
- Output connectors: Couchbase, MongoDB, MySQL, zip-file, snappy-file, Avro, Kafka.
- Introduce Filter dispatchers to split data flow to few streams (e.g. to optimize database inserts), 
  option to run them in separate processes.
- Add input comnnectors layer. Imput connectors for databases (query as source of data).
- Readers/Writers: Python pickle, Pandas.
- Output connector: Postgresql binary file (for COPY clause).
- Better support for running Datconv as paralell proceses
  e.g. convering big files in paralell processes (using rfrom/rto settings). Support for skipping headers footers etc.
- Create Windows binary form of program (with cx_Freeze package) that does not require Python installation 
  and upload to github.
- I'm considerating rewriting program in Julia language.

Notes about versioning schema
----------------------------------
- Major number will be changed when changes breaks backward compatibility, 
  i.e. users may have to slightly change their own modules or configuration in order to work with new release. 
  However if this number is zero, API is considerated unstable and may change with any feature release.
  This is called Major Release, and in this case midle and minor numbers are reset to zero.
- Midle number will be changed when new features or options will be introduced but without API break.
  This is called Feature Release, and in this case minor number is reset to zero.
- Minor number will be changed when fixes or very small, non-risky features are introduced.
  This is called Fix Release.

0.8.1-2 (2019.12.28)
----------------------------------
Improvements
^^^^^^^^^^^^
- Verified package against Python 3.7
- Fixes in package long description (separate file for sphinx)

0.8.0 (2018.08.21)
----------------------------------
Improvements
^^^^^^^^^^^^
- Added ``columns: 1`` parameter to ``datconv.writers.dccsv``. It allows to place headers in first line of output when all records have the same structure.
- Added new output connector: ``datconv.outconn.dcexcel`` to be used with CSV writer for writing MS Excel (.xlsx) files.

0.7.3 (2018.08.07)
----------------------------------
Improvements
^^^^^^^^^^^^
- Added support for schema names to database output connectors.

0.7.0-2 (2018.04.19)
----------------------------------
Improvements
^^^^^^^^^^^^
- Added possibility to run Datconv as iterator (i.e. obtain output records directly in Python code).

Fixes
^^^^^^^^^^^^
- Default log level is set to INFO when run from command line and ERROR when run from Python.
- Added additional range checks when cast option is used in ``datconv.outconn.postgresql.jinsert``
  to prevent INSERT errors.
- Fixed bug in ``datconv.writers.dcjson`` which produced invalid output ``key: NaN`` while converting "Nan" string.

0.6.1 (2018.03.17)
----------------------------------
Improvements
^^^^^^^^^^^^
- Improved command line option ``--default``.
- ``datconv.outconn.postgresql.jddl``: new connector
- ``datconv.outconn.postgresql.jinsert``: added support for JSON types.
- ``datconv.outconn.postgresql.jinsert``: added support for casting to ARRAY.
- More flexible configuration of ddl connectors (not backword compatible changes - see :doc:`Upgrade`)

Fixes
^^^^^^^^^^^^
- ``datconv.outconn.postgresql.jinsert``: when ``autocommit: false`` no records are saved in case of error.

0.6.0 (2018.02.17)
----------------------------------
Improvements
^^^^^^^^^^^^
- Added output connectors layer - see :ref:`outconn_skeleton`.
- Added parameters ``rectyp_separator`` and ``add_type`` to XPath Writer to better support database ddl connectors.
- Introduced :doc:`default`.

Fixes
^^^^^^^^^^^^
- Fix program crash with json readers when status reporting was enabled.

0.5.1 (2018.01.20)
----------------------------------
Improvements
^^^^^^^^^^^^
- Added optional filter method ``setFooter()`` to inform filter about contents of data footer and give it a chance to change it.
- Convert standard filters pipe, stat, statex to use ``setFooter()`` instead of ``__del__()``.

Fixes
^^^^^^^^^^^^
- Fix program crash when dcjson writer was used with ``with_prop: true`` option.

0.5.0 (2018.01.06)
----------------------------------
Improvements
^^^^^^^^^^^^
- Added new standard filters: pipe, gen_rec.
- Added optional filter method ``setHeader()`` to inform filter about contents of data header and give it a chance to change it.

0.4.1 (2017.08.16)
----------------------------------
Fixes
^^^^^^^^^^^^
- Small fixes in documentation.

0.4.0 (2017.08.15)
----------------------------------
Improvements
^^^^^^^^^^^^
- XML Reader: added parameter ``foottags``.
- XML Reader: parameter ``rectags`` can be empty (see documentation).
- XML Writer: added parameters ``add_header``, ``add_footer``.
- Added JSON Writer.
- Added JSON Readers.
- Added CSV Reader.
- Added command line option: ``--help``.

0.3.4 (2017.05.12)
----------------------------------
Fixes
^^^^^^^^^^^^
- Small fixes after documentation was published `on-line <http://datconv.readthedocs.io>`_.

0.3.3 (2017.05.06)
----------------------------------
Improvements
^^^^^^^^^^^^
- Adopted pydoc descriptions in sources to Sphinx.
- Created first version of documentation using `Sphinx Project <http://www.sphinx-doc.org>`_.

0.3.2 (2016.06.01)
----------------------------------
Improvements
^^^^^^^^^^^^
- Extended method ``Datconv().Version()`` for possibility to display version of external module.

0.3.1 (2016.05.27)
----------------------------------
Fixes
^^^^^^^^^^^^
- Fixed exceptions being logged only to console (stderr, not by configured logger).
- Fixed duplicated log entries to console (bug introduded by 0.3.0 version).

Improvements
^^^^^^^^^^^^
- Added method ``Datconv().Version()``.

0.3.0 (2016.05.24)
----------------------------------
Fixes
^^^^^^^^^^^^
- Fixed value returned to shell by ``datconv`` script.

Improvements
^^^^^^^^^^^^
- Port to Python 3.
- Add option to inherit logger (to use when datconv is called from Python script that already has its own logger).
- Created basic test scripts - available as separate ``datconv_tests`` package.
- New filter: ``datconv.filters.statex``.

0.2.4 (2016.03.06)
----------------------------------
Fixes
^^^^^^^^^^^^
- Fixed bug that caused writers/dcxml.py to write multiply XML closing tags in case 
  when the same writer class instance was used to process multiply files.

0.2.3 (2016.01.20)
----------------------------------
Fixes
^^^^^^^^^^^^
- Fixed exception when user press ``Ctrl-C`` before script finish.

Improvements
^^^^^^^^^^^^
- Added command line option: ``--version``.

0.2.2 (2016.01.15)
----------------------------------
Fixes
^^^^^^^^^^^^
- Fixed ``conf_template.yaml`` files.

0.2.1 (2016.01.06)
----------------------------------
Fixes
^^^^^^^^^^^^
- Installation script no longer require ``PyYAML`` to be installed.
- Corrected import statements in ``_skeleton.py`` files.

0.2.0 (2015.12.29)
----------------------------------
Fixes
^^^^^^^^^^^^
- Ensure that XML Output is correct (i.e. have one root element).

Improvements
^^^^^^^^^^^^
- Project/program/package rename due to conflicts with existing
  projects: Pandata -> Datconv.
- As consequence of above, renamed some modules and classes. See included Upgrade.md 
  file for more information - changes in user files are needed.
- Added Datconv class - i.e. data conversion can be run as stand alone script: |br| 
  ``datconv [options]``  |br|
  or from python code::

    import datconv  
    dc = datconv.Datconv()  
    conf = {...}  
    dc.Run(conf)  

  This also implies that all subpackages were moved to one, root ``datconv`` package.
- Separated common and IGT specific modules into two separate
  packages. Datconv is now distributed as 2 packages created
  according python standard (``datconv`` and ``datconv-igt``).
- Added standard ``setup.py`` installation script. This means that package
  files are being installed in Python 3rd party package standard location. 
- Licensed ``datconv`` under Python Software Foundation like license.

0.1 (2015.10 - 2015.12.04)
----------------------------------
- Initial not-public release. Delivered only to IGT coworkers.

