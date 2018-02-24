# -*- coding: utf-8 -*-
"""This module implements Datconv Output Connector which sends data to multiply connectors."""

# Standard Python Libs
from importlib import import_module

# Datconv packages
from . import STRING, OBJECT, ITERABLE


Log = None
"""Log varaible is automatically set by main datconv script using logging.getLogger method.
Use it for logging messages in need.
"""

class DCConnector:
    """Please see constructor description for more details."""
    def __init__(self, clist):
        """Parameters are usually passed from YAML file as subkeys of OutConnector:CArg key.
        
        :param clist:  list of filters to be run in chain with their parameters.
        
        For more detailed descriptions see :ref:`conf_template.yaml <outconn_conf_template>` file in this module folder.
        """
        assert Log is not None
        assert isinstance(clist, list)
        self._clist = []
        for conn in clist:
            conn_path = conn['Module']
            conn_carg = conn.get('CArg')
            conn_mod = import_module(conn_path)
            conn_mod.Log = Log
            conn_class = getattr(conn_mod, 'DCConnector')
            Log.debug('Adding connector: %s(%s)', conn_path, str(conn_carg))
            conn_inst = conn_class(**conn_carg) if conn_carg else conn_class()
            self._clist.append(conn_inst)
        
    def supportedInterfases(self):
        ret = 0
        for conn in self._clist:
            ret |= conn.supportedInterfases()
        return ret
    
    def pushString(self, strData):
        for conn in self._clist:
            if conn.supportedInterfases() & STRING:
                conn.pushString(strData)
    
    def getStreams(self):
        ret = []
        for conn in self._clist:
            if conn.supportedInterfases() & STRING:
                for stream in conn.getStreams():
                    ret.append(stream)
        return ret
    
    def tryObject(self, obj):
        for conn in self._clist:
            if conn.supportedInterfases() & OBJECT:
                if not conn.tryObject(obj):
                    return False
        return True
    
    def pushObject(self, obj):
        for conn in self._clist:
            if conn.supportedInterfases() & OBJECT:
                conn.pushObject(obj)

    def onFinish(self, bSuccess):
        for conn in self._clist:
            if hasattr(conn, 'onFinish'):
                conn.onFinish(bSuccess)
        
