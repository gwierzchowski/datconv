# -*- coding: utf-8 -*-
"""
Module supporting storing data to `Crate <https://crate.io>`_ database.

General interface description: :ref:`outconn_skeleton`.

.. note::
   In this module all options ``lowercase`` and ``no_underscore`` are enabled by default, because
   Crate (versions 2.2 and 2.3) sometimes silently converts field names to lower case and 
   does not load data (using COPY command) if fields begin with underscore.
"""

# https://crate.io/docs/crate/reference/en/2.2/sql/reference/lexical_structure.html
_Keywords = """
ABS 	DEREF 	MEMBER 	SECOND
ABSOLUTE 	DESC 	MERGE 	SECTION
ACTION 	DESCRIBE 	METHOD 	SELECT
ADD 	DESCRIPTOR 	MIN 	SENSITIVE
AFTER 	DETERMINISTIC 	MINUTE 	SESSION
ALL 	DIAGNOSTICS 	MOD 	SESSION_USER
STATE 	STRING 	DIRECTORY 	SHORT
ALLOCATE 	DISCONNECT 	MODIFIES 	SET
ALTER 	DISTINCT 	MODULE 	SETS
AND 	DO 	MONTH 	SIGNAL
ANY 	DOMAIN 	MULTISET 	SIMILAR
ARE 	DOUBLE 	NAMES 	SIZE
ARRAY 	DROP 	NATIONAL 	SMALLINT
ARRAY_AGG 	DYNAMIC 	NATURAL 	SOME
ARRAY_MAX_CARDINALITY 	EACH 	NCHAR 	SPACE
AS 	ELEMENT 	NCLOB 	SPECIFIC
ASC 	ELSE 	NEW 	SPECIFICTYPE
ASENSITIVE 	ELSEIF 	NEXT 	SQL
ASSERTION 	END 	NO 	SQLCODE
ASYMMETRIC 	END_FRAME 	NONE 	SQLERROR
AT 	END_PARTITION 	NORMALIZE 	SQLEXCEPTION
ATOMIC 	END_EXEC 	NOT 	SQLSTATE
AUTHORIZATION 	EQUALS 	NTH_VALUE 	SQLWARNING
AVG 	ESCAPE 	NTILE 	SQRT
BEFORE 	EVERY 	NULL 	START
BEGIN 	EXCEPT 	NULLIF 	NULLS
BEGIN_FRAME 	EXCEPTION 	NUMERIC 	STATIC
BEGIN_PARTITION 	EXEC 	OBJECT 	STDDEV_POP
BETWEEN 	EXECUTE 	OCTET_LENGTH 	STDDEV_SAMP
BIGINT 	EXISTS 	OF 	SUBMULTISET
BINARY 	EXIT 	OFFSET 	SUBSTRING
BIT 	EXTERNAL 	OLD 	SUBSTRING_REGEX
BIT_LENGTH 	EXTRACT 	ON 	SUCCEEDSBLOB
FALSE 	ONLY 	SUM 	UNBOUNDED
BOOLEAN 	FETCH 	OPEN 	SYMMETRIC
BOTH 	FILTER 	OPTION 	SYSTEM
BREADTH 	FIRST 	OR 	SYSTEM_TIME
BY 	FIRST_VALUE 	ORDER 	SYSTEM_USER
CALL 	FLOAT 	ORDINALITY 	TABLE
CALLED 	FOR 	OUT 	TABLESAMPLE
CARDINALITY 	FOREIGN 	OUTER 	TEMPORARY
CASCADE 	FOUND 	OUTPUT 	THEN
CASCADED 	FRAME_ROW 	OVER 	TIME
CASE 	FREE 	OVERLAPS 	TIMESTAMP
CAST 	FROM 	OVERLAY 	TIMEZONE_HOUR
CATALOG 	FULL 	PAD 	TIMEZONE_MINUTE
CEIL 	FUNCTION 	PARAMETER 	TO
CEILING 	FUSION 	PARTIAL 	TRAILING
YEAR 	PARTITION 	TRY_CAST 	TRANSLATE
CHAR 	GENERAL 	PERSISTENT 	TRANSACTION
CHAR_LENGTH 	GET 	PATH 	TRANSIENT
CHARACTER 	GLOBAL 	PERCENT 	TRANSLATE_REGEX
CHARACTER_LENGTH 	GO 	PERCENT_RANK 	TRANSLATION
CHECK 	GOTO 	PERCENTILE_CONT 	TREAT
CLOB 	GRANT 	PERCENTILE_DISC 	TRIGGER
CLOSE 	GROUP 	PERIOD 	TRIM
COALESCE 	GROUPING 	PORTION 	TRIM_ARRAY
COLLATE 	GROUPS 	POSITION 	TRUE
COLLATION 	HANDLER 	POSITION_REGEX 	TRUNCATE
COLLECT 	HAVING 	POWER 	UESCAPE
COLUMN 	HOLD 	PRECEDES 	UNDER
COMMIT 	HOUR 	PRECISION 	UNDO
CONDITION 	IDENTITY 	PREPARE 	UNION
CONNECT 	IF 	PRESERVE 	UNIQUE
CONNECTION 	IMMEDIATE 	PRIMARY 	UNKNOWN
CONSTRAINT 	IN 	PRIOR 	UNNEST
CONSTRAINTS 	INDICATOR 	PRIVILEGES 	UNTIL
CONSTRUCTOR 	INITIALLY 	PROCEDURE 	UPDATE
CONTAINS 	INNER 	PUBLIC 	UPPER
CONTINUE 	INOUT 	RANGE 	USAGE
CONVERT 	INPUT 	RANK 	USER
CORR 	INSENSITIVE 	READ 	USING
CORRESPONDING 	INSERT 	READS 	VALUE
COUNT 	INT 	REAL 	VALUES
COVAR_POP 	INTEGER 	RECURSIVE 	VALUE_OF
COVAR_SAMP 	INTERSECT 	REF 	VAR_POP
CREATE 	INTERSECTION 	REFERENCES 	VAR_SAMP
CROSS 	INTERVAL 	REFERENCING 	VARBINARY
CUBE 	INTO 	REGR_AVGX 	VARCHAR
CUME_DIST 	IS 	REGR_AVGY 	VARYING
CURRENT 	ISOLATION 	REGR_COUNT 	VERSIONING
CURRENT_CATALOG 	ITERATE 	REGR_INTERCEPT 	VIEW
CURRENT_DATE 	JOIN 	REGR_R2 	WHEN
STRATIFY 	KEY 	REGR_SLOPE 	WHENEVER
CURRENT_PATH 	LANGUAGE 	REGR_SXX 	WHERE
CURRENT_ROLE 	LARGE 	REGR_SXYREGR_SYY 	WHILE
CURRENT_ROW 	LAST 	RELATIVE 	WIDTH_BUCKET
CURRENT_SCHEMA 	LAST_VALUE 	RELEASE 	WINDOW
CURRENT_TIME 	LATERAL 	REPEAT 	WITH
CURRENT_TIMESTAMP 	LEAD 	RESIGNAL 	WITHIN
ZONE 	LEADING 	RESTRICT 	WITHOUT
CURRENT_USER 	LEAVE 	RESULT 	WORK
CURSOR 	LEFT 	RETURN 	WRITE
CYCLE 	LEVEL 	RETURNS 	BYTE
DATA 	LIKE 	REVOKE 	RESET
DATE 	LIKE_REGEX 	RIGHT 	INDEX
DAY 	LIMIT 	ROLE 	IP
DEALLOCATE 	LN 	ROLLBACK 	SCROLL
DEC 	LOCAL 	ROLLUP 	LONG
DECIMAL 	LOCALTIME 	ROUTINE 	STRATIFY
DECLARE 	LOCALTIMESTAMP 	ROW 	SEARCH
DEFAULT 	LOCATOR 	ROW_NUMBER 	MAX
DEFERRABLE 	LOOP 	ROWS 	DEPTH
DEFERRED 	LOWER 	SAVEPOINT 	 
DELETE 	MAP 	SCHEMA 	 
DENSE_RANK 	MATCH 	SCOPE
_ID
"""

