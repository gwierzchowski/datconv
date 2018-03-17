# -*- coding: utf-8 -*-
"""This module implements Datconv Output Connector which generates CREATE TABLE cause in database crate.io dialect. 
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

_CrateType = { \
    'int': 'integer', \
    'float': 'float', \
    'str': 'string', \
    }

class DCConnector:
    """Please see constructor description for more details."""
    def __init__(self, table, path, mode = 'w', \
            check_keywords = True, lowercase = 1, no_underscore = 1, \
            column_constraints = {}, common_column_constraints = None, table_constraints = None):
        """Parameters are usually passed from YAML file as subkeys of OutConnector:CArg key.
        
        :param table: name of the table.
        :param path: relative or absolute path to output file.
        :param mode: output file opening mode.
        :param check_keywords: if true, prevents conflicts with SQL keywords. Data field names that are in conflict will be suffixed with undderscore.
        :param lowercase: if >1, all JSON keys will be converted to lower-case; if =1, only first level keys; if =0, no conversion happen.
        :param no_underscore: if >1, leading ``_`` will be removed from all JSON keys; if =1, only from first level of keys; if =0, option is disabled.
        :param column_constraints: dictionary: key=column name, value=column constraint.
        :param common_column_constraints: column constatins to be added after column definitions. Should be declared as string.
        :param table_constraints: table constatins and creation options. Should be declared as string.
        
        For more detailed descriptions see :ref:`conf_template.yaml <outconn_crate_conf_template>` file in this module folder.
        """
        assert Log is not None

        self._path = path
        self._out = open(path, mode)
        self._tablename = table
        self._chkkwd = check_keywords
        if check_keywords:
            if self._tablename.upper() in Keywords:
                Log.warning('Conflict with Crate key-word. Table %s remaned to %s' % (self._tablename, self._tablename + '_'))
                self._tablename += '_'
        self._lowercase = lowercase
        if self._lowercase > 0:
            self._tablename = self._tablename.lower()
        self._no_underscore = no_underscore
        self._cconst = column_constraints
        self._ccconst = common_column_constraints
        self._tconst = table_constraints
        
        self._fields = []
        self._fields_names = set()
        
    def supportedInterfases(self):
        return LIST
    
    def tryObject(self, obj):
        return isinstance(obj, list)
    
    def pushObject(self, obj):
        # TODO: Add suport for OBJECTS (depper levels) (idea: recursive call with taking xpatha[3], xpatha[4], ...)
        #obj: [ColumnName,RecordType,XPath,Default,DataType]
        if len(obj) < 5:
            return
        xpatha = obj[2].split('/')
        if len(xpatha) < 3:
            return
        fname = xpatha[2]

        if fname[0] == '@': #XML property
            fname = fname[1:]

        if '[' in fname:
            fname = fname.split('[')[0]
            is_array = True
        else:
            is_array = False

        if len(xpatha) > 3:
            ftype = 'object'
        else:
            ftype = _CrateType[obj[4]]
        
        if not is_array and ftype != 'object':
            fname = obj[0]
            
        if self._lowercase > 0:
            fname = fname.lower()

        if self._no_underscore > 0:
            if fname[0] == '_':
                fname = fname[1:]

        if self._chkkwd:
            if fname.upper() in Keywords:
                Log.warning('Conflict with Crate key-word. %s remaned to %s' % (fname, fname + '_'))
                fname += '_'
        
        if fname in self._fields_names:
            return
        self._fields_names.add(fname)
        
        if is_array:
            ftype = 'array(%s)' % ftype
  
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
       
