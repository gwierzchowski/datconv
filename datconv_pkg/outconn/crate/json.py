# -*- coding: utf-8 -*-
"""This module implements Datconv Output Connector which saves data to file that contain one JSON object per line.
Such files can serve as imput files for COPY FROM caluse used in crate.io database.
This connector should be used with Writer: datconv.writers.dcjson
"""

# Standard Python Libs
import sys
import json
import collections

# Datconv packages
from .. import STRING, OBJECT
from . import *


Log = None
"""Log varaible is automatically set by main datconv script using logging.getLogger method.
Use it for logging messages in need.
"""


class DCConnector:
    """Please see constructor description for more details."""
    def __init__(self, path, check_keywords = True, lowercase = 1, no_underscore = 1, move_to_front = [], cast = None):
        """Parameters are usually passed from YAML file as subkeys of OutConnector:CArg key.
        
        :param path: relative or absolute path to output file.
        :param check_keywords: if true, prevents conflicts with SQL keywords.
        :param lowercase: if >1, all JSON keys will be converted to lower-case; if =1, only first level keys; if =0, no conversion happen.
        :param no_underscore: if >1, leading ``_`` will be removed from all JSON keys; if =1, only from first level of keys; if =0, option is disabled.
        :param move_to_front: those first level keys will be placed at begin of record. This option requires ``dcjson`` Writer option ``preserve_order`` to be set.
        :param cast: array of arrays of the form: [['rec', 'value'], str], what means that record: {"rec": {"value": 5025}} will be writen as {"rec": {"value": "5025"}} - i.e. it is ensured that "value" will allways be string. First position determines address of data to be converted, last position specifies the type: str, bool, int, long or float. Field names shold be given after all other configured transformations (lowercase, no_underscore, check_keywords).
        
        For more detailed descriptions see :ref:`conf_template.yaml <outconn_crate_conf_template>` file in this module folder.
        """
        assert Log is not None

        self._path = path
        self._out = open(path, "w")
        self._chkkwd = check_keywords
        self._cast = cast
        self._lowercase = lowercase
        self._no_underscore = no_underscore
        self._move = move_to_front
        if len(move_to_front) > 0 and sys.version_info[0] < 3:
            # no collections.OrderedDict.move_to_end
            Log.warning("move_to_front outconn.crate.json option is not supported in Python 2, option ignored")
            self._move = []
        self._total_no = 0
        
    def supportedInterfases(self):
        return OBJECT
    
    def tryObject(self, obj):
        self._total_no = 0
        if len(self._move) > 0:
            return isinstance(obj, collections.OrderedDict)
        else:
            return isinstance(obj, dict)
    
    def pushObject(self, obj):
        self._total_no += 1
        if self._lowercase > 0:
            lowerKeys(obj, self._lowercase > 1)
        if self._no_underscore > 0:
            removeUnder(obj, self._no_underscore > 1)
        if self._chkkwd:
            checkKeywords(obj)
        if self._cast:
            castValues(obj, self._cast)
        if len(self._move) > 0:
            self._moveKeys(obj)
        json.dump(obj, self._out)
        self._out.write('\n')
    
    def onFinish(self, bSuccess):
        if Log:
            if bSuccess:
                Log.info('%d records saved to %s' % (self._total_no, self._path))
            else:
                Log.error('Program did not finished properly: output saved to %s may be inconsistent' % self._path)
        self._out.close()
           
    def _moveKeys(self, obj):
        for item in reversed(self._move):
            if item in obj:
                obj.move_to_end(item, last = False)
