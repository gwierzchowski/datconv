.. include:: defs.rst

datconv.outconn package 
-----------------------------------------
.. automodule:: datconv.outconn
   :members:

.. _outconn_skeleton:

Output Connector interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: datconv.outconn._skeleton
   :members:

datconv.outconn.dcnull module 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: datconv.outconn.dcnull
   :members:

datconv.outconn.dcstdout module 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: datconv.outconn.dcstdout
   :members:

datconv.outconn.dcfile module 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: datconv.outconn.dcfile
   :members:

datconv.outconn.dcexcel module 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: datconv.outconn.dcexcel
   :members:

datconv.outconn.dcmultiplicator module 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: datconv.outconn.dcmultiplicator
   :members:

.. _outconn_conf_template:

Configuration keys
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Listing of all possible configuration keys to be used with output connectors contained in this package.

There are sample values given, if key is not specified in configuration file, than default value is assumed.

.. literalinclude:: ../../datconv_pkg/outconn/conf_template.yaml
   :language: yaml
