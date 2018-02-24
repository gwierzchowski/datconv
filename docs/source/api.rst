The Datconv API reference
=========================

.. _datconv_program:

datconv program
-----------------------------
The :command:`datconv` script has following call syntax::

    datconv [=]conf_file [--key1:val [--key2:val ...]] [arg1 [arg2 ...]]
    where:
    conf_file - path to file in YAML format in which Reader, Filter and Writer compoments are configured.
                See below listing for more detailed desctiption of this file.
                If there is '=' before conf_file then default configuration file is not used.
                If conf_file is equal to 'def' than only default configuration file is used.
    --key1:val - any number of arguments that add new settings or overwrite settings from conf_file.
                It works this way: let say that in conf_file we have:
                Writer:
                    Module: datconv.writers.dcxml
                    CArg: 
                        pretty:   true
                by invoking option --Writer:CArg:pretty:false we overwrite 'pretty' option of Writer.
                Note that in YAML file we must have space after : at end of the key, while in command line there are no spaces.
    arg1 - any number of arguments (that do not begin with --).
        Those arguments will replace $1, $2, ... markers in conf_file according to their position in command line:
        i.e. $1 will be replaced by first argument that do not begin with --, etc.
    or
    datconv --default
    which prints path to and contents of default configuration file.
    
    or
    datconv --version
    which prints version number to standard output and exit.
    
    or
    datconv --help
    which prints short usage information

    The datconv script returns to shell:
        0 on sucess 
        1 on general error (exception)
        2 on invalid command parameters
        3 on user break (Ctrl-C)

Sample main YAML configuration file layout:

.. literalinclude:: ../../datconv_pkg/conf_template.yaml
   :language: yaml

See also:

- :ref:`Readers configuration keys <readers_conf_template>`
- :ref:`Filters configuration keys <filters_conf_template>`
- :ref:`Writers configuration keys <writers_conf_template>`
- :ref:`Output connectors configuration keys <outconn_conf_template>`

datconv package
---------------------------------
.. automodule:: datconv
   :members:
 
datconv sub-packages
---------------------------------
.. toctree::

   api_readers
   api_filters
   api_writers
   api_outconn
   api_outconn_sqlite
   api_outconn_postgresql
   api_outconn_crate

   
..    :maxdepth: 3
   
