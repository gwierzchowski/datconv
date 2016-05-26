**datconv** is a script intended to perform configurable comversion of file
with data in one format to file with data in another format.

Script should be run using Python 2.7 or Python 3.x interpretter. It also requires
installation of external modules: lxml, PyYAML. For more information see
README.md file distributed in source ball.

Both input and output files can be text or binary files. However it is
assumed that both input and output files have following structure: 
```
---
Header 
---
Record 1 
Record 2 
... 
Record N 
--- 
Footer
---
```
There may be different types of records (i.e. every record has string
characteristic called record type). Each record may contain different
number and kind of data (have different internal structure) even among
records of the same type.

Program has modular architecture with following swichable compoments:

- Reader - major obligatory component responsible for: 
  - reading input data (i.e. every reader class assumes certain input file format) 
  - driving entire data conversion process (i.e. main processing loop in implemented in this class) 
  - determine internal representation of header, records and footer (this strongly depands on reader and kind of input format).
- Filter - optional compoment that is able to: 
  - filter data (i.e. do not pass certain records further - i.e. to writer)
  - change data (i.e. change on the fly contents of certain records) 
  - produce data (i.e. cause that certain records, maybe slightly modified, are being sent multiply times to writer) 
  - break conversion process (i.e. cause that conversion stop on certain record). 
- Writer - obligatory component responsible for: 
  - writing data to output file. 
- Logger - all messages intended to be presented to user are being send 
  (except few very initial error messages) to Logger classes from Python standard
library `logging`. This script can use all logging comfiguration power available in `logging` package.

In this version of package following compoments are included: 

- Readers: XML. 
- Filters: Few basic/sample filters.
- Writers: XML, CSV, XPath (helper module).

Package repository and home page: [Datconv Project](https://github.com/gwierzchowski/datconv).

If you'd prefer to work in JavaScript environment please look at [Pandat Project](https://github.com/pandat-team/pandat/) which has similar design and purpose.

