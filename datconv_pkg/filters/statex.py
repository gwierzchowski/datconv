#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""General Filter that allows to calculate and print required statistics about processed data - extended version.
Filter prints counts or sums of records that fulfill given expression with option to group by certain data.
Filter prints statistics at program exit as logger INFO messages."""

# Standard Python Libs
from importlib import import_module

# Libs installed using pip
from lxml import etree


Log = None
"""Log varaible is automatically set by main pandoc script using logging.getLogger method.
Use it for logging messages in need.
"""

class DCFilter:
    def __init__(self, retval = 1, fields = [], statfile = None, statwriter = None):
        """Parameters are usually passed from YAML file as subkeys of Filter:CArg key.
        retval - value that filter returns (0 to skip records, 1 to write records);
        fields - list of 5 or 6 elements' lists that define calculated statistics.
        statfile - file to write final statistics
        statwriter - datconv writer module to write final statistics
        For more detailed descriptions see conf_template.yaml file in this module folder.
        """
        assert Log is not None
        self._retval = retval
        self._fields = fields
        self._sfile = statfile
        self._swconf = statwriter
        self._swri = None
        self._stats = {}
        self._recno = 1

    def filterRecord(self, record):
        for fld in self._fields:
            if len(fld) < 5:
                Log.warning('Too few items in fields definition: %s' % str(fld))
                continue
            if fld[1] is None or record.tag == str(fld[1]):
                if fld[2] == False:
                    continue
                elif fld[2] == True:
                    eval = True
                else:
                    res = record.xpath(fld[2])
                    eval = bool(_eval_xpath_result_as_scalar(res))
                if eval:
                    if fld[3] is None:
                        key = '*'
                    else:
                        res = record.xpath(fld[3])
                        key = _eval_xpath_result_as_scalar(res)
                        if key is None:
                            key = 'null'
                    if fld[4] == 'c':
                        aval = 1
                    elif fld[4] == 's' and fld[5]:
                        res = record.xpath(fld[5])
                        val = _eval_xpath_result_as_scalar(res)
                        try:
                            aval = float(val)
                        except:
                            aval = 0
                        if int(aval) == aval:
                            aval = int(aval)
                    else:
                        continue
                    stat = self._stats.get(fld[0])
                    if not stat:
                        self._stats[fld[0]] = stat = {}
                    val = stat.get(key)
                    stat[key] = (val + aval) if val else aval
         
        self._recno = self._recno + 1
        return self._retval
    
    def __del__(self):
        self._init_swriter()
        for fld in self._fields:
            stat = self._stats.get(fld[0])
            if stat:
                for key in sorted(stat.keys()):
                    val = stat[key]
                    self._write_stat(fld[0], key, val)
            else:
                self._write_stat(fld[0], '', 0)
        if self._swri:
            self._swri.writeFooter([])

    def _init_swriter(self):
        if self._swconf:
            sw_path = self._swconf.get('Module')
            if sw_path:
                sw_mod = import_module(sw_path)
                sw_mod.Log = Log.getChild('statwriter')
                sw_class = getattr(sw_mod, 'DCWriter')
                sw_carg = self._swconf.get('CArg')
                self._swri = sw_class(**sw_carg) if sw_carg else sw_class()
            else:
                Log.error("Invalid configuration: there is statwriter defined but no sub-key: Module")
            if self._sfile:
                self._swri.setOutput(open(self._sfile, 'w'))
                self._swri.writeHeader([])
            else:
                self._swri = None
                Log.error("Invalid configuration: there is statwriter defined but no key: statfile")

    def _write_stat(self, sname, key, val):
        if self._swri:
            stag = etree.Element('STAT')
            stag.text = sname
            ktag = etree.SubElement(stag, 'KEY')
            ktag.text = str(key)
            vtag = etree.SubElement(stag, 'VAL')
            vtag.text = str(val)
            self._swri.writeRecord(stag)
        else:
            Log.info("{}[{}]: {}".format(sname, key, val))
                
def _eval_xpath_result_as_scalar(res):
    if res is None or res == []:
        return None
    if isinstance(res, list) and len(res) > 0:
        res = res[0]
    if etree.iselement(res):
        val = res.text
    elif isinstance(res, str):
        val = res
    elif isinstance(res, float):
        val = res
        if int(val) == val:
            val = int(val)
    elif isinstance(res, int):
        val = res
    elif isinstance(res, bool):
        val = res
    else:
        val = str(res)
    return val
                