# -*- coding: utf-8 -*-
"""This module implements Datconv Writer which saves data in form of CSV file.
Supports connectors of type: STRING, LIST, ITERABLE.
"""

# In Python 2.7 only
from __future__ import print_function

# Standard Python Libs
import sys
import csv
import logging

# Libs installed using pip
from lxml import etree

#Datconv classes
from . import dcxpaths
from datconv.outconn import STRING, LIST, ITERABLE


Log = None
"""Log varaible is automatically set by main datconv script using logging.getLogger method.
Use it for logging messages in need.
"""

class DCWriter:
    """Please see constructor description for more details."""
    def __init__(self, columns = None, simple_xpath = False, add_header = False, col_names = True, csv_opt = None):
        """Parameters are usually passed from YAML file as subkeys of Writer:CArg key.
        
        :param columns: this parameter may be one of 3 possible types or None:
            if it is a string, it should be the path to file that contain specification of columns in output file. \n
            if it is a list, it directly specifies columns in output file. \n
            if it is None or distionary, columns in output CSV file are being generated automatically based on contentents of input file. When this option is used number of columns in different records in CSV file may very because new columns are being added when discovered.
        :param simple_xpath: determines weather simple xpaths are used in column specification. See pdxpath Writer for more descripption.
        :param add_header: if True, generic header (as initialized by Reader) is added as first line of output file.
        :param col_names: if True, line with column names (fields) is added before data or after data (in case of auto option).
        :param csv_opt: dictionary with csv writer options. See `documentation <https://docs.python.org/3/library/csv.html>`_ of csv standard Python library.
        
        For more detailed descriptions see :ref:`conf_template.yaml <writers_conf_template>` file in this module folder.
        """
        assert Log is not None
        dcxpaths.Log = Log

        self._out = None
        self._out_flags = 0;
        self._writers = []
        self._auto_xpw = None
        self._auto_cno = 0
        self._col = []
        if columns is not None:
            if isinstance(columns, str):
                rea = csv.reader(open(columns), lineterminator='\n')
                for col in rea:
                    if col and len(col) >= 4 and col[0][0] != '#':
                        self._col.append(col)
            if isinstance(columns, dict):
                self._auto_xpw = dcxpaths.DCWriter(simple_xpath = simple_xpath, **columns)
                if columns.get('colno'):
                    self._auto_cno = columns.get('colno')
            if isinstance(columns, list):
                for col in columns:
                    if col and len(col) >= 4 and col[0][0] != '#':
                        self._col.append(col)
        else:
            self._auto_xpw = dcxpaths.DCWriter(simple_xpath = simple_xpath)
        self._simple_xpath = simple_xpath
        self._add_header = add_header
        self._col_names = col_names
        self._csv = csv_opt

    def setOutput(self, out):
        self._writers = []
        self._out = None
        self._out_flags = out.supportedInterfases();
        if self._out_flags & STRING:
            for stream in out.getStreams():
                if self._csv:
                    self._writers.append(csv.writer(stream, **self._csv))
                else:
                    self._writers.append(csv.writer(stream))
        if self._out_flags & (LIST | ITERABLE):
            if not out.tryObject(list()):
                raise Exception('Incompatible OutConnector used, dccsv Writer requires that connector supports list objects')
            self._out = out
        if self._auto_xpw:
            self._auto_xpw.resetXPaths()
            self._col = []
       
    def writeHeader(self, header):
        if self._add_header:
            self._writeRow([str(header)] + [None]*(len(self._col) - 1))
        if self._col_names and self._auto_xpw is None:
            self._writeRow([c[0] for c in self._col])

    def writeFooter(self, header):
        if self._col_names and self._auto_xpw is not None:
            cn = [c[0] for c in self._col]
            if self._auto_cno > 0 and len(cn) < self._auto_cno:
                cn = cn + ['Spare']*(self._auto_cno - len(cn))
            self._writeRow(cn)
        
    def writeRecord(self, record):
        try:
            line = []
            if self._auto_xpw:
                new_col = self._auto_xpw.checkXPath(record, ret_new = True)
                if new_col:
                    for col in new_col:
                        self._col.append(col)

            for col in self._col:
                val = col[3]
                if col[1] in ['*', record.tag]:
                    if self._simple_xpath:
                        res = record.find(col[2])
                    else:
                        res = record.xpath(col[2])
                    if res is not None:
                        if isinstance(res, list) and len(res) > 0:
                            res = res[0]
                        #if isinstance(res, etree._Element): #Undocumented
                        if etree.iselement(res):
                            val = res.text
                        elif isinstance(res, str):
                            val = res
                        elif not isinstance(res, list): # exclude empty list
                            val = str(res)
                if val and sys.version_info.major == 2:
                    line.append(val.encode('utf8'))
                else:
                    line.append(val)

            if self._auto_cno > 0 and len(line) < self._auto_cno:
                line = line + [None]*(self._auto_cno - len(line))

            self._writeRow(line)
        except:
            Log.debug('record=%s' % etree.tostring(record, pretty_print = False))
            Log.debug('col=%s' % str(col))
            raise
    
    def _writeRow(self, line):
        if self._out_flags & STRING:
            for wri in self._writers:
                wri.writerow(line)
        if self._out_flags & (LIST | ITERABLE):
            self._out.pushObject(line)
