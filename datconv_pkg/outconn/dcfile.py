# -*- coding: utf-8 -*-
"""This module implements Datconv Output Connector which saves data to regular file."""


# Datconv packages
from . import STRING


Log = None
"""Log varaible is automatically set by main datconv script using logging.getLogger method.
Use it for logging messages in need.
"""

class DCConnector:
    """Please see constructor description for more details."""
    def __init__(self, path, mode = 'w'):
        """Parameters are usually passed from YAML file as subkeys of OutConnector:CArg key.
        
        :param path: relative or absolute path to output file.
        :param mode: output file opening mode.
        
        For more detailed descriptions see :ref:`conf_template.yaml <outconn_conf_template>` file in this module folder.
        """
        assert Log is not None

        self._path = path
        self._out = open(path, mode)
        
    def supportedInterfases(self):
        return STRING
    
    def pushString(self, strData):
        self._out.write(strData)
    
    def getStreams(self):
        return [self._out]

    def onFinish(self, bSuccess):
        if Log:
            if bSuccess:
                Log.info('Output saved to %s' % self._path)
            else:
                Log.error('Program did not finished properly: output saved to %s may be inconsistent' % self._path)
        self._out.close()
        
