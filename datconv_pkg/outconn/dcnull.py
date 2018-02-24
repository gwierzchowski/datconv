# -*- coding: utf-8 -*-
"""This module implements Datconv Output Connector which discards output (like writing to /dev/null)."""


Log = None
"""Log varaible is automatically set by main datconv script using logging.getLogger method.
Use it for logging messages in need.
"""

class DCConnector:
    def __init__(self):
        assert Log is not None
        
    def supportedInterfases(self):
        return 0
