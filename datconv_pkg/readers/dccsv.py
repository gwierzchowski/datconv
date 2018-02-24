# -*- coding: utf-8 -*-
# Checked with python 2.7
"""This module implements Datconv Reader which reads data from CSV file."""

# Standard Python Libs
import logging
import csv

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
    """This module implements Datconv Reader which reads data from CSV file."""
    def __init__(self, columns = 'item', strip = False, csv_opt = None):
        """Parameters are usually passed from YAML file as subkeys of Reader:CArg key.
        
        :param columns: this parameter may be one of 3 possible types:\n
            if it is positive number, it specifies line number in input file that stores column names. \n
            if it is a list, it directly specifies column names in input file. \n
            if it is string it stands for column name prefix, i.e. columns will have names <prefix>1, <prefix>2, ...
        :param strip: if True, strips white spaces from values
        :param csv_opt: dictionary with csv writer options. See `documentation <https://docs.python.org/3/library/csv.html>`_ of csv standard Python library. If None, Reader tries to recognize format using ``csv.Sniffer`` class.
        
        For more detailed descriptions see :ref:`conf_template.yaml <readers_conf_template>` file in this module folder.
        """
        assert Log is not None
        self._wri = self._flt = None
        if isinstance(columns, int):
            self._colrow = columns
        else:
            self._colrow = 0
        self._column = {}
        if isinstance(columns, list):
            colnr = 1
            for col in columns:
                self._column[colnr] = col
                colnr = colnr + 1
        if isinstance(columns, str):
            self._colpref = columns
        else:
            self._colpref = 'item'
        self._strip = strip
        self._csv = csv_opt

    def setWriter(self, writer):
        self._wri = writer

    def setFilter(self, flt):
        self._flt = flt

    def Process(self, inpath, outpath = None, rfrom = 1, rto = 0):
        """Parameters are usually passed from YAML file as subkeys of ``Reader:PArg`` key.
        
        :param inpath: Path to input file.
        :param outpath: Path to output file passed to Writer (fall-back if output connector is not defined).
        :param rfrom-rto: specifies scope of records to be processed.
        
        For more detailed descriptions see :ref:`readers_conf_template`.
        """
        
        #fout = open(outpath, "w")
        
        ## OBLIGATORY
        #self._wri.setOutput(fout)
        
        # OBLIGATORY
        header = []
        if self._flt is not None:
            if hasattr(self._flt, 'setHeader'):
                self._flt.setHeader(header)
        
        # OBLIGATORY
        self._wri.writeHeader(header)

        with open(inpath, newline='') as csvfile:
            if self._csv:
                _rea = csv.reader(csvfile, **self._csv)
            else:
                dialect = csv.Sniffer().sniff(csvfile.read(1024))
                csvfile.seek(0)
                _rea = csv.reader(csvfile, dialect)
            rowno = 0
            recno = 0
            for line in _rea:
                rowno = rowno + 1
                if rowno < self._colrow:
                    continue
                colno = 1
                if rowno == self._colrow:
                    for item in line:
                        self._column[colno] = _NormalizeTag(item)
                        colno = colno + 1
                    continue
                recno = recno + 1
                if recno < rfrom:
                    continue
                if rto > 0 and recno > rto:
                    break
                rec = etree.Element('rec')
                for item in line:
                    if colno in self._column:
                        key = self._column[colno]
                    else:
                        key = self._colpref + str(colno)
                        self._column[colno] = key
                    if self._strip:
                        etree.SubElement(rec, key).text = item.strip()
                    else:
                        etree.SubElement(rec, key).text = item
                    colno = colno + 1
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

        # OBLIGATORY
        footer = []
        if self._flt is not None:
            if hasattr(self._flt, 'setFooter'):
                self._flt.setFooter(footer)
        self._wri.writeFooter(footer)
        
def _NormalizeTag(tagname):
    return tagname.strip().translate(str.maketrans('', '', '<> /\\?:;[]{}~`!@#$%^&*()+=|"\''))
