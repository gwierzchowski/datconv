# -*- coding: utf-8 -*-
"""This module implements Datconv Reader which reads data from JSON file."""

# Standard Python Libs
import logging

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
    """This Datconv Reader class is utility class to help discover structure of JSON data file.
    It returns events generated by Python ``ijson`` JSON files parser.\n
    Example records returned by this reader (mode == 3):\n
    Input:
    
    .. code-block:: json

        {
          "PadnDrawNbrs": {
            "cdc": 5019,
            "product": "addn"
          }
        }

    Output (:ref:`writers_dccsv`):
    
    .. code-block:: none

        prefix , event , value 
        item , start_map , None 
        item , map_key , PadnDrawNbrs 
        item.PadnDrawNbrs , start_map , None 
        item.PadnDrawNbrs , map_key , cdc 
        item.PadnDrawNbrs.cdc , number , 5019 
        item.PadnDrawNbrs , map_key , product 
        item.PadnDrawNbrs.product , string , addn 
        item.PadnDrawNbrs , end_map , None 
        item , end_map , None 

    Usage instructions of ``ijson`` package:

    * `<https://pypi.python.org/pypi/ijson/>`_
    * `<http://softwaremaniacs.org/blog/2010/09/18/ijson/en/>`_
    * `<http://explique.me/Ijson/>`_
    """
    def __init__(self, mode = 3, rec_tag = 'rec', log_prog_step = 0, backend = None):
        """Parameters are usually passed from YAML file as subkeys of ``Reader:CArg`` key.
        
        :param mode: returns: 1-only unique prefixes; 2-unique (prefix,event) pairs; 3-all events (including data).
        :param rec_tag: name or tag to be placed as record marker.
        :param log_prog_step: log info message after this number of records or does not log progress messages if this key is 0.
        :param backend: backend used by ijson package to parse json file, possible values:\n
        ``yajl2_cffi`` - requires ``yajl2`` C library and ``cffi`` Python package to be installed in the system;\n
        ``yajl2`` - requires ``yajl2`` C library to be installed in the system;\n
        None - uses default, Python only backend.
        
        For more detailed descriptions see :ref:`readers_conf_template`.
        """
        assert Log is not None

        self._wri = self._flt = None
        self._mode = mode
        self._rec_tag = rec_tag
        self._lp_step = log_prog_step
        self._backend = backend

    # OBLIGATORY
    def setWriter(self, writer):
        self._wri = writer

    # OBLIGATORY
    def setFilter(self, flt):
        self._flt = flt
    
    def Process(self, inpath, outpath, rfrom = 1, rto = 0):
        """Parameters are usually passed from YAML file as subkeys of ``Reader:PArg`` key.
        
        :param inpath: Path to input file.
        :param outpath: Path to output file passed to Writer.
        :param rfrom-rto: specifies scope of records to be processed.
        
        For more detailed descriptions see :ref:`readers_conf_template`.
        """
        if self._backend == 'yajl2_cffi':
            import ijson.backends.yajl2_cffi as ijson
        elif self._backend == 'yajl2':
            import ijson.backends.yajl2 as ijson
        else:
            import ijson

        _recno = 1
        _lp_rec = 0
        if self._mode in [1, 2]:
            _unique = set()
        elif self._mode == 3:
            _unique = None
        else:
            Log.error('Invalid value of key mode (=%d); allowed values [1,2,3]' % self._mode)
            return
        if self._lp_step > 0 and Log.isEnabledFor(logging.INFO):
            _lp_rec = self._lp_step

        fout = open(outpath, "w")
        
        # OBLIGATORY
        self._wri.setOutput(fout)
        
        try:
            header = [{'_tag_':'ijson_events', '_bra_':True}]
            if self._flt is not None:
                if hasattr(self._flt, 'setHeader'):
                    self._flt.setHeader(header)
            self._wri.writeHeader(header)
            
            with open(inpath, 'r') as fd:
                parser = ijson.parse(fd)
                for prefix, event, value in parser:
                    if rto > 0 and _recno > rto:
                        raise ToLimitBreak
                    if prefix in ['item', ''] and not event in ['start_array', 'start_map', 'map_key']:
                        _recno = _recno + 1
                        if _recno == _lp_rec:
                            Log.info('Processed %d records' % _recno)
                            _lp_rec = _lp_rec + self._lp_step
                    if _recno < rfrom:
                        return

                    if self._mode == 1:
                        if prefix in _unique:
                            continue
                        _unique.add(prefix)
                        rec = etree.Element(self._rec_tag)
                        p_xml = etree.SubElement(rec, 'prefix')
                        p_xml.text = str(prefix)
                    elif self._mode == 2:
                        if (prefix, event) in _unique:
                            continue
                        _unique.add((prefix, event))
                        rec = etree.Element(self._rec_tag)
                        p_xml = etree.SubElement(rec, 'prefix')
                        p_xml.text = str(prefix)
                        e_xml = etree.SubElement(rec, 'event')
                        e_xml.text = str(event)
                    elif self._mode == 3:
                        rec = etree.Element(self._rec_tag)
                        p_xml = etree.SubElement(rec, 'prefix')
                        p_xml.text = str(prefix)
                        e_xml = etree.SubElement(rec, 'event')
                        e_xml.text = str(event)
                        v_xml = etree.SubElement(rec, 'value')
                        v_xml.text = str(value)
                                        
                    if self._flt is not None:
                        while True:
                            # OBLIGATORY
                            res = self._flt.filterRecord(rec)
                            if res & WRITE:
                                self._wri.writeRecord(rec)
                            if res & REPEAT:
                                continue
                            if res & BREAK:
                                Log.info('Filter caused Process to stop on record %d' % _recno)
                                raise FilterBreak
                            break
                    else:
                        # OBLIGATORY
                        self._wri.writeRecord(rec)
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
            fout.close()
            Log.info('Output saved to %s' % outpath)
