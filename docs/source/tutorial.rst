Tutorial, Samples
======================
.. note::
    Below examples are suited for Linux system. In Windows System:
    
    - use Windows file paths
    - replace main program name ``datconv`` with ``datconv-run.py``
    - if you use Notepad++ editor, use ``.yml`` configuration file extension rather than ``.yaml``,
      this ensures that syntax hightlighting will be working out of box.
      
Minimal XML to JSON conversion example
--------------------------------------

Let say we have following XML file that we want to convert to JSON format ``file.xml``:

.. code-block:: xml

    <Data>
        <Hello>World</Hello>
    </Data>

At first we have to write simple configuration file ``conv.yaml``:

.. code-block:: yaml

    Reader: 
        Module:  datconv.readers.dcxml
        CArg:
            bratags: [Data]
        PArg:
            inpath:  ./file.xml
            outpath: ./file.json

    Writer:
        Module: datconv.writers.dcjson

then, run Datconv tool against this file::

    datconv ./conv.yaml

or skip ``PArg:`` key in the configuration file and pass file names in command line::

    datconv ./conv.yaml --Reader:PArg:inpath:./file.xml --Reader:PArg:outpath:./file.json

Following ``file.json`` file will be created:

.. code-block:: json

    [
    {"Data": {}},
    {"Hello": "World"}
    ]

If you don't want ``Data`` object to be in output file, additional parameter must be added to 
writer's arguments in configuration file:

.. code-block:: yaml
    :emphasize-lines: 3-4

    Writer:
        Module: datconv.writers.dcjson
        CArg:
            add_header: false

In case your input file would look like this:

.. code-block:: xml

    <Data>
        <Hello World="!" />
    </Data>

you typically want to add another argument in configuration file:

.. code-block:: yaml
    :emphasize-lines: 5
    
    Writer:
        Module: datconv.writers.dcjson
        CArg:
            add_header: false
            with_prop: true

to obtain output:

.. code-block:: json

    [
    {"Hello": {"World": "!"}}
    ]

or with yet another option:

.. code-block:: yaml
    :emphasize-lines: 6-7
    
    Writer:
        Module: datconv.writers.dcjson
        CArg:
            add_header: false
            with_prop: true
            json_opt: 
                indent: 2

.. code-block:: json

    [
    {
      "Hello": {
          "World": "!"
      }
    }
    ]

.. _json2xml_sample:

JSON to XML conversion example
------------------------------

Let say we have JSON query result returned by ``cbq`` tool from `Couchbase <https://www.couchbase.com>`_ saved in file ``cb.json`` that we want to convert to XML:

.. code-block:: json

    {
        "requestID": "f5a71946-275a-45ef-a13e-f2a335b9b84b",
        "signature": {
            "name": "json",
            "phone": "json"
        },
        "results": [
            {
                "name": "Hilton Chambers",
                "phone": "+44 161 236-4414"
            },
            {
                "name": "Sachas Hotel",
                "phone": null
            },
            {
                "name": "The Mitre Hotel",
                "phone": "+44 161 834-4128"
            }
        ],
        "status": "success",
        "metrics": {
            "elapsedTime": "9.516157ms",
            "executionTime": "9.488693ms",
            "resultCount": 3,
            "resultSize": 253,
            "sortCount": 3
        }
    }

configuration file would look like this:

.. code-block:: yaml

    Reader: 
        Module:  datconv.readers.dcijson_keys
        CArg:
            headkeys: [requestID, signature]
            reckeys: [results]
            footkeys: [status, metrics]
        PArg:
            inpath:  ./cb.json
            outpath: ./cb.json.xml

    Writer:
        Module: datconv.writers.dcxml
        CArg: 
            pretty: true

and output file ``cb.json.xml``:

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <Datconv>
    <requestID val="f5a71946-275a-45ef-a13e-f2a335b9b84b"/>
    <signature phone="json" name="json"/>
    <results>
        <name>Hilton Chambers</name>
        <phone>+44 161 236-4414</phone>
    </results>

    <results>
        <name>Sachas Hotel</name>
        <phone>None</phone>
    </results>

    <results>
        <name>The Mitre Hotel</name>
        <phone>+44 161 834-4128</phone>
    </results>

    <status val="success"/>
    <metrics sortCount="3" executionTime="9.488693ms" elapsedTime="9.516157ms" resultCount="3" resultSize="253"/>
    </Datconv>


XML to CSV conversion example
------------------------------

Let say we want to convert output XML file from above example to CSV.

Configuration file:

.. code-block:: yaml

    Reader: 
        Module:  datconv.readers.dcxml
        CArg:
            rectags: [results]
        PArg:
            inpath:  ./cb.json.xml
            outpath: ./cb.xml.csv

    Writer:
        Module: datconv.writers.dccsv
        CArg: 
            columns: 
                - ['name','*','name',null]
                - ['phone','*','phone',null]

and output file:

