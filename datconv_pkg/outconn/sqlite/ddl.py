# -*- coding: utf-8 -*-
"""This module implements Datconv Output Connector which generates CREATE TABLE cause in SQLite dialect.
Output of this connector should be treated as starting point for further manual edition, it is not recommended to use it for automatic table generation.
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
_SQLiteType = { \
    'int': 'INTEGER', \
    'float': 'REAL', \
    'str': 'TEXT', \
    }

class DCConnector:
    """Please see constructor description for more details."""
    def __init__(self, table, path, mode = 'w', \
            check_keywords = True, lowercase = 0, \
            column_constraints = {}, common_column_constraints = None, table_constraints = None):
        """Parameters are usually passed from YAML file as subkeys of OutConnector:CArg key.
        
        :param table: name of the table.
        :param path: relative or absolute path to output file.
        :param mode: output file opening mode.
        :param check_keywords: if true, prevents conflicts with SQL keywords. Data field names that are in conflict will be suffixed with undderscore.
        :param lowercase: if >1, all JSON keys will be converted to lower-case; if =1, only first level keys; if =0, no conversion happen.
        :param column_constraints: dictionary: key=column name, value=column constraint.
        :param common_column_constraints: column constatins to be added after column definitions. Should be declared as string.
        :param table_constraints: table constatins and creation options. Should be declared as string.
        
        For more detailed descriptions see :ref:`conf_template.yaml <outconn_sqlite_conf_template>` file in this module folder.
        """
        assert Log is not None

        self._path = path
        self._out = open(path, mode)
        self._tablename = table
        self._chkkwd = check_keywords
        if check_keywords:
            if self._tablename.upper() in Keywords:
                Log.warning('Conflict with SQLite key-word. Table %s remaned to %s' % (self._tablename, self._tablename + '_'))
                self._tablename += '_'
        self._lowercase = lowercase
        if self._lowercase > 0:
            self._tablename = self._tablename.lower()
        self._cconst = column_constraints
        self._ccconst = common_column_constraints
        self._tconst = table_constraints
        
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
        ftype = _SQLiteType[obj[4]]
            
        if self._lowercase > 0:
            fname = fname.lower()

        if self._chkkwd:
            if fname.upper() in Keywords:
                Log.warning('Conflict with SQLite key-word. %s remaned to %s' % (fname, fname + '_'))
                fname += '_'
        
        if fname in self._fields_names:
            return
        self._fields_names.add(fname)

        if is_array:
            ftype += '[]'
        
        if fname in self._cconst:
            self._fields.append(fname + ' ' + ftype  + ' ' + self._cconst[fname])
        else:
            self._fields.append(fname + ' ' + ftype)
    
    def onFinish(self, bSuccess):
        if bSuccess:
            sql = '''
CREATE TABLE %s (
  %s
)
%s;
''' % (         self._tablename, \
                ',\n  '.join(self._fields + self._ccconst) , \
                '\n'.join(self._tconst))
            self._out.write(sql)
            if Log:
                Log.info('Output saved to %s' % self._path)
        self._out.close()
       
