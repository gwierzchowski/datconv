# -*- coding: utf-8 -*-
"""This module implements Datconv Output Connector which generates CREATE TABLE cause in PostreSQL dialect. 
Output of this connector should be treated as starting point for further manual edition, it is not recommended to use it for automatic table generation..
This connector should be used with Writer: :ref:`writers_dcxpaths` with options ``add_header: false`` and ``add_type: true``.
"""

# Standard Python Libs

# Datconv packages
from .. import LIST
from . import Keywords


Log = None
"""Log varaible is automatically set by main datconv script using logging.getLogger method.
Use it for logging messages in need.
"""

# TODO: make it configurable.
_PostgresType = { \
    'int': 'INTEGER', \
    'float': 'REAL', \
    'str': 'TEXT', \
    }

class DCConnector:
    """Please see constructor description for more details."""
    def __init__(self, path, table, check_keywords = True, lowercase = 0, primary_key = [], not_null = []):
        """Parameters are usually passed from YAML file as subkeys of OutConnector:CArg key.
        
        :param path: relative or absolute path to output file.
        :param table: name of the table.
        :param check_keywords: if true, prevents conflicts with SQL keywords. Data field names that are in conflict will be suffixed with undderscore.
        :param lowercase: if >1, all JSON keys will be converted to lower-case; if =1, only first level keys; if =0, no conversion happen.
        :param primary_key: those first level keys will be declared as primary keys.
        :param not_null: those fields will be declared as not nullable; place ['*'] to mark all fields.
        
        For more detailed descriptions see :ref:`conf_template.yaml <outconn_postgresql_conf_template>` file in this module folder.
        """
        assert Log is not None

        self._path = path
        self._out = open(path, "w")
        self._tablename = table
        self._chkkwd = check_keywords
        if check_keywords:
            if self._tablename.upper() in Keywords:
                Log.warning('Conflict with PostreSQL key-word. Table %s remaned to %s' % (self._tablename, self._tablename + '_'))
                self._tablename += '_'
        self._lowercase = lowercase
        if self._lowercase > 0:
            self._tablename = self._tablename.lower()
        self._pkeys = primary_key
        self._notnull = not_null
        self._all_notnull = '*' in not_null
        
        self._fields = []
        self._fields_names = set()
        
    def supportedInterfases(self):
        return LIST
    
    def tryObject(self, obj):
        return isinstance(obj, list)
    
    def pushObject(self, obj):
        #obj: [ColumnName,RecordType,XPath,Default,DataType]
        if len(obj) < 5:
            return
        xpatha = obj[2].split('/')
        if len(xpatha) < 3:
            return
        xpathroot = xpatha[2]
        fname = obj[0]
        is_array = ( '[' in xpathroot)
        ftype = _PostgresType[obj[4]]
            
        if self._lowercase > 0:
            fname = fname.lower()

        if self._chkkwd:
            if fname.upper() in Keywords:
                Log.warning('Conflict with PostreSQL key-word. %s remaned to %s' % (fname, fname + '_'))
                fname += '_'
        
        if fname in self._fields_names:
            return
        self._fields_names.add(fname)

        fconstr = ''
        if self._all_notnull or fname in self._notnull:
            fconstr += ' NOT NULL'
        if is_array:
            ftype = '%s[]' % ftype
        if fname in self._pkeys:
            self._fields.insert(0, fname + ' ' + ftype  + fconstr)
        else:
            self._fields.append(fname + ' ' + ftype + fconstr)
    
    def onFinish(self, bSuccess):
        if bSuccess:
            self._out.write('CREATE TABLE %s (' % self._tablename)
            for i in range(0, len(self._fields)):
                if i < len(self._fields) - 1:
                    self._out.write('\n  %s,' % self._fields[i])
                else:
                    self._out.write('\n  %s' % self._fields[i])
            if len(self._pkeys) > 0:
                self._out.write(',\n  PRIMARY KEY (%s)' % ','.join(self._pkeys))
            self._out.write('\n);\n')
            if Log:
                Log.info('Output saved to %s' % self._path)
        self._out.close()
       
