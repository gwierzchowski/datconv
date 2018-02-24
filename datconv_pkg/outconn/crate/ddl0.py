# -*- coding: utf-8 -*-
"""This module implements Datconv Output Connector which generates CREATE TABLE cause in database crate.io dialect.
This connector should be used with Writer: datconv.writers.dcxpaths with option add_header = false and add_type = true.
"""

# Standard Python Libs

# Datconv packages
from .. import LIST


Log = None
"""Log varaible is automatically set by main datconv script using logging.getLogger method.
Use it for logging messages in need.
"""

_CrateType = { \
    'int': 'integer', \
    'float': 'float', \
    'str': 'string', \
    }

_CrateKeyword = [ \
    'count', \
    'float', \
    'string', \
    # TODO: Complete list
    ]

class DCConnector:
    """Please see constructor description for more details."""
    def __init__(self, path, tablename, check_keywords = True, lowercase = 0, no_underscore = 0, primary_key = []):
        """Parameters are usually passed from YAML file as subkeys of OutConnector:CArg key.
        
        :param path: relative or absolute path to output file.
        :param tablename: name of the table.
        :param check_keywords: if true prevents conflicts with SQL keywords.
        :param lowercase: if >1 all JSON keys will be converted to lower-case, if =1 only first level keys.
        :param no_underscore: if >1 ``_`` will be removed from all JSON keys, if =1 only from first level of keys.
        :param primary_key: those first level keys will be declared as primary keys.
        
        For more detailed descriptions see :ref:`conf_template.yaml <outconn_conf_template>` file in this module folder.
        """
        assert Log is not None

        self._path = path
        self._out = open(path, "w")
        self._tablename = tablename
        self._chkkwd = check_keywords
        if check_keywords:
            if self._tablename in _CrateKeyword:
                self._tablename = self._tablename + '_'
        self._lowercase = lowercase
        self._no_underscore = no_underscore
        self._pkeys = primary_key
        
        self._fields = []
        self._curr_field = None
        self._curr_level = 1
        
    def supportedInterfases(self):
        return LIST
    
    def tryObject(self, obj):
        return isinstance(obj, list)
    
    def pushObject(self, obj):
        if len(obj) < 5:
            return
        xpatha = obj[2].split('/')
        fname = xpatha[-1]
        if self._lowercase > 0:
            fname = fname.lower()
        if self._no_underscore > 0:
            if fname[0] == '_':
                fname = fname[1:]
        if self._chkkwd:
            if fname in _CrateKeyword:
                fname = fname + '_'
        if fname in self._pkeys:
            self._fields.insert(0, fname + ' ' + _CrateType[obj[4]] + ' PRIMARY KEY')
        else:
            self._fields.append(fname + ' ' + _CrateType[obj[4]])
    
    def onFinish(self, bSuccess):
        if bSuccess:
            self._out.write('CREATE TABLE %s (\n' % self._tablename)
            for i in range(0, len(self._fields)):
                if i < len(self._fields) - 1:
                    self._out.write('  %s,\n' % self._fields[i])
                else:
                    self._out.write('  %s\n' % self._fields[i])
            self._out.write(');\n')
            if Log:
                Log.info('Output saved to %s' % self._path)
        self._out.close()
       
