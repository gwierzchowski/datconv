.. Keep this file pure reST code (no Sphinx estensions)

**Datconv** is a program designed to perform configurable comversion of file
with data in one format to file with data in another format.

Program should be run using Python 2.7 or Python 3.x interpretter. It also requires
installation of external packages: ``lxml``, ``PyYAML``. For more information see
:doc:`README.rst <README>` file distributed in source ball.

Both input and output files can be text or binary files. However it is
assumed that those files have following structure:

|    -----
|    Header 
|    -----
|    Record 1 
|    Record 2 
|    .....
|    Record N 
|    -----
|    Footer
|    -----

There may be different types of records (i.e. every record has attribute
called record type). Each record may contain different number and kind of 
data (has different internal structure) even among records of the same type.

Program has modular architecture with following swichable compoments:

*Reader*
    Major obligatory component responsible for:
    
    * reading input data (i.e. every reader class assumes certain input file format) 
    * driving entire data conversion process (i.e. main processing loop in implemented in this class) 
    * determine internal representation of header, records and footer (this strongly depands on reader and kind of input format).
    
    For API of this component see: :ref:`readers_skeleton`

*Filter*
    Optional compoment that is able to: 
    
    * filter data (i.e. do not pass certain records further - i.e. to Writer)
    * change data (i.e. change on the fly contents of certain records) 
    * produce data (i.e. cause that certain records, maybe slightly modified, are being sent multiply times to writer) 
    * break conversion process (i.e. cause that conversion stop on certain record). 

    For API of this component see: :ref:`filters_skeleton`

*Writer*
    Obligatory component responsible for: 
    
    * writing data to output file. 

    For API of this component see: :ref:`writers_skeleton`
    
*Logger*
    All messages intended to be presented to user are being send 
    (except few very initial error messages) to Logger classes from Python standard
    package ``logging``. Datconv can use all logging comfiguration power available in this package.

In this version of package following compoments are included: 

* Readers: XML (sax), CSV (sax), JSON (sax). 
* Filters: Few basic/sample filters.
* Writers: XML, CSV, XPath (helper module), JSON.

So Datconv program can be used to convert files between XML, CVS and JSON formats. 
Sax means that used parsers are of event type - i.e. entire data are not being stored in memory (typically only just one record), what means that program is able to process large files without allocating a lot of memory.
It may be also usefull in case you have some files in custom program/company specific data format that you want to look up or convert. Then it is enough to write the reader component for your cutom data format compatible with Datconv API and let Datconv do the rest. 
Actually this is how I'm currently using this program in my work.

Package repository and home page: `Datconv Project <https://github.com/gwierzchowski/datconv>`_.

If you'd prefer to work in JavaScript environment please look at `Pandat Project <https://github.com/pandat-team/pandat/>`_ which has similar design and purpose.

Writing this program I was inspired by design of `Pandoc Project <http://pandoc.org/>`_.

