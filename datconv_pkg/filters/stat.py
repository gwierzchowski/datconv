#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""General Filter that allows to calculate and print required statistics about processed data.
Filter prints first record number when given XPath expression is met and number of records in which it is met.
Filter prints statistics at program exit as logger INFO messages."""

# Libs installed using pip
from lxml import etree


Log = None
"""Log varaible is automatically set by main pandoc script using logging.getLogger method.
Use it for logging messages in need.
"""

class DCFilter:
    def __init__(self, retval = 1, rectyp = True, printzero = False, fields = []):
        """Parameters are usually passed from YAML file as subkeys of Filter:CArg key.
        retval - value that filter returns (0 to skip records, 1 to write records);
        rectyp - if True, record type (root tag) is included into statistics;
                 i.e. it is printed how many records are of particular types.
        printzero - if True, not found records (with count 0) are included into summary (except when groupping is used)
        fields - list of 2 elements' lists:
                 first element is absolute XPath expression to make statistics against 
                 (lxml.etree._element.xpath method compatible)
                 second element is a digit:
                 0 - if we test against element existance (i.e. not None and not [])
                 1 - if we are grouping against element value
                 2 - if given XPath expression returns boolean value.
        For more detailed descriptions see conf_template.yaml file in this module folder.
        """
        assert Log is not None
        self._retval = retval
        self._rectyp = rectyp
        self._fields = fields
        self._stats = {}
        self._recno = 1
        if printzero:
            for fld in self._fields:
                if fld[1] != 1:
                    self._stats[fld[0]] = 'not found', 0

    def filterRecord(self, record):
        if self._rectyp:
            val = self._stats.get(record.tag)
            if val:
                f, c = val
                self._stats[record.tag] = f, c + 1
            else:
                self._stats[record.tag] = self._recno, 1
        
        for fld in self._fields:
            res = record.xpath(fld[0])
            if res is not None and res != []:
                if fld[1] == 0:
                    key = fld[0]
                elif fld[1] == 1:
                    # Equivalent code is in writers.pdcsv.py / writeRecord
                    if isinstance(res, list) and len(res) > 0:
                        res = res[0]
                    if etree.iselement(res):
                        val = res.text
                    elif isinstance(res, str):
                        val = res
                    elif not isinstance(res, list): # exclude empty list
                        val = str(res)
                    else:
                        continue
                    key = fld[0] + ' = ' + val
                elif fld[1] == 2:
                    if res:
                        key = fld[0]
                    else:
                        continue
                else:
                    continue
                val = self._stats.get(key)
                if val:
                    f, c = val
                    if c > 0:
                        self._stats[key] = f, c + 1
                    else:
                        self._stats[key] = self._recno, 1
                else:
                    self._stats[key] = self._recno, 1
         
        self._recno = self._recno + 1
        return self._retval

    def __del__(self):
        for k in sorted(self._stats.keys()):
            v = self._stats[k]
            if isinstance(v[0], int):
                Log.info("%s: first %d, count %d", k, v[0], v[1])
            else:
                Log.info("%s: first %s, count %d", k, str(v[0]), v[1])
            