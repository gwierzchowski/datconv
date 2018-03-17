# -*- coding: utf-8 -*-
"""
Module supporting storing data to `PostreSQL <https://www.postgresql.org>`_ database.

General interface description: :ref:`outconn_skeleton`.
"""
import json

# https://www.postgresql.org/docs/10/static/sql-keywords-appendix.html
# Allowed words marked as non-reserved in PostgreSQL column.
# https://www.postgresql.org/docs/10/static/ddl-system-columns.html
_Keywords = """
A
ABS
ABSENT
ACCORDING
ADA
ALL
ALLOCATE
ANALYSE
ANALYZE
AND
ANY
ARE
ARRAY
ARRAY_AGG
ARRAY_MAX_CARDINALITY
AS
ASC
ASENSITIVE
ASYMMETRIC
ATOMIC
ATTRIBUTES
AUTHORIZATION
AVG
BASE64
BEGIN_FRAME
BEGIN_PARTITION
BERNOULLI
BINARY
BIT_LENGTH
BLOB
BLOCKED
BOM
BOTH
BREADTH
C
CALL
CARDINALITY
CASE
CAST
CATALOG_NAME
CEIL
CEILING
CHARACTERS
CHARACTER_LENGTH
CHARACTER_SET_CATALOG
CHARACTER_SET_NAME
CHARACTER_SET_SCHEMA
CHAR_LENGTH
CHECK
CLASS_ORIGIN
CLOB
COBOL
COLLATE
COLLATION
COLLATION_CATALOG
COLLATION_NAME
COLLATION_SCHEMA
COLLECT
COLUMN
COLUMN_NAME
COMMAND_FUNCTION
COMMAND_FUNCTION_CODE
CONCURRENTLY
CONDITION
CONDITION_NUMBER
CONNECT
CONNECTION_NAME
CONSTRAINT
CONSTRAINT_CATALOG
CONSTRAINT_NAME
CONSTRAINT_SCHEMA
CONSTRUCTOR
CONTAINS
CONTROL
CONVERT
CORR
CORRESPONDING
COUNT
COVAR_POP
COVAR_SAMP
CREATE
CROSS
CUME_DIST
CURRENT_CATALOG
CURRENT_DATE
CURRENT_DEFAULT_TRANSFORM_GROUP
CURRENT_PATH
CURRENT_ROLE
CURRENT_ROW
CURRENT_SCHEMA
CURRENT_TIME
CURRENT_TIMESTAMP
CURRENT_TRANSFORM_GROUP_FOR_TYPE
CURRENT_USER
CURSOR_NAME
DATALINK
DATE
DATETIME_INTERVAL_CODE
DATETIME_INTERVAL_PRECISION
DB
DEFAULT
DEFERRABLE
DEFINED
DEGREE
DENSE_RANK
DEPTH
DEREF
DERIVED
DESC
DESCRIBE
DESCRIPTOR
DETERMINISTIC
DIAGNOSTICS
DISCONNECT
DISPATCH
DISTINCT
DLNEWCOPY
DLPREVIOUSCOPY
DLURLCOMPLETE
DLURLCOMPLETEONLY
DLURLCOMPLETEWRITE
DLURLPATH
DLURLPATHONLY
DLURLPATHWRITE
DLURLSCHEME
DLURLSERVER
DLVALUE
DO
DYNAMIC
DYNAMIC_FUNCTION
DYNAMIC_FUNCTION_CODE
ELEMENT
ELSE
EMPTY
END
END-EXEC
END_FRAME
END_PARTITION
ENFORCED
EQUALS
EVERY
EXCEPT
EXCEPTION
EXEC
EXP
EXPRESSION
FALSE
FETCH
FILE
FINAL
FIRST_VALUE
FLAG
FLOOR
FOR
FOREIGN
FORTRAN
FOUND
FRAME_ROW
FREE
FREEZE
FROM
FS
FULL
FUSION
G
GENERAL
GET
GO
GOTO
GRANT
GROUP
GROUPS
HAVING
HEX
HIERARCHY
ID
IGNORE
ILIKE
IMMEDIATELY
IMPLEMENTATION
IN
INDENT
INDICATOR
INITIALLY
INNER
INSTANCE
INSTANTIABLE
INTEGRITY
INTERSECT
INTERSECTION
INTO
IS
ISNULL
JOIN
K
KEY_MEMBER
KEY_TYPE
LAG
LAST_VALUE
LATERAL
LEAD
LEADING
LEFT
LENGTH
LIBRARY
LIKE
LIKE_REGEX
LIMIT
LINK
LN
LOCALTIME
LOCALTIMESTAMP
LOCATOR
LOWER
M
MAP
MATCHED
MAX
MAX_CARDINALITY
MEMBER
MERGE
MESSAGE_LENGTH
MESSAGE_OCTET_LENGTH
MESSAGE_TEXT
MIN
MOD
MODIFIES
MODULE
MORE
MULTISET
MUMPS
NAMESPACE
NATURAL
NCLOB
NESTING
NFC
NFD
NFKC
NFKD
NIL
NORMALIZE
NORMALIZED
NOT
NOTNULL
NTH_VALUE
NTILE
NULL
NULLABLE
NUMBER
OCCURRENCES_REGEX
OCTETS
OCTET_LENGTH
OFFSET
ON
ONLY
OPEN
OR
ORDER
ORDERING
OTHERS
OUTER
OUTPUT
OVERLAPS
P
PAD
PARAMETER
PARAMETER_MODE
PARAMETER_NAME
PARAMETER_ORDINAL_POSITION
PARAMETER_SPECIFIC_CATALOG
PARAMETER_SPECIFIC_NAME
PARAMETER_SPECIFIC_SCHEMA
PASCAL
PASSTHROUGH
PATH
PERCENT
PERCENTILE_CONT
PERCENTILE_DISC
PERCENT_RANK
PERIOD
PERMISSION
PLACING
PLI
PORTION
POSITION_REGEX
POWER
PRECEDES
PRIMARY
PUBLIC
RANK
READS
RECOVERY
REFERENCES
REGR_AVGX
REGR_AVGY
REGR_COUNT
REGR_INTERCEPT
REGR_R2
REGR_SLOPE
REGR_SXX
REGR_SXY
REGR_SYY
REQUIRING
RESPECT
RESTORE
RESULT
RETURN
RETURNED_CARDINALITY
RETURNED_LENGTH
RETURNED_OCTET_LENGTH
RETURNED_SQLSTATE
RETURNING
RIGHT
ROUTINE
ROUTINE_CATALOG
ROUTINE_NAME
ROUTINE_SCHEMA
ROW_COUNT
ROW_NUMBER
SCALE
SCHEMA_NAME
SCOPE
SCOPE_CATALOG
SCOPE_NAME
SCOPE_SCHEMA
SECTION
SELECT
SELECTIVE
SELF
SENSITIVE
SERVER_NAME
SESSION_USER
SIMILAR
SIZE
SOME
SOURCE
SPACE
SPECIFIC
SPECIFICTYPE
SPECIFIC_NAME
SQLCODE
SQLERROR
SQLEXCEPTION
SQLSTATE
SQLWARNING
SQRT
STATE
STATIC
STDDEV_POP
STDDEV_SAMP
STRUCTURE
STYLE
SUBCLASS_ORIGIN
SUBMULTISET
SUBSTRING_REGEX
SUCCEEDS
SUM
SYMMETRIC
SYSTEM_TIME
SYSTEM_USER
T
TABLE
TABLESAMPLE
TABLE_NAME
THEN
TIES
TIMEZONE_HOUR
TIMEZONE_MINUTE
TO
TOKEN
TOP_LEVEL_COUNT
TRAILING
TRANSACTIONS_COMMITTED
TRANSACTIONS_ROLLED_BACK
TRANSACTION_ACTIVE
TRANSFORMS
TRANSLATE
TRANSLATE_REGEX
TRANSLATION
TRIGGER_CATALOG
TRIGGER_NAME
TRIGGER_SCHEMA
TRIM_ARRAY
TRUE
UESCAPE
UNDER
UNION
UNIQUE
UNLINK
UNNAMED
UNNEST
UNTYPED
UPPER
URI
USAGE
USER
USER_DEFINED_TYPE_CATALOG
USER_DEFINED_TYPE_CODE
USER_DEFINED_TYPE_NAME
USER_DEFINED_TYPE_SCHEMA
USING
VALUE_OF
VARBINARY
VARIADIC
VAR_POP
VAR_SAMP
VERBOSE
VERSIONING
WHEN
WHENEVER
WHERE
WIDTH_BUCKET
WINDOW
WITH
XMLAGG
XMLBINARY
XMLCAST
XMLCOMMENT
XMLDECLARATION
XMLDOCUMENT
XMLITERATE
XMLQUERY
XMLSCHEMA
XMLTEXT
XMLVALIDATE

OID TABLEOID XMIN CMIN XMAX CMAX CTID 
"""