.. code-block:: none

    name,phone
    Hilton Chambers,+44 161 236-4414
    Sachas Hotel,None
    The Mitre Hotel,+44 161 834-4128

Using filter
-------------

If we want to somehow change the data on the fly during conversion we can use the filter.
There are few filters shipped with ``datconv`` package, see: :doc:`api_filters`.
But usually you need to write your own custom filter. For instance imagine that in above described conversion 
we want to skip records that do not have phone number. We should write folliwing filter::

    # Standard Python Libs
    import logging

    # Libs installed using pip
    from lxml import etree

    # Datconv generic modules
    from datconv.filters import SKIP, WRITE, REPEAT, BREAK

    Log = None

    class DCFilter:
        def filterRecord(self, record):
            tag = record.find('.//phone')
            if tag is not None and tag.text != 'None':
                return WRITE
            else:
                return SKIP

and save it as file ``with_phone.py`` in folder ``custom`` created where we run ``datconv`` program.
In addtion we have to create empty file ``__init__.py`` in this folder (to make it valid Python package) and add 
following key to conversion configuration file:

.. code-block:: yaml

    Filter:
        Module: custom.with_phone

Then when you run conversion, you will get expected result:

.. code-block:: none

    name,phone
    Hilton Chambers,+44 161 236-4414
    The Mitre Hotel,+44 161 834-4128

Note that current folder is automatically added to Python search path by ``datconv`` script.

Concatenating several filters 
-----------------------------

If we have a library of generic filters and woud like to use few of them in one data conversion run 
it is possible with provided ``pipe`` filter. 
E.g. following configuration will use above filter and standard filter that will remove ``name`` field from the output records:

.. code-block:: yaml

    Filter:
        Module: datconv.filters.pipe
        CArg: 
            flist:
                - Module: custom.with_phone
                - Module: datconv.filters.delfield
                  CArg:
                      field: [name]

Populating database 
--------------------

Let say we have output file from: :ref:`json2xml_sample` (file ``cb.json.xml``) that we would like to import to SQLite database. At first we have to create table with respective
fields to store data. Connector :ref:`outconn_sqlite_ddl` can be helpfull here. Let's run datconv with following configuration:

.. code-block:: yaml

    Reader: 
        Module: datconv.readers.dcxml
        CArg:
            rectags: [results]
        PArg:
            inpath: ./sampl.xml

    Writer:
        Module: datconv.writers.dcxpaths
        CArg:
            add_header: false
            add_type: true
            ignore_rectyp: true

    OutConnector:
        Module: datconv.outconn.sqlite.ddl
        CArg:
            path: ./sampl.sql
            table: sample

This will produce file ``sampl.sql`` with proposed table definition:

.. code-block:: sql

    CREATE TABLE sample (
      name TEXT,
      phone TEXT
    );

Edit this definition (possibly define primary key etc.) and run with your database to create table. 
This step may look somewhat like art-for-art in this simple sample, but with large number of
fields or tables may save you some typing or copy/pasting.

Then, change Writer and Connector in your configuration file in following way
(place path to your SQLite database file as ``connstring:`` parameter):

.. code-block:: yaml

    Reader: 
        Module: datconv.readers.dcxml
        CArg:
            rectags: [results]
        PArg:
            inpath: ./sampl.xml

    Writer:
        Module: datconv.writers.dcjson
        CArg:
            ignore_rectyp: true

    OutConnector:
        Module: datconv.outconn.sqlite.jinsert
        CArg:
            connstring: ./sampl.sqlite
            table: sample

and run datconv again to insert records into the table.
Note use of ``ignore_rectyp`` option to get rid of outer ``<results>`` tag which otherwise 
would be interpretted as the only one column in the table. In case of problems with inserts 
one can add ``dump_sql`` option to Connector in order to dump generated INSERT statements to 
file or change OutConnector to plain file to check generated JSON.

Default Configuration
---------------------

It may happen that we have some typical files or typical conversion scenario that we frequently use. In such case it is reasonable to use :doc:`default` file.
Let say we frequently do conversion described in section :ref:`json2xml_sample`.
To simplify program usage we may save configuration file for this case as the file ``.datconv_def.yml`` located in root of our home folder making one change in the file:
replacing file names with positional arguments, like below:

.. code-block:: yaml
    :emphasize-lines: 8-9

    Reader: 
        Module:  datconv.readers.dcijson_keys
        CArg:
            headkeys: [requestID, signature]
            reckeys: [results]
            footkeys: [status, metrics]
        PArg:
            inpath:  $1
            outpath: $2

    Writer:
        Module: datconv.writers.dcxml
        CArg: 
            pretty: true

After that one may call datconv in following way::

    datconv def <imput file> <output file>
    
to perform conversion according to saved schema.

More examples 
-------------

More examples are contained in package ``datconv_test`` avaialble from `PyPi <https://pypi.python.org/pypi/datconv_test>`_.
