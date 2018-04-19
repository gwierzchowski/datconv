# -*- coding: utf-8 -*-
"""This module implements Datconv Output Connector which generates CREATE TABLE cause in PostreSQL dialect. 
Output of this connector should be treated as starting point for further manual edition, it is not recommended to use it for automatic table generation..
This connector should be used with Writer: :ref:`writers_dcjson` with options ``add_header: false, add_footer:false`` and ``convert_values: true``.
"""

# Standard Python Libs
import sys

# Datconv packages
from .. import OBJECT
from . import *


Log = None
"""Log varaible is automatically set by main datconv script using logging.getLogger method.
Use it for logging messages in need.
"""

class DCConnector:
    """Please see constructor description for more details."""
    def __init__(self, table, path, mode = 'w', \
        check_keywords = True, lowercase = 0, cast = None, \
        column_constraints = {}, common_column_constraints = [], table_constraints = []):
        """Parameters are usually passed from YAML file as subkeys of OutConnector:CArg key.
        
        :param table: name of the table.
        :param path: relative or absolute path to output file.
        :param mode: output file opening mode.
        :param check_keywords: if true, prevents conflicts with SQL keywords. Data field names that are in conflict will be suffixed with undderscore.
        :param lowercase: if >1, all JSON keys will be converted to lower-case; if =1, only first level keys; if =0, no conversion happen.
        :param cast: array of arrays of the form: [['rec', 'value'], str], what means that record: {"rec": {"value": 5025}} will be writen as {"rec": {"value": "5025"}} - i.e. it is ensured that "value" will allways be string. First position determines address of data to be converted, last position specifies the type: str, bool, int, long or float. Field names shold be given after all other configured transformations (lowercase, no_underscore, check_keywords).
        :param column_constraints: dictionary: key=column name, value=column constraint.
        :param common_column_constraints: column constatins to be added after column definitions. Should be a list.
        :param table_constraints: table constatins and creation options. Should be a list.
        
        For more detailed descriptions see :ref:`conf_template.yaml <outconn_postgresql_conf_template>` file in this module folder.
        """
        assert Log is not None

        import datconv.outconn.postgresql
        datconv.outconn.postgresql.PckLog = Log
        self._path = path
        self._out = open(path, mode)
        self._tablename = table
        self._chkkwd = check_keywords
        if check_keywords:
            if self._tablename.upper() in Keywords:
                Log.warning('Conflict with PostreSQL key-word. Table %s remaned to %s' % (self._tablename, self._tablename + '_'))
                self._tablename += '_'
        self._lowercase = lowercase
        if self._lowercase > 0:
            self._tablename = self._tablename.lower()
        self._cast = cast
        self._cconst = column_constraints
        self._ccconst = common_column_constraints
        self._tconst = table_constraints
        
        self._fields = []
        self._fields_names = set()
        
    def supportedInterfases(self):
        return OBJECT
    
    def tryObject(self, obj):
        return isinstance(obj, dict)
    
    def pushObject(self, obj):
        if self._lowercase > 0:
            lowerKeys(obj, self._lowercase > 1)
        if self._chkkwd:
            checkKeywords(obj)
        if self._cast:
            castValues(obj, self._cast)
        
        for k, v in obj.items():
            fname = str(k)
            if fname in self._fields_names:
                continue
            self._fields_names.add(fname)
            
            ftype = 'TEXT'
            is_array = False
            if isinstance(v, int):
                if (MIN_INT <= v and v <= MAX_INT):
                    ftype = 'INTEGER'
                elif (MIN_BIGINT <= v and v <= MAX_BIGINT):
                    ftype = 'INTEGER'
                else:
                    ftype = 'NUMERIC'
            elif sys.version_info.major == 2 and isinstance(v, long):
                ftype = 'BIGINT'
            elif isinstance(v, float):
                ftype = 'REAL'
            elif isinstance(v, list):
                is_array = True
                if len(v) > 0:
                    if isinstance(v[0], int):
                        if (MIN_INT <= v[0] and v[0] <= MAX_INT):
                            ftype = 'INTEGER'
                        elif (MIN_BIGINT <= v[0] and v[0] <= MAX_BIGINT):
                            ftype = 'INTEGER'
                        else:
                            ftype = 'NUMERIC'
                    elif sys.version_info.major == 2 and isinstance(v[0], long):
                        ftype = 'BIGINT'
                    elif isinstance(v[0], float):
                        ftype = 'REAL'
                    elif isinstance(v[0], dict):
                        ftype = 'JSONB'
            elif isinstance(v, dict):
                ftype = 'JSONB'
            if is_array:
                ftype += '[]'
            
            if fname in self._cconst:
                self._fields.append('"' + fname + '" ' + ftype  + ' ' + self._cconst[fname])
            else:
                self._fields.append('"' + fname + '" ' + ftype)

    def onFinish(self, bSuccess):
        if bSuccess:
            sql = '''
CREATE TABLE "%s" (
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
       
