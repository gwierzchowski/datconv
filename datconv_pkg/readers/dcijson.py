# -*- coding: utf-8 -*-
"""This module implements Datconv Reader which reads data from JSON file."""

# Standard Python Libs
import logging
from collections import deque

# Libs installed using pip
from lxml import etree  # http://lxml.de/tutorial.html

# Datconv generic modules
from datconv.filters import WRITE, REPEAT, BREAK

####################################################################
Log = None
"""Log variable is automatically set by main datconv script using logging.getLogger method.
Use it for logging messages in need.
"""

class FilterBreak(Exception):
    """Exception class to support Reader.process break isued from Filter class."""
    pass

class ToLimitBreak(Exception):
    """Exception class to support Reader.process break caused by reaching configured record limit."""
    pass

####################################################################
class DCReader:
    """This Datconv JSON Reader class uses ijson sax-type parser to read and interpret JSON file.
    It assumes that input file contain array of json objects and every such object is passed as record to Writer. This Reader passes always empty header and footer to Writer.\n
    Example:\n
    Input:
    
    .. code-block:: json

        [
        {
          "PadnDrawNbrs": {
            "cdc": 5019,
            "product": "addn"
          }
        },
        {
          "SiteData": {
            "siteId": 38
          },
          "rec0Control": {
            "curDraw": 5
          }
        }
        ]

    Output (:ref:`writers_dcxml`):

    .. code-block:: xml
    
        <Datconv>
        <rec>
            <PadnDrawNbrs>
                <cdc>5019</cdc>
                <product>addn</product>
            </PadnDrawNbrs>
        </rec>
        <rec>
            <SiteData>
                <siteId>38</siteId>
            </SiteData>
            <rec0Control>
                <curDraw>5</curDraw>
            </rec0Control>
        </rec>
        </Datconv>
    """
    def __init__(self, rec_tag = 'rec', log_prog_step = 0, backend = None):
        """Parameters are usually passed from YAML file as subkeys of ``Reader:CArg`` key.
        
        :param rec_tag: name or tag to be placed as record marker.
        :param log_prog_step: log info message after this number of records or does not log progress messages if this key is 0 or logging level is set to value higher than INFO.
        :param backend: backend used by ijson package to parse json file, possible values:\n
            ``yajl2_cffi`` - requires ``yajl2`` C library and ``cffi`` Python package to be installed in the system;\n
            ``yajl2`` - requires ``yajl2`` C library to be installed in the system;\n
            None - uses default, Python only backend.
        
        For more detailed descriptions see :ref:`readers_conf_template`.
        """
        assert Log is not None

        self._wri = self._flt = None
        self._rec_tag = rec_tag
        self._lp_step = log_prog_step
        self._backend = backend
        
    # OBLIGATORY
    def setWriter(self, writer):
        self._wri = writer

    # OBLIGATORY
    def setFilter(self, flt):
        self._flt = flt
    
    def Process(self, inpath, outpath = None, rfrom = 1, rto = 0):
        """Parameters are usually passed from YAML file as subkeys of ``Reader:PArg`` key.
        
        :param inpath: Path to input file.
        :param outpath: Path to output file passed to Writer (fall-back if output connector is not defined).
        :param rfrom-rto: specifies scope of records to be processed.
        
        For more detailed descriptions see :ref:`readers_conf_template`.
        """
        if self._backend == 'yajl2_cffi':
            import ijson.backends.yajl2_cffi as ijson
        elif self._backend == 'yajl2':
            import ijson.backends.yajl2 as ijson
        else:
            import ijson
        
        self._rfrom = rfrom
        self._rto = rto

        self._recno = 1
        self._lp_rec = 0
        if self._lp_step > 0 and Log.isEnabledFor(logging.INFO):
            self._lp_rec = self._lp_step
        
        # Common or this function local variables
        # 0 - outside element (e.g. between records)
        # 2 - inside record while reading
        # 3 - inside record while skipping
        self._mode = 0
        _curkey = self._rec_tag
        _deck = deque()
        
        # Used for read records
        self._rectag = None
        self._curtag = None

        # Used for skipped records
        self._s_nestlev = 0

        #fout = open(outpath, "w")
        
        ## OBLIGATORY
        #self._wri.setOutput(fout)
        
        try:
            # OBLIGATORY
            header = []
            if self._flt is not None:
                if hasattr(self._flt, 'setHeader'):
                    self._flt.setHeader(header)
            self._wri.writeHeader(header)
            
            with open(inpath, 'rb') as fd: #binary mode required by C-based backends
                _not_first_event = False
                _parser = ijson.basic_parse(fd)
                for event, value in _parser:
                    if event == 'map_key':
                        _curkey = value
                    elif event == 'start_map':
                        _deck.append(_curkey)
                        if _curkey is not None:
                            self._OnObjStart(_curkey)
                    elif event == 'end_map':
                        _curkey = _deck.pop()
                        if _curkey is not None:
                            self._OnObjEnd(_curkey)
                    elif event == 'start_array':
                        if _not_first_event and _curkey is None:
                            _deck.append('arr')
                            self._OnObjStart('arr')
                    elif event == 'end_array':
                        if len(_deck) > 0:
                            key = _deck.pop()
                            if key == 'arr':
                                self._OnObjEnd('arr')
                            else:
                                _deck.append(key)
                    else:
                        key = _curkey if _curkey is not None else event
                        self._OnData(key, value)
                    _not_first_event = True
        except FilterBreak:
            pass
        except ToLimitBreak:
            pass
        finally:
            # OBLIGATORY
            footer = []
            if self._flt is not None:
                if hasattr(self._flt, 'setFooter'):
                    self._flt.setFooter(footer)
            self._wri.writeFooter(footer)
            #fout.close()
            #Log.info('Output saved to %s' % outpath)
    
    def _OnObjStart(self, key):
        if self._mode == 0:
            if self._recno < self._rfrom:
                self._mode = 3
                return
            self._curtag = self._rectag = etree.Element(key)
            self._mode = 2
        elif self._mode == 2:
            assert self._curtag is not None
            self._curtag = etree.SubElement(self._curtag, key)
        elif self._mode == 3:
            self._s_nestlev = self._s_nestlev + 1
    
    def _OnData(self, key, value):
        if self._mode == 0:
            self._recno = self._recno + 1
            if self._recno <= self._rfrom:
                return

            rec = etree.Element(key)
            rec.text = str(value)
            if self._flt is not None:
                while True:
                    # OBLIGATORY
                    res = self._flt.filterRecord(rec)
                    if res & WRITE:
                        self._wri.writeRecord(rec)
                    if res & REPEAT:
                        continue
                    if res & BREAK:
                        Log.info('Filter caused Process to stop on record %d' % (self._recno - 1))
                        raise FilterBreak
                    break
            else:
                # OBLIGATORY
                self._wri.writeRecord(rec)

            if self._rto > 0 and self._recno > self._rto:
                raise ToLimitBreak
            if self._recno - 1 == self._lp_rec:
                Log.info('Processed %d records' % (self._recno - 1))
                self._lp_rec = self._lp_rec + self._lp_step
        elif self._mode == 2:
            assert self._curtag is not None
            tag = etree.SubElement(self._curtag, key)
            tag.text = str(value)
        elif self._mode == 3:
            pass
    
    def _OnObjEnd(self, key):
        if self._mode == 0:
            pass
        elif self._mode == 2:
            assert self._curtag is not None
            if self._curtag == self._rectag:
                self._recno = self._recno + 1

                rec = self._curtag
                if self._flt is not None:
                    while True:
                        # OBLIGATORY
                        res = self._flt.filterRecord(rec)
                        if res & WRITE:
                            self._wri.writeRecord(rec)
                        if res & REPEAT:
                            continue
                        if res & BREAK:
                            Log.info('Filter caused Process to stop on record %d' % (self._recno - 1))
                            raise FilterBreak
                        break
                else:
                    # OBLIGATORY
                    self._wri.writeRecord(rec)

                if self._rto > 0 and self._recno > self._rto:
                    raise ToLimitBreak
                if self._recno - 1 == self._lp_rec:
                    Log.info('Processed %d records' % (self._recno - 1))
                    self._lp_rec = self._lp_rec + self._lp_step
                self._mode = 0
            else:
                self._curtag = self._curtag.getparent()
        elif self._mode == 3:
            if self._s_nestlev > 0:
                self._s_nestlev = self._s_nestlev - 1
            else:
                self._recno = self._recno + 1
                self._mode = 0
