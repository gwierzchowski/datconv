#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""General Filter that allows to filter out certain record types."""

# Libs installed using pip
from lxml import etree

# Datconv packages
from . import SKIP, WRITE


Log = None
"""Log varaible is automatically set by main pandoc script using logging.getLogger method.
Use it for logging messages in need.
"""

class DCFilter:
    def __init__(self, inclusive = True, rectyp = []):
        """Parameters are usually passed from YAML file as subkeys of Filter:CArg key.
        inclusive - if False, record types given in rectyp are excluded, otherwise only rectyp records are included;
        rectyp - list of record types (root tags of records).
        For more detailed descriptions see conf_template.yaml file in this module folder.
        """
        assert Log is not None
        self._inclusive = inclusive
        self._reclist = rectyp

    def filterRecord(self, record):
        if record.tag in self._reclist:
            return WRITE if self._inclusive else SKIP
        return SKIP if self._inclusive else WRITE
