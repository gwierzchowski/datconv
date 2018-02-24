# -*- coding: utf-8 -*-
"""This module implements Datconv Reader which reads data from XML file."""

# Standard Python Libs
import xml.sax as sax
import logging

# Libs installed using pip
from lxml import etree  # http://lxml.de/tutorial.html

# Datconv generic modules
from datconv.filters import WRITE, REPEAT, BREAK

####################################################################
Log = None
"""Log variable is automatically set by main pandoc script using logging.getLogger method.
Use it for logging messages in need.
"""

class FilterBreak(Exception):
    """Exception class to support Reader.process break isued from Filter class."""
    pass

class ToLimitBreak(Exception):
    """Exception class to support Reader.process break caused by reaching configured record limit."""
    pass

####################################################################
class ContentGenerator(sax.handler.ContentHandler):
    """This class handles XML events generated by parser created by xml.sax.make_parser().
    It implements most of the functionality of this XML Reader.
    See documentation of its base class for description of methods meaning.
    """
    def __init__(self, bratags, headtags, rectags, foottags, wri, flt = None, lp_step = 0, rfrom = 1, rto = 0):
        """See description of DCReader constructor and Process() method for meaning of most parameters."""
        sax.handler.ContentHandler.__init__(self)
        self._btags = bratags
        self._htags = headtags
        self._rtags = rectags
        self._ftags = foottags
        self._wri  = wri
        self._flt  = flt
        self._lp_step  = lp_step
        self._rfrom    = rfrom
        self._rto  = rto
        self._bs   = None
        self._curtag = None
        self._header = []
        self._footer = []
        self._header_read = False

    # ContentHandler methods
    def startDocument(self):
        self._recno = 0
        self._lp_rec = 0
        if self._lp_step > 0 and Log.isEnabledFor(logging.INFO):
            self._lp_rec = self._lp_step

    def endDocument(self):
        if not self._header_read:
            # OBLIGATORY
            if self._flt is not None:
                if hasattr(self._flt, 'setHeader'):
                    self._flt.setHeader(self._header)
            self._wri.writeHeader(self._header)
            self._header_read = True

        # OBLIGATORY
        if self._flt is not None:
            if hasattr(self._flt, 'setFooter'):
                self._flt.setFooter(self._footer)
        self._wri.writeFooter(self._footer)

    def startElement(self, name, attrs):
        if not self._header_read and name in self._btags:
            h = dict()
            h['_tag_'] = name
            h['_bra_'] = True
            for (aname, avalue) in attrs.items():
                h[aname] = avalue
            self._header.append(h)
        elif not self._header_read and name in self._htags:
            h = dict()
            h['_tag_'] = name
            h['_bra_'] = False
            for (aname, avalue) in attrs.items():
                h[aname] = avalue
            self._header.append(h)
        elif self._bs is None and name in self._ftags:
            f = dict()
            f['_tag_'] = name
            for (aname, avalue) in attrs.items():
                f[aname] = avalue
            self._footer.append(f)
        elif (self._bs is None and name in self._rtags) or \
             (self._bs is None and len(self._rtags) == 0):
            if not self._header_read:
                if self._flt is not None:
                    if hasattr(self._flt, 'setHeader'):
                        self._flt.setHeader(self._header)
                self._wri.writeHeader(self._header)
                self._header_read = True
            self._recno = self._recno + 1
            if self._recno < self._rfrom:
                return
            if self._rto > 0 and self._recno > self._rto:
                self.endDocument()
                raise ToLimitBreak
            self._bs = etree.Element(name)
            self._curtag = self._bs
            for (aname, avalue) in attrs.items():
                self._curtag.set(aname, avalue)
        elif self._bs is not None:
            if name in self._rtags:
                Log.error('Nested record tag: <%s> in %d record; file will not be interpretted correctly' % (name, self._recno))
            ntag = etree.SubElement(self._curtag, name)
            self._curtag = ntag
            for (aname, avalue) in attrs.items():
                self._curtag.set(aname, avalue)

    def endElement(self, name):
        if self._bs is not None:
            #if name in self._rtags:
            if name == self._bs.tag:
                if self._recno == self._lp_rec:
                    Log.info('Processed %d records' % self._recno)
                    #self._log.info('Processed %d records' % self._recno)
                    self._lp_rec = self._lp_rec + self._lp_step
                
                if self._flt is not None:
                    rec = self._bs
                    while True:
                        # OBLIGATORY
                        res = self._flt.filterRecord(rec)
                        if res & WRITE:
                            self._wri.writeRecord(rec)
                        if res & REPEAT:
                            continue
                        if res & BREAK:
                            self.endDocument()
                            Log.info('Filter caused Process to stop on record %d' % self._recno)
                            raise FilterBreak
                        break
                else:
                    # OBLIGATORY
                    self._wri.writeRecord(self._bs)
                self._bs = None
                self._curtag = None
            else:
                self._curtag = self._curtag.getparent()

    def characters(self, content):
        if not self._bs is None:
            content = content.strip()
            if len(content) > 0:
                if self._curtag.text is None:
                    self._curtag.text = content
                else:
                    self._curtag.text = self._curtag.text + content
                    #self._curtag.tail = content

