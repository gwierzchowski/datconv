# -*- coding: utf-8 -*-
"""This module implements Datconv Output Connector which writes data to standard output stream."""

# Standard Python Libs
import sys

# Datconv packages
from . import STRING


Log = None
"""Log varaible is automatically set by main datconv script using logging.getLogger method.
Use it for logging messages in need.
"""

class DCConnector:
    def __init__(self):
        assert Log is not None
        
    def supportedInterfases(self):
        return STRING
    
    def pushString(self, strData):
        sys.stdout.write(strData)
    
    def getStreams(self):
        return [sys.stdout]
