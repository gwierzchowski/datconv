# -*- coding: utf-8 -*-
"""This module implements Pandoc Writer which saves data in form of CSV file.
Please see DCWriter constructor description for more details.
"""

# In Python 2.7 only
from __future__ import print_function

# Standard Python Libs
import sys
import csv
import logging

# Libs installed using pip
from lxml import etree

#Datconv writer classes
from . import dcxpaths


Log = None
"""Log varaible is automatically set by main pandoc script using logging.getLogger method.
Use it for logging messages in need.
"""

class DCWriter:
    def __init__(self, columns = None, simple_xpath = False, add_header = False, col_names = True, csv_opt = None):
        """Parameters are usually passed from YAML file as subkeys of Writer:CArg key.
        columns - this parameter may be one of 3 possible types or None.
                  If it is a string, it should be the path to file that contain specification of columns in output file.
                  If it is a list, it directly specifies columns in output file.
                  If it is None or distionary, columns in output CSV file are being generated automatically 
                  based on contentents of input file. Number of columns in different records in CSV file 
                  (when this option is used) may very as new columns are being added when discovered.
        simple_xpath - determines weather simple xpaths are used in column specification.
                       See pdxpath Writer for more descripption.
        add_header - if True, generic header (as initialized by Reader) is added as first line of output file.
        col_names - if True, line with column names (fields) is added before data or after data (in case of auto option).
        csv_opt - dictionary with csv writer options. See documantation of csv standard Python library.
        For more detailed descriptions see conf_template.yaml file in this module folder.
        """
        assert Log is not None
        dcxpaths.Log = Log

        self._wri = None
        self._auto_xpw = None
        self._auto_cno = 0
        self._col = []
        if columns is not None:
            if isinstance(columns, str):
                rea = csv.reader(open(columns), lineterminator='\n')
                for col in rea:
                    if col and len(col) == 4 and col[0][0] != '#':
                        self._col.append(col)
            if isinstance(columns, dict):
                self._auto_xpw = dcxpaths.DCWriter(simple_xpath = simple_xpath, **columns)
                if columns.get('colno'):
                    self._auto_cno = columns.get('colno')
            if isinstance(columns, list):
                for col in columns:
                    if col and len(col) == 4 and col[0][0] != '#':
                        self._col.append(col)
        else:
            self._auto_xpw = dcxpaths.DCWriter(simple_xpath = simple_xpath)
        self._simple_xpath = simple_xpath
        self._add_header = add_header
        self._col_names = col_names
        self._csv = csv_opt

    def setOutput(self, out):
        if self._csv:
            self._wri = csv.writer(out, **self._csv)
        else:
            self._wri = csv.writer(out)
        if self._auto_xpw:
            self._auto_xpw.resetXPaths()
            self._col = []
       
    def writeHeader(self, header):
        if self._add_header:
            self._wri.writerow([str(header)] + [None]*(len(self._col) - 1))
        if self._col_names and self._auto_xpw is None:
            self._wri.writerow([c[0] for c in self._col])

    def writeFooter(self, header):
        if self._col_names and self._auto_xpw is not None:
            cn = [c[0] for c in self._col]
            if self._auto_cno > 0 and len(cn) < self._auto_cno:
                cn = cn + ['Spare']*(self._auto_cno - len(cn))
            self._wri.writerow(cn)
        
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

            self._wri.writerow(line)
        except:
            Log.debug('record=%s' % etree.tostring(record, pretty_print = False))
            Log.debug('col=%s' % str(col))
            raise
