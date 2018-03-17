# -*- coding: utf-8 -*-
"""This module implements Datconv Writer which saves data in form of XML file."""

# In Python 2.7 only
from __future__ import print_function

# Standard Python Libs
import sys

# Libs installed using pip
from lxml import etree

# Datconv generic modules
from datconv.outconn import STRING, OBJECT

Log = None
"""Log varaible is automatically set by main datconv script using logging.getLogger method.
Use it for logging messages in need.
"""

class DCWriter:
    """Please see constructor description for more details."""
    def __init__(self, pretty = True, encoding = 'unicode', cnt_tag = None, cnt_attr = None, add_header = True, add_footer = True):
        """Constructor parameters are usually passed from YAML file as subkeys of Writer:CArg key.
        
        :param pretty: this parameter is passed to lxml.etree.tostring function. If True, XML is formated in readable way (one tag in one line), otherwise full record is placed in one line (more compact,suitable for computers).
        :param encoding: this parameter is passed to lxml.etree.tostring function. It determines emcoding used in output XML file. See documantation of codecs standard Python library for possible encodings. This parameter is ignored in Python3, where always unicode coding is used.
        :param cnt_tag: tag name to store records count, if not set record count will not be printed in output footer
        :param cnt_attr: attribute of cnt_tag tag to store records count, if not set record count will be printed as tag text
        :param add_header: if True, generic header (as initialized by Reader) is added as first tag of output file.
        :param add_footer: if True, generic footer (as initialized by Reader) is added as last tag of output file.
        
        For more detailed descriptions see :ref:`conf_template.yaml <writers_conf_template>` file in this module folder.
        """
        assert Log is not None

        self._pretty = pretty
        self._enc = encoding
        if sys.version_info.major > 2 and encoding != 'unicode':
            self._enc = 'unicode'
            Log.warning('Unsupported parameter: "encoding" used; setting ignored')
        if sys.version_info.major == 2 and encoding == 'unicode':
            self._enc = 'utf8'
        self._cnt_tag = cnt_tag
        self._cnt_attr = cnt_attr
        #self._out = sys.stdout
        self._out = None
        self._out_flags = 0;
        self._cnt = 0
        self._bratags = []
        self._add_header = add_header
        self._add_footer = add_footer

    def setOutput(self, out):
        self._out = out
        self._out_flags = out.supportedInterfases();
        # currently this writer strictly require string output connector
        # we wre currntly not checkeing this bit further.
        # TODO: Rewrite Header/Footer to create tree-element and use compatible OBJECT connector.
        assert self._out_flags & STRING
        self._cnt = 0
        self._bratags = []
        
    def writeHeader(self, header):
        if self._enc in ['unicode', 'utf8']:
            self._out.pushString('<?xml version="1.0" encoding="UTF-8"?>\n')
        else:
            self._out.pushString('<?xml version="1.0" encoding="%s"?>\n' % self._enc)
        for h in header:
            if isinstance(h, dict):
                if '_tag_' in h and '_bra_' in h and h['_bra_']:
                    self._bratags.append(h['_tag_'])
                    self._out.pushString('<' + h['_tag_'])
                    for (aname, avalue) in h.items():
                        if aname != '_tag_'and aname != '_bra_':
                            self._out.pushString(' ' + str(aname) + '="' + str(avalue) + '"')
                    self._out.pushString('>\n')
                    del header[header.index(h)]
                    break
        if len(self._bratags) == 0:
            self._bratags.append('Datconv')
            self._out.pushString('<Datconv>\n')
        if self._add_header:
            for h in header:
                if isinstance(h, dict):
                    if '_tag_' in h:
                        self._out.pushString('<' + h['_tag_'])
                        for (aname, avalue) in h.items():
                            if aname != '_tag_'and aname != '_bra_':
                                self._out.pushString(' ' + str(aname) + '="' + str(avalue) + '"')
                        if '_bra_' in h and h['_bra_']:
                            self._out.pushString('>\n')
                            self._bratags.append(h['_tag_'])
                        else:
                            self._out.pushString('/>\n')
                    else:
                        self._out.pushString('<Header')
                        for (aname, avalue) in h.items():
                            self._out.pushString(' ' + str(aname) + '="' + str(avalue) + '"')
                        self._out.pushString('/>\n')
                else:
                    self._out.pushString('<Header>%s</Header>\n' % str(h))

    def writeFooter(self, footer):
        if self._cnt_tag:
            if self._cnt_attr:
                self._out.pushString('<%s %s="%d"/>\n' % (self._cnt_tag, self._cnt_attr, self._cnt))
            else:
                self._out.pushString('<%s>%d</%s>\n' % (self._cnt_tag, self._cnt, self._cnt_tag))
        if self._add_footer:
            for f in footer:
                if isinstance(f, dict):
                    if '_tag_' in f:
                        self._out.pushString('<' + f['_tag_'])
                        for (aname, avalue) in f.items():
                            if aname != '_tag_':
                                self._out.pushString(' ' + str(aname) + '="' + str(avalue) + '"')
                        self._out.pushString('/>\n')
                    else:
                        self._out.pushString('<Footer')
                        for (aname, avalue) in f.items():
                            self._out.pushString(' ' + str(aname) + '="' + str(avalue) + '"')
                        self._out.pushString('/>\n')
                else:
                    self._out.pushString('<Footer>%s</Footer>\n' % str(f))
        for i in range(len(self._bratags) - 1, -1, -1):
            self._out.pushString('</' + self._bratags[i] + '>\n')

    def writeRecord(self, record):
        for stream in self._out.getStreams():
            print(etree.tostring(record, pretty_print = self._pretty, encoding = self._enc), file = stream)
        self._cnt = self._cnt + 1
