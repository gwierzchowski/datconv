# -*- coding: utf-8 -*-
"""
Module supporting storing data to `SQLIte <https://sqlite.org>`_ database files.

General interface description: :ref:`outconn_skeleton`.
"""

# https://sqlite.org/lang_keywords.html
# https://sqlite.org/withoutrowid.html
# Updated for SQLIte 3.22.0
_Keywords = """
    ABORT
    ACTION
    ADD
    AFTER
    ALL
    ALTER
    ANALYZE
    AND
    AS
    ASC
    ATTACH
    AUTOINCREMENT
    BEFORE
    BEGIN
    BETWEEN
    BY
    CASCADE
    CASE
    CAST
    CHECK
    COLLATE
    COLUMN
    COMMIT
    CONFLICT
    CONSTRAINT
    CREATE
    CROSS
    CURRENT_DATE
    CURRENT_TIME
    CURRENT_TIMESTAMP
    DATABASE
    DEFAULT
    DEFERRABLE
    DEFERRED
    DELETE
    DESC
    DETACH
    DISTINCT
    DROP
    EACH
    ELSE
    END
    ESCAPE
    EXCEPT
    EXCLUSIVE
    EXISTS
    EXPLAIN
    FAIL
    FOR
    FOREIGN
    FROM
    FULL
    GLOB
    GROUP
    HAVING
    IF
    IGNORE
    IMMEDIATE
    IN
    INDEX
    INDEXED
    INITIALLY
    INNER
    INSERT
    INSTEAD
    INTERSECT
    INTO
    IS
    ISNULL
    JOIN
    KEY
    LEFT
    LIKE
    LIMIT
    MATCH
    NATURAL
    NO
    NOT
    NOTNULL
    NULL
    OF
    OFFSET
    ON
    OR
    ORDER
    OUTER
    PLAN
    PRAGMA
    PRIMARY
    QUERY
    RAISE
    RECURSIVE
    REFERENCES
    REGEXP
    REINDEX
    RELEASE
    RENAME
    REPLACE
    RESTRICT
    RIGHT
    ROLLBACK
    ROW
    SAVEPOINT
    SELECT
    SET
    TABLE
    TEMP
    TEMPORARY
    THEN
    TO
    TRANSACTION
    TRIGGER
    UNION
    UNIQUE
    UPDATE
    USING
    VACUUM
    VALUES
    VIEW
    VIRTUAL
    WHEN
    WHERE
    WITH
    WITHOUT

    ROWID 
"""

Keywords = set(_Keywords.split())

####################################################################

def obj2str(obj):
    if obj is None:
        return 'NULL'
    if  isinstance(obj, int):
        return str(obj)
    if  isinstance(obj, float):
        return str(obj)
    return "'" + str(obj) + "'"

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

def checkKeywords(obj):
    k_to_del = []
    for k, v in obj.items():
        if isinstance(k, str) and k.upper() in Keywords:
            #Log.warning('Conflict with SQLite key-word. %s remaned to %s' % (fname, fname + '_'))
            # TODO: log warning
            k_to_del.append(k)
        if isinstance(v, dict):
            checkKeywords(v)
    for k in k_to_del:
        obj[k + '_'] = obj[k]
        del obj[k]