####################################################################
class DCReader:
    """This Datconv XML Reader class uses xml.sax parser to read and interpret XML file.
    This parser uses ContentGenerator class from this module to handle XML events.
    See documentation of standard Python xml.sax library for more information how it works.
    This Reader assumens that srtucture of input XML file is following:

    * there is/are some (one or more) BRACE tag(s);
      entire document content is included in this/those brace tag(s);
      well-formed XML document should have at least one such tag;
    * then there is/are some optional HEAD tag(s);
      head tags begin and end completly before record tags begin;
    * then there are RECORD tags;
      everything what is inside record tags is treated as record data and is being passed to Filter and Writer;
      record tags can not be nested - every record tag must end before another record tag begin;
      there may be several kinds (names) or record tags - in such case we say that we have multiply record types.
      If list of record tags is empty then every tag which is one level under brace tag and which is not head nor foot tag is treated as record tag.
    * then there is/are some optional FOOTER tag(s);
      footer tags begin and end completly after record tags;
      
    Constructor parameters explicitly list which tags are of what kind.\n
    TODO: The text inside brace, header and footer tags is discarded (only attributes are passed to Writer).\n
    TODO: The header tags between record tags are discarded (only ones before first record tag are passed to Writer.\n
    TODO: This class does not support CDATA inside XML.
    """
    def __init__(self, bratags = [], headtags = [], rectags = [], foottags = [], log_prog_step = 0):
        """Parameters are usually passed from YAML file as subkeys of ``Reader:CArg`` key.
        
        :param bratags: list of tag names that will be treated as brace tags (see above).
        :param headtags: list of tag names that will be treated as header tags (see above).
        :param rectags: list of tag names that will be treated as record tags (see above).
        :param foottags: list of tag names that will be treated as footer tags (see above).
        :param log_prog_step: log info message after this number of records or does not log progress messages if this key is 0 or logging level is set to value higher than INFO.
        
        For more detailed descriptions see :ref:`readers_conf_template`.
        """
        assert Log is not None

        self._wri = self._flt = None
        self._btags = bratags
        self._htags = headtags
        self._rtags = rectags
        self._ftags = foottags
        self._lp_step = log_prog_step

    # OBLIGATORY
    def setWriter(self, writer):
        self._wri = writer

    # OBLIGATORY
    def setFilter(self, filter):
        self._flt = filter
    
    def Process(self, inpath, outpath = None, rfrom = 1, rto = 0):
        """Parameters are usually passed from YAML file as subkeys of ``Reader:PArg`` key.
        
        :param inpath: Path to input file.
        :param outpath: Path to output file passed to Writer (fall-back if output connector is not defined).
        :param rfrom-rto: specifies scope of records to be processed.
        
        For more detailed descriptions see :ref:`readers_conf_template`.
        """

        #fout = open(outpath, "w")
        
        # OBLIGATORY
        #self._wri.setOutput(fout)
        
        parser = sax.make_parser()
        parser.setContentHandler( \
            ContentGenerator( \
                bratags = self._btags, \
                headtags = self._htags, \
                rectags = self._rtags, \
                foottags = self._ftags, \
                wri = self._wri, \
                flt = self._flt, \
                lp_step = self._lp_step, \
                rfrom = rfrom, \
                rto = rto \
                ) \
            )
        try:
            parser.parse(inpath)
        except FilterBreak:
            pass
        except ToLimitBreak:
            pass
        #finally:
            #fout.close()
            #Log.info('Output saved to %s' % outpath)
