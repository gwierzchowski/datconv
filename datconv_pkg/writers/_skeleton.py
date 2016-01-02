# -*- coding: utf-8 -*-
# Checked with python 2.7
"""This module contain Pandoc Writer skeleton class suitable as starting point for new writers."""

# Standard Python Libs
import logging

# Libs installed using pip
from lxml import etree


####################################################################
Log = None
"""Log varaible is automatically set by main pandoc script using logging.getLogger method.
Use it for logging messages in need.
"""

class DCWriter:
    """This class must be called exactly DCWriter.
    It is responsible for:
      - writing data to output file.
    """
    def __init__(self):
        """Method called when object is being created.
        Additional parameters may be added to this method, but they all have to be named parameters.
        Parameters are usually passed from YAML file as subkeys of Writer:CArg key.
        """
        assert Log is not None
        self._out = None
        # ...

    def setOutput(self, out):
        """Obligatory method that must be defined in Writer class.
        It is called by Reader after it open output stream.
        out - is instance of output stream opened for writing (e.g. returned by open() built-in function).
        This method in some rare cases may be called multiply times (e.g. when convering set of files).
        Do initialization of some variables related to output file (like output records counter etc.)
        """
        self._out = out

    def writeHeader(self, header):
        """Obligatory method that must be defined in Writer class.
        Write header to output file (if it makes sense).
        header - is instance of header as passed by Reader (always a list, but kind of elements is up to Reader).
        """
        pass

    def writeFooter(self, footer):
        """Obligatory method that must be defined in Writer class.
        Write footer to output file (if it makes sense).
        footer - is instance of footer as passed by Reader (always a list, but kind of elements is up to Reader).
        """
        pass
  
    def writeRecord(self, record):
        """Obligatory method that must be defined in Writer class.
        Write record to output file.
        record - is instance of lxml.etree.ElementTree class as passed by Reader.
        See filters._skeleton and package lxml documantation for information how to obtain structure and data from record.
        """
        pass
  