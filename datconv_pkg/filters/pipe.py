#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
General Filter that allows users to run several other filters one after one.
Values returned by configured filters' are combined in following way:

- to get record written (sent to Writer) all filters must set WRITE bit
- to get record repeated at leat one filter must set REPEAT bit
- to get process break at leat one filter must set BREAK bit
- REPEAT bit takes precedence over BREAK bit (i.e. if both are set record is re-evaluated)
"""

# Standard Python Libs
from importlib import import_module

# Datconv packages
from . import SKIP, WRITE, REPEAT, BREAK


Log = None
"""Log variable is automatically set by main datconv script using logging.getLogger method.
Use it for logging messages in need.
"""

class DCFilter:
    """Please see constructor description for more details."""
    def __init__(self, flist, pass_skiped = True):
        """Constructor parameters are usually passed from YAML file as subkeys of Filter:CArg key.
        
        :param flist: list of filters to be run in chain with their parameters;
        :param pass_skiped: if it is False, records for which some filter returned SKIP will not be passed to next filters;
        
        For more detailed descriptions see :ref:`conf_template.yaml <filters_conf_template>` file in this module folder.
        """
        assert Log is not None
        assert isinstance(flist, list)
        self._pass_skiped = pass_skiped
        self._flist = []
        for flt in flist:
            flt_path = flt['Module']
            flt_carg = flt.get('CArg')
            flt_mod = import_module(flt_path)
            flt_mod.Log = Log
            flt_class = getattr(flt_mod, 'DCFilter')
            Log.debug('Adding filter: %s(%s)', flt_path, str(flt_carg))
            flt_inst = flt_class(**flt_carg) if flt_carg else flt_class()
            self._flist.append(flt_inst)

    def setHeader(self, header):
        for flt in self._flist:
            if hasattr(flt, 'setHeader'):
                flt.setHeader(header)

    def filterRecord(self, record):
        res = WRITE
        for flt in self._flist:
            ret = flt.filterRecord(record)
            if ret & REPEAT:
                res |= REPEAT
            if ret & BREAK:
                res |= BREAK
            if not (ret & WRITE):
                res &= ~WRITE
                if not self._pass_skiped:
                    break
        return res

    def setFooter(self, footer):
        for flt in self._flist:
            if hasattr(flt, 'setFooter'):
                flt.setFooter(footer)
