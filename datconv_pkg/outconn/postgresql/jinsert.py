# -*- coding: utf-8 -*-
"""This module implements Datconv Output Connector which directly inserts data to PostreSQL database.
This connector should be used with Writer: :ref:`writers_dcjson`.
It requires Python package ``psycopg2`` to be installed.
"""

# Standard Python Libs

# Libs installed using pip
import psycopg2

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
        check_keywords = True, lowercase = 0, cast = None, \
        on_conflict = None, options = []):
        """Parameters are usually passed from YAML file as subkeys of OutConnector:CArg key.
        
        :param table: table name where to insert records.
        :param connstring: connection string to database.
        :param dump_sql: if true, insert statements are being saved to file specified as ``connstring`` and not inserted to database (option to be used for debugging).
        :param autocommit: parameter passed to connection, if true every insert is automatically commited (slows down insert operations radically), if false chenges are commited at the end - i.e. if any insert fail everything is rolled back and no records are added.
        :param check_keywords: if true, prevents conflicts with SQL keywords.
        :param lowercase: if >1, all JSON keys will be converted to lower-case; if =1, only first level keys; if =0, no conversion happen.
        :param cast: array of arrays of the form: [['rec', 'value'], str], what means that record: {"rec": {"value": 5025}} will be writen as {"rec": {"value": "5025"}} - i.e. it is ensured that "value" will allways be string. First position determines address of data to be converted, last position specifies the type: str, bool, int, long, float or array. Field names shold be given after all other configured transformations (lowercase, no_underscore, check_keywords).
        :param on_conflict: specify what to do when record with given primary key exist in the table; one of strings 'ignore', 'update' or None (raise error in such situation).
        :param options: array or additional options added to INSERT caluse (see Posgresql documentation).
        
        For more detailed descriptions see :ref:`conf_template.yaml <outconn_postgresql_conf_template>` file in this module folder.
        """
        assert Log is not None

        import datconv.outconn.postgresql
        datconv.outconn.postgresql.PckLog = Log
        self._tablename = table
        self._connstring = connstring
        self._autocommit = autocommit
        self._dump = dump_sql
        if dump_sql:
            self._conn = open(connstring, "w")
        else:
            self._conn = psycopg2.connect(connstring)
            if autocommit:
                self._conn.autocommit = True
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
        self._conflict_opt = 0
        self._conflict_str = ''
        self._conflict_keys = None
        if on_conflict is not None:
            if on_conflict.lower() == 'ignore':
                self._conflict_opt = 1
                self._conflict_str = '\nON CONFLICT DO NOTHING'
            elif on_conflict.lower() == 'update':
                if dump_sql:
                    constr = '???'
                    self._conflict_keys = []
                else:
                    tablename = self._tablename.split('.')
                    if len(tablename) > 1:
                        schemaname = '.'.join(tablename[:-1])
                        tablename = tablename[-1]
                    else:
                        schemaname = 'public'
                        tablename = tablename[0]
                    self._cur.execute('SELECT column_name FROM information_schema.key_column_usage WHERE table_name = %s AND table_schema = %s', (tablename, schemaname))
                    keys = self._cur.fetchall()
                    if keys:
                        self._conflict_keys = [c[0] for c in keys]
                        constr = ','.join(self._conflict_keys)
                    else:
                        raise Exception('Table %s does not exists or has no primary key' % tablename)
                self._conflict_opt = 2
                self._conflict_str = '\nON CONFLICT (%s) DO UPDATE SET' % constr
        self._options = '\n'.join(options)
        
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
        if self._chkkwd:
            checkKeywords(obj)
        if self._cast:
            castValues(obj, self._cast)
        self._pushRecord(obj)
    
    def onFinish(self, bSuccess):
        if self._dump:
            if Log:
                if bSuccess:
                    Log.info('%d records saved to %s' % (self._inserted_no, self._connstring))
                else:
                    Log.error('Program did not finished properly: output saved to %s may be inconsistent' % self._connstring)
        else:
            if bSuccess:
                self._conn.commit()
                if Log:
                    Log.info('%d out of %d records inserted to table %s' % (self._inserted_no, self._total_no, self._tablename))
            else:
                self._conn.rollback()
                if Log:
                    if self._autocommit:
                        Log.error('Program did not finished properly: only %d out of %d records were saved' % (self._inserted_no, self._total_no))
                    else:
                        Log.error('Program did not finished properly: no records were saved')
        self._conn.close()

    def _pushRecord(self, obj):
        fields = ''
        params = ''
        values = []
        conflict_str = self._conflict_str
        for k, v in obj.items():
            fields += '"' + str(k) + '",'
            if self._dump:
                params += obj2str(v) + ','
            else:
                params += '%s,'
                values.append(obj2db(v))
            if self._conflict_opt == 2:
                if str(k) not in self._conflict_keys:
                    conflict_str += ' "%s"=EXCLUDED."%s",' % (str(k), str(k))
        if self._conflict_opt == 2:
            conflict_str = conflict_str[:-1]
        if self._dump:
            sql = self._PREFIX + fields[:-1] + \
                ') VALUES (' + params[:-1] + ')' + \
                conflict_str + \
                self._options + ';\n'
            self._conn.write(sql)
            self._inserted_no += 1
        else:
            sql = self._PREFIX + fields[:-1] + \
                ') VALUES (' + params[:-1] + ')' + \
                conflict_str + \
                self._options
            try:
                self._cur.execute(sql, tuple(values))
            except:
                Log.error('Failed query ' + sql)
                raise
            self._inserted_no += self._cur.rowcount
       
