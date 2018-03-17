# -*- coding: utf-8 -*-
"""This module implements Datconv Output Connector which directly inserts data to SQLite database.
This connector should be used with Writer: :ref:`writers_dcjson`.
"""

# Standard Python Libs

# Libs installed using pip
#import yaml
from sqlite3 import connect, OperationalError

# Datconv packages
from .. import OBJECT
from . import *


Log = None
"""Log varaible is automatically set by main datconv script using logging.getLogger method.
Use it for logging messages in need.
"""


class DCConnector:
    """Please see constructor description for more details."""
    def __init__(self, table, connstring, \
        dump_sql = False, \
        autocommit = False, \
        bulk_size = 10000, \
        check_keywords = True, lowercase = 0, cast = None):
        """Parameters are usually passed from YAML file as subkeys of OutConnector:CArg key.
        
        :param table: table name where to insert records.
        :param connstring: connection string to database (path to file in this case). 
        :param dump_sql: if true, insert statements are being saved to file specified as ``connstring`` with added '.sql' extension and not applied to database (option to be used for debugging).
        :param bulk_size: if consequtive records have similar structure (i.e. have the same fields) - they are groupped into one pack (up to the size specified as this parameter) and inserted in one command. If set value is 0 than every insert is done individaually - warning: it is quite slow operation.
        :param autocommit: if true, every insert is automatically commited (slows down insert operations radically); if false, chenges are commited at the end - i.e. if any insert fail everything is rolled back and no records are added.
        :param check_keywords: if true prevents conflicts with SQL keywords.
        :param lowercase: if >1, all JSON keys will be converted to lower-case; if =1, only first level keys; if =0, no conversion happen.
        :param cast: array of arrays of the form: [['rec', 'value'], str], what means that record: {"rec": {"value": 5025}} will be treated as {"rec": {"value": "5025"}} - i.e. it is ensured that "value" will allways be string. First position determines address of data to be converted, last position specifies the type: str, bool, int, long or float. Field names shold be given after all other configured transformations (lowercase, check_keywords).
        
        For more detailed descriptions see :ref:`conf_template.yaml <outconn_sqlite_conf_template>` file in this module folder.
        """
        assert Log is not None

        self._tablename = table
        self._connstring = connstring
        self._dump = dump_sql
        if dump_sql:
            self._conn = open(connstring + '.sql', "w")
        else:
            if autocommit:
                self._conn = connect(connstring, isolation_level = None)
            else:
                self._conn = connect(connstring)
            self._cur = self._conn.cursor()
        self._bulk_size = bulk_size
        self._chkkwd = check_keywords
        if check_keywords:
            if self._tablename.upper() in Keywords:
                self._tablename = self._tablename + '_'
        self._lowercase = lowercase
        if self._lowercase > 0:
            self._tablename = self._tablename.lower()
        self._PREFIX = 'INSERT INTO "%s" (' % self._tablename
        self._cast = cast
        self.tryObject(None) # initialize state variables
        
    def supportedInterfases(self):
        return OBJECT
    
    def tryObject(self, obj):
        self._total_no = 0
        self._inserted_no = 0
        self._prev_fields = ''
        self._prev_params = ''
        self._curr_size = 0
        self._curr_values = []
        return isinstance(obj, dict)
    
    def pushObject(self, obj):
        self._total_no += 1
        if self._lowercase > 0:
            lowerKeys(obj, self._lowercase > 1)
        if self._chkkwd:
            checkKeywords(obj)
        if self._cast:
            castValues(obj, self._cast)
        self._pushRecord(obj)
    
    def onFinish(self, bSuccess):
        if self._dump:
            if self._curr_size > 0:
                sql = self._PREFIX + self._prev_fields + ') VALUES ' + self._prev_params[:-1] + ';\n'
                self._conn.write(sql)
                self._inserted_no += 1
            if Log:
                if bSuccess:
                    Log.info('%d expressions with %d records saved to %s' % (self._inserted_no, self._total_no, self._connstring))
                else:
                    Log.error('Program did not finished properly: output saved to %s may be inconsistent' % self._connstring)
        else:
            if self._curr_size > 0:
                sql = self._PREFIX + self._prev_fields + ') VALUES (' + self._prev_params + ')'
                try:
                    self._cur.executemany(sql, self._curr_values)
                    if self._cur.rowcount > 0:
                        self._inserted_no += self._cur.rowcount
                    if self._cur.rowcount < len(self._curr_values):
                        Log.error('%d records not inserted' % (len(self._curr_values) - max(0, self._cur.rowcount))) # TODO: Improve - list not inserted records based on list returned by executemany
                except OperationalError as e:
                    Log.error('Record #%d not inserted: %s' % (self._total_no, str(e)))
            self._conn.commit()
            if Log:
                if bSuccess:
                    Log.info('%d out of %d records inserted to table %s in %s' % (self._inserted_no, self._total_no, self._tablename, self._connstring))
                else:
                    Log.error('Program did not finished properly: only %d out of %d records were saved' % (self._inserted_no, self._total_no))
        self._conn.close()

    def _pushRecord(self, obj):
        fields = ''
        params = ''
        values = []
        for k, v in obj.items():
            fields += '"' + str(k) + '",'
            if self._dump:
                params += obj2str(v) + ','
            else:
                params += '?,'
                values.append(v)
        if self._bulk_size > 0:
            if self._prev_fields == fields[:-1]:
                if self._dump:
                    self._prev_params += '(' + params[:-1] + '),'
                else:
                    self._curr_values.append(tuple(values))
                if self._curr_size < self._bulk_size:
                    self._curr_size += 1
                else:
                    if self._dump:
                        sql = self._PREFIX + self._prev_fields + ') VALUES ' + self._prev_params[:-1] + ';\n'
                        self._conn.write(sql)
                        self._inserted_no += 1
                    else:
                        sql = self._PREFIX + self._prev_fields + ') VALUES (' + params[:-1] + ')'
                        try:
                            self._cur.executemany(sql, self._curr_values)
                            if self._cur.rowcount > 0:
                                self._inserted_no += self._cur.rowcount
                            if self._cur.rowcount < len(self._curr_values):
                                Log.error('%d records not inserted' % (len(self._curr_values) - max(0, self._cur.rowcount))) # TODO: Improve - list not inserted records based on list returned by executemany
                        except OperationalError as e:
                            Log.error('Record #%d not inserted: %s' % (self._total_no, str(e)))
                    self._prev_fields = ''
                    self._prev_params = ''
                    self._curr_size = 0
                    self._curr_values = []
            else:
                if self._curr_size > 0:
                    if self._dump:
                        sql = self._PREFIX + self._prev_fields + ') VALUES ' + self._prev_params[:-1] + ';\n'
                        self._conn.write(sql)
                        self._inserted_no += 1
                    else:
                        sql = self._PREFIX + self._prev_fields + ') VALUES (' + self._prev_params + ')'
                        try:
                            self._cur.executemany(sql, self._curr_values)
                            if self._cur.rowcount > 0:
                                self._inserted_no += self._cur.rowcount
                            if self._cur.rowcount < len(self._curr_values):
                                Log.error('%d records not inserted' % (len(self._curr_values) - max(0, self._cur.rowcount))) # TODO: Improve - list not inserted records based on list returned by executemany
                        except OperationalError as e:
                            Log.error('Record #%d not inserted: %s' % (self._total_no, str(e)))
                self._prev_fields = fields[:-1]
                self._curr_size = 1
                if self._dump:
                    self._prev_params = '(' + params[:-1] + '),'
                else:
                    self._prev_params = params[:-1]
                    self._curr_values = [tuple(values)]
        else:
            if self._dump:
                sql = self._PREFIX + fields[:-1] + ') VALUES (' + params[:-1] + ');\n'
                self._conn.write(sql)
                self._inserted_no += 1
            else:
                sql = self._PREFIX + fields[:-1] + ') VALUES (' + params[:-1] + ')'
                try:
                    self._cur.execute(sql, tuple(values))
                    self._inserted_no += self._cur.rowcount
                except OperationalError as e:
                    Log.error('Record #%d not inserted: %s' % (self._total_no, str(e)))
       
