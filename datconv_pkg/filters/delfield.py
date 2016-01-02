#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""General Filter that allows to remove certain fields from record."""

# Libs installed using pip
from lxml import etree

# Datconv packages
from . import WRITE


Log = None
"""Log varaible is automatically set by main pandoc script using logging.getLogger method.
Use it for logging messages in need.
"""

class DCFilter:
    def __init__(self, field = []):
        """Parameters are usually passed from YAML file as subkeys of Filter:CArg key.
        field - list of fields to remove.
                Fields must be in form of XPaths understandable by lxml.etree._Element.find method (relative paths)
        For more detailed descriptions see conf_template.yaml file in this module folder.
        """
        assert Log is not None
        self._fields = field

    def filterRecord(self, record):
        for fld in self._fields:
            tag = record.find(fld)
            if tag is not None:
                record.remove(tag)
        return WRITE
