# -*- coding: utf-8 -*-
"""This module implements Datconv Output Connector which directly inserts data to crate.io database.
This connector should be used with Writer: ``datconv.writers.dcjson``.
It requires Python package ``crate`` to be installed.
"""

# Standard Python Libs
import sys
import json
import collections

# Libs installed using pip
#import yaml
from crate import client

# Datconv packages
from .. import STRING, OBJECT
from . import *


Log = None
"""Log varaible is automatically set by main datconv script using logging.getLogger method.
Use it for logging messages in need.
"""


class DCConnector:
    """Please see constructor description for more details."""
    def __init__(self, table, connstring, user = None, password = None, \
        check_keywords = True, cast = None, lowercase = 0, no_underscore = 0):
        """Parameters are usually passed from YAML file as subkeys of OutConnector:CArg key.
        
        :param table: table name where to insert records.
        :param connstring: connection string to database. If it begins with file: insert statements are being saved to given file.
        :param user: user name for databse connection.
        :param password: password for databse connection.
        :param check_keywords: if true prevents conflicts with SQL keywords.
        :param cast: array of arrays of the form: [['rec', 'value'], str], what means that record: {"rec": {"value": 5025}} will be writen as {"rec": {"value": "5025"}} - i.e. it is ensured that "value" will allways be string. First position determines address of data to be converted, last position specifies the type: str, bool, int, long or float. Field names shold be given after all other configured transformations (lowercase, no_underscore, check_keywords).
        :param lowercase: if >1 all JSON keys will be converted to lower-case, if =1 only first level keys.
        :param no_underscore: if >1 ``_`` will be removed from all JSON keys, if =1 only from first level of keys.
        
        For more detailed descriptions see :ref:`conf_template.yaml <outconn_conf_template>` file in this module folder.
        """
        assert Log is not None

        self._tablename = table
        self._connstring = connstring
        if connstring.startswith('file:'):
            self._debug = True
            self._conn = open(connstring[7:], "w")
        else:
            self._debug = False
            self._conn = client.connect(connstring,\
                username = user,\
                password = password)
            self._cur = self._conn.cursor()
        self._chkkwd = check_keywords
        if check_keywords:
            if self._tablename.upper() in Keywords:
                self._tablename = self._tablename + '_'
        self._lowercase = lowercase
        if self._lowercase > 0:
            self._tablename = self._tablename.lower()
        self._PREFIX = 'INSERT INTO "%s"(' % self._tablename
        self._cast = cast
        self._no_underscore = no_underscore
        self._total_no = 0
        self._inserted_no = 0
        
    def supportedInterfases(self):
        return OBJECT
    
    def tryObject(self, obj):
        self._total_no = 0
        self._inserted_no = 0
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
        self._pushRecord(obj)
    
    def onFinish(self, bSuccess):
        if Log:
            if self._debug:
                if bSuccess:
                    Log.info('%d records saved to %s' % (self._inserted_no, self._connstring))
                else:
                    Log.error('Program did not finished properly: output saved to %s may be inconsistent' % self._connstring)
                self._conn.close()
            else:
                if bSuccess:
                    Log.info('%d out of %d records inserted to table %s in %s' % (self._inserted_no, self._total_no, self._tablename, self._connstring))
                else:
                    Log.error('Program did not finished properly: only %d out of %d records were saved' % (self._inserted_no, self._total_no))
                self._cur.close()
                self._conn.close()

    def _pushRecord(self, obj):
        fields = ''
        params = ''
        values = []
        for k, v in obj.items():
            fields += '"' + str(k) + '",'
            if self._debug:
                params += obj2str(v) + ','
            else:
                params += '?,'
                values.append(v)
        if self._debug:
            sql = self._PREFIX + fields[:-1] + ') VALUES (' + params[:-1] + ');\n'
            self._conn.write(sql)
            self._inserted_no += 1
        else:
            sql = self._PREFIX + fields[:-1] + ') VALUES (' + params[:-1] + ')'
            self._cur.execute(sql, tuple(values))
            self._inserted_no += self._cur.rowcount
       