Keywords = set(_Keywords.split())

####################################################################

def obj2db(obj):
    """Converts Python object to object acceptable as parameter replacement in execute() function"""
    if obj is None:
        return None
    if isinstance(obj, str):
        return obj
    if isinstance(obj, int):
        return obj
    if isinstance(obj, float):
        return obj
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        try:
            return psycopg2.extras.Json(obj)
        except NameError:
            import psycopg2.extras
            return psycopg2.extras.Json(obj)
    return "'" + str(obj) + "'"

def obj2str(obj, quota = "'"):
    """Converts Python object to string to be used in INSERT clause"""
    if obj is None:
        return 'NULL'
    if isinstance(obj, str):
        return quota + obj + quota
    if isinstance(obj, int):
        return str(obj)
    if isinstance(obj, float):
        return str(obj)
    if isinstance(obj, list):
        return quota + _list2str(obj) + quota
    if isinstance(obj, dict):
        return quota + json.dumps(obj) + quota
    return quota + str(obj) + quota

def _list2str(ll):
    ret = '{'
    first = True
    for l in ll:
        if not first:
            ret += ','
        if isinstance(l, list):
            ret += obj2str(l, quota = "")
        if isinstance(l, dict):
            ret += obj2str(l, quota = "")
        else:
            ret += obj2str(l, quota = '"')
        first = False
    return ret + '}'

