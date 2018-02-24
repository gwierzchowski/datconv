# -*- coding: utf-8 -*-
# Checked with python 2.7
"""This module contain Datconv Reader skeleton class suitable as starting point for new readers."""

# Standard Python Libs
import logging

# Libs installed using pip
from lxml import etree

# Datconv generic modules
from datconv.filters import WRITE, REPEAT, BREAK

####################################################################
Log = None
"""Log varaible is automatically set by main datconv script using logging.getLogger method.
Use it for logging messages in need.
"""

class DCReader:
    """This class must be named exactly DCReader.
    It is responsible for:
    
    - reading input data (i.e. every reader class assumes certain input file format)
    - driving entire data conversion process (i.e. main processing loop in implemented in this class)
    - determine internal representation of header, records and footer (this strongly depands on reader and kind of input format).
    """
    def __init__(self):
        """Additional constructor parameters may be added to constructor, but they all have to be named parameters.
        Parameters are usually passed from YAML file as subkeys of Reader:CArg key.
        """
        assert Log is not None
        self._wri = self._flt = None
        # ...

    def setWriter(self, writer):
        """Obligatory method that must be defined in Reader class.
        It is called by main datconv.py script after it read configuration file and create Writer class.
        
        :param writer: is instance of Writer class.
        """
        self._wri = writer

    def setFilter(self, flt):
        """Obligatory method that must be defined in Reader class.
        It may be called by main datconv.py script after it read configuration file and create Filter class.
        If Filter is not configured this method is not called.
        
        :param flt: is instance of Filter class.
        """
        self._flt = flt

    def Process(self, inpath, outpath = None, rfrom = 1, rto = 0):
        """Main method that drive all data conversion process.
        Parameters are usually passed from YAML file as subkeys of Reader:PArg key.
        Parameters given in this method are typical ones, however thay may be customized.
        Usually some kind of input and output path should be passed here.
        Also if structure of input data format allows for it, it is recommended to implement reading data 
        from certain to certain record number.
        """
        
        # Here is skeleton of Process method.
        # Real implementations are of course more complicated.
        # Here we only pay attantion to obligatory calls (API) that must be called here
        
        # Fake declaration to make below code compile
        header = footer = None
        
        ## This method should open input stream,
        ## open output stream, and then make following call
        ## using writer class previously passed using setWriter().
        ## fout is opened output stream.
        #self._wri.setOutput(fout)
        
        # Then it should inform filter about contents of data header and make following call.
        # Passed header must be a Python list object,
        # but items of this list are facultative (i.e. it is up to the reader class what to place here).
        # Header argument must be later passed to Writer (filter may change it)
        if self._flt is not None:
            if hasattr(self._flt, 'setHeader'):
                self._flt.setHeader(header)
    
        # Then it should read input data header and make following call.
        # Passed header must be a Python list object,
        # but items of this list are facultative (i.e. it is up to the reader class what to place here).
        self._wri.writeHeader(header)

        # Then main processing loop should follow, it may looks like:
        recno = 0
        while True:
            recno = recno + 1
            if recno < rfrom:
                continue
            if rto > 0 and recno > rto:
                break
            # Returned rec should be class of lxml.etree.ElementTree
            rec = self._readRecord() # sample method that reads record from input
            if rec is None: # end of stream
                break
            if self._flt is not None:
                filter_break = False
                while True:
                    res = self._flt.filterRecord(rec)
                    if res & WRITE:
                        self._wri.writeRecord(rec)
                    if res & REPEAT:
                        continue
                    if res & BREAK:
                        filter_break = True
                    break
                if filter_break:
                    Log.info('Filter caused Process to stop on record %d' % recno)
                    break
            else:
                self._wri.writeRecord(rec)

        # Then it should inform filter about contents of data footer and make following call.
        # Passed footer must be a Python list object,
        # but items of this list are facultative (i.e. it is up to the reader class what to place here).
        # Footer argument must be later passed to Writer (filter may change it)
        if self._flt is not None:
            if hasattr(self._flt, 'setFooter'):
                self._flt.setFooter(footer)
        
        # Then it should make following call.
        # Passed footer must be a Python list object (just like the header was)
        # but items of this list are facultative (i.e. it is up to the reader class what to place here).
        self._wri.writeFooter(footer)
        
        # Then it should probably close input and output streams and make some other cleanup
        #Log.info('Output saved to %s' % outpath)
        
    # Fake declaration to make this sample skeleton compile.
    # This method name and existance is completly facultative.
    def _readRecord(self):
        rec = etree.Element('RECORD')
        return rec
    
