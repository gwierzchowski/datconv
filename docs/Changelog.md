Development plans for near future:
----------------------------------
Points are specified in priority (and probably implementation) order:

- Port to Python 3.
- Write basic getting started guide.
- Better support for running datconv as paralell proceses
  e.g. convering big files in paralell (using rfrom/rto settings).
- Readers: CSV; Writers: Database, PostgreSQL binary input files.

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