####################################################################

def castValues(obj, castlist):
    for cast in castlist:
        pv = v = obj
        try:
            for c in cast[0]:
                pv = v
                v = v[c]
                if v is None:
                    break
        except KeyError:
            continue
        if v is not None:
            if cast[1] == 'str':
                pv[c] = str(v)
            elif cast[1] == 'int':
                try:
                    pv[c] = int(v)
                except ValueError:
                    # TODO: log warning
                    pv[c] = None
            elif cast[1] == 'boolean':
                try:
                    v = int(v)
                    pv[c] = (v != 0)
                except ValueError:
                    # TODO: log warning
                    pv[c] = None
            elif cast[1] == 'long':
                try:
                    pv[c] = long(v)
                except ValueError:
                    # TODO: log warning
                    pv[c] = None
            elif cast[1] == 'float':
                try:
                    pv[c] = float(v)
                except ValueError:
                    # TODO: log warning
                    pv[c] = None
            elif cast[1] == 'array':
                if not isinstance(v, list):
                    pv[c] = [v]

def lowerKeys(obj, recurse):
    k_to_del = []
    for k, v in obj.items():
        if isinstance(k, str) and k.lower() != k:
            k_to_del.append(k)
        if recurse and isinstance(v, dict):
            lowerKeys(v, recurse)
    for k in k_to_del:
        # Warning: we overwite keys if there are both small and big ones, but no other choice.
        obj[k.lower()] = obj[k]
        del obj[k]

def checkKeywords(obj):
    k_to_del = []
    for k, v in obj.items():
        if isinstance(k, str) and k.upper() in Keywords:
            #Log.warning('Conflict with PostreSQL key-word. %s remaned to %s' % (fname, fname + '_'))
            # TODO: log warning
            k_to_del.append(k)
        if isinstance(v, dict):
            checkKeywords(v)
    for k in k_to_del:
        obj[k + '_'] = obj[k]
        del obj[k]