Keywords = set(_Keywords.split())

####################################################################

def obj2str(obj):
    if obj is None:
        return 'NULL'
    if isinstance(obj, dict):
        return _dict2str(obj)
    if  isinstance(obj, list):
        return _list2str(obj)
    if  isinstance(obj, str):
        return "'" + obj + "'"
    if  isinstance(obj, int):
        return str(obj)
    if  isinstance(obj, float):
        return str(obj)
    return "'" + str(obj) + "'"

def _dict2str(dd):
    ret = '{'
    first = True
    for k, v in dd.items():
        if not first:
            ret += ','
        ret += '"' + str(k) + '"=' + obj2str(v)
        first = False
    return ret + '}'

def _list2str(ll):
    ret = '['
    first = True
    for l in ll:
        if not first:
            ret += ','
        ret += obj2str(l)
    return ret + ']'

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

def removeUnder(obj, recurse):
    k_to_del = []
    for k, v in obj.items():
        if isinstance(k, str) and k[0] == '_':
            k_to_del.append(k)
        if recurse and isinstance(v, dict):
            removeUnder(v, recurse)
    for k in k_to_del:
        # Warning: we overwite keys if there are both small and big ones, but no other choice.
        obj[k[1:]] = obj[k]
        del obj[k]

def checkKeywords(obj):
    k_to_del = []
    for k, v in obj.items():
        if isinstance(k, str) and k.upper() in Keywords:
            # TODO: log warning
            k_to_del.append(k)
        if isinstance(v, dict):
            checkKeywords(v)
    for k in k_to_del:
        obj[k + '_'] = obj[k]
        del obj[k]
