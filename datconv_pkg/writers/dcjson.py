# -*- coding: utf-8 -*-
"""This module implements Datconv Writer which saves data in form of JSON file.
Supports connectors of type: STRING, OBJECT (dict()), ITERABLE."""

# In Python 2.7 only
from __future__ import print_function

# Standard Python Libs
import sys
import json
import collections
import logging

# Libs installed using pip
from lxml import etree

# Datconv generic modules
from datconv.outconn import STRING, OBJECT, ITERABLE


Log = None
"""Log varaible is automatically set by main datconv script using logging.getLogger method.
Use it for logging messages in need.
"""

class DCWriter:
    """Please see constructor description for more details."""
    def __init__(self, add_header = True, add_footer = True, add_newline = True, \
        convert_values = 2, null_text = 'None', preserve_order = False, \
        text_key = 'text', text_eliminate = True, with_prop = False, ignore_rectyp = False, json_opt = None):
        """Parameters are usually passed from YAML file as subkeys of Writer:CArg key.
        
        :param add_header: if True, generic header (as initialized by Reader) is added as first object of output file.
        :param add_footer: if True, generic footer (as initialized by Reader) is added as last object of output file.
        :param add_newline: if True, adds newline character after each record.
        :param convert_values: 0 - does not convert (all values are text); 1 - tries to convert values to int, bool or float (do not quote in json file) - little slower; 2 - like 1 but in addition checks if int values can be stored in 64 bits, if not place them as string value.
        :param null_text: text that is converted to JSON null value (apply if convert_values is True).
        :param preserve_order: if True, order of keys in json output match order in source.
        :param text_key: name of key to store XML text.
        :param text_eliminate: if True, XML text key will be eliminated if there are no other tag components.
        :param with_prop: if True, XML properties are being saved in JSON file.
        :param ignore_rectyp: if True, XML root tag for records (aka record type) will not be saved in JSON file (simplifies output layout in case there is one record type).
        :param json_opt: dictionary with json.dump() options. See `documentation <https://docs.python.org/3/library/json.html>`_ of json standard Python library.
        
        For more detailed descriptions see :ref:`conf_template.yaml <writers_conf_template>` file in this module folder.
        """
        assert Log is not None

        self._out = None
        self._out_flags = 0;
        self._add_header = add_header
        self._add_footer = add_footer
        self._add_newline = add_newline
        self._convert_values = convert_values
        self._max_int = 2**64 - 1
        self._min_int = - 2**63
        self._null_text = null_text
        self._preserve_order = preserve_order
        self._text_key = text_key
        self._text_eliminate = text_eliminate
        self._with_prop = with_prop
        self._ign_rectyp = ignore_rectyp
        self._json_opt = json_opt

    def setOutput(self, out):
        self._first = True
        self._out = out
        self._out_flags = out.supportedInterfases();
        if self._out_flags & (OBJECT | ITERABLE):
            if self._preserve_order:
                if not out.tryObject(collections.OrderedDict()):
                    raise Exception('Incompatible OutConnector used, dcjson Writer option requires that connector supports dict objects')
            else:
                if not out.tryObject(dict()):
                    raise Exception('Incompatible OutConnector used, dcjson Writer requires that connector supports dict objects or OutConnector requires dcjson preserve_order option')
       
    def writeHeader(self, header):
        if self._out_flags & STRING:
            self._out.pushString('[')
        if self._add_header:
            for h in header:
                if self._first:
                    self._first = False
                elif self._out_flags & STRING:
                    self._out.pushString(',')
                if self._add_newline and self._out_flags & STRING:
                    self._out.pushString('\n')
                if isinstance(h, dict):
                    if self._convert_values > 0:
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
                    if self._convert_values > 0:
                        h = self._TryConvert(h)
                    obj = {'header': str(h)}
                if self._out_flags & STRING:
                    for stream in self._out.getStreams():
                        if self._json_opt:
                            json.dump(obj, stream, **self._json_opt)
                        else:
                            json.dump(obj, stream)
                if self._out_flags & (OBJECT | ITERABLE):
                    self._out.pushObject(collections.OrderedDict(obj))

    def writeFooter(self, footer):
        if self._add_footer:
            for f in footer:
                if self._first:
                    self._first = False
                elif self._out_flags & STRING:
                    self._out.pushString(',')
                if self._add_newline and self._out_flags & STRING:
                    self._out.pushString('\n')
                if isinstance(f, dict):
                    if self._convert_values > 0:
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
                    if self._convert_values > 0:
                        f = self._TryConvert(f)
                    obj = {'footer': str(f)}
                if self._out_flags & STRING:
                    for stream in self._out.getStreams():
                        if self._json_opt:
                            json.dump(obj, stream, **self._json_opt)
                        else:
                            json.dump(obj, stream)
                if self._out_flags & (OBJECT | ITERABLE):
                    self._out.pushObject(collections.OrderedDict(obj))
        if self._out_flags & STRING:
            if self._add_newline:
                self._out.pushString('\n')
            self._out.pushString(']')
        
    def writeRecord(self, record):
        try:
            if self._first:
                self._first = False
            elif self._out_flags & STRING:
                self._out.pushString(',')
            if self._add_newline and self._out_flags & STRING:
                self._out.pushString('\n')
            obj = {}
            if self._with_prop:
                element2obj = self._element2objP
            else:
                element2obj = self._element2obj
            if self._ign_rectyp:
                obj = element2obj(record)
            else:
                obj[record.tag] = element2obj(record)
            if self._out_flags & STRING:
                for stream in self._out.getStreams():
                    if self._json_opt:
                        json.dump(obj, stream, **self._json_opt)
                    else:
                        json.dump(obj, stream)
            if self._out_flags & (OBJECT | ITERABLE):
                self._out.pushObject(obj)
        except:
            Log.debug('record=%s' % etree.tostring(record, pretty_print = False))
            raise
        
    #############################################################
    # Internal Methods
    #############################################################
    
    def _element2obj(self, el):
        """XML properties are ignored"""
        if self._text_eliminate and len(el) == 0:
            if self._convert_values > 0:
                return self._TryConvert(el.text)
            else:
                return el.text
        if self._preserve_order:
            ret = collections.OrderedDict()
        else:
            ret = {}
        if el.text is not None:
            if self._convert_values > 0:
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
            if self._convert_values > 0:
                return self._TryConvert(el.text)
            else:
                return el.text
        if self._preserve_order:
            ret = collections.OrderedDict()
        else:
            ret = {}
        for (pname, pprop) in el.items():
            if self._convert_values > 0:
                pprop = self._TryConvert(pprop)
            ret[pname] = pprop
        if el.text is not None:
            if self._convert_values > 0:
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
            if self._convert_values > 1:
                ret = int(val)
                if ret > self._max_int or ret < self._min_int:
                    return val
                return ret
            else:
                return int(val) #Note: True=>1; False=>0
        except ValueError:
            try:
                return float(val)
            except ValueError:
                return val
        except TypeError:
            return val
