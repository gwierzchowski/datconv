#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
General Filter that allows to generate new records.
Every record is cloned by conifigurable number of times.
This Filter is suitable for subclassing if more rebust generation strategies are required.
"""

from lxml import etree
from datconv.filters import SKIP, WRITE, REPEAT, BREAK

Log = None
"""Log varaible is automatically set by main datconv script using logging.getLogger method.
Use it for logging messages in need.
"""

class DCFilter:
    """Please see constructor description for more details."""
    def __init__(self, n = 1, fake_flg = None):
        """Constructor parameters are usually passed from YAML file as subkeys of Filter:CArg key.
        
        :param n: determines how many clones are generated for every record.
        :param fake_flg: if set (to string) a tag of set name is added to every generated cloned record with the value 1.
        
        For more detailed descriptions see :ref:`conf_template.yaml <filters_conf_template>` file in this module folder.
        """
        assert Log is not None
        assert n >= 0
        if fake_flg:
            assert isinstance(fake_flg, str)
        self._dupcnt = 0
        self._n = n
        self._fake_flg = fake_flg
        
    def filterRecord(self, record):
        if self._n == 0:
            return WRITE
        if self._dupcnt == 0:
            self._dupcnt = 1
            return WRITE | REPEAT
        if self._dupcnt == 1 and self._fake_flg:
            tag = etree.Element(self._fake_flg)
            tag.text = '1'
            record.insert(0, tag)

        self._dupcnt += 1

        if self._dupcnt > self._n:
            self._dupcnt = 0
            return WRITE
        return WRITE | REPEAT
    
