Development plans for future:
----------------------------------
Points are specified in priority (and probably implementation) order:

- Write basic getting started guide (qustionable - see provided test scripts as documentation)
- Better support for running datconv as paralell proceses
  e.g. convering big files in paralell (using rfrom/rto settings).
- Readers: CSV; Writers: Database, PostgreSQL binary input files.
- XPath Writer: Improve generated column names (possibly use _ instead of . and make col names unique).
  This is in preparation for SQL Writers (col names as database fields).

Notes about versioning schema:
- First, major number will be changed when changes breaks backward compatibility, 
  i.e. users may have to slightly change their own modules or configuration in order to work with new release. 
  However if this number is zero, API is considerated unstable and may change with any feature release.
  This is labeled as Major Release, and in this case midle and minor numbers are reset to zero.
- Second, midle number will be changed when new features or options will be introduced but without API break.
  This is labeled as Feature Release, and in this case minor number is reset to zero.
- Third, minor number will be changed when fixes or very small, non-risky features are introduced.
  This is labeled as Fix Release.

0.3.0 (2016.05.24):
----------------------------------
### Fixes
- Fixed value returned to shell by datconv script 

### Improvements
- Port to Python 3.
- Add option to inherit logger (to use when datconv is called from Python script that already has its own logger).
- Created basic test scripts - available as separate `datconv_tests` package.
- New filter: `datconv.filters.statex`.

0.2.4 (2016.03.06):
----------------------------------
### Fixes
- Fixed bug that caused writers/dcxml.py to write multiply XML closing tags in case 
  when the same writer class instance was used to process multiply files.

0.2.3 (2016.01.20):
----------------------------------
### Fixes
- Fixed exception when user press Ctrl-C before script finish.

### Improvements
- Added command line option: --version.

0.2.2 (2016.01.15):
----------------------------------
### Fixes
- Fixed conf_template.yaml files.

0.2.1 (2016.01.06):
----------------------------------
### Fixes
- Installation script no longer require PyYAML to be installed.
- Corrected import statements in _skeleton.py files.

0.2.0 (2015.12.29):
----------------------------------
### Fixes
- Ensure that XML Output is correct (i.e. have one root element).

### Improvements
- Project/program/package rename due to conflicts with existing
  projects: Pandata -> Datconv.
- As consequence of above, renamed some modules and classes. See included Upgrade.md 
  file for more information - changes in user files are needed.
- Added Datconv class - i.e. data conversion can be run as stand alone script:  
  `datconv [options]`  
  or from python code:
```python
import datconv  
dc = datconv.Datconv()  
conf = {...}  
dc.Run(conf)  
```
  This also implies that all subpackages were moved to one, root `datconv` package.
- Separated common and IGT specific modules into two separate
  packages. Datconv is now distributed as 2 packages created
  according python standard (`datconv` and `datconv-igt`).
- Added standard `setup.py` installation script. This means that package
  files are being installed in Python 3rd party package standard location. 
- Licensed `datconv` under Python Software Foundation like license.

0.1 (2015.10 - 2015.12.04):
----------------------------------
- Initial not-public release. Delivered only to IGT coworkers.

