# -*- coding: utf-8 -*-
"""This is internal module used by Datconv when run in interactive mode."""

# Standard Python Libs

# Datconv packages
from . import OBJECT, ITERABLE


Log = None
"""Log varaible is automatically set by main datconv script using logging.getLogger method.
Use it for logging messages in need.
"""

class DCConnector:
    """Please see constructor description for more details."""
    # TODO: Add support for storing in temporary pickeles.
    def __init__(self):
        """Parameters are usually passed from YAML file as subkeys of OutConnector:CArg key.
        
        For more detailed descriptions see :ref:`conf_template.yaml <outconn_conf_template>` file in this module folder.
        """
        assert Log is not None
        self._records = None
        
    def supportedInterfases(self):
        return OBJECT | ITERABLE
    
    def tryObject(self, obj):
        self._records = []
        return True
    
    def pushObject(self, obj):
        self._records.append(obj)

    def __iter__(self):
        return iter(self._records)
