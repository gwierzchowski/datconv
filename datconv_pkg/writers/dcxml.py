# -*- coding: utf-8 -*-
"""This module implements Pandoc Writer which saves data in form of XML file.
Please see DCWriter constructor description for more details.
"""

# In Python 2.7 only
from __future__ import print_function

# Standard Python Libs
import sys

# Libs installed using pip
from lxml import etree

Log = None
"""Log varaible is automatically set by main pandoc script using logging.getLogger method.
Use it for logging messages in need.
"""

class DCWriter:
    def __init__(self, pretty = True, encoding = 'unicode', cnt_tag = None, cnt_attr = None):
        """Parameters are usually passed from YAML file as subkeys of Writer:CArg key.
        pretty - this parameter is passed to lxml.etree.tostring function.
                 If True, XML is formated in readable way (one tag in one line),
                 otherwise full record is placed in one line (more compact,suitable for computers).
        encoding - this parameter is passed to lxml.etree.tostring function.
                   It determines emcoding used in output XML file.
                   See documantation of codecs standard Python library for possible encodings.
                   Note: This parameter is ignored in Python3, where always unicode coding is used.
        cnt_tag  - tag name to store records count, if not set record count will not be printed in output footer
        cnt_attr - attribute of cnt_tag tag to store records count, if not set record count will be printed as tag text
        For more detailed descriptions see conf_template.yaml file in this module folder.
        """
        assert Log is not None

        self._pretty = pretty
        self._enc = encoding
        if sys.version_info.major > 2 and encoding != 'unicode':
            self._enc = 'unicode'
            Log.warning("Unsupported parameter: encoding used; setting ignored")
        if sys.version_info.major == 2 and encoding == 'unicode':
            self._enc = 'utf8'
        self._cnt_tag = cnt_tag
        self._cnt_attr = cnt_attr
        self._out = sys.stdout
        self._cnt = 0
        self._bratags = []

    def setOutput(self, out):
        self._out = out
        self._cnt = 0
        self._bratags = []
        
    def writeHeader(self, header):
        if self._enc == 'unicode':
            self._out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        else:
            self._out.write('<?xml version="1.0" encoding="%s"?>\n' % self._enc)
        for h in header:
            if isinstance(h, dict):
                if '_tag_' in h and '_bra_' in h and h['_bra_']:
                    self._bratags.append(h['_tag_'])
                    self._out.write('<' + h['_tag_'] + ' ')
                    for (aname, avalue) in h.items():
                        if aname != '_tag_'and aname != '_bra_':
                            self._out.write(str(aname) + '="' + str(avalue) + '" ')
                    self._out.write('>\n')
                    del header[header.index(h)]
                    break
        if len(self._bratags) == 0:
            self._bratags.append('Datconv')
            self._out.write('<Datconv>\n')
        for h in header:
            if isinstance(h, dict):
                if '_tag_' in h:
                    self._out.write('<' + h['_tag_'] + ' ')
                    for (aname, avalue) in h.items():
                        if aname != '_tag_'and aname != '_bra_':
                            self._out.write(str(aname) + '="' + str(avalue) + '" ')
                    if '_bra_' in h and h['_bra_']:
                        self._out.write('>\n')
                        self._bratags.append(h['_tag_'])
                    else:
                        self._out.write('/>\n')
            else:
                self._out.write('<Header>%s</Header>\n' % str(h))

    def writeFooter(self, footer):
        if self._cnt_tag:
            if self._cnt_attr:
                self._out.write('<%s %s="%d"/>\n' % (self._cnt_tag, self._cnt_attr, self._cnt))
            else:
                self._out.write('<%s>%d</%s>\n' % (self._cnt_tag, self._cnt, self._cnt_tag))
        for f in footer:
            if isinstance(f, dict):
                if '_tag_' in f:
                    self._out.write('<' + f['_tag_'] + ' ')
                    for (aname, avalue) in f.items():
                        if aname != '_tag_':
                            self._out.write(str(aname) + '="' + str(avalue) + '" ')
                    self._out.write('/>\n')
            else:
                self._out.write('<Footer>%s</Footer>\n' % str(f))
        for i in range(len(self._bratags) - 1, -1, -1):
            self._out.write('</' + self._bratags[i] + '>\n')

    def writeRecord(self, record):
        print(etree.tostring(record, pretty_print = self._pretty, encoding = self._enc), file = self._out)
        self._cnt = self._cnt + 1
