Default Configuration
=====================

Default Configuration file is a file with specific name: ``.datconv_def.yml`` located in 
root of user home folder. So in typical installations it this the file:

=======  ===========================================
System   Standard Datconv default configuration file
=======  ===========================================
Linux    ``/home/<login>/.datconv_def.yml``
Windows  ``C:\Users\<login>\.datconv_def.yml``
OS X     ``/Users/<login>/.datconv_def.yml``
=======  ===========================================

Existance of this file is optional.
Datconv during startup checks if the file is present. If is present it is read and interpretted
as YAML file. The keys in this file are being merged with keys in main configuration file 
(file passed as first positional argument during datconv invocation from shell).
This merge is being done under following rules:

1. Keys from main configuration file takes presedence. 
   I.e. keys from default configuration file are used only if there is no equivalent key in main configuration file.
2. If main configuration file declare different ``Module:`` that default configuration file,
   then respective (from the same component) ``CArg:`` key from default configuration file is
   completly discarded.
3. If there is '=' character before main configuration file name specified in shell,
   than default configuration file is not baing read and discarded ('=' character is stripped from main configuration file name).
4. If main configuration file is declared as 'def' then it means that there is no main
   configuration file, and all settings are taken from default configuration file.
5. If option is not present neither in main nor default configuration file, then value listed 
   as 'defaut` in documentation (class constructor default value or value given as default in 
   conf_template.yaml file) is used.
   
The syntax of default configuration file is the same as main configuration: :ref:`datconv_program`.

Defaults configuration file can be used in one of follwing ways:

- not used at all. Clear configuration, no hidden logic.
- used as only one configuration file. User allways edit default configuration file, and then 
  run ``datconv def <in> <out>`` from folder where data fiels are without worying of path to configuration file.
- mixed mode. E.g. logger configuration or ``DefLogLevel:`` kay can be specified in default 
  configuration file and the rest in main configuration file.
  
.. note::

  - When Datconv is called directly from Python (as ``Datconv.Run(conf)`` invocation) then
    default configuration file is not used.
  - When DEBUG logging level is emabled, Datconv logs its run configuration (after merging).
