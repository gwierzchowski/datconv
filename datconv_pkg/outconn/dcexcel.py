# -*- coding: utf-8 -*-
"""
This module implements Datconv Output Connector which writes data to MS Excel (*.xlsx) file.
This connector should be used with Writer: :ref:`writers_dccsv`.
It requires Python package ``openpyxl`` to be installed.
It does not require Excel program to be installed.

.. note::
    This is very initial version of the package (beta quality):

    - there is no support for cell value types: currently all data are placed as text
    - output uses default font, sheet name etc.
    - do not use this connector with very large data: all data are kept in memory before baing saved.
"""

# Standard Python Libs

# Libs installed using pip
from openpyxl import Workbook #documentation: https://openpyxl.readthedocs.io/en/latest/index.html

# Datconv packages
from . import LIST


Log = None
"""Log varaible is automatically set by main datconv script using logging.getLogger method.
Use it for logging messages in need.
"""

class DCConnector:
    """Please see constructor description for more details."""
    def __init__(self, path):
        """Parameters are usually passed from YAML file as subkeys of OutConnector:CArg key.
        
        :param path: relative or absolute path to output file.
        
        For more detailed descriptions see :ref:`conf_template.yaml <outconn_conf_template>` file in this module folder.
        """
        assert Log is not None

        self._path = path
        self._wb = Workbook()
        self._ws = self._wb.active
        self._rowno = 1
        
    def supportedInterfases(self):
        return LIST
    
    def tryObject(self, obj):
        self._rowno = 1
        return isinstance(obj, list)
    
    def pushObject(self, obj):
        colno = 1
        for dat in obj:
            self._ws.cell(column=colno, row=self._rowno, value=str(dat))
            colno += 1
        self._rowno += 1

    def onFinish(self, bSuccess):
        self._wb.save(filename = self._path) #TODO: Check how to handle save error.
        if Log:
            if bSuccess:
                Log.info('Output saved to %s' % self._path)
            else:
                Log.error('Program did not finished properly: output saved to %s may be inconsistent' % self._path)
        
