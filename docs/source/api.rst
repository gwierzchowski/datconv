The Datconv API reference
=========================

The datconv program reference
-----------------------------
The :command:`datconv` script has following call syntax::

    datconv yaml_file [--key1:val [--key2:val ...]] [arg1 [arg2 ...]]
    where:
    yaml_file - is obligatory path to file in YAML format in which Reader, Filter and Writer compoments are set up.
                See below listing for more detailed desctiption of this file.
    --key1:val - any number of arguments that add new settings or overwrite settings from yaml_file.
                It works this way: let say that in yaml_file we have:
                Writer:
                    Module: writers.dcxml
                    CArg: 
                        pretty:   true
                by invoking option --Writer:CArg:pretty:false we overwrite 'pretty' option of Writer.
                Note that in YAML file we have to have space after : at end of the key, while in command line there are no spaces.
    arg1 - any number of arguments (that do not begin with --).
        Those arguments will replace $1, $2, ... markers in yaml_file according to their position in command line:
        i.e. $1 will be replaced by first argument that do not begin with --, etc.
    or
    datconv --version
    which prints version number to standard output and exit.

    The datconv script returns to shell:
        0 on sucess 
        1 on general error (exception)
        2 on invalid command parameters
        3 on user break (Ctrl-C)

Main YAML configuration file layout:

.. literalinclude:: ../../datconv_pkg/conf_template.yaml
   :language: yaml

See also:

- :ref:`readers_conf_template`
- :ref:`filters_conf_template`
- :ref:`writers_conf_template`

The datconv package reference
---------------------------------
.. automodule:: datconv
   :members:
 
The datconv sub-packages
---------------------------------
.. toctree::
   :maxdepth: 2

   api_readers
   api_filters
   api_writers
