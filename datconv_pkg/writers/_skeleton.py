# -*- coding: utf-8 -*-
# Checked with python 2.7
"""This module contain Datconv Writer skeleton class suitable as starting point for new writers."""

# Standard Python Libs
import logging

# Libs installed using pip
from lxml import etree

# Datconv generic modules
from datconv.outconn import STRING, OBJECT, ITERABLE


####################################################################
Log = None
"""Log varaible is automatically set by main pandoc script using logging.getLogger method.
Use it for logging messages in need.
"""

class DCWriter:
    """This class must be named exactly DCWriter. It is responsible for:
    
    - writing data to output file.
    """
    def __init__(self):
        """Additional constructor parameters may be added to this method, but they all have to be named parameters.
        Parameters are usually passed from YAML file as subkeys of Writer:CArg key.
        """
        assert Log is not None
        self._out_flags = 0;
        self._out = None
        self._header = None
        self._footer = None
        # ...

    def setOutput(self, out):
        """Obligatory method that must be defined in Writer class.
        It is called by main Datconv.Run() function before conversion begin and before any write* function is being called.
        
        :param out: is instance of datconv Output Connector class according to configuration file. In case Output Connector is not defined in configuration file there are two fallbacks checked: a) if Reader:PArg:outpath is defined, the file connector with specified path is used, b) standard output stream is used as output.
        
        This method in some rare cases may be called multiply times (e.g. when convering set of files).
        Initialization of some variables related to output file (like output records counter etc.) 
        should be done here.
        """
        self._out = out
        self._out_flags = out.supportedInterfases();
        # write* functions should chek bits in this flag and call appropriate connector functions.

    def writeHeader(self, header):
        """Obligatory method that must be defined in Writer class.
        Write header to output file (if it makes sense).
        
        :param header: is instance of header as passed by Reader (always a list, but type of elements is up to Reader).
        """
        self._header = header
        # ...

    def writeFooter(self, footer):
        """Obligatory method that must be defined in Writer class.
        Write footer to output file (if it makes sense).
        
        :param footer: is instance of footer as passed by Reader (always a list, but type of elements is up to Reader).
        """
        self._footer = header
        # ...
    
    def getHeader(self):
        """Obligatory method that returnes header passed to ``writeHeader``."""
        return self._header
    
    def getFooter(self):
        """Obligatory method that returnes footer passed to ``writeFooter``."""
        return self._footer
  
    def writeRecord(self, record):
        """Obligatory method that must be defined in Writer class.
        Transform passed record to its specific formet and pass to output connecte=or either as object or string.
        
        :param record: is instance of lxml.etree.ElementTree class as passed by Reader.
        :returns: Transformed record that this writer passed to object type connector.
        
        See :ref:`filters_skeleton` and package ``lxml`` documentation for information how to obtain structure and data from record.
        """
        pass
  
