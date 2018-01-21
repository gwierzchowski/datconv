# -*- coding: utf-8 -*-
"""This module implements Datconv Writer which saves data in form of JSON file."""

# In Python 2.7 only
from __future__ import print_function

# Standard Python Libs
import sys
import json
import collections
import logging

# Libs installed using pip
from lxml import etree


Log = None
"""Log varaible is automatically set by main datconv script using logging.getLogger method.
Use it for logging messages in need.
"""

class DCWriter:
    """Please see constructor description for more details."""
    def __init__(self, add_header = True, add_footer = True, add_newline = True, \
        convert_values = False, null_text = 'None', preserve_order = False, \
        text_key = 'text', text_eliminate = True, with_prop = False, ign_rectyp = False, json_opt = None):
        """Parameters are usually passed from YAML file as subkeys of Writer:CArg key.
        
        :param add_header: if True, generic header (as initialized by Reader) is added as first object of output file.
        :param add_footer: if True, generic footer (as initialized by Reader) is added as last object of output file.
        :param add_newline: if True, adds newline character after each record.
        :param convert_values: if True, tries to convert velues to int, bool or float (do not quote in json file) - little slower, oterwise all values are placed as strings in json.
        :param null_text: text that is converted to JSON null value (apply if convert_values is True).
        :param preserve_order: if True, order of keys in json output match order in source.
        :param text_key: name of key to store XML text.
        :param text_eliminate: if True, XML text key will be eliminated if there are no other tag components.
        :param with_prop: if True, XML properties are being saved in JSON file.
        :param ign_rectyp: if True, XML root tag for records (aka record type) will not be saved in JSON file (simplifies output layout in case there is one record type).
        :param json_opt: dictionary with json.dump() options. See `documentation <https://docs.python.org/3/library/json.html>`_ of json standard Python library.
        
        For more detailed descriptions see :ref:`conf_template.yaml <writers_conf_template>` file in this module folder.
        """
        assert Log is not None

        self._out = sys.stdout
        self._add_header = add_header
        self._add_footer = add_footer
        self._add_newline = add_newline
        self._convert_values = convert_values
        self._null_text = null_text
        self._preserve_order = preserve_order
        self._text_key = text_key
        self._text_eliminate = text_eliminate
        self._with_prop = with_prop
        self._ign_rectyp = ign_rectyp
        self._json_opt = json_opt

    def setOutput(self, out):
        self._out = out
        self._first = True
       
    def writeHeader(self, header):
        self._out.write('[')
        if self._add_header:
            for h in header:
                if self._first:
                    self._first = False
                else:
                    self._out.write(',')
                if self._add_newline:
                    self._out.write('\n')
                if isinstance(h, dict):
                    if self._convert_values:
                        for (key, val) in h.items():
                            val = self._TryConvert(val)
                            h[key] = val
                    if '_tag_' in h:
                        tag = h['_tag_']
                        del h['_tag_']
                        if '_bra_' in h:
                            del h['_bra_']
                        obj = {tag: h}
                    else:
                        obj = h
                else:
                    if self._convert_values:
                        h = self._TryConvert(h)
                    obj = {'header': str(h)}
                if self._json_opt:
                    json.dump(obj, self._out, **self._json_opt)
                else:
                    json.dump(obj, self._out)

    def writeFooter(self, footer):
        if self._add_footer:
            for f in footer:
                if self._first:
                    self._first = False
                else:
                    self._out.write(',')
                if self._add_newline:
                    self._out.write('\n')
                if isinstance(f, dict):
                    if self._convert_values:
                        for (key, val) in f.items():
                            val = self._TryConvert(val)
                            f[key] = val
                    if '_tag_' in f:
                        tag = f['_tag_']
                        del f['_tag_']
                        obj = {tag: f}
                    else:
                        obj = f
                else:
                    if self._convert_values:
                        f = self._TryConvert(f)
                    obj = {'footer': str(f)}
                if self._json_opt:
                    json.dump(obj, self._out, **self._json_opt)
                else:
                    json.dump(obj, self._out)
        if self._add_newline:
            self._out.write('\n')
        self._out.write(']')
        
    def writeRecord(self, record):
        try:
            if self._first:
                self._first = False
            else:
                self._out.write(',')
            if self._add_newline:
                self._out.write('\n')
            obj = {}
            if self._with_prop:
                element2obj = self._element2objP
            else:
                element2obj = self._element2obj
            if self._ign_rectyp:
                obj = element2obj(record)
            else:
                obj[record.tag] = element2obj(record)
            if self._json_opt:
                json.dump(obj, self._out, **self._json_opt)
            else:
                json.dump(obj, self._out)
        except:
            Log.debug('record=%s' % etree.tostring(record, pretty_print = False))
            raise
        
    #############################################################
    # Internal Methods
    #############################################################
    
    def _element2obj(self, el):
        """XML properties are ignored"""
        if self._text_eliminate and len(el) == 0:
            if self._convert_values:
                return self._TryConvert(el.text)
            else:
                return el.text
        if self._preserve_order:
            ret = collections.OrderedDict()
        else:
            ret = {}
        if el.text is not None:
            if self._convert_values:
                text = self._TryConvert(el.text)
                ret[self._text_key] = text
            else:
                ret[self._text_key] = el.text
        for tag in el:
            if tag.tag in ret:
                if isinstance(ret[tag.tag], list):
                    ret[tag.tag].append(self._element2obj(tag))
                else:
                    ret[tag.tag] = [ret[tag.tag], self._element2obj(tag)]
            else:
                ret[tag.tag] = self._element2obj(tag)
        return ret
    
    def _element2objP(self, el):
        """XML properties are saved as keys"""
        if self._text_eliminate and len(el) == 0 and len(el.items()) == 0:
            if self._convert_values:
                return self._TryConvert(el.text)
            else:
                return el.text
        if self._preserve_order:
            ret = collections.OrderedDict()
        else:
            ret = {}
        for (pname, pprop) in el.items():
            if self._convert_values:
                pprop = self._TryConvert(pprop)
            ret[pname] = pprop
        if el.text is not None:
            if self._convert_values:
                text = self._TryConvert(el.text)
                ret[self._text_key] = text
            else:
                ret[self._text_key] = el.text
        for tag in el:
            if tag.tag in ret:
                if isinstance(ret[tag.tag], list):
                    ret[tag.tag].append(self._element2objP(tag))
                else:
                    ret[tag.tag] = [ret[tag.tag], self._element2objP(tag)]
            else:
                ret[tag.tag] = self._element2objP(tag)
        return ret
        
    #############################################################
    # Helper Functions
    #############################################################
    def _TryConvert(self, val):
        if val is None:
            return None
        if val == self._null_text:
            return None
        try:
            return int(val) #Note: True=>1; False=>0
        except ValueError:
            try:
                return float(val)
            except ValueError:
                return val
        except TypeError:
            return val
