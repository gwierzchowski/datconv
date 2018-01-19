#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""General Filter that allows to filter out certain record types."""

# Libs installed using pip
from lxml import etree

# Datconv packages
from . import SKIP, WRITE


Log = None
"""Log variable is automatically set by main datconv script using logging.getLogger method.
Use it for logging messages in need.
"""

class DCFilter:
    """Please see constructor description for more details."""
    def __init__(self, inclusive = True, rectyp = []):
        """Constructor parameters are usually passed from YAML file as subkeys of Filter:CArg key.
        
        :param inclusive: if False, record types given in rectyp are excluded, otherwise only rectyp records are included;
        :param rectyp: list of record types (root tags of records).
        
        For more detailed descriptions see :ref:`conf_template.yaml <filters_conf_template>` file in this module folder.
        """
        assert Log is not None
        self._inclusive = inclusive
        self._reclist = rectyp

    def filterRecord(self, record):
        if record.tag in self._reclist:
            return WRITE if self._inclusive else SKIP
        return SKIP if self._inclusive else WRITE
